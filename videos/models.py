from django.db import models


class Video(models.Model):
    CATEGORY_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Documentary', 'Documentary'),
        ('Animation', 'Animation'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    video_file = models.FileField(upload_to='videos/original/')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
