from django.shortcuts import render
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from blog.models import Blog

EachPageNumOfSearch = 10


def index(request):
    return render(request, 'index.html')


def search_paginator(request, search_list):
    content = {}
    # 分页
    paginator = Paginator(search_list, EachPageNumOfSearch)
    page_num = int(request.GET.get('page', 1))
    page_of_search = paginator.get_page(page_num)
    print(page_of_search)
    page_range = [x for x in range(int(page_num) - 1, int(page_num) + 2) if 0 < x <= paginator.num_pages]
    if page_range[0]-1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 添加首页和尾页
    if page_range[0] != 1 :
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    content['page_of_search'] = page_of_search
    content['page_range'] = page_range
    return content


def search(request):
    content = {}
    search_words = request.GET.get('key_word', '').strip()
    # 分词：按空格 & | ~
    condition = None
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)

    if condition is not None:
        # 筛选：搜索
        search_blogs = []
        search_blogs = Blog.objects.filter(condition)
        if search_words !=  '':
            content = search_paginator(request, search_blogs)
            content['search_blogs_count'] = search_blogs.count()

    content['search_words'] = search_words
    return render(request, 'search.html', content)
