from django.urls import path
from . import views

urlpatterns = [
    path('manifest.json', views.pwa_manifest, name='pwa_manifest'),
    path('service-worker.js', views.service_worker, name='service_worker'),
    path('setup/', views.setup_wizard, name='setup_wizard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
]
