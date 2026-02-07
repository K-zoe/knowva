from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.apps import apps
from django.contrib import auth

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user_object(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('ユーザー名は必須です。')

        if not email:
            raise ValueError('メールアドレスは必須です。')
        
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email = email, **extra_fields)
        user.set_password(password)
        return user

    def _create_user(self, username, email, password, **extra_fields):
        user = self._create_user_object(username, email, password, **extra_fields)
        user.save(using=self._db)
        return user
    
    async def _acreate_user(self, username, email, password, **extra_fields):
        user = self._create_user_object(username, email, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    create_user.alters_data = True

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return await self._acreate_user(username, email, password, **extra_fields)

    acreate_superuser.alters_data = True

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).' % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'ユーザー名',
        max_length=20,
        unique=True,
        help_text= '20文字以内で入力してください。文字、数字、「@.+-_」が使用できます。',
        validators=[username_validator],
        error_messages={
            'unique': 'そのユーザー名は既に使用されています。'
        },
    )

    email = models.EmailField(
        'メールアドレス',
        unique = True,
        blank=False,
        help_text= 'メールアドレスを入力してください。',
        error_messages={
            'unique':'そのメールアドレスは使用できません。'
        }
    )

    is_staff = models.BooleanField(
        '管理者権限',
        default=False,
        help_text='管理者権限を指定します。'
    )

    is_active = models.BooleanField(
        'アクティブフラグ',
        default=True,
        help_text='ユーザーがアクティブかどうかを判断します。'
    )
    
    created_at = models.DateTimeField(
        'ユーザー作成日',
        auto_now_add=True,
        help_text= 'ユーザー作成日を記録します。'
    )

    #BAN機能
    is_banned = models.BooleanField(
        'BANフラグ',
        default=False,
        help_text= 'BANフラグです。'
    )

    banned_reason = models.CharField(
        'BAN理由',
        max_length=300,
        null=True,
        blank=True,
        help_text = 'BAN理由を入力してください。'
    )

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー一覧'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(blank=True, null = True)