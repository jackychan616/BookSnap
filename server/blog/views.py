<<<<<<< HEAD
from rest_framework import viewsets, status
=======
from rest_framework import viewsets
from .models import Country, Author, PostType, Post, Image, Reel
from .serializers import CountrySerializer, AuthorSerializer, PostTypeSerializer, PostSerializer, ImageSerializer, ReelSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages 
from rest_framework.decorators import api_view, parser_classes, authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser
>>>>>>> 675d26b (reel model)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post, PostType, PostImage, Event, TemplateImage
from .serializers import (
    PostSerializer, PostTypeSerializer, PostImageSerializer,
    EventSerializer, TemplateImageSerializer
)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['GET'])
    def recent(self, request):
        recent_posts = Post.objects.order_by('-created_at')[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)

<<<<<<< HEAD
    def create(self, request, *args, **kwargs):
        # 處理多個圖片上傳
=======

class ImageViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class ReelViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Reel.objects.all()
    serializer_class = ReelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@login_required
def upload_file(request):
    # 檢查用戶是否已登入
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        context = {
            'post_types': PostType.objects.all(),
            'countries': Country.objects.all(),
            'authors': Author.objects.all(),
            'user': request.user,
        }

        if 'add_post_type' in request.POST:
            name = request.POST.get('post_type_name')
            if not name:
                messages.error(request, '文章類型名稱不能為空')
                context['post_type_error'] = '請輸入文章類型名稱'
            elif PostType.objects.filter(name=name).exists():
                messages.error(request, '此文章類型已存在')
                context['post_type_error'] = '此文章類型已存在'
            else:
                PostType.objects.create(name=name)
                messages.success(request, '文章類型新增成功')
                return HttpResponseRedirect(request.path)
            
        elif 'add_country' in request.POST:
            name = request.POST.get('country_name')
            if not name:
                messages.error(request, '國家名稱不能為空')
                context['country_error'] = '請輸入國家名稱'
            elif Country.objects.filter(name=name).exists():
                messages.error(request, '此國家已存在')
                context['country_error'] = '此國家已存在'
            else:
                Country.objects.create(name=name)
                messages.success(request, '國家新增成功')
                return HttpResponseRedirect(request.path)
            
        elif 'add_author' in request.POST:
            name = request.POST.get('author_name')
            if not name:
                messages.error(request, '作者名稱不能為空')
                context['author_error'] = '請輸入作者名稱'
            elif Author.objects.filter(name=name).exists():
                messages.error(request, '此作者已存在')
                context['author_error'] = '此作者已存在'
            else:
                Author.objects.create(name=name)
                messages.success(request, '作者新增成功')
                return HttpResponseRedirect(request.path)

        return render(request, 'upload.html', context)

    context = {
        'post_types': PostType.objects.all(),
        'countries': Country.objects.all(),
        'authors': Author.objects.all(),
        'user': request.user,
    }
    return render(request, 'upload_post.html', context)

@login_required
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def api_create_post(request):
    try:
        # 確保用戶已登入
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        # 獲取表單數據
        post_type_id = request.data.get('post_type')
        country_id = request.data.get('country')
        author_id = request.data.get('author')
        content = request.data.get('content')
        title = request.data.get('title')

        # 驗證必要欄位
        if not all([post_type_id, content, title]):
            return Response({
                'error': 'Please fill in all required fields'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 檢查標題是否重複
        if Post.objects.filter(title=title).exists():
            return Response({
                'error': '此標題已存在'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 創建貼文
        post = Post(
            post_type_id=post_type_id,
            country_id=country_id,
            author_id=author_id if author_id else None,
            content=content,
            title=title,
            user=request.user
        )
        post.save()

        # 處理圖片上傳
>>>>>>> 675d26b (reel model)
        images = request.FILES.getlist('images')
        data = request.data.dict()
        data['uploaded_images'] = images
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

<<<<<<< HEAD
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
=======
@login_required
def download_posts(request):
    post_ids = request.GET.get('ids', '').split(',')
    
    try:
        # 创建个临时的ZIP文件
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for post_id in post_ids:
                try:
                    post = Post.objects.get(id=post_id)
                    
                    # 为每个帖子创建一个文件夹
                    folder_name = f'{post.title}'
                    
                    # 添加文���内容
                    content_file = StringIO() 
                    content_file.write(f"{post.content}")
                    zip_file.writestr(f'{folder_name}/content.txt', content_file.getvalue())
                    
                    # 添加图片
                    for i, image in enumerate(post.images.all()):
                        image_path = image.image.path
                        image_name = os.path.basename(image_path)
                        zip_file.write(image_path, f'{folder_name}/images/{image_name}')
                        
                except Post.DoesNotExist:
                    continue

        # 准备响应
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="selected_posts.zip"'
>>>>>>> 675d26b (reel model)
        
        # 處理多個圖片上傳
        images = request.FILES.getlist('images')
        data = request.data.dict()
        data['uploaded_images'] = images
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

<<<<<<< HEAD
class PostTypeViewSet(viewsets.ModelViewSet):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer

class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    parser_classes = (MultiPartParser, FormParser)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=False, methods=['GET'])
    def upcoming(self, request):
        upcoming_events = Event.objects.filter(
            date__gte=timezone.now()
        ).order_by('date', 'time')[:5]
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

class TemplateImageViewSet(viewsets.ModelViewSet):
    queryset = TemplateImage.objects.all()
    serializer_class = TemplateImageSerializer 
=======
@login_required
def dashboard(request):
    # 獲取基礎數據
    total_posts = Post.objects.count()
    total_authors = Author.objects.count()
    total_countries = Country.objects.count()
    total_reels = Reel.objects.count()  # 新增：總影片數量
    
    # 獲取最近一個月的數據
    last_month = timezone.now() - timedelta(days=30)
    recent_posts = Post.objects.filter(created_at__gte=last_month).count()
    recent_reels = Reel.objects.filter(created_at__gte=last_month).count()  # 新增：最近一個月的影片數量
    
    # 按文章類型統計
    posts_by_type = Post.objects.values('post_type__name')\
        .annotate(count=Count('id'))\
        .order_by('-count')
    
    # 按國家統計
    posts_by_country = Post.objects.values('country__name')\
        .annotate(count=Count('id'))\
        .order_by('-count')
    
    # 按月份統計文章數量
    posts_by_month = Post.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')[:12]  # 最近12個月
    
    # 新增：獲取最近發布的文章
    recent_posts_list = Post.objects.select_related(
        'post_type', 'country', 'author', 'user'
    ).order_by('-created_at')[:10]
    
    # 新增：每個用戶的發文統計
    posts_by_user = Post.objects.values('user__username')\
        .annotate(count=Count('id'))\
        .order_by('-count')[:10]
    
    # 新增：含圖片最多的文章
    posts_with_most_images = Post.objects.annotate(
        image_count=Count('images')
    ).order_by('-image_count')[:5]
    
    # 新增：本週發文統計
    this_week = timezone.now() - timedelta(days=7)
    posts_this_week = Post.objects.filter(created_at__gte=this_week).count()
    
    # 最活躍的作者
    top_authors = Author.objects.annotate(
        post_count=Count('post')
    ).order_by('-post_count')[:5]
    
    # 新增：最近發布的影片
    recent_reels_list = Reel.objects.select_related('user').order_by('-created_at')[:10]
    
    context = {
        'total_posts': total_posts,
        'total_authors': total_authors,
        'total_countries': total_countries,
        'total_reels': total_reels,  # 新增
        'recent_posts': recent_posts,
        'recent_reels': recent_reels,  # 新增
        'posts_by_type': posts_by_type,
        'posts_by_country': posts_by_country,
        'posts_by_month': posts_by_month,
        'top_authors': top_authors,
        'recent_posts_list': recent_posts_list,
        'posts_by_user': posts_by_user,
        'posts_with_most_images': posts_with_most_images,
        'posts_this_week': posts_this_week,
        'recent_reels_list': recent_reels_list,  # 新增
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def create_reel(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video = request.FILES.get('video')
        content = request.POST.get('content')
        
        reel = Reel.objects.create(
            title=title,
            video=video,
            content=content,
            user=request.user
        )
        
        messages.success(request, '影片上傳成功！')
        return redirect('reel_detail', pk=reel.pk)  
        
    return render(request, 'create_reel.html')

@login_required
def reel_list(request):
    # Get filter parameters from URL
    page = int(request.GET.get('page', 1))
    reels_per_page = 20
    
    # Base queryset
    reels = Reel.objects.all()
    
    # Order by created_at (descending)
    reels = reels.order_by('-created_at')
    
    # Calculate total reels for pagination
    total_reels = reels.count()
    
    # Get paginated reels
    start = (page - 1) * reels_per_page
    end = page * reels_per_page
    reels = reels[start:end]
    
    context = {
        'reels': reels,
        'has_more': total_reels > end,
        'current_page': page,
    }
    
    return render(request, 'reel_list.html', context)
>>>>>>> 675d26b (reel model)
