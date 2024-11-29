# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib import messages

def home(request):
    # Retrieve all posts from the database
    posts = Post.objects.all()  # Optionally, you can add filtering, ordering, etc.
    context = {'posts': posts}
    
    # Render the 'home.html' template with the context
    return render(request, 'blog/home.html', context)

def index(request):
    if request.user.is_authenticated:
        # Filter posts by the 'author' field (not 'user')
        posts = Post.objects.filter(author=request.user).order_by('-created_at')  # Show posts for logged-in user
    else:
        posts = Post.objects.all().order_by('-created_at')  # If not logged in, show all posts
    
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all()  # Fetch all the posts
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def posts_view(request):
    posts = Post.objects.all()  # Fetch all posts from the database
    return render(request, 'blog/posts.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('post_list')
    return render(request, 'blog/delete_post.html', {'post': post})






