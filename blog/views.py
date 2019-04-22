from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from blog.models import Blog, BlogType
# Create your views here.

EachPageNumOfBlog = 6


def get_blog_list_common_date(request, blogs_all_list):

    '''
    公共方法
    :param request:
    :param blogs_all_list:
    :return: content
    '''

    content = {}
    # 每10个blog一页
    paginaotr = Paginator(blogs_all_list, EachPageNumOfBlog)
    # 获取url的页码参数
    page_num = int(request.GET.get('page', 1))
    page_of_blogs = paginaotr.get_page(page_num)
    # 当前页码的前后3页的范围
    page_range = [x for x in range(int(page_num)-2, int(page_num)+3) if 0 < x <= paginaotr.num_pages]
    print(page_range)
    if page_range[0]-1 >= 2:
        page_range.insert(0, "...")
    if paginaotr.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 添加首页和尾页
    if page_range[0] != 1 :
        page_range.insert(0, 1)
    if page_range[-1] != paginaotr.num_pages:
        page_range.append(paginaotr.num_pages)

    content['blogs'] = page_of_blogs
    content['page_of_blogs'] = page_of_blogs
    content['page_range'] = page_range
    content['blogs_count'] = Blog.objects.all().count()
    content['blog_types'] = BlogType.objects.all()
    content['blog_dates'] = Blog.objects.dates('create_date', 'month', order='DESC')
    return content


def blog_list(request):
    blog_all_list = Blog.objects.all()
    content = get_blog_list_common_date(request, blog_all_list)
    return render(request, 'blog_list.html', content)


def blog_with_type(request, blog_type_pk):
    # 获取blog分类的类型
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    content = get_blog_list_common_date(request, blog_all_list)
    # 通过blog的类型筛选出所有同一个类型的blog
    content['blog_type'] = blog_type
    return render(request, 'blog_type.html', content)


def blog_with_date(request, year, month):
    content = {}
    # 获取blog分类的类型
    blog_all_list = Blog.objects.filter(create_date__year=year, create_date__month=month)
    content = get_blog_list_common_date(request, blog_all_list)

    # 通过blog的类型筛选出所有同一个类型的blog
    content['blog_date'] = '%s年%s月' % (year, month)
    content['blog_dates'] = Blog.objects.dates('create_date', 'month', order='DESC')
    return render(request, 'blog_date.html', content)


def blog_detail(request, blog_pk):
    content= {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 通过时间筛选出前一篇和后一篇博客对象
    content['previous_blog'] = Blog.objects.filter(create_date__lt=blog.create_date).first()
    content['next_blog'] = Blog.objects.filter(create_date__gt=blog.create_date).last()
    content['blog'] = blog
    return render(request, 'blog_detail.html', content)