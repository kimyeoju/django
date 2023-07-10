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
# 헬퍼클래스
class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        now = timezone.localtime()
        email = self.normalize_email(email)
        # normalize_email 정규화를 실행하는 메서드(함수)이다.
        # 이메일 주소의 대소문자 구분에 따른 중복계정 방지를 위해 사용된다.
        user = self.model(
            email = email,
            is_staff = is_staff,
            is_active = True,
            is_superuser = is_superuser,
            last_login = now,
            date_joined = now,
            **extra_fields
        )
        # 일반 유저인지 관리자 유저인지를 메서드 실행시 입력 받은 값으로 구분해서 유저를 생성한다.
        user.set_password(password)
        # 암호화 과정을 더 해줌
        user.save(using=self._db)
        # using은 어떤 데이터베이스를 사용할 지 정해주는 매개변수로 self._db는 현재 사용중인 데이터베이스를 의미한다.
        # 일반유저로 생성할 것인지, 슈퍼유저로 생성할 것인지 판단 이후에 유저를 최종적으로 생성하는 부분
        return user
    # create_user -> usermanager안에 있는 원래 있던 기능
    # create_superuser -> 원래 있던 기능
    def create_user(self,email,password,**extra_fields):
        # user을 생성하는 함수
        return self._create_user(email,password,False,False,**extra_fields)
    def create_superuser(self, email, password, **extra_fields):
        # 관리자 user을 생성하는 함수
        return self._create_user(email,password, True,True, **extra_fields)
    
    
# 실제 모델이 상속받아 생성하는 클래스
class User(AbstractUser):
    username = None
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
    
    USERNAME_FIELD = 'email'
    # unique idntifier, unique = true가 옵션으로 설정된 필드값으로 설정
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    # 유니크한 값을 이메일로 많이 주다 보니까 views.py에 username을 이메일로 준다는 것이다.
    
    # required_fields 는 터미널에 이메일, 패스워드 입력해주는 값 넣는것
    
    objects = UserManager()
    # 반드시 objects 값을 통해 헬퍼 클래스를 지정해야 한다.
    
    # def __str__(self):
    #     return self.name
    # 클래스 user 객체 생성되었을 때 admin에서 이름으로 보여지는게 편할 것 같아서 설정
    # 그래서 admin에 들어가보면 사용자 'aaa' 이렇게 name으로 들어가있다

class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/media')
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)