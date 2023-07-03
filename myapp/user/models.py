from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Create your models here.
# AbstractUser -> 인증된 사용자 모델
# 이것을 사용하려면 settings.py에 AUTH_USER_MODEL = 'user.User' 설정해줘야 하며 설정하지 않을 경우 에러가 남
'''
Auth User model
- 생성
- 삭제
- 수정
--> UserManager helper class 도움주는 클래스
'''

class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            is_staff = is_staff,
            is_active = True,
            is_superuser = is_superuser,
            last_login = now,
            data_joined = now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # create_user -> usermanager안에 있는 원래 있던 기능
    # create_superuser -> 원래 있던 기능
    def create_user(self,email,password,**extra_fields):
        return self._create_user(email,password,False,False,**extra_fields)
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email,password, True,True, **extra_fields)
    


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length = 255)
    # 이메일을 적는 필드 unique=True를 줌으로써 user가 여러명 있어도 중복되지 않아야 한다. 
    name = models.CharField(max_length=50, null=True, blank=True)
    # 회원가입 과정에서 null=True, blank=True를 줌으로써 이름을 빈칸으로 안써도 된다. -> 나중에 회원정보 수정할 때 이름을 넣어도 가능하니까
    # password = models.CharField(max_length=50)
    # registered_date = models.DateTimeField(auto_now_add=True)
    # 처음 가입 한 날 최초 생성할 땐 auto_now_add 이 생성일은 변하지 않는다.
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELDS = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    # 유니크한 값을 이메일로 많이 주다 보니까 views.py에 username을 이메일로 준다는 것이다.
    
    # required_fields 는 터미널에 이메일, 패스워드 입력해주는 값 넣는것
    
    objects = UserManager()
    
    def __str__(self):
        return self.name
    # 클래스 user 객체 생성되었을 때 admin에서 이름으로 보여지는게 편할 것 같아서 설정
    # 그래서 admin에 들어가보면 사용자 'aaa' 이렇게 name으로 들어가있다