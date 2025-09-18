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
"""
from django.contrib import admin
from django.urls import path, include
from sisu.views import (
username_logic,
event_detail,
delete_guest,
edit_guest,
add_guest,
get_guest_by_event,
update_guest
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('sisu.urls')),
    path('event/<str:event_name_id>/login', username_logic, name='username_login'),
    path('event/<str:event_name_id>/', event_detail, name='event_detail'),
    path('event/<str:event_name_id>/delete/<int:guest_id>/', delete_guest, name='delete_guest'),
    path('event/<str:event_name_id>/edit/<int:guest_id>/', edit_guest, name='edit_guest'),
    path('event/<str:event_name_id>/save/', add_guest, name='add_guest'),
    path('api/events/<str:event_name_id>', get_guest_by_event, name='get_guest_by_event'),
    path('api/events/update/<str:event_name_id>', update_guest, name='update_guest'),
]
