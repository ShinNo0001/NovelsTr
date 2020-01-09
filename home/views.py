from django.shortcuts import render,HttpResponse
from novel.models import Chapter
from django.core.paginator import Paginator

def home_view(request):
    chapter_list= Chapter.objects.all()
    paginator = Paginator(chapter_list, 20) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    chapter = paginator.get_page(page_number)
    return render(request,'home.html', { 'chapter':chapter })
