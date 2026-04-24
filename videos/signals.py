import django_rq
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from .utils import convert_to_hls


@receiver(post_save, sender=Video)
def start_hls_conversion(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default')
        queue.enqueue(convert_to_hls, instance)
