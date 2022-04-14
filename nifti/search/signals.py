from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from search.models import Post
from search.distance_calculation import get_coords_by_addr
from django.db.models import signals

#when a post receives the post_save signal, do this
@receiver(post_save, sender=Post)
def update_coordinates(sender, instance, **kwargs):
    lat,long = get_coords_by_addr(instance.address)
    instance.latitude = lat
    instance.longitude = long
    #disconnect so not endless loop
    signals.post_save.disconnect(update_coordinates, sender=Post)
    instance.save()
    signals.post_save.connect(update_coordinates, sender=Post)
