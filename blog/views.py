from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .models import Post, Like, Comment, PostMedia
from .forms import PostForm, CommentForm
from main.models import Profile


# ── Blog home ─────────────────────────────────────────────────────────────
@login_required
def blog_home(request):
    query = request.GET.get('q', '').strip()

    posts = Post.objects.prefetch_related(
        'media_files', 'comments', 'likes'
    ).select_related('author').order_by('-created_at')

    if query:
        posts = posts.filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

    comment_form = CommentForm()

    return render(request, 'posts/blog_home.html', {
        'posts':        posts,
        'comment_form': comment_form,
        'query':        query,
    })


# ── Create post ───────────────────────────────────────────────────────────
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post        = form.save(commit=False)
            post.author = request.user
            post.save()

            # media_files is already a list from MultipleFileField
            files = form.cleaned_data.get('media_files') or []
            if not isinstance(files, list):
                files = [files]

            for i, file in enumerate(files):
                if file:
                    PostMedia.objects.create(post=post, file=file, order=i)

            messages.success(request, 'Post created successfully 🚀')
            return redirect('blog_home')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})

# ── Like (toggle) ─────────────────────────────────────────────────────────
@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    obj, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        obj.delete()   # toggle off
    return redirect('blog_home')


# ── Add / reply comment ───────────────────────────────────────────────────
@login_required
def comment_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        text      = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent_id')

        if text:
            comment      = Comment(post=post, user=request.user, text=text)
            if parent_id:
                parent = Comment.objects.filter(id=parent_id).first()
                if parent:
                    comment.parent = parent
            comment.save()
            messages.success(request, 'Comment added 💬')

    return redirect('blog_home')


# ── Search suggestions (AJAX) ─────────────────────────────────────────────
from django.http import JsonResponse

def search_suggestions(request):
    q       = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        posts = Post.objects.filter(
            Q(content__icontains=q) | Q(author__username__icontains=q)
        ).select_related('author').values('id', 'content', 'author__username')[:6]
        results = [
            {
                'id':              p['id'],
                'title':           p['content'][:60],
                'author__username': p['author__username'],
            }
            for p in posts
        ]
    return JsonResponse({'results': results})
