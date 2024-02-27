from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('createpost/',views.CreatePost, name="createpost"),
    path('list/', views.ItemList, name ="list"),
    path('update/<int:pk>/', views.update_item, name='update_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('facebook/login/', views.facebook_login, name='facebook_login'),
    path('facebook/callback/', views.facebook_callback, name='facebook_callback'),
    path('post-on-facebook-with-media/', views.post_on_facebook_with_media, name='post_on_facebook_with_media'),



    path('generate-token/', views.generate_token, name='generate_token'),
    path('get-access-token/', views.get_access_token, name='get_access_token'),
    path('verify-token/', views.verify_token, name='verify_token'),
    path('create-post/', views.create_post, name='create_post'),

    #social auth
    path('login2/', auth_views.LoginView.as_view(), name='login2'),
    path('logout2/', auth_views.LogoutView.as_view(next_page='home'), name='logout2'),
]