from django.shortcuts import render, get_object_or_404
from .models import Post


def home(request):
    posts = Post.published.all()
    template = 'blog/post/list.html'
    context = {
        'posts': posts,
    }

    return render(request, template, context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    print(post)
    template = 'blog/post/detail.html'
    context = {
        'post': post,
    }

    return render(request, template, context)
