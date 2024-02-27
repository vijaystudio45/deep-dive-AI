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
from pyfacebook import GraphAPI
import uuid
import os
import requests
from social_media_post.models import UserAccessToken




def index(request):
    return render(request, 'index.html')




def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
            return JsonResponse({'success': False, 'message': error_message,  'icon': True}, status=200)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email address."
            return JsonResponse({'success': False, 'message': error_message, 'icon': True}, status=200)
        # Create user
        User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        success_message = "Signup successful. You can now login."
        return HttpResponse(success_message)

    return render(request, 'signup.html')





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            success_message = "Login successful"
            return HttpResponse(success_message)

        else:
            error_message = "Invalid username or password. Please try again."
            return JsonResponse({'success': False, 'message': error_message}, status=500)

          

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')




User = get_user_model()

class CustomPasswordResetView(View):
    template_name = 'password_reset.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_message = {"error": "User with this email does not exist."}
            return JsonResponse(error_message, status=400)

        else:
            self.send_reset_email(request, user)
        success_message = "Password reset email has been sent."
        return HttpResponse(success_message)

       

    def send_reset_email(self, request, user):
        user_id_bytes = str(user.id).encode('utf-8')

        encoded_user_id = base64.b64encode(user_id_bytes).decode('utf-8')
        print(encoded_user_id,'encoded_user_idencoded_user_id')
        reset_url = reverse('password_reset_confirm', kwargs={'user_id': encoded_user_id})

        subject = 'Password Reset'
        message = render_to_string('authentication/templates/password_reset_email.txt', {
            'user': user,
            'reset_url': request.build_absolute_uri(reset_url),
        })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])





class CustomPasswordResetConfirmView(View):
    def get(self, request, user_id, *args, **kwargs):
        user_id_bytes = base64.b64decode(user_id.encode('utf-8'))
        user_id = int(user_id_bytes.decode('utf-8'))
        return render(request,"password_reset_confirm.html",{'user_id':user_id})
        
      

    def post(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'Password reset successful. You can now log in with your new password.'})
    

def privacypolicy(request):
    return render(request, 'privacy.html')




# ---- linkdin function ---#
def LinkeInAuthentication(request):
    url = f"{settings.LINKEDIN_BASE_URL}?response_type=code&client_id={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY}&state=random&redirect_uri={settings.LINKEDIN_REDIRECT_URL}&scope={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE}"
    return redirect(url)

def LinkedInAcessToken(request):
    auth_code = request.GET.get("code",None)
    if auth_code:
        payload = {
            'grant_type' : 'authorization_code',
            'code' : auth_code,
            'redirect_uri' : settings.LINKEDIN_REDIRECT_URL,
            'client_id' : settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
            'client_secret' : settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET
        }
        response = requests.post(url=settings.LINKEDIN_ACCESS_URL, params=payload)
        response_json = response.json()
        user_token = UserAccessToken.objects.filter(user=request.user,types='LinkedIn')
        if user_token:
            new_user_token = user_token.first()
            new_user_token.token =  response_json['access_token']
            new_user_token.save()
                        
        else:
            user_token = UserAccessToken.objects.create(user=request.user,types='LinkedIn',token=response_json['access_token'])
            user_token.save()
        # Extract the access_token from the response_json
        access_token = response_json['access_token']
        return redirect('/')
    return HttpResponse("something went wrong")





# def CreatePost(request):
#     if request.method == 'POST':
#         titl1e = request.POST.get('title')
#         print("herer is ",titl1e)
#         post_date = request.POST.get('post_date')
#         image = request.FILES.get('image')
#         option = request.POST.get('option')
#         description = request.POST.get('description')

#         item = PostList.objects.create(title=titl1e, post_date=post_date, image=image, option=option, description=description)
#         item.save()
#         try:
#             post_on_facebook(titl1e, description)  # Assuming image.url is the URL of the image
#         except Exception as e:
#             # Handle exceptions here
#             print("Failed to post on Facebook:", e)
#         return redirect('list')
#     return render(request, 'createpost.html')

# def post_on_facebook(titl1e, description):
#     # Initialize the GraphAPI with your access token
#     graph = GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
    
#     # Define the parameters of the post
#     params = {
#         'message': titl1e + "\n\n" + description
#     }
    
#     # If there's an image, add it to the parameters
    
#     # Post to Facebook
#     graph.put_object(parent_object='me', connection_name='feed', **params)
# # post_on_facebook("Title", "Description", "https://example.com/image.jpg")





# def ItemList(request):
#     item = PostList.objects.all()
#     return render(request,'list.html',{'item':item})

# def update_item(request, pk):
#     item = get_object_or_404(PostList, pk=pk)
#     if request.method == 'POST':
#         item.title = request.POST['title']
#         item.post_date = request.POST['post_date']
#         if 'image' in request.FILES:
#             item.image = request.FILES['image']
#         item.option = request.POST['option']
#         item.description = request.POST['description']
#         item.save()
#         return redirect('list')
#     return render(request, 'update.html', {'item': item})


# def delete_item(request, pk):
#     item = get_object_or_404(PostList, pk=pk)
#     item.delete()
#     return redirect('list')
   