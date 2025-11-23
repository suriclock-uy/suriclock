# Guía de Instalación: Automatización de Sueldos en Google Sheets

Esta guía te explica cómo instalar el script que calcula automáticamente las horas trabajadas y genera recibos PDF.

## Paso 1: Abrir el Editor de Scripts
1.  Abre tu Hoja de Cálculo de Google (la que configuraste en Suriclock).
2.  En el menú superior, ve a **Extensiones** > **Apps Script**.
3.  Se abrirá una nueva pestaña con un editor de código.

## Paso 2: Copiar el Código
1.  Borra cualquier código que aparezca en el archivo `Code.gs` (por defecto aparece `function myFunction() {...}`).
2.  Copia **todo** el contenido del archivo `google_sheets/google_apps_script.js` que está en este proyecto.
3.  Pégalo en el editor de Apps Script.

## Paso 3: Guardar y Ejecutar
1.  Dale un nombre al proyecto arriba a la izquierda (ej: "Suriclock Automation").
2.  Haz clic en el icono de **Guardar** (💾).
3.  Haz clic en el botón **Ejecutar** (▶️) para probar la función `onOpen`.
4.  Google te pedirá permisos ("Authorization required").
    *   Haz clic en **Review Permissions**.
    *   Elige tu cuenta.
    *   Si sale una advertencia ("Google hasn't verified this app"), haz clic en **Advanced** > **Go to Suriclock Automation (unsafe)**.
    *   Haz clic en **Allow**.

## Paso 4: Usar el Menú Suriclock
1.  Vuelve a tu Hoja de Cálculo.
2.  Verás un nuevo menú llamado **🦦 Suriclock** (si no aparece, recarga la página).
3.  Opciones disponibles:
    *   **🔄 Calcular Horas**: Lee las marcas, calcula horas trabajadas y extras, y crea una hoja "Reporte_Horas".
    *   **📄 Generar Recibo PDF**: Te pide el nombre de un empleado y crea un PDF en tu Google Drive.

## Notas Importantes
-   El script asume que las columnas de datos son: `[Fecha, Empleado, Tipo, Sector, Lat, Long]`. Si cambias el orden en Django, avísame para ajustar el script.
-   Las horas extras se calculan si se superan las 8 horas diarias.
