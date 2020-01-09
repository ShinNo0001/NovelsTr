from django.conf.urls import url
from .views import *

app_name="novel"

urlpatterns = [
    url(r'^novel-list/$', novel_list,name='novel-list'),
    url(r'^novel-create/$', novel_create,name='novel-create'),
    url(r'^chapter-create/$', chapter_create, name='chapter-create'),

    url(r'^(?P<slug>[\w-]+)/detail/$', chapter_detail, name='chapter_detail'),
    url(r'^(?P<slug>[\w-]+)/$', novel_detail, name='novel-detail'),

    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='commentdelete'),
    url(r'^(?P<id>\d+)/yorum-sil/$', ncomment_delete, name='ncommentdelete'),


    #url(r'^(?P<slug>[\w-]+)/chapter_update/$', chapter_update, name='chapter-update'),

]
