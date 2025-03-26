from datetime import date

from django.db import models
from django.urls import reverse

HOST_URL_DOMAIN = ''

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateTimeField()
    place = models.CharField(max_length=300, default='', blank=True)
    event_name_id = models.CharField(max_length=300, blank=True, editable=False)
    host_link_invitation = models.CharField(max_length=300, default='', blank=True)
    invitation_link = models.CharField(max_length=300, default='', blank=True)

    def save(self, *args, **kwargs):
        #Save the object to get and ID if it doesn't have one
        if not self.name:
            super(Event, self).save(*args, **kwargs)
        self.event_name_id = f"{self.name.replace(' ', '').lower()}"
        '''
        self.host_link_invitation = f"event/{self.id}/login"
        self.invitation_link = f"event/{self.event_name_id}"
        '''
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_guests_url(self):
        return reverse('sisu:event_guests_view', args=[self.pk])

class Guest(models.Model):
    name = models.CharField(max_length=300)
    invitations = models.IntegerField(default=0)
    cellphone = models.CharField(max_length=100)
    assists = models.BooleanField(default=False)
    extraGuests = models.CharField(max_length=300, default='', blank=True)
    event = models.ForeignKey(Event, related_name='guests', on_delete=models.CASCADE, default='')
    table_number = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Host(models.Model):
    username = models.CharField(max_length=100)
    evento = models.ForeignKey(Event, related_name='hosts', on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.username