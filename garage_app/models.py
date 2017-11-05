from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Vehicle(models.Model):
    """Vehicle model"""
    reg_no = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, blank=True, default='')
    model = models.CharField(max_length=50, blank=True, default='')
    no_of_wheels = models.IntegerField(default=4,
                                       validators=[MaxValueValidator(20), MinValueValidator(0)])
    park_time = models.DateTimeField(auto_now_add=True)
    vehicle_type = models.ForeignKey('VehicleType')
    owner = models.ForeignKey('GarageMember')

    def __str__(self):
        return self.reg_no

    def get_absolute_url(self):
        return reverse('vehicle_list')

class VehicleType(models.Model):
    name = models.CharField(max_length=50)
    size = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.name

class GarageMember(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True) # validators should be a list

    def __str__(self):
        return self.first_name + " " + self.last_name


