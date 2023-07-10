from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    # 작성자 foreignkey class User
    created_at = models.DateTimeField(auto_now_add=True) # 초기값
    updated_at = models.DateTimeField(auto_now=True) # 수정할때마다 바뀜


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # 위의 Post를 연결하는 관계 데이터베이스 on_delete를 하면 Post에 있는 글이 사라지면 post 안에 있는 comment도 사라진다. Post:Comment --> '1:N의 관계'표현 
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    # writer을 post로 접근해서 포렌키를 하면 모든 유저들이 comment를 달 수 있기 때문에 아예 User로 접근
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    # admin 페이지에 가면 comment on '포스트제목'의 댓글들을 확인할 수 있다.
    # id 값 대신 제목을 표시할 수 있다.     
    
    
class HashTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name 