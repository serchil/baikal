from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.




class User(AbstractUser):
    name =  models.CharField(max_length=200, blank=True, null = True)
    second_name =  models.CharField(max_length=200, blank=True, null = True)
    surname =  models.CharField(max_length=200, blank=True, null = True)
    phone_number = models.CharField(max_length=200, blank=True, null = True)
    email = models.CharField(max_length=200, unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email





class Slider(models.Model):
    name = models.CharField(max_length=200)
    img = models.FileField(upload_to="images", max_length=100, null=True)
    show_on_main_status = models.BooleanField()

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null = True)
    preview_descr = models.TextField()
    preview_img = models.FileField(upload_to="images", max_length=100, null=True)
    header_place = models.ForeignKey('self', null=True, blank=True, related_name='placee', on_delete=models.SET_NULL)
    coords = models.CharField(max_length=200, null=True)
    slider = models.ManyToManyField(Slider)
    activity_status = models.BooleanField()
    min_price = models.IntegerField()
    show_on_main_status = models.BooleanField()
    def __str__(self):
        return self.name



class Tour(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=200)
    number_of_days = models.IntegerField()
    min_price = models.IntegerField()
    places = models.ManyToManyField(Place,  null=True, blank=True)
    slider = models.ManyToManyField(Slider,  null=True, blank=True)
    preview_descr = models.TextField()
    preview_img = models.FileField(upload_to="images", max_length=100, null=True, blank=True)
    activity_status = models.BooleanField()
    show_on_main_status = models.BooleanField()
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['id']





class Day(models.Model):
    header = models.CharField(max_length=200)
    number = models.IntegerField()
    description = models.TextField()
    img = models.FileField(upload_to="images", max_length=100, null=True)
    tourID = models.ForeignKey(Tour, on_delete=models.CASCADE)
    def __str__(self):
        return self.header



class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    preview_descr = models.TextField()
    preview_img = models.FileField(upload_to="images", max_length=100, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    min_price = models.IntegerField()
    coords = models.CharField(max_length=200, null=True)
    slider = models.ManyToManyField(Slider, null=True, blank=True)
    activity_status = models.BooleanField()
    def __str__(self):
        return self.name





class TourInTimetable(models.Model):
    name = models.CharField(max_length=200)
    tourID = models.ForeignKey(Tour, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField()
    capacity = models.IntegerField()
    hotels = models.ManyToManyField(Hotel)
    def __str__(self):
        return self.name


class BookingTour(models.Model):
    tourInT = models.ForeignKey(TourInTimetable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    payment = models.IntegerField()
    number_of_people = models.IntegerField()
    date_of_booking = models.DateField(null=True, blank=True)
    def __int__(self):
        return self.id



class Publications(models.Model):
    name = models.CharField(max_length=200)
    preview_descr = models.TextField()
    allText = models.TextField()

    preview_img = models.FileField(upload_to="images", max_length=100, null=True)
    img = models.FileField(upload_to="images", max_length=100, null=True)
    activity_status = models.BooleanField()
    def __str__(self):
        return self.name




class Team(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField()
    img = models.FileField(upload_to="images", max_length=100, null=True)
    def __str__(self):
        return self.name
