from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from accounts.models import Profile, Like


def _has_admin_access(request):
    return request.session.get('admin_logged_in', False)


def _wants_json(request):
    return (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or 'application/json' in (request.headers.get('Accept') or '')
        or 'application/json' in (request.headers.get('Content-Type') or '')
    )


def admin_login(request):
    if _has_admin_access(request):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''
        
        admin_email = (settings.ADMIN_PANEL_EMAIL or '').strip().lower()
        admin_password = settings.ADMIN_PANEL_PASSWORD or ''

        if email == admin_email and password == admin_password:
            request.session['admin_logged_in'] = True
            request.session['admin_email'] = settings.ADMIN_PANEL_EMAIL
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
        if _wants_json(request):
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        return redirect('admin_login')
    
    try:
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        profile.is_active = not profile.is_active
        profile.save()

        if _wants_json(request):
            return JsonResponse({'status': 'success', 'is_active': profile.is_active})
        return redirect(request.META.get('HTTP_REFERER') or reverse('admin_user_detail', args=[user_id]))
    except Exception as e:
        if _wants_json(request):
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        return redirect(request.META.get('HTTP_REFERER') or reverse('admin_users'))


@require_POST
@csrf_protect
def admin_delete_user(request, user_id):
    if not _has_admin_access(request):
        if _wants_json(request):
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        return redirect('admin_login')
    
    try:
        user = get_object_or_404(User, id=user_id)
        username = user.username
        user.delete()
        if _wants_json(request):
            return JsonResponse({'status': 'success', 'message': f'User {username} deleted successfully'})
        return redirect('admin_users')
    except Exception as e:
        if _wants_json(request):
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        return redirect(request.META.get('HTTP_REFERER') or reverse('admin_users'))


@require_POST
@csrf_protect
def admin_deactivate_user(request, user_id):
    if not _has_admin_access(request):
        if _wants_json(request):
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        return redirect('admin_login')

    try:
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        profile.is_active = False
        profile.save(update_fields=['is_active'])
        user.is_active = False
        user.save(update_fields=['is_active'])
        if _wants_json(request):
            return JsonResponse({'status': 'success', 'message': f'User {user.username} deactivated successfully'})
        return redirect(request.META.get('HTTP_REFERER') or reverse('admin_user_detail', args=[user_id]))
    except Exception as e:
        if _wants_json(request):
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        return redirect(request.META.get('HTTP_REFERER') or reverse('admin_users'))


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
