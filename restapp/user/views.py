from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
# from .models import User
from .forms import RegisterForm, LoginForm


# Create your views here.
# user 관련된 기능
# 회원가입
# 로그인
# 로그아웃

### Registration
class Registration(View):
    # 일반 'view'는 def get/ def post로 나타날 수 있다.
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        # 회원가입 페이지
        # 정보를 입력 할 폼을 보여주어야 한다.
        form = RegisterForm()
        context = {
            'form':form,
            'title': 'User'
        }
        return render(request, 'user/user_register.html', context)
    
    def post(self,request):
        # submit 눌렀을 때 post요청해야한다.
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 폼의 내용을 저장 해주겠다
            # 로그인한 다음 이동
            return redirect('user:login')
        # 회원가입하고 로그인 페이지로 넘어가기
        

### Login
class Login(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        
        form = LoginForm()
        context = {
            'form': form,
            'title': 'User'
        }
        return render(request, 'user/user_login.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        
        form = LoginForm(request, request.POST)
        if form.is_valid():
            # cleaned_data로 값을 불러옴
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user가 진짜 있는 유저인지 알려줌
            # username=email에 넣는 것 models.py에서 설정
            user = authenticate(username=email, password=password) # boolean값으로 나옴 사용자가 여기 회원인가? 아닌가? True,False로 반환
            
            if user: # True면?
                # user를 로그인 된 상태가 된다.
                login(request, user)
                return redirect('blog:list')
            
            # if문이 유효하지 않다면(False)라면?
            form.add_error(None, '아이디가 없습니다.')
            # 폼 안에 기본적인 함수 add_error
            
        context = {
            # 에러가 들어간 폼을 보여주는 것
            'form' : form
        }
            
        return render(request, 'user/user_login.html', context)
    
    
### Logout
# 로그인이 되어야 로그아웃을 할 수 있기 때문에
# 로그인이 되어있는게 전제조건이다
class Logout(View):
    def get(self, request):
        # 이 요청 안에는 이미 user의 로그인이 되어있다.
        logout(request)
        # auth형태이기 때문에 로그아웃을 할 수 있다.
        return redirect('blog:list')


### Profile
# 조회, 쓰기
# 수정, 삭제
class ProfileWrite(APIView):
    # def get():
    #     pass # url로 이동
    def post(self, request):
        user = request.data.get('user') # request.user
        image = request.data.get('image')
        age = request.data.get('age')
        
        profile = Profile.objects.create(user=user, image=image, age=age)
        serializer = ProfileSerializer(profile)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
# 과제
class ProfileUpdate(APIView):
    def get():
        pass
    def post():
        pass
    

class ProfileDelete(APIView):
    def post(self, request):
        # profile - user
        profile = Profile.objects.get(user=request.user)