from django.shortcuts import render
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
# from django.utils.encoding import force_text
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.http import Http404
from django.views import View
import base64
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.http import JsonResponse
from .models import PostList,UserAccessToken
from pyfacebook import GraphAPI
import uuid
import os
import requests
from .helper import *
# Create your views here.


def CreatePost(request):
    if request.method == 'POST':
        titl1e = request.POST.get('title')
        post_date = request.POST.get('post_date')
        image = request.FILES.get('image')
        option = request.POST.get('option')
        description = request.POST.get('description')
        page_id = request.POST.get('page_id')
        item = PostList.objects.create(title=titl1e, post_date=post_date, image=image, option=option, description=description,page_id=page_id)
        item.save()
        token = UserAccessToken.objects.filter(user=request.user,types='LinkedIn').first()
        if token and not item.image.url:
            data = create_linkedin_post(page_id,token.token,description)
        if  token and  item.image.url:
            data =  create_media_linkedin_post(page_id,token.token,description,f'{settings.BASE_URL}{item.image.url}')
            
        return redirect('list')
    return render(request, 'createpost.html')





def ItemList(request):
    item = PostList.objects.all()
    return render(request,'list.html',{'item':item})




def update_item(request, pk):
    item = get_object_or_404(PostList, pk=pk)
    if request.method == 'POST':
        item.title = request.POST['title']
        item.post_date = request.POST['post_date']
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        item.option = request.POST['option']
        item.description = request.POST['description']
        item.save()
        return redirect('list')
    return render(request, 'update.html', {'item': item})


def delete_item(request, pk):
    item = get_object_or_404(PostList, pk=pk)
    item.delete()
    return redirect('list')


###########_________________________________facebook_________________________##############################


from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
import requests


def facebook_login(request):
    redirect_uri = request.build_absolute_uri(reverse('facebook_callback'))
    print(redirect_uri,'========')
    facebook_dialog_url = f"https://www.facebook.com/v11.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&scope=manage_pages,publish_pages,pages_manage_post"
    return redirect(facebook_dialog_url)



def facebook_callback(request):
    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri(reverse('facebook_callback'))
    access_token_url = f"https://graph.facebook.com/v11.0/oauth/access_token?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&client_secret={settings.FACEBOOK_APP_SECRET}&code={code}"
    response = requests.get(access_token_url)
    data = response.json()
    access_token = data.get('access_token')
    print("herer is token")
    print(access_token)

    if access_token:
        user_id = request.user.id 
        token_type = 'Facebook'
        try:
            user_token = UserAccessToken.objects.get(user_id=user_id, types=token_type)
            user_token.token = access_token
            user_token.save()
        except UserAccessToken.DoesNotExist:
            UserAccessToken.objects.create(user_id=user_id, token=access_token)

    return redirect('/')




def facebook_post(access_token, message, media_url):
    post_url = f"https://graph.facebook.com/v11.0/me/photos"
    params = {
        'message': message,
        'url': media_url,
        'EAAMyO3w2oHEBO3HE7b56eXRCrOaDGZAzJ80pdezaGXVNsQnzFOQIaWA8DZC1uYBAxmW47ShVhZB1kuQrlD2U3ZBgpXwDiEqP74dK3dZBJy60bPZB2IADhuEB5ZAzCtcajEdeMfCAokEg67dbCPZA0QC3Jsw1ZCEAsvSGpLotpHw7KFPWj20FK0JHleHq0dPPbyVWSIzMi79ttzVigeaZBTZBVOiEWwg6GO8wBUzzu1DS8PZBBgrFCUut08wAlgaHEi26': access_token
    }
    response = requests.post(post_url, data=params)
    return response.json()



def post_on_facebook_with_media(request):
    access_token = request.session.get('access_token') 
    message = "Check out this amazing photo!"
    media_url = "https://example.com/path/to/your/image.jpg"  
    
    if access_token:
        response = facebook_post(access_token, message, media_url)
        if 'id' in response:
            return redirect('/')  
        else:
            return redirect('/')
    else:
        return redirect('/')





#####_________________________Linked In __________________________________#####################
    

from django.shortcuts import render
from django.http import JsonResponse
import requests

def generate_token(request):
    authorization_url = 'https://www.linkedin.com/oauth/v2/authorization'
    client_id = '77x0dj98nkfbjx'
    redirect_uri = 'https://ddivesocial.com/'
    state = '12345'
    scope = 'r_liteprofile'

    redirect_url = f"{authorization_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}"
    return redirect(redirect_url)

def get_access_token(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            url = 'https://www.linkedin.com/oauth/v2/accessToken'
            params = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'https://yourwebsite.com/callback',
                'client_id': '77x0dj98nkfbjx',
                'client_secret': 'RXh9auhH88gPQLwp'
            }
            response = requests.post(url, data=params)
            if response.status_code == 200:
                access_token = response.json()['access_token']
                return JsonResponse({'access_token': access_token})
            else:
                return JsonResponse({'error': 'Failed to retrieve access token'}, status=400)

def verify_token(request):
    if request.method == 'GET':
        access_token = request.GET.get('access_token')
        if access_token:
            api_url = 'https://api.linkedin.com/v2/me'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/json',
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                return JsonResponse({'message': 'Access token is valid!'})
            else:
                return JsonResponse({'error': 'Access token is invalid or has expired'}, status=400)

def create_post(request):
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        if access_token:
            api_url = 'https://api.linkedin.com/v2/ugcPosts'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/json',
            }
            post_body = request.POST.get('post_body', {})
            response = requests.post(api_url, headers=headers, json=post_body)
            if response.status_code == 201:
                return JsonResponse({'message': 'Post successfully created!'})
            else:
                return JsonResponse({'error': f'Post creation failed with status code {response.status_code}: {response.text}'}, status=400)