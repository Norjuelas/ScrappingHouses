import firebase_admin
from firebase_admin import credentials, db
import csv

# Inicializar Firebase Admin SDK
cred = credentials.Certificate('./Keys/scrapping-23f1a-firebase-adminsdk-3u3sg-718f03964d.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://scrapping-23f1a-default-rtdb.firebaseio.com/'
})

# Referencia a la base de datos
ref = db.reference('publicaciones')

# Ruta del archivo CSV
csv_file = './airbnb_listings.csv'

# Leer el archivo CSV y subir los datos a Firebase
with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Crear un diccionario para almacenar los datos de la fila actual
        data = {
            'link': row.get('link', ''),
            'locationDescription': row.get('location', ''),
            'description': row.get('description', ''),
            'image': row.get('image', ''),
            'price': row.get('price', ''),
            'rating': row.get('rating', ''),
            'id_publicacion': row.get('id', ''),
            'lat': row.get('lat', ''),
            'lon': row.get('lon', ''),
            'last_read_date': row.get('last_read_date', ''),
            'TipoArrendamiento': row.get('TipoArrendamiento', ''),
            'HistorialPrecios': row.get('HistorialPrecios', '').split(','),  # Convertir cadena a lista
            'fechaprimerComentario': row.get('fechaprimerComentario', '')
        }
        
        # Subir los datos a Firebase bajo una nueva clave
        ref.push(data)

    print(f"Datos del archivo CSV {csv_file} cargados exitosamente a Firebase!")
