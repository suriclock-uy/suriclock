from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os

def pwa_manifest(request):
    manifest_path = os.path.join(settings.BASE_DIR, 'pwa', 'manifest.json')
    with open(manifest_path, 'r') as f:
        return HttpResponse(f.read(), content_type='application/json')

def service_worker(request):
    sw_path = os.path.join(settings.BASE_DIR, 'pwa', 'service-worker.js')
    with open(sw_path, 'r') as f:
        return HttpResponse(f.read(), content_type='application/javascript')

from .models import Sector, Empleado, Marcacion, SystemConfig

def setup_wizard(request):
    if request.method == 'POST':
        try:
            # Handle File Upload
            if 'credentials' in request.FILES:
                creds_file = request.FILES['credentials']
                save_path = os.path.join(settings.BASE_DIR, 'google_sheets', 'credentials.json')
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                with open(save_path, 'wb+') as destination:
                    for chunk in creds_file.chunks():
                        destination.write(chunk)

            # Handle Sheet ID
            sheet_id = request.POST.get('sheet_id')
            
            # Save Config
            config, created = SystemConfig.objects.get_or_create(id=1)
            config.google_sheet_id = sheet_id
            config.is_configured = True
            config.save()
            
            return redirect('login')
            
        except Exception as e:
            return render(request, 'attendance/setup.html', {'error': str(e)})

    return render(request, 'attendance/setup.html')

def login_view(request):
    # Check if configured
    if not SystemConfig.objects.filter(is_configured=True).exists():
        return redirect('setup_wizard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'attendance/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'attendance/dashboard.html', {'user': request.user})

import json
from django.views.decorators.csrf import csrf_exempt
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * 1000 # meters

@csrf_exempt
@login_required
def mark_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sector_id = data.get('sector_id') # QR content should be the ID or code
            tipo = data.get('tipo') # 'entrada' or 'salida'
            lat = data.get('lat')
            lon = data.get('lon')
            
            # Validate Sector
            try:
                sector = Sector.objects.get(id=sector_id)
            except (Sector.DoesNotExist, ValueError):
                return JsonResponse({'status': 'error', 'message': 'Sector no válido'}, status=400)

            # Validate Geolocation
            if sector.requiere_geolocalizacion:
                if lat is None or lon is None:
                    return JsonResponse({'status': 'error', 'message': 'Ubicación requerida para este sector'}, status=400)
                
                dist = haversine(float(lon), float(lat), float(sector.longitud), float(sector.latitud))
                if dist > sector.radio_metros:
                    return JsonResponse({
                        'status': 'error', 
                        'message': f'Estás fuera del rango ({int(dist)}m). Acércate al sector.'
                    }, status=400)

            # Get Empleado profile
            try:
                empleado = request.user.empleado
            except Empleado.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Usuario no configurado como empleado'}, status=400)

            # Save Marcacion
            Marcacion.objects.create(
                empleado=empleado,
                tipo=tipo,
                sector=sector,
                latitud=lat,
                longitud=lon,
                manual=False
            )
            
            return JsonResponse({'status': 'ok', 'message': 'Marca registrada exitosamente'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
