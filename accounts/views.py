from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from .models import Profile, Like, ChatMessage
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm, SearchForm
from .firebase_utils import (
    firebase_web_config,
    firebase_is_configured,
    create_firebase_custom_token,
)

def home(request):
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        context = {
            "profile": profile,
            "likes_received": Like.objects.filter(to_user=request.user).count(),
            "matched_count": len(_matched_user_ids(request.user)),
        }
        return render(request, "home_logged_in.html", context)
    return render(request, "home_with_hero.html")


def _matched_user_ids(user):
    outgoing = Like.objects.filter(from_user=user).values_list('to_user_id', flat=True)
    incoming = Like.objects.filter(to_user=user).values_list('from_user_id', flat=True)
    return sorted(set(outgoing).intersection(set(incoming)))


def _chat_room_id(user_a_id, user_b_id):
    uid1, uid2 = sorted([int(user_a_id), int(user_b_id)])
    return f"{uid1}_{uid2}"


def _can_chat(user_a, user_b):
    if not user_a or not user_b or user_a == user_b:
        return False
    return Like.objects.filter(from_user=user_a, to_user=user_b).exists() and Like.objects.filter(
        from_user=user_b, to_user=user_a
    ).exists()


def _profile_image_url(profile, request):
    if profile and profile.profile_picture:
        return request.build_absolute_uri(profile.profile_picture.url)
    return ""


def _serialize_matched_users(request):
    matched_ids = _matched_user_ids(request.user)
    users = User.objects.filter(id__in=matched_ids).select_related("profile").order_by("first_name", "username")
    data = []
    for matched_user in users:
        profile = getattr(matched_user, "profile", None)
        full_name = f"{matched_user.first_name} {matched_user.last_name}".strip() or matched_user.username
        data.append(
            {
                "id": matched_user.id,
                "username": matched_user.username,
                "fullName": full_name,
                "profilePicture": _profile_image_url(profile, request),
                "roomId": _chat_room_id(request.user.id, matched_user.id),
                "profileUrl": reverse("profile_view", args=[matched_user.username]),
                "chatUrl": reverse("chat_room", args=[matched_user.username]),
            }
        )
    return data


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    Profile.objects.get_or_create(user=user)
                login(request, user)
                return redirect('profile_edit')
            except Exception:
                form.add_error(None, 'Registration failed. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    pass
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.session.get('admin_logged_in'):
        return redirect('admin_dashboard')

    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = (form.cleaned_data['email'] or '').strip()
            password = form.cleaned_data['password']
            admin_email = (settings.ADMIN_PANEL_EMAIL or '').strip().lower()
            admin_password = settings.ADMIN_PANEL_PASSWORD or ''

            if email.lower() == admin_email and password == admin_password:
                request.session['admin_logged_in'] = True
                request.session['admin_email'] = settings.ADMIN_PANEL_EMAIL
                return redirect('admin_dashboard')

            try:
                db_user = User.objects.get(email__iexact=email)
                if not db_user.is_active:
                    form.add_error(None, 'Your account is inactive. Please contact support.')
                    return render(request, 'login.html', {'form': form})

                auth_user = authenticate(request, username=db_user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    return redirect('dashboard')
                else:
                    form.add_error(None, 'Invalid credentials')
            except User.DoesNotExist:
                form.add_error(None, 'User not found')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    likes_received = Like.objects.filter(to_user=request.user).count()
    likes_given = Like.objects.filter(from_user=request.user).count()
    matched_count = len(_matched_user_ids(request.user))
    
    context = {
        'profile': profile,
        'likes_received': likes_received,
        'likes_given': likes_given,
        'matched_count': matched_count,
    }
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'profile_edit.html', context)


@login_required(login_url='login')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    is_liked = False
    is_matched = False
    if request.user.is_authenticated and request.user != user:
        is_liked = Like.objects.filter(from_user=request.user, to_user=user).exists()
        reverse_like_exists = Like.objects.filter(from_user=user, to_user=request.user).exists()
        is_matched = is_liked and reverse_like_exists
    
    context = {
        'profile': profile,
        'is_liked': is_liked,
        'is_matched': is_matched,
        'profile_user': user,
    }
    
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def search_users(request):
    profiles = Profile.objects.filter(is_active=True, user__is_active=True).exclude(user=request.user)
    form = SearchForm(request.GET)
    
    if form.is_valid():
        if form.cleaned_data['gender']:
            profiles = profiles.filter(gender=form.cleaned_data['gender'])
        if form.cleaned_data['religion']:
            profiles = profiles.filter(religion=form.cleaned_data['religion'])
        if form.cleaned_data['age_min']:
            profiles = profiles.filter(age__gte=form.cleaned_data['age_min'])
        if form.cleaned_data['age_max']:
            profiles = profiles.filter(age__lte=form.cleaned_data['age_max'])
        if form.cleaned_data['location']:
            profiles = profiles.filter(location__icontains=form.cleaned_data['location'])
    
    paginator = Paginator(profiles, 12)
    page = request.GET.get('page')
    profiles = paginator.get_page(page)
    
    context = {
        'profiles': profiles,
        'form': form,
        'matched_user_ids': set(_matched_user_ids(request.user)),
        'liked_user_ids': set(Like.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)),
    }
    
    return render(request, 'search.html', context)


@login_required(login_url='login')
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'profile_user': request.user})


@login_required(login_url='login')
def chat_home(request):
    matched_users = _serialize_matched_users(request)
    selected_username = request.GET.get("with", "")
    selected_user = None

    if selected_username:
        selected_user = next((u for u in matched_users if u["username"] == selected_username), None)
    elif matched_users:
        selected_user = matched_users[0]

    bootstrap = {
        "firebaseEnabled": firebase_is_configured(),
        "firebaseConfig": firebase_web_config(),
        "currentUser": {
            "id": request.user.id,
            "uid": str(request.user.id),
            "username": request.user.username,
            "fullName": f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            "profilePicture": _profile_image_url(getattr(request.user, "profile", None), request),
        },
        "matches": matched_users,
        "selectedUser": selected_user,
        "tokenEndpoint": reverse("chat_firebase_token"),
        "fallbackMessageEndpoint": reverse("chat_messages_api", args=[selected_user["username"]]) if selected_user else "",
    }

    return render(
        request,
        "chat.html",
        {
            "chat_bootstrap": bootstrap,
            "matched_users": matched_users,
            "selected_user": selected_user,
            "firebase_enabled": bootstrap["firebaseEnabled"],
        },
    )


@login_required(login_url='login')
def chat_room(request, username):
    if username not in [user["username"] for user in _serialize_matched_users(request)]:
        return HttpResponseForbidden("You can only chat with matched users.")
    return redirect(f"{reverse('chat_home')}?with={username}")


@login_required(login_url='login')
def chat_firebase_token(request):
    uid = str(request.user.id)
    token = create_firebase_custom_token(uid)
    if not token:
        return JsonResponse(
            {
                "ok": False,
                "message": "Firebase is not configured on server. Check environment settings.",
            },
            status=503,
        )
    return JsonResponse({"ok": True, "token": token, "uid": uid})


@login_required(login_url='login')
def chat_messages_api(request, username):
    peer = get_object_or_404(User, username__iexact=username)
    if not _can_chat(request.user, peer):
        return JsonResponse({"ok": False, "message": "You can only chat with matched users."}, status=403)

    room_id = _chat_room_id(request.user.id, peer.id)
    if request.method == "GET":
        messages = (
            ChatMessage.objects.filter(room_id=room_id)
            .select_related("sender")
            .order_by("-created_at")[:100]
        )
        payload = [
            {
                "senderUid": str(msg.sender_id),
                "senderName": msg.sender.first_name or msg.sender.username,
                "text": msg.message,
                "createdAt": msg.created_at.isoformat(),
            }
            for msg in reversed(messages)
        ]
        return JsonResponse({"ok": True, "messages": payload})

    if request.method == "POST":
        text = (request.POST.get("message") or "").strip()
        if not text:
            return JsonResponse({"ok": False, "message": "Message cannot be empty."}, status=400)
        ChatMessage.objects.create(
            sender=request.user,
            recipient=peer,
            room_id=room_id,
            message=text[:500],
        )
        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False, "message": "Method not allowed."}, status=405)


@login_required(login_url='login')
@require_POST
def like_user(request, username):
    wants_json = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )
    fallback_redirect = request.META.get("HTTP_REFERER") or reverse("search")

    to_user = get_object_or_404(
        User,
        Q(username__iexact=username) | Q(email__iexact=username)
    )
    
    if request.user == to_user:
        if wants_json:
            return JsonResponse({'status': 'error', 'message': 'Cannot like yourself'}, status=400)
        return redirect(fallback_redirect)
    
    like, created = Like.objects.get_or_create(
        from_user=request.user,
        to_user=to_user
    )
    
    if not created:
        like.delete()
        if wants_json:
            return JsonResponse({'status': 'success', 'action': 'unliked'})
        return redirect(fallback_redirect)
    
    if wants_json:
        return JsonResponse(
            {
                'status': 'success',
                'action': 'liked',
                'is_matched': Like.objects.filter(from_user=to_user, to_user=request.user).exists(),
            }
        )
    return redirect(fallback_redirect)
