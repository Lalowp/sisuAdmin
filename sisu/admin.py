import csv

from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.html import format_html

from .forms import CSVUploadForm
from .models import Event, Guest, Host

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'place', 'event_name_id', 'host_link_invitation','invitation_link','view_guests_link')
    actions = ['generar_host_links', 'generar_invitation_link']

    def generar_host_links(self, request, queryset):
        for obj in queryset:
            obj.host_link_invitation = f"http://127.0.0.1:8000/event/{obj.id}/login"
            obj.save()
            messages.success(request,"Links creados para el anfitrion")
    generar_host_links.short_description = "Link de Anfitrion"

    def generar_invitation_link(self, request, queryset):
        for obj in queryset:
            obj.invitation_link = f"https://sisuinvitaciones.com/{obj.event_name_id}/login"
            obj.save()
            messages.success(request, "Links creados para la invitacion")
    generar_invitation_link.short_description = "Link de invitacion"

    def view_guests_link(self, obj):
        return format_html('<a href="{}">Ver Invitados</a>', obj.get_guests_url())
    view_guests_link.allow_tags = True
    view_guests_link.short_description = 'Invitados'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:event_id>/guests/', self.admin_site.admin_view(self.view_guests), name='event_guests'),
        ]
        return custom_urls + urls

    def view_guests(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        guests = event.guests.all()
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    next(reader, None)
                    for row in reader:
                        name, invitations, cellphone, attend = row
                        confirmation_status = str_to_bool(attend)
                        Guest.objects.create(name=name, invitations=invitations, cellphone=cellphone,
                                             assists=confirmation_status, has_clicked=False, event=event)
                    messages.success(request, 'Archivo enviado')
                    return redirect('event_guests_view', event_id=event.id)
                except Exception as e:
                    messages.error(request, f'Error importando CSV: {e}')
            else:
                messages.error(request, 'El archivo no fue enviado')
        else:
            form = CSVUploadForm()

        context = dict(
            self.admin_site.each_context(request),
            event=event,
            guests=guests,
            form=form
        )
        return TemplateResponse(request, "sisu/event_guests.html", context)

def str_to_bool(value):
    return value.lower() in ['true', '1', 'yes', 'si', 'y']

def str_to_integer(value):
    return int(value)


class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'cellphone', 'invitations', 'assists', 'event')
    list_filter = ('event', 'assists',)
    search_fields = ('event', 'name',)
    list_editable = ('invitations', 'cellphone',)
    list_per_page = 25

class HostAdmin(admin.ModelAdmin):
    list_display = ('username', 'evento')

admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Host, HostAdmin)