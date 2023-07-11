from django.urls import path
from . import views

app_name = 'blog'
# 간단하게 url 입력할때도 blog:detail(name)으로 표기할 수 있음

urlpatterns = [
    # path(패턴, 매핑) /blog/
    # path("", views.index), # FBV
    # 글 목록 조회
    path("",views.Index.as_view(), name='list'),
    # ""는 /blog/ 메인주소를 나타내는 것과 같음 
    # 위의 views.Index 는 views.py 파일의 Index 함수를 의미
    
    # 글 상세 조회
    path("detail/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # /blog/detail/1 -> 전개
    
    # 글 작성
    path("write/", views.Write.as_view(), name='write'),
    # 위의 /blog/write/ -> 전개 views.py에 Write클래스
    
    # 글 수정
    path("detail/<int:pk>/edit/", views.Update.as_view(), name='edit'),
    # edit을 붙이게 되면 Update.as_visw의 함수가 실행 ! 
    
    # 글 삭제
    path("detail/<int:pk>/delete/", views.Delete.as_view(), name='delete'),
    
    # 코멘트 작성
    path("detail/<int:pk>/comment/write/", views.CommentWrite.as_view(), name='cm-write'),
    
    # 코멘트 삭제
    # comment -> id다 
    # 코멘트 중에서 어떤 객체를 지워야 할지 정해야 하니까 comment/ <int:pk>
    path("detail/comment/<int:pk>/delete/", views.CommentDelete.as_view(), name='cm-delete'),
    # detail comment 11 삭제
    # 코멘트의 어떤 값을 삭제 할 것인가 ? 
    
    # 태그 작성
    path("detail/<int:pk>/hashtag/write/", views.HashTagWrite.as_view(), name='tag-write'),
    
    # 태그 삭제
    path("detail/<int:pk>/hashtag/delete/", views.HashTagDelete.as_view(), name='tag-delete'),
]