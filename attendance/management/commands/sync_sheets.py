import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.core.management.base import BaseCommand
from django.conf import settings
from attendance.models import Marcacion, SystemConfig
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Sync attendance records to Google Sheets'

    def handle(self, *args, **options):
        self.stdout.write('Starting Google Sheets sync...')

        # 1. Setup Credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds_path = os.path.join(settings.BASE_DIR, 'google_sheets', 'credentials.json')
        
        if not os.path.exists(creds_path):
            self.stdout.write(self.style.ERROR(f'Credentials file not found at: {creds_path}'))
            return

        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
            client = gspread.authorize(creds)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error authenticating: {str(e)}'))
            return

        # 2. Open Sheet
        config = SystemConfig.objects.first()
        if not config or not config.google_sheet_id:
            self.stdout.write(self.style.ERROR('System not configured. Please run setup wizard.'))
            return
            
        sheet_id = config.google_sheet_id

        try:
            sheet = client.open_by_key(sheet_id).sheet1 # Opens first sheet
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error opening sheet: {str(e)}'))
            return

        # 3. Get Data (Sync unsynced or just all for now? Let's do all for today)
        today = timezone.now().date()
        marcas = Marcacion.objects.filter(fecha_hora__date=today).order_by('fecha_hora')
        
        self.stdout.write(f'Found {marcas.count()} records for today.')

        # 4. Prepare Rows
        rows = []
        for marca in marcas:
            rows.append([
                marca.fecha_hora.strftime('%Y-%m-%d'),
                marca.fecha_hora.strftime('%H:%M:%S'),
                marca.empleado.ci,
                f"{marca.empleado.user.first_name} {marca.empleado.user.last_name}",
                marca.tipo,
                str(marca.sector),
                "Manual" if marca.manual else "QR"
            ])

        # 5. Append to Sheet
        if rows:
            try:
                sheet.append_rows(rows)
                self.stdout.write(self.style.SUCCESS(f'Successfully synced {len(rows)} rows.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error writing to sheet: {str(e)}'))
        else:
            self.stdout.write('No records to sync.')
