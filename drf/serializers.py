from curses.ascii import US
from rest_framework import serializers
from .models import drf_Article
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User


User = get_user_model()


# read_only 将此设置为 True 以确保在序列化表示时使用该字段，但在反序列化期间更新实例时不使用该字段。 默认为false
# required 通常，如果在反序列化期间未提供字段，则会引发错误。如果在反序列化期间不需要此字段，则设置为 false。 默认为true

# class UserSerializer(serializers.ModelSerializer):
    
#     articles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'articles',)
#         read_only_fields = ('id', 'username',)
class UserSerializer(serializers.ModelSerializer):
    # articles 这个名字不是随便写的 是关联表的ForeignKey 字段的related_name的值
    
    # PrimaryKeyRelatedField 只返回primarykey字段的值
    # articles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    # StringRelatedField 返回__str__函数指定的字段
    articles = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'articles',)
        read_only_fields = ('id', 'username',)

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=True, max_length=128)
    body = serializers.CharField(required=False, allow_blank=True)
    # author = serializers.ReadOnlyField(source="author.id")
    # author = serializers.ReadOnlyField(source="author.username")
    # 使用嵌套序列化器 嵌套上面的UserSerializer
    author = UserSerializer(read_only=True)
    status = serializers.ChoiceField(choices=drf_Article.STATUS_CHOICES, default='p')
    # full_status字段为get_status_display方法返回的完整状态。状态为只读
    full_status = serializers.ReadOnlyField(source="get_status_display")
    create_date = serializers.DateTimeField(read_only=True)
    # 展示中文状态 添加独立字段 使用SerializerMethodField，它可用于将任何类型的数据添加到对象的序列化表示中
    cn_status = serializers.SerializerMethodField()


    def create(self, validated_data):
        return drf_Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
    class Meta:
        model = drf_Article
        fields = '__all__'

    # 与上面的cn_status字段对应
    def get_cn_status(self, obj):
        if obj.status == 'p':
            return "已发表"
        elif obj.status == 'd':
            return "草稿"
        else:
            return ''
