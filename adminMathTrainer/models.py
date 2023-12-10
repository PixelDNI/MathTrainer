from django.db import models

from django.contrib.auth.models import Group, Permission

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    groups = models.ManyToManyField(Group, related_name='custom_user', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user', blank=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_content_creator(self):
        if self.is_author:
            return True
        return False


class MathCourse(models.Model):
    title = models.CharField(max_length=255, blank=True)
    course_image = models.ImageField(null=True, upload_to='mathCourseImg/')
    description = models.TextField()
    course_content = RichTextField(default='')
    price = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course_user = models.ManyToManyField(User, related_name='enrolled_courses')
    user_favorites = models.ManyToManyField(User, related_name='liked_courses')
    course_length = models.IntegerField()
    course_discount = models.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ], default=0)


    def __str__(self):
        return self.title



class CourseRate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.OneToOneField(MathCourse, on_delete=models.CASCADE)
    rate = models.FloatField()


class CourseModule(models.Model):
    title = models.CharField(max_length=255)
    module_image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    math_course = models.ForeignKey(MathCourse, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    title = models.CharField(max_length=550, null=True)
    lecture_image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    paragraph = RichTextField()
    course_module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title


class CommonTest(models.Model):
    title = models.CharField(max_length=550, null=True)
    question = RichTextField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to='questionImg/', blank=True)
    answer = models.CharField(max_length=550)
    explanation = RichTextField(null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ChoiceTest(models.Model):
    question = RichTextField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to='questionImg/', blank=True)
    explanation = models.TextField(null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = RichTextField()
    is_right = models.BooleanField()
    choice_test = models.ForeignKey(ChoiceTest, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.answer
