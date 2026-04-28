from django.db.models.signals import post_save
from django.dispatch import receiver
import django_rq
from .models import Video
from .utils import convert_to_hls, regenerate_thumbnail


@receiver(post_save, sender=Video)
def start_hls_conversion(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default')
        queue.enqueue(convert_to_hls, instance.id)


@receiver(post_save, sender=Video)
def handle_missing_thumbnail(sender, instance, created, **kwargs):
    if not created and not instance.thumbnail:
        queue = django_rq.get_queue('default')
        queue.enqueue(regenerate_thumbnail, instance.id)
