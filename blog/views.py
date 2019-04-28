from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from blog.models import Blog, BlogType
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from read_statistics.utlis import read_statistics_once_read
from comment.forms import CommentForm
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


    '''
    BlogType.objects.annotate(blog_count=Count('blog'))等价下方效果
     # 获取博客分类的数量
    blog_type_list = []
    blog_types = BlogType.objects.all()
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_type_list.append(blog_type)
    '''

    # 获得日期归档的数量
    blog_datas = Blog.objects.dates('create_date', 'month', order='DESC')
    blog_datas_dict = {}
    for blog_date in blog_datas:
        blog_count = Blog.objects.filter(create_date__year=blog_date.year,
                                         create_date__month=blog_date.month).count()
        blog_datas_dict[blog_date] = blog_count

    content['blogs'] = page_of_blogs
    content['page_of_blogs'] = page_of_blogs
    content['page_range'] = page_range
    content['blogs_count'] = Blog.objects.all().count()
    content['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog')) #获得分类数量
    content['blog_dates'] = blog_datas_dict
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
    return render(request, 'blog_date.html', content)


def blog_detail(request, blog_pk):
    content = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 通过识别cookie来判断用户是否阅读过本页面
    read_cookie_key = read_statistics_once_read(request, blog)

    # 获得评论的对象的类型
    blog_content_type = ContentType.objects.get_for_model(blog)    # 筛选出blog对应的评论
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_pk)

    # 通过时间筛选出前一篇和后一篇博客对象
    content['previous_blog'] = Blog.objects.filter(create_date__lt=blog.create_date).first()
    content['next_blog'] = Blog.objects.filter(create_date__gt=blog.create_date).last()
    content['blog'] = blog
    content['comments'] = comments
    content['comment_forms'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk})
    response = render(request, 'blog_detail.html', content)
    # 响应时发送一个子定义cookie来作为判断的参数
    # 阅读cookie
    response.set_cookie(read_cookie_key, 'true')
    return response

