from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError('이메일은 필수로 설정되어야 합니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', False)
        return self._create_user(email, name, password, **other_fields)

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        return self._create_user(email, name, password, **other_fields)


class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성')
    )
    LANGUAGE_CHOICES = (
        ('ko', '한국어'),
        ('zh_CN', '中文(简体)'),
        ('en', 'English')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    email = models.EmailField('이메일 주소', unique=True)
    name = models.CharField('이름', max_length=64)

    address1 = models.CharField('기본 주소', max_length=128)
    address2 = models.CharField('상세 주소', max_length=128)
    phone = models.CharField('유선전화', max_length=16)
    _phone = models.CharField('유선전화 w/o 하이픈', max_length=16)
    mobile_phone = models.CharField('휴대전화', max_length=16)
    _mobile_phone = models.CharField('휴대전화 w/o 하이픈', max_length=16)
    birth = models.DateField('생년월일', null=True)
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='ko')

    is_staff = models.BooleanField('어드민 여부', default=False)
    is_dormant = models.BooleanField('휴면 계정 여부', default=False)
    joined_time = models.DateTimeField('가입일시', default=timezone.now)

    is_certified = models.BooleanField('본인인증 여부', default=False)
    cert_imp_uid = models.CharField('본인인증 imp_uid', max_length=64)  # 아임포트 uid
    cert_unique_key = models.CharField('본인인증 unique_key', max_length=88)  # 개인 고유구분 식별키 (CI)
    cert_unique_in_site = models.CharField('본인인증 unique_in_site', max_length=64)  # 가맹점 내 고유구분 식별키 (DI)
    certified_time = models.DateTimeField('인증일시', null=True)

    objects = UserManager()

    def __str__(self):
        return self.email
