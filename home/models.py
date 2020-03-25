from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinLengthValidator, int_list_validator
from PIL import Image

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length = 1000)
    desc = models.TextField()
    Address = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    PhoneNo = models.CharField(verbose_name="Phone number", max_length=10,validators=[int_list_validator(sep=''),MinLengthValidator(10),], default='1234567890')
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_pics', blank=False)

    def __str__(self):
        return self.title
    
    def save(self):
        super().save()
        img=Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)



    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
