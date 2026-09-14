# VajiSTech — Django + MySQL

Proyecto académico de inmobiliaria para SENA. Incluye:
- Inicio / landing
- Catálogo de propiedades
- Filtros por ciudad, tipo y operación
- Detalle de propiedad
- Registro e inicio de sesión
- Favoritos
- Panel de administración de Django
- Asistente inmobiliario Vaji (versión local, sin API externa)
- MySQL
- Diseño responsive

## 1. Crear entorno virtual

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Crear base de datos MySQL

En MySQL Workbench ejecuta el contenido de `database.sql`.

Después copia `.env.example` como `.env` y pon tu contraseña de MySQL.

## 4. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 5. Cargar propiedades de prueba

```bash
python manage.py shell
```

Pega:

```python
from inmobiliaria.models import Property

data = [
{"title":"Casa en Chía","city":"Chía","neighborhood":"Vereda La Balsa","property_type":"Casa","operation":"Venta","price":650000000,"bedrooms":4,"bathrooms":3,"parking":2,"area":210,"description":"Casa moderna con amplias zonas verdes, excelente iluminación y espacios familiares.","image_url":"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80","featured":True},
{"title":"Casa Moderna","city":"Bogotá","neighborhood":"Cedritos","property_type":"Casa","operation":"Venta","price":450000000,"bedrooms":4,"bathrooms":3,"parking":2,"area":180,"description":"Casa moderna en zona residencial, cercana a comercio y transporte.","image_url":"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80","featured":True},
{"title":"Apartamento Laureles","city":"Medellín","neighborhood":"Laureles","property_type":"Apartamento","operation":"Venta","price":320000000,"bedrooms":3,"bathrooms":2,"parking":1,"area":95,"description":"Apartamento cómodo en Laureles, ideal para vivir o invertir.","image_url":"https://images.unsplash.com/photo-1502672023488-70e25813eb80?auto=format&fit=crop&w=1200&q=80","featured":True},
{"title":"Casa en Medellín","city":"Medellín","neighborhood":"Belén","property_type":"Casa","operation":"Venta","price":450000000,"bedrooms":4,"bathrooms":4,"parking":1,"area":160,"description":"Casa familiar en sector tradicional de Medellín.","image_url":"https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1200&q=80","featured":False},
{"title":"Casa Campestre","city":"Chía","neighborhood":"Zona rural","property_type":"Casa","operation":"Venta","price":650000000,"bedrooms":5,"bathrooms":4,"parking":3,"area":320,"description":"Casa campestre con piscina y amplias zonas verdes.","image_url":"https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=80","featured":False},
{"title":"Apartamento Bogotá","city":"Bogotá","neighborhood":"Chapinero","property_type":"Apartamento","operation":"Arriendo","price":2200000,"bedrooms":2,"bathrooms":2,"parking":1,"area":72,"description":"Apartamento para arriendo con excelente ubicación y acceso a transporte.","image_url":"https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80","featured":False},
]
for item in data:
    Property.objects.get_or_create(title=item["title"], defaults=item)
print("Propiedades cargadas.")
```

Salir:
```python
exit()
```

## 6. Ejecutar

```bash
python manage.py runserver
```

Abrir:
http://127.0.0.1:8000/

Administración:
http://127.0.0.1:8000/admin/

## GitHub

```bash
git init
git add .
git commit -m "Proyecto VajiSTech inmobiliaria"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git push -u origin main
```

No subas `.env` a GitHub. Agrega un `.gitignore` con:
```
venv/
.env
__pycache__/
*.pyc
media/
```

## Para la sustentación

Puedes explicar la arquitectura así:
- `models.py`: estructura de propiedades y favoritos.
- `views.py`: lógica de negocio.
- `urls.py`: rutas.
- `templates/`: interfaz HTML.
- `static/`: CSS y JavaScript.
- MySQL: persistencia de usuarios, propiedades y favoritos.
- Django Admin: administración de inmuebles.
- Vaji IA: módulo de asistencia conversacional.
