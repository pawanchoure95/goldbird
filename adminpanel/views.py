from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from accounts.models import Profile, Like


def _has_admin_access(request):
    return request.session.get('admin_logged_in', False)


def admin_login(request):
    if _has_admin_access(request):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''
        
        if email == 'sundisk95@gmail.com' and password == 'Sneha11@':
            request.session['admin_logged_in'] = True
            request.session['admin_email'] = 'Sundisk95@gmail.com'
            return redirect('admin_dashboard')

        error = 'Invalid email or password'
        return render(request, 'admin_login.html', {'error': error})
    
    return render(request, 'admin_login.html')


def admin_logout(request):
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    if 'admin_email' in request.session:
        del request.session['admin_email']
    return redirect('admin_login')


def admin_dashboard(request):
    if not _has_admin_access(request):
        if request.user.is_authenticated:
            return redirect('home')
        return redirect('admin_login')
    
    total_users = User.objects.count()
    active_users = Profile.objects.filter(is_active=True).count()
    total_likes = Like.objects.count()
    total_profiles = Profile.objects.count()
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_likes': total_likes,
        'total_profiles': total_profiles,
    }
    
    return render(request, 'admin_dashboard.html', context)


def admin_users(request):
    if not _has_admin_access(request):
        if request.user.is_authenticated:
            return redirect('home')
        return redirect('admin_login')
    
    users = User.objects.all()
    profiles = Profile.objects.all()
    
    # Create a dictionary mapping user IDs to profiles for easier access
    profile_dict = {p.user_id: p for p in profiles}
    
    context = {
        'users': users,
        'profiles': profiles,
        'profile_dict': profile_dict,
    }
    
    return render(request, 'admin_users.html', context)


@require_POST
@csrf_protect
def admin_toggle_user_status(request, user_id):
    if not _has_admin_access(request):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        profile.is_active = not profile.is_active
        profile.save()
        
        return JsonResponse({'status': 'success', 'is_active': profile.is_active})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@require_POST
@csrf_protect
def admin_delete_user(request, user_id):
    if not _has_admin_access(request):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        user = get_object_or_404(User, id=user_id)
        username = user.username
        user.delete()
        
        return JsonResponse({'status': 'success', 'message': f'User {username} deleted successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def admin_view_user(request, user_id):
    if not _has_admin_access(request):
        if request.user.is_authenticated:
            return redirect('home')
        return redirect('admin_login')
    
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    
    context = {
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'admin_user_detail.html', context)
