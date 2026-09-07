# Sistema de Administración de Edificio

Sistema web (Flask + base de datos + login) para reemplazar tu Excel de control
de ingresos/egresos, lecturas de medidores de agua y cuentas por cobrar de cada vecino.

## Qué incluye

- **Login protegido** (usuario y contraseña, con hash seguro).
- **Libro diario**: registro de ingresos y egresos (caja/banco/QR), con filtros por fecha y tipo.
- **Lecturas de agua**: registras lectura anterior/actual y el sistema calcula automáticamente
  consumo en m³, costo de agua, expensa fija, multa y total a cobrar.
- **Estado de cuenta por vecino**: cuánto debe cada uno (agua + expensas + otras deudas como préstamos).
- **Vecinos**: alta/baja, número de medidor, teléfono.
- **Configuración**: monto de expensa, precio del agua por m³, precios de limpieza — editables sin tocar código.
- **Reportes**: resumen de caja, estado de cuentas y planilla de lecturas, en pantalla y exportables a Excel.

## 1. Probarlo en tu computadora (antes de subirlo)

```bash
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
flask --app app init-db         # crea la base de datos y el usuario admin
flask --app app run
```

Abre `http://localhost:5000`, usuario **admin**, contraseña **admin123**
(cámbiala de inmediato desde el menú de usuario → "Cambiar contraseña").

### Importar tus datos actuales del Excel

Para no empezar de cero, puedes cargar tu archivo actual:

```bash
python import_excel.py "Libro_I_O_Eva_1_-__2025.xlsx"
```

Esto crea automáticamente a los vecinos, sus lecturas de agua históricas y los movimientos
de caja (ingresos/egresos) que ya tenías registrados. Revisa los datos después de importar,
ya que un Excel puede tener formatos irregulares que conviene verificar manualmente.

## 2. Subirlo a internet gratis (para tener tu link propio) — Render.com

Yo no puedo dejar un servidor corriendo permanentemente desde aquí, pero desplegar esto
en Render toma unos 10 minutos y es gratis para este tamaño de proyecto:

1. Crea una cuenta en https://render.com (puedes entrar con GitHub).
2. Sube esta carpeta a un repositorio de GitHub (o usa "Upload" si Render lo permite en tu plan).
3. En Render: **New +** → **Web Service** → conecta tu repositorio.
4. Configuración del servicio:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. En **Environment**, agrega la variable `SECRET_KEY` con un valor largo y aleatorio.
6. (Opcional pero recomendado) Crea una base de datos **PostgreSQL** gratuita en Render
   y copia su "Internal Database URL" como variable de entorno `DATABASE_URL` — así tus
   datos no se pierden si Render reinicia el disco. Si no la configuras, el sistema usa
   SQLite (un archivo local), que funciona pero puede reiniciarse en el plan gratuito.
7. Deploy. Render te da un link tipo `https://tu-app.onrender.com` — ese es el link que
   compartes con los vecinos o usas tú para administrar.
8. La primera vez que corre, el sistema crea solas las tablas y el usuario admin/admin123.
   Entra y cambia la contraseña de inmediato.

Alternativas equivalentes si prefieres: **Railway.app** (pasos casi idénticos) o
**PythonAnywhere** (bueno si nunca usaste GitHub).

## 3. Seguridad básica ya incluida

- Todas las páginas (excepto login) exigen sesión iniciada.
- Contraseñas guardadas con hash (nunca en texto plano).
- Cambia `SECRET_KEY` y la contraseña de `admin` antes de compartir el link.

## 4. Estructura del proyecto

```
edificio_app/
├── app.py              # rutas y lógica principal
├── models.py           # tablas de la base de datos
├── import_excel.py      # importador de tu Excel actual
├── requirements.txt
├── Procfile             # para Render/Railway
└── templates/           # páginas HTML
```

## Nota sobre pruebas

Este entorno de trabajo no tiene acceso a internet, así que no pude instalar las
dependencias (Flask-SQLAlchemy, Flask-Login, gunicorn) para correr una prueba en vivo
aquí mismo; sí verifiqué que el código no tiene errores de sintaxis. Al instalar
`requirements.txt` en tu computadora o en Render, si aparece algún error dime el mensaje
exacto y lo corrijo.
