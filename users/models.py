from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings 
import uuid


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    from_city = models.CharField(max_length=100)
    from_country = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=25)
    sex = models.CharField(max_length=1, default="m")
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def getAsDict(self):
        return { 'email': self.email, 'first_name': self.first_name, 'last_name': self.last_name, 'phone_num': self.phone_num, 'sex': self.sex, 'from_city': self.from_city, 'from_country': self.from_country, 'is_staff': self.is_staff, 'is_active': self.is_active, 'is_admin': self.is_admin }

    def addOtherUserInfo(self, first_name, last_name, phone_num, sex, from_city, from_country):
        return { **self.getAsDict(), 'first_name': first_name, 'last_name': last_name, 'phone_num': phone_num, 'sex': sex, 'from_city': from_city, 'from_country': from_country }

    def __str__(self):
        return self.email

    # original function name: has_perm
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    # original name: has_module_perms
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin