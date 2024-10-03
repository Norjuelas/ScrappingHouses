import firebase_admin
from firebase_admin import credentials, storage, db
import csv
from pathlib import Path
import time

# Inicializar Firebase Admin SDK
cred = credentials.Certificate('./Keys/scrapping-23f1a-firebase-adminsdk-3u3sg-718f03964d.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://scrapping-23f1a-default-rtdb.firebaseio.com/',
    'storageBucket': 'scrapping-23f1a.appspot.com'  # Asegúrate de que coincida con tu bucket
})

# Referencia a la base de datos
ref = db.reference('publicaciones')
ref2 = db.reference('csv_files')

# Ruta del archivo CSV
csv_file = './airbnb_listings.csv'
bucket = storage.bucket()

# Subir el archivo CSV a Firebase Storage
blob = bucket.blob(f'csv_files/{Path(csv_file).name}')
blob.upload_from_filename(csv_file)

# Obtener la URL de descarga
download_url = blob.generate_signed_url(version='v4', expiration=3600)

# Almacenar la URL en la base de datos
ref2.push({
    'file_name': Path(csv_file).name + " " + str(time.time),
    'file_url': download_url
})

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


print(f"Archivo CSV '{csv_file}' subido a Firebase Storage y URL almacenada en la base de datos.")
