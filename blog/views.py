from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm


# Create your views here.
def post_list(request):
    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = post[::-1]
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        cmnt = request.POST.get('comment', '')
        com = Comment(cmnt = cmnt, authr = request.user, post_id = post.id)
        com.save()
    view_comments = Comment.objects.filter(post_id = post.id)
    # print(view_comments)
    # view = []
    # for item in view_comments:
    #     view.append(item.cmnt)
    # print(view)
    return render(request, 'blog/post_detail.html', {'post': post, 'view':view_comments})


def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def register(request):
    return render(request, 'blog/register.html')
