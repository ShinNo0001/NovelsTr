from django.shortcuts import render, HttpResponse,get_object_or_404,HttpResponseRedirect, redirect, Http404
from .models import Novel, Chapter, ChapterComment, NovelComment
from .forums import NovelForm, ChapterForm, NovelCommentForm,ChapterCommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator


def novel_list(request):
    novels_list = Novel.objects.all()
    query = request.GET.get('q')
    if query:
        novels_list = novels_list.filter(
            Q(title__icontains=query)|
            Q(auth__icontains=query)|
            Q(name__icontains=query)|
            Q(type__icontains=query)|
            Q(genre__icontains=query)|
            Q(tags__icontains=query)|
            Q(league__icontains=query)|
            Q(year__icontains=query)
        ).distinct()

    paginator = Paginator(novels_list, 40) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    novels = paginator.get_page(page_number)

    return render(request, 'post/index.html', {'novels':novels})

def novel_detail(request, slug):
    novel = get_object_or_404(Novel, slug=slug)

    form = NovelCommentForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.nc_novel = novel
        post.save()
        messages.success(request, 'Yorumunuz yayınlanmıştır')
        return HttpResponseRedirect(novel.get_absolute_url())

    context = {
        'novel' : novel,
        'form':form,
    }
    return render(request,'post/detail.html',context)

def novel_create(request):
    form = NovelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Seriniz yayınlanmıştır')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form':form,
    }

    return render(request,'post/create.html', context)


"""
Bölüm Viewleri
"""

def chapter_detail(request, slug):
    chapter = get_object_or_404(Chapter, slug=slug)
    novel = chapter.novel

    form = ChapterCommentForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.cc_novel = chapter
        post.save()
        messages.success(request, 'Yorumnuz yayınlanmıştır')
        return HttpResponseRedirect(chapter.get_absolute_url())

    context = {
        'chapter' : chapter,
        'novel' : novel,
        'form' : form,

    }
    return render(request,'post/chapter_detail.html',context)

def chapter_create(request):
    form = ChapterForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, 'Bölümünüz yayınlanmıştır')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form':form,
    }

    return render(request,'post/create.html', context)

def comment_delete(request, id):
    post = get_object_or_404(ChapterComment, id=id)
    post.delete()
    messages.success(request, 'Yorum silinmiştir')
    return HttpResponseRedirect(post.cc_novel.get_absolute_url())

def ncomment_delete(request, id):

    post = get_object_or_404(NovelComment, id=id)
    post.delete()
    messages.success(request, 'Yorum silinmiştir')
    return HttpResponseRedirect(post.nc_novel.get_absolute_url())
