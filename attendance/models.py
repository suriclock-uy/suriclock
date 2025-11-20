from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Sector(models.Model):
    nombre = models.CharField(max_length=50)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    radio_metros = models.IntegerField(default=150)  # geofence

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ci = models.CharField(max_length=12, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    es_dueno = models.Boolean inField(default=False)  # puede marcar manual sin QR

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.sector}"

class Marcacion(models.Model):
    TIPO = (('entrada', 'Entrada'), ('salida', 'Salida'))
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=10, choices=TIPO)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    manual = models.BooleanField(default=False)

    class Meta:
        unique_together = ('empleado', 'fecha_hora', 'tipo')

    def __str__(self):
        return f"{self.empleado} - {self.tipo} - {self.fecha_hora.strftime('%d/%m %H:%M')}"