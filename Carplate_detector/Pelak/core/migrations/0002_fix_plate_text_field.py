from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detectedplate',
            name='plate_text',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='detectedplate',
            name='frame_image',
            field=models.ImageField(blank=True, null=True, upload_to='results/'),
        ),
    ]
