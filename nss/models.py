
from asyncio.windows_events import NULL
from email.policy import default
from pickle import TRUE
from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser


DEPT_CHOICES = (
    ("ECE", "ECE"),
    ("ISE", "ISE"),
    ("CSE", "CSE"),
    ("EEE", "EEE"),
    ("CIVIL", "CIVIL"),
    ("AERO", "AERO"),
    ("MECH", "MECH")
)
GENDER_CHOICES= (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("OTHER", "OTHER")
)



class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_ngo = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=TRUE)

    def __str__(self):
        return str(self.username)
   

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None,unique=True)
    phone_number = models.CharField(max_length=10)
    department = models.CharField(choices = DEPT_CHOICES,
    default = NULL, max_length=50)
    gender = models.CharField(choices = GENDER_CHOICES,
    default = NULL, max_length=50)
    

    def __str__(self):
        return str(self.user)


class Ngo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, unique=True)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
   
    
    def __str__(self):
        return str(self.user)




