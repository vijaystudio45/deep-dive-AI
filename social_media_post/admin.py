from django.contrib import admin

# Register your models here.
from .models import PostList,UserAccessToken

class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_date', 'option')  # Customize the fields you want to display in the list view


class UserAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'types') 



# Register your models here.
admin.site.register(PostList, ListAdmin)
admin.site.register(UserAccessToken, UserAccessTokenAdmin)