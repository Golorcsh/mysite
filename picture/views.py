from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from picture.models import Picture
# Create your views here.

EachPageNumOfPicture = 9


def paginator(request, picture_all_list):
    content = {}
    # 每10个blog一页
    paginator = Paginator(picture_all_list, EachPageNumOfPicture)
    # 获取url的页码参数
    page_num = int(request.GET.get('page', 1))
    page_of_pictures = paginator.get_page(page_num)
    # 当前页码的前后3页的范围
    page_range = [x for x in range(int(page_num)-2, int(page_num)+3) if 0 < x <= paginator.num_pages]
    print(page_range)
    if page_range[0]-1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 添加首页和尾页
    if page_range[0] != 1 :
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    content['page_of_pictures'] = page_of_pictures
    content['page_range'] = page_range

    return content


def picture(request):
    picture_list = Picture.objects.all()
    content = paginator(request, picture_list)
    return render(request, 'picture.html', content)


def picture_detail(request, picture_pk):
    content = {}
    picture = get_object_or_404(Picture, pk=picture_pk)
    content['picture'] = picture
    return render(request, 'picture_detail.html', content)