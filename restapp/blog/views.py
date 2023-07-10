from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, HashTag
from .serializers import PostSerializer, CommentSerializer, HashTagSerializer

## Post
class Index(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, many=True) # 직렬화
        # ORM(장고의SQL)은 파이썬 객체이기 때문에 클라이언트에게 보내줄 땐 문자열로 변환해서 보내줘야 하기 때문에 직렬화를 통해서 보내줘야함
        return Response(serialized_posts.data)
        # 직렬화 된 상태로 데이터만 넘어간다
        

class Write(APIView):
    # Write 관련된 API는 POST로 날려버리면 돼서 따로 클라이언트에게 보여주는 template가 필요없음
    # def get(self, request):
    #     # 사용자 작성 Form만들어서 보내줌
    #     pass
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # 유저 저장하기 전에 commit=False로 저장 미룸
            post = serializer.save(commit=False)
            post.writer = request.user
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Update(APIView):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        # 보내는 직렬화?
        return Response(serializer.data)
        # 직렬화 된 포스트를 돌려주는구나
        # 여기선 get을 하는 이유? 전의 수정하기 전 값을 되돌려줘야함 위의 글 작성에선 get을 쓰지 않는 이유는 화면 form만 보여줘야하니까 데이터를 굳이 보내주지 않아도됨
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Delete(APIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        # serializer = PostSerializer(post)
        # if serializer.is_valid():
        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)


## Comment
class CommentWrite(APIView):
    def post(self,request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(writer=request.user)
            comment.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CommentDelete(APIView):
    def post(self,request,pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class HashTagWrite(APIView):
    def post(self,request, pk):
        serializer = HashTagSerializer(data=request.data)
        if serializer.is_valid():
            hashtag = serializer.save(writer=request.user)
            hashtag.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HashTagDelete(APIView):
    def post(self,request,pk):
        hashtag = HashTag.objects.get(pk=pk)
        hashtag.delete()
        serializer = HashTagSerializer(hashtag)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        
        
