from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, PostSearchForm


def post_list(request):
    """List all published posts with search and filtering"""
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')

    # Search functionality
    search_form = PostSearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )

        if category:
            posts = posts.filter(category=category)

    # Ordering
    order_by = request.GET.get('order', '-published_at')
    if order_by in ['-published_at', '-views', 'title']:
        posts = posts.order_by(order_by)

    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'posts': posts_page,
        'search_form': search_form,
        'categories': Category.objects.all(),
        'popular_tags': Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:10],
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, slug):
    """View a single post with comments"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments__author'),
        slug=slug
    )

    # Increment views only if post is published
    if post.status == 'published':
        post.increment_views()

    # Handle comment form
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
        'related_posts': Post.objects.filter(
            category=post.category,
            status='published'
        ).exclude(id=post.id)[:3]
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, f'Post "{post.title}" created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_update(request, slug):
    """Update an existing post"""
    post = get_object_or_404(Post, slug=slug)

    # Only author can edit
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts!')
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Post "{post.title}" updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {'form': form, 'action': 'Update', 'post': post})


@login_required
def post_delete(request, slug):
    """Delete a post"""
    post = get_object_or_404(Post, slug=slug)

    # Only author can delete
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" deleted successfully!')
        return redirect('my_posts')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required
def my_posts(request):
    """View user's own posts"""
    posts = Post.objects.filter(author=request.user).select_related('category')

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter in ['draft', 'published']:
        posts = posts.filter(status=status_filter)

    # Search
    query = request.GET.get('q', '')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'posts': posts_page,
        'status_filter': status_filter,
        'query': query,
        'draft_count': Post.objects.filter(author=request.user, status='draft').count(),
        'published_count': Post.objects.filter(author=request.user, status='published').count(),
    }
    return render(request, 'posts/my_posts.html', context)


def category_posts(request, slug):
    """View posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').select_related('author')

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': posts_page,
    }
    return render(request, 'posts/category_posts.html', context)


def tag_posts(request, slug):
    """View posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published').select_related('author', 'category')

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'posts': posts_page,
    }
    return render(request, 'posts/tag_posts.html', context)


@login_required
def comment_delete(request, comment_id):
    """Delete a comment"""
    comment = get_object_or_404(Comment, id=comment_id)

    # Only comment author or post author can delete
    if comment.author != request.user and comment.post.author != request.user:
        messages.error(request, 'You cannot delete this comment!')
        return redirect('post_detail', slug=comment.post.slug)

    post_slug = comment.post.slug
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('post_detail', slug=post_slug)
