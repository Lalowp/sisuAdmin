"""
URL configuration for sisuInvitaciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    /admin/sisu/event/2/guests
    href="/admin/sisu/event/2/guests"
    http://127.0.0.1:8000/admin/sisu/event/2/download-guests
"""
from django.urls import path
from . import views

app_name='sisu'
urlpatterns = [
    path('sisu/event/<int:event_id>/guests', views.event_guests_view, name='event_guests_view'),
]
