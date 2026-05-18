from django.shortcuts import get_object_or_404, render, redirect

from main.models import Profile
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login

#login view
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login Successful 🚀"
            )

            return redirect('home')

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, 'login.html')


def blog_home(request):
    return render(request, 'blog_home.html')

@login_required
def blog_home(request):
    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'posts/blog_home.html', {'posts': posts, 'comment_form': comment_form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post created successfully.')
            return redirect('blog_home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def like_post(request, id):
    post = Post.objects.get(id=id)
    Like.objects.create(post=post)
    messages.success(request, 'Post liked successfully.')
    return redirect('blog_home')


def comment_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    messages.success(request, 'Comment added successfully.')
    return redirect('blog_home')

# AUTHOR PROFILE
@login_required
def author_profile(request, username):
    from django.contrib.auth.models import User
    author = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=author)
    author_posts = Post.objects.filter(author=author).order_by('-created_at')
    return render(request, 'author_profile.html', {
        'author': author,
        'profile': profile,
        'author_posts': author_posts,
    })