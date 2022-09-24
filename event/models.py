from lzma import PRESET_DEFAULT
from operator import mod
from django.db import models

from nss.models import Ngo, Student, User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
# Create your models here.





class Activity(models.Model):
    name = models.CharField('Activity Name', max_length=300)
    event_date = models.DateTimeField('Activity Date')
    venue = models.TextField(blank=True)
    manager = models.ForeignKey(Ngo, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    
    def __str__(self):
	    return str(self.name)


class Activity_Details(models.Model):

    ABSENT = 'A'
    PRESENT = 'P'
    ATTEND_CHOICES = (
    (PRESENT,"Present"),
    (ABSENT, "Absent")
    )

    activity_name = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Student, blank=True)
    attendence = models.CharField(attendees,max_length=1, choices=ATTEND_CHOICES, default= PRESENT)
    marks = models.IntegerField(attendees, validators=[MinValueValidator(0), MaxValueValidator(100)])
    def __str__(self):
	    return str(self.activity_name)


