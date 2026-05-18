from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Post, Profile
from .forms  import SignupForm, PostForm, ProfileForm


# ── helpers ───────────────────────────────────────────────────────────────
def is_admin(user):
    return user.is_superuser


# ── auth ──────────────────────────────────────────────────────────────────
def signup_view(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        login(request, user)
        messages.success(request, "Welcome to Century Innovative 🚀")
        return redirect('home')
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            messages.success(request, "Login Successful 🚀")
            return redirect('home')
        messages.error(request, "Invalid Username or Password")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully 👋")
    return redirect('home')


# ── pages ─────────────────────────────────────────────────────────────────
def home(request):
    # show 3 latest blog posts on homepage
    from blog.models import Post as BlogPost
    latest_posts = BlogPost.objects.select_related('author') \
                            .prefetch_related('media_files') \
                            .order_by('-created_at')[:3]
    return render(request, 'home.html', {'latest_posts': latest_posts})


def posts(request):
    all_posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts.html', {'posts': all_posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})


# ── profile ───────────────────────────────────────────────────────────────
@login_required
def author_profile(request, username):
    author       = get_object_or_404(User, username=username)
    profile, _   = Profile.objects.get_or_create(user=author)

    # use blog posts (the ones shown in blog_home)
    from blog.models import Post as BlogPost
    author_posts = BlogPost.objects.filter(author=author) \
                           .prefetch_related('media_files') \
                           .order_by('-created_at')

    return render(request, 'author_profile.html', {
        'author':       author,
        'profile':      profile,
        'author_posts': author_posts,
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated ✅")
        return redirect('author_profile', username=request.user.username)
    return render(request, 'edit_profile.html', {'form': form})


# ── main posts (separate from blog) ──────────────────────────────────────
@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post        = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Post created successfully ✨")
        return redirect('blog_home')
    return render(request, 'create_post.html', {'form': form})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect('posts')
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Post updated ✏")
        return redirect('post_detail', id=post.id)
    return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, "Post deleted 🗑")
    return redirect('posts')


# ── admin ─────────────────────────────────────────────────────────────────
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {
        'total_users': User.objects.count(),
        'total_posts': Post.objects.count(),
        'posts':       Post.objects.all(),
    })
