from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import VideoUploadView, PlateResultView

app_name = 'license_plate'

urlpatterns = [
    path("upload/", VideoUploadView.as_view(), name='upload'),
    path("result/<str:plate_text>", PlateResultView.as_view(), name='result'),

    # 👇 add these two lines
    path("login/", LoginView.as_view(template_name="license_plate/login.html"), name='login'),
    path("logout/", LogoutView.as_view(next_page="license_plate:upload"), name='logout'),
]
