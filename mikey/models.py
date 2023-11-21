from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model

class RegisterManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse e-mail doit être définie')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Register(AbstractBaseUser):
    pseudo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=8)
    confirm_passwd = models.CharField(max_length=8)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RegisterManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['pseudo']

    def __str__(self):
        return self.pseudo
class Comment(models.Model):
    pseudo = models.ForeignKey('Register', on_delete=models.CASCADE, related_name='pseudo_comments')
   # profile_picture = models.ForeignKey('Register', on_delete=models.CASCADE, related_name='profile_picture_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    '''  @property
    def pseudo_photo(self):
        return self.pseudo.photo.url if self.pseudo.photo else None

    @property
    def profile_photo(self):
        return self.profile_picture.photo.url if self.profile_picture.photo else None
    '''
    def __str__(self):
        return f'{self.pseudo} - {self.created_at}'
