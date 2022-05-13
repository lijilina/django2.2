from tkinter import SE
from django.http import Http404
from redis import AuthenticationError
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from .models import drf_Article
from .serializers import ArticleSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# @api_view(['GET', 'POST'])
# def article_list(request, format=None):
#     if request.method == 'GET':
#         articles = drf_Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# request.POST  # 只处理表单数据, 只适用于'POST'方法
# request.data  # 处理任意数据, 适用于'POST'，'PUT'和'PATCH'方法

class ArticleList(APIView):

    # IsAuthenticatedOrReadOnly 类，它将确保经过身份验证的请求获得读写访问权限，未经身份验证的请求将获得只读读的权限。
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    # 指定auth
    Authentication_class = (SessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        # articles = drf_Article.objects.all()
        # serializer = ArticleSerializer(articles, many=True)
        # return Response(serializer.data)
        content = {
            'user': request.user,  # `django.contrib.auth.User` 实例。
            'auth': request.auth,  # None
        }
        return Response(content)

        

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET', 'PUT', 'DELETE'])
# def article_detail(request, pk, format=None):
#     try:
#         article = drf_Article.objects.get(pk=pk)
#     except drf_Article.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ArticleDetail(APIView):
    # 添加如果为登陆认证则只有只读权限 IsOwnerOrReadOnly为自定义权限
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


    def get_objects(request, pk):
        try:
            return drf_Article.objects.get(pk=pk)
        except drf_Article.DoesNotExist:
            return Http404
    
    def get(self, request, pk, format=None):

        article = self.get_objects(pk)
        print(article.author == request.user)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        article = self.get_objects(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_objects(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
