from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache


@receiver(user_logged_in, sender=User)
def login_successful(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    print("Clients IP :" ,ip)
    request.session['ip']= ip
    ct = cache.get('count', 0, version=user.pk)
    new_count = ct + 1
    cache.set('count', new_count, 60*60*24 , version=user.pk)
