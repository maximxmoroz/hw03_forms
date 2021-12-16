from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import PostForm
from .models import Post, Group
from django.core.paginator import Paginator


def pagination(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return(page_obj)


def index(request):
    post_list = Post.objects.all()
    page_number = request.GET.get('page')
    page_obj = pagination(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all()
    page_number = request.GET.get('page')
    page_obj = pagination(request, post_list)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    post_user_list = Post.objects.select_related('author', 'group').all()
    number_of_posts = post_user_list.count()
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    page_number = request.GET.get('page')
    page_obj = pagination(request, post_list)
    context = {
        'page_obj': page_obj,
        'author': user,
        'number_of_posts': number_of_posts,

    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_count = post.author.posts.count()
    context = {
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        author = request.user
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = author
            new_post.save()
            return redirect('posts:profile', author.username)
        return render(request, 'posts/create_post.html',
                      {'is_edit': True, 'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html',
                  {'is_edit': True, 'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id)
        context = {'form': form, 'is_edit': True}
        return render(request, 'posts/create_post.html', context)
    form = PostForm(instance=post)
    return render(request, 'posts/create_post.html',
                  {'is_edit': True, 'form': form})
