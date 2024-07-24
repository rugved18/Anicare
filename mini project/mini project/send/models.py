#models.py
from django.db import models
from django.conf import settings
import os
from django.core.validators import EmailValidator

# from django.contrib.gis.db import models

class UserSubmission(models.Model):
    user_name = models.CharField(max_length=100)
    submission_data = models.TextField()
    submission_time = models.DateTimeField(auto_now_add=True)


# class ngoForm(models.Model):
#     ngoUserName = models.CharField(max_length=20)
#     ngoPhoneNumber = models.IntegerField()
#     ngoImage = models.ImageField()
#     # ngoLocation = models.PointField()
#     ngoDesc = models.TextField()
#     ngoAniType = models.CharField(max_length=10)
#     ngoAniPriority = models.CharField(max_length=15)


from django.db import models

class AnimalReport(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=200, default='Unknown Location')  # Set a default value
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    animal_type = models.CharField(max_length=10, choices=[('pet', 'Pet'), ('stray', 'Stray')])
    priority = models.CharField(max_length=15, choices=[('emergency', 'Emergency'), ('urgent', 'Urgent'), ('not_urgent', 'Not Urgent')], default='not_urgent')  # Set a default value
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    def __str__(self):
        return self.name


class UploadFile(models.Model):
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.file.name
    
    def save(self, *args, **kwargs):
        # Get the base directory of the Django project
        base_directory = settings.BASE_DIR
        # Define the full path where the file will be saved
        file_path = os.path.join(base_directory, 'uploads', self.file.name)
        super().save(*args, **kwargs)
