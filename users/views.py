from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, LoginForm, PostCreateForm, UserProfileForm
from .models import Post

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('users:feed')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.get_full_name()}! Your account is ready.')
            return redirect('users:feed')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('users:feed')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            next_url = request.GET.get('next', 'users:feed')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


@login_required
def feed(request):
    posts = Post.objects.select_related('user').all()
    paginator = Paginator(posts, 10)
    page_obj  = paginator.get_page(request.GET.get('page'))
    return render(request, 'users/feed.html', {'page_obj': page_obj})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post published successfully!')
            return redirect('users:feed')
    else:
        form = PostCreateForm()
    return render(request, 'users/create_post.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('users:feed')


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user)
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
