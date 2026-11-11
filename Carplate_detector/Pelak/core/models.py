from django.db import models

class VideoUpload(models.Model):
    color = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        plate = self.detectedplate_set.first()
        return f"{self.car_type} - {plate.plate_text if plate else 'Without Plate'}"


class DetectedPlate(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    plate_text = models.CharField(max_length=20)          # قبلاً اشتباهاً ImageField بود
    frame_image = models.ImageField(upload_to="results/", blank=True, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)
