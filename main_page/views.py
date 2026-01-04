from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Article, Category, Tag, Comment, Like, Announcement

from .forms import ArticleForm, CommentForm, CategoryForm, TagForm, AnnouncementForm

from django.http import HttpResponseForbidden

from django.db import models

from django.db.models import Q, Count

def main_page(request):
    sort = request.GET.get('sort', 'latest')

    if request.user.is_authenticated:
        if request.user.is_admin:
            articles = Article.objects.all()
        elif request.user.is_author:
            articles = Article.objects.filter(
                Q(status='published') | Q(author=request.user)
            )
        else:
            articles = Article.objects.filter(status='published')
    else:
        articles = Article.objects.filter(status='published')

    articles = articles.annotate(
        comment_count=Count('comments', distinct=True),
        like_count=Count('likes', distinct=True)
    ).select_related(
        'author', 'category'
    ).prefetch_related('tags')

    if sort == 'popular':
        articles = articles.order_by('-like_count', '-created_at')
    else:
        articles = articles.order_by('-created_at')

    latest_articles = articles[:5]

    popular_articles = (
        Article.objects
        .filter(status='published')
        .annotate(like_count=Count('likes'))
        .order_by('-like_count')[:5]
    )

    categories = Category.objects.annotate(
        articles_count=Count('article')
    )

    tags = Tag.objects.all()

    announcements = Announcement.objects.all() if (
    request.user.is_authenticated and request.user.role == 'admin'
    ) else Announcement.objects.filter(is_active=True)

    return render(
        request,
        'main_page/main_page.html',
        {
            'articles': latest_articles,
            'popular_articles': popular_articles,
            'categories': categories,
            'tags': tags,
            'sort': sort,
            'announcements': announcements,
        }
    )


@login_required
def article_create(request):
    if not request.user.is_author and not request.user.is_admin:
        return redirect('main_page')

    form = ArticleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        form.save_m2m()
        return redirect('main_page')

    return render(request, 'main_page/article_form.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if not (request.user == article.author or request.user.is_admin):
        return HttpResponseForbidden('You do not have permission')

    form = ArticleForm(request.POST or None, instance=article)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('main_page')

    return render(
        request,
        'main_page/article_form.html',
        {'form': form, 'edit': True}
    )

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if not (request.user == article.author or request.user.is_admin):
        return HttpResponseForbidden('You do not have permission')

    if request.method == 'POST':
        article.delete()
        return redirect('main_page')

    return render(
        request,
        'main_page/article_confirm_delete.html',
        {'article': article}
    )

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, status='published')
    comments = article.comments.filter(is_approved=True)

    return render(
        request,
        'main_page/article_detail.html',
        {
            'article': article,
            'comments': comments
        }
    )

@login_required
def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        form = CommentForm()

    return render(
        request,
        'main_page/add_comment.html',
        {
            'form': form,
            'article': article
        }
    )

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if (
        request.user.role == 'admin' or
        comment.article.author == request.user
    ):
        comment.delete()

    return redirect('article_detail', pk=comment.article.id)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main_page/category_list.html', {
        'categories': categories
    })

@login_required
def category_create(request):
    if request.user.role != 'admin':
        return redirect('category_list')

    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'main_page/category_form.html', {
        'form': form,
        'title': 'Create Category'
    })

@login_required
def category_edit(request, pk):
    if request.user.role != 'admin':
        return redirect('category_list')

    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'main_page/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })

@login_required
def category_delete(request, pk):
    if request.user.role == 'admin':
        Category.objects.filter(pk=pk).delete()
    return redirect('category_list')

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main_page/tag_list.html', {'tags': tags})

@login_required
def tag_create(request):
    if request.user.role != 'admin':
        return redirect('tag_list')

    form = TagForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('tag_list')

    return render(request, 'main_page/tag_form.html', {
        'form': form,
        'title': 'Create Tag'
    })

@login_required
def tag_edit(request, pk):
    if request.user.role != 'admin':
        return redirect('tag_list')

    tag = get_object_or_404(Tag, pk=pk)
    form = TagForm(request.POST or None, instance=tag)

    if form.is_valid():
        form.save()
        return redirect('tag_list')

    return render(request, 'main_page/tag_form.html', {
        'form': form,
        'title': 'Edit Tag'
    })

@login_required
def tag_delete(request, pk):
    if request.user.role == 'admin':
        Tag.objects.filter(pk=pk).delete()
    return redirect('tag_list')

@login_required
def toggle_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        article=article
    )

    if not created:
        like.delete()

    return redirect('main_page')

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def announcements_list(request):
    announcements = Announcement.objects.filter(is_active=True)

    return render(
        request,
        'main_page/announcements_list.html',
        {'announcements': announcements}
    )

@user_passes_test(is_admin)
def announcement_create(request):
    form = AnnouncementForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('announcements')

    return render(
        request,
        'main_page/announcement_form.html',
        {'form': form}
    )

@user_passes_test(is_admin)
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    form = AnnouncementForm(request.POST or None, instance=announcement)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('announcements')

    return render(
        request,
        'main_page/announcement_form.html',
        {'form': form, 'edit': True}
    )

@user_passes_test(is_admin)
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements')

    return render(
        request,
        'main_page/announcement_confirm_delete.html',
        {'announcement': announcement}
    )