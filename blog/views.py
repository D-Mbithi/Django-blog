from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    if tag_slug:
        tag_slug = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    tag = None

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    template = 'blog/post/list.html'

    context = {
        'page': page,
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

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # get all post comments
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    template = 'blog/post/detail.html'

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }

    return render(request, template, context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recomments you to read {post.title}."
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comment']}."
            send_mail(subject, message, 'mbaamutendwa@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    template_name = 'blog/share.html'

    context = {
        'post': post,
        'form': form,
        'sent': sent
    }

    return render(request, template_name, context)
