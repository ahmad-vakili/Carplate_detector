from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import upload_video, show_result

app_name = 'license_plate'

urlpatterns = [
    path('', upload_video, name='upload'),
    path('result/', show_result, name='show_result'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='license_plate:upload'), name='logout'),
]

