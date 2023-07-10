from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # user/ 이 user을 생략해도 되는 이유는 전체 urls.py에서 user/ 을 저장했기 때문
    # 회원가입
    path('register/', views.Registration.as_view(), name='register'),
    # 로그인
    path('login/', views.Login.as_view(), name='login'),
    # 로그아웃
    path('logout/', views.Logout.as_view(), name='logout'),
]