from django.shortcuts import render, get_object_or_404
from blog.models import Blog,BlogType
# Create your views here.


def blog_list(request):
    content = {}
    content['blogs']= Blog.objects.all()
    content['blogs_count'] = Blog.objects.all().count()
    return render(request, 'blog_list.html', content)


def blog_detail(request, blog_pk):
    content= {}
    content['blog']=get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog_detail.html', content)


def blog_with_type(request, blog_type_pk):
    content = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    content['blogs'] = Blog.objects.filter(blog_type=blog_type)
    content['blog_type'] = blog_type
    return render(request, 'blog_type.html', content)



