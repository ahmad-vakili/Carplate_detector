from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .detect import detect_license_plate_yolo
from core.models import VideoUpload, DetectedPlate


def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        video_path = fs.path(filename)

        # تشخیص پلاک با YOLO + EasyOCR
        result_text = detect_license_plate_yolo(video_path)

        video_obj = VideoUpload.objects.create(
            color=request.POST.get('color', ''),
            car_type=request.POST.get('car_type', ''),
            video=video.name,
        )
        detected_plate = DetectedPlate.objects.create(
            video=video_obj,
            plate_text=result_text,
        )

        # نام متغیر باید دقیقاً با چیزی که result.html انتظار داره یکی باشه
        return render(request, 'license_plate/result.html', {'plate': detected_plate})

    # ⬅️ اینجا مسیر درست فایل HTML
    return render(request, 'license_plate/upload_video.html')


def show_result(request):
    return render(request, 'license_plate/result.html')