import csv

from django.contrib import admin, messages
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html

from .forms import CSVUploadForm
from .models import Event, Guest, Host


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'place', 'event_name_id', 'host_link_invitation','invitation_link','view_guests_link')
    actions = ['generar_host_links', 'generar_invitation_link']

    def generar_host_links(self, request, queryset):
        for obj in queryset:
            obj.host_link_invitation = f"https://sisuadmineventos.com/event/{obj.id}/login"
            obj.save()
            messages.success(request,"Links creados para el anfitrion")
    generar_host_links.short_description = "Link de Anfitrion"

    def generar_invitation_link(self, request, queryset):
        for obj in queryset:
            obj.invitation_link = f"https://sisuinvitaciones.com/{obj.event_name_id}"
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
                    reader = csv.DictReader(decoded_file)

                    success_count = 0
                    update_count = 0
                    error_count = 0
                    error_details = []

                    for row_num, row in enumerate(reader, start=2):
                        try:
                            # Normalize column names
                            row_lower = {k.lower(): v for k, v in row.items()}

                            name = row_lower.get('name', '').strip()
                            invitations_str = row_lower.get('invitations', '0').strip()
                            cellphone = row_lower.get('cellphone', '').strip()
                            attend_str = row_lower.get('attend', 'false').strip().lower()
                            extra_guests = row_lower.get('extraguests', '').strip() or ''
                            table_number_str = row_lower.get('tablenumber', '0').strip()

                            # Validate required fields
                            if not name:
                                raise ValueError("Nombre es requerido")

                            # Convert values
                            try:
                                invitations = int(invitations_str) if invitations_str.isdigit() else 0
                                table_number = int(table_number_str) if table_number_str.isdigit() else 0
                            except ValueError:
                                invitations = 0
                                table_number = 0

                            confirmation_status = str_to_bool(attend_str)

                            # Update or create
                            guest, created = Guest.objects.update_or_create(
                                name=name,
                                event=event,
                                defaults={
                                    'invitations': invitations,
                                    'cellphone': cellphone,
                                    'assists': confirmation_status,
                                    'extraGuests': extra_guests,
                                    'table_number': table_number
                                }
                            )

                            if created:
                                success_count += 1
                            else:
                                update_count += 1

                        except Exception as e:
                            error_count += 1
                            error_details.append(f'Fila {row_num}: {str(e)}')
                            continue

                    # Show summary messages
                    if success_count or update_count:
                        messages.success(request,
                                         f'Procesamiento completado: {success_count} nuevos, {update_count} actualizados')

                    if error_count:
                        messages.warning(request, f'{error_count} errores encontrados')
                        # Show first 3 errors to avoid message overload
                        for error in error_details[:3]:
                            messages.warning(request, error)
                        if error_count > 3:
                            messages.info(request, f'... y {error_count - 3} errores más')

                except Exception as e:
                    messages.error(request, f'Error procesando archivo CSV: {e}')
            else:
                messages.error(request, 'Formulario inválido')
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
    return value.lower() in ['true', '1', 'yes', 'si', 'y', 's']

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