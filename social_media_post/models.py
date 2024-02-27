from django.db import models
from django.contrib.auth.models import User

# Create your models here.
OPTIONS_ON = (
    ('LinkedIn', 'LinkedIn'),
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook')
)

class PostList(models.Model):
    title = models.CharField(max_length=100)
    post_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')  # Specify the upload_to directory
    option = models.CharField(max_length=10, choices=OPTIONS_ON)  # Change 'options' to 'option'
    description = models.TextField()
    is_active = models.BooleanField(default = True)
    page_id = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.title
    



OPTIONS_ON = (
    ('LinkedIn', 'LinkedIn'),
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook')
)


class UserAccessToken(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='user_access_token' )
    token = models.CharField(max_length=4000)
    types = models.CharField(max_length=10, choices=OPTIONS_ON)
    created_at = models.DateTimeField(auto_now_add=True)