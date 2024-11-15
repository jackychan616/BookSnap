from rest_framework import serializers
from .models import PostType, Post, PostImage, Event, TemplateImage
from django.utils import timezone

class PostTypeSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = PostType
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date', 'time', 
                 'created_at', 'updated_at']
        
    def validate(self, data):
        # 確保日期不是過去的日期
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("活動日期不能是過去的日期")
        return data

class TemplateImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TemplateImage
        fields = ['id', 'image', 'description', 'created_at', 'updated_at', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ['id', 'image', 'alt_text', 'created_at', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'tag', 'type', 
                 'created_at', 'updated_at', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        post = Post.objects.create(**validated_data)
        
        for image in uploaded_images:
            PostImage.objects.create(post=post, image=image)
        
        return post

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        # Update post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Add new images
        for image in uploaded_images:
            PostImage.objects.create(post=instance, image=image)
        
        return instance 

