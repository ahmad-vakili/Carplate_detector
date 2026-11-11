from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from .forms import VideoUpload
from .models import DetectedPlate
from license_plate.detect import detect_license_plate_yolo
import cv2
from django.core.files.base import ContentFile
import numpy as np

class VideoUploadView(FormView):
    template_name = 'license_plate/upload_video.html'
    form_class = VideoUpload

    def form_valid(self, form):
        video_obj = form.save(commit=False)
        video_obj.user = self.request.user
        video_obj.save()

        # پردازش پلاک
        plate_text = detect_license_plate_yolo(video_obj.video.path)

        # ذخیره فریم نمونه
        cap = cv2.VideoCapture(video_obj.video.path)
        ret, frame = cap.read()
        cap.release()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            image_file = ContentFile(buffer.tobytes(), name='frame.jpg')

            DetectedPlate.objects.create(
                video=video_obj,
                plate_text=plate_text,
                frame_image=image_file
            )

        return redirect('license_plate:result', plate_text=plate_text)

class PlateResultView(TemplateView):
    template_name = 'license_plate/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plate_text = self.kwargs.get('plate_text')
        plate_obj = DetectedPlate.objects.filter(plate_text=plate_text).last()
        context['plate'] = plate_obj
        return context