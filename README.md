<div align="center">

# Suriclock · Sistema de Control Horario

Plataforma Django para registrar asistencia con kioscos QR, panel administrativo y sincronización con Google Sheets.

</div>

## Tabla de contenidos

1. [Descripción general](#descripción-general)
2. [Arquitectura y módulos](#arquitectura-y-módulos)
3. [Características principales](#características-principales)
4. [Requisitos previos](#requisitos-previos)
5. [Puesta en marcha rápida](#puesta-en-marcha-rápida)
6. [Variables de entorno](#variables-de-entorno)
7. [Operación diaria](#operación-diaria)
8. [Mantenimiento y tareas programadas](#mantenimiento-y-tareas-programadas)
9. [Pruebas automatizadas](#pruebas-automatizadas)
10. [Estructura del repositorio](#estructura-del-repositorio)
11. [Créditos](#créditos)

## Descripción general

Suriclock digitaliza el proceso de marcación de personal mediante QR o ingreso manual supervisado. Los empleados realizan marcajes desde un kiosco optimizado para tablets, mientras que RRHH administra sectores, licencias y reportes desde un panel seguro. Toda la información queda disponible en la base de datos local y, opcionalmente, en Google Sheets para análisis adicional.

## Arquitectura y módulos

- `attendance`: núcleo de negocio (modelos, vistas de administración y kiosco, utilidades, comandos).
- `FacultyView` / `StudentView`: frontales heredados para casos académicos (QR en aula).
- `suriclock`: proyecto Django, configuración y URLs raíz.
- `docs/`: guías específicas (Apps Script, etc.).
- `pwa/`: manifiesto y *service worker* opcionales para el kiosco.

El stack principal incluye Django 4.2, PostgreSQL/SQLite (via `dj-database-url`), autenticación estándar y entrega de estáticos con WhiteNoise.

## Características principales

- Gestión de empleados, sectores con geocercas y credenciales PIN.
- Marcaciones con soporte de foto, geolocalización y distintos tipos (entrada, salida, descansos).
- Dashboard administrativo con métricas diarias, solicitudes de reseteo de PIN y licencias.
- Reporte de horas con cálculo de extras al 50 %/100 % y nocturnas.
- Sincronización opcional hacia Google Sheets (`sync_sheets`).
- Limpieza automática de fotografías antiguas (`purge_old_photos`).
- Kiosco preparado para PWA/offline y cambio de PIN por el empleado.

## Requisitos previos

- Python 3.11+
- `pip` y entorno virtual opcional
- Acceso a SQLite (por defecto) o PostgreSQL
- Credenciales de servicio de Google si se activará la sincronización

## Puesta en marcha rápida

```bash
git clone https://github.com/<tu-org>/suriclock.git
cd suriclock
python -m venv venv && source venv/bin/activate  # opcional pero recomendado
pip install --upgrade pip
pip install -r requirements.txt
cp env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Abre `http://localhost:8000` para acceder al kiosco y `http://localhost:8000/admin/` para el backoffice.

## Variables de entorno

El archivo `env.example` documenta todas las claves soportadas. Las más relevantes:

| Variable | Descripción |
| --- | --- |
| `SECRET_KEY` | Clave criptográfica de Django. Genera una nueva para producción. |
| `DEBUG` | `True` solo en desarrollo. |
| `ALLOWED_HOSTS` | Lista separada por comas. Incluye dominio público o *.railway.app*. |
| `CSRF_TRUSTED_ORIGINS` | Orígenes seguros para formularios. |
| `DATABASE_URL` | Cadena compatible con `dj-database-url` (`postgres://`, `sqlite:///path`, etc.). |
| `DJANGO_LOG_LEVEL` | Nivel de log (`INFO`, `WARNING`, etc.). |

Guarda credenciales de Google en `google_sheets/credentials.json` y configura `SystemConfig.google_sheet_id` desde el panel o shell.

## Operación diaria

1. **Panel Admin**: permite crear empleados, asignar sectores y aprobar licencias (`/admin/dashboard`).
2. **Kiosco**: expone QR con la IP local y permite marcar usando PIN o cámara (`/kiosk`).
3. **Reset de PIN**: los empleados solicitan cambios; el administrador atiende desde la vista de empleados.
4. **Reportes**: la sección de asistencia consolida horas, extras y nocturnidad para los últimos 30 días.

Consulta `docs/APPS_SCRIPT_GUIDE.md` para integrar Apps Script o exponer el kiosco en pantallas dedicadas.

## Mantenimiento y tareas programadas

| Tarea | Comando | Frecuencia sugerida |
| --- | --- | --- |
| Limpiar fotos (>30 días) | `python manage.py purge_old_photos` | Diario |
| Sincronizar Google Sheets | `python manage.py sync_sheets` | Cada hora o al cierre |
| Copia de seguridad BD | `python manage.py dumpdata > backup.json` | Semanal |

Agrega estas tareas a `cron`, `systemd timers` o el scheduler de tu hosting (Railway, Heroku, etc.).

## Pruebas automatizadas

La carpeta `attendance/tests/` cubre vistas admin, flujo de PIN, licencias y utilidades. Ejecuta:

```bash
python manage.py test
```

Integra este comando en tu pipeline CI antes de desplegar a producción.

## Estructura del repositorio

```text
attendance/        # App principal (modelos, vistas, templates, tests)
FacultyView/       # Interfaces para docentes
StudentView/       # Interfaces para estudiantes
google_sheets/     # Scripts y credenciales de integración
docs/              # Guías adicionales
pwa/               # Manifest y service worker
suriclock/         # Configuración del proyecto Django
manage.py
```

## Créditos

- Basado originalmente en el proyecto “QR Attendance System” de Team Hokage.
- Mejoras, localización y capacidades de RRHH aportadas por la comunidad Suriclock.

¿Quieres contribuir? Envía un PR con pruebas actualizadas o abre un issue describiendo la mejora/bug. Mantén el estilo PEP 8 y actualiza documentación cuando corresponda.
