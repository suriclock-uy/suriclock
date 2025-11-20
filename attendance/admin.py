from django.contrib import admin
from .models import Sector, Empleado, Marcacion

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud', 'radio_metros')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'ci', 'sector', 'es_dueno')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'ci')

@admin.register(Marcacion)
class MarcacionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha_hora', 'tipo', 'sector', 'manual')
    list_filter = ('tipo', 'manual', 'fecha_hora', 'sector')
    search_fields = ('empleado__user__username', 'empleado__ci')
