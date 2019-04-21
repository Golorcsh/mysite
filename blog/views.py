from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from blog.models import Blog, BlogType
# Create your views here.


def blog_list(request):

    blog_all_list = Blog.objects.all()
    # 每10个blog一页
    paginaotr = Paginator(blog_all_list, 10)
    # 获取url的页码参数
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginaotr.get_page(page_num)



    content = {}
    content['blogs']= page_of_blogs.object_list
    content['page_of_blogs'] = page_of_blogs
    content['blogs_count'] = Blog.objects.all().count()
    content['blog_types'] = BlogType.objects.all()
    return render(request, 'blog_list.html', content)


def blog_detail(request, blog_pk):
    content= {}
    content['blog']=get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog_detail.html', content)


def blog_with_type(request, blog_type_pk):
    content = {}
    # 获取blog分类的类型
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    content['blogs'] = Blog.objects.filter(blog_type=blog_type)
    # 通过blog的类型筛选出所有同一个类型的blog
    content['blogs_count'] = Blog.objects.filter(blog_type=blog_type).count()
    content['blog_type'] = blog_type
    content['blog_types'] = BlogType.objects.all()
    return render(request, 'blog_type.html', content)



