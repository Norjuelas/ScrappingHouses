import requests
from bs4 import BeautifulSoup

# Hacer la solicitud HTTP
response = requests.get('https://www.airbnb.com.co/rooms/700915825501568023/reviews?adults=1&children=0&enable_m3_private_room=true&infants=0&pets=0&search_mode=regular_search&check_in=2024-10-03&check_out=2024-10-08&source_impression_id=p3_1727984719_P35QTLCwRIrie2wM&previous_page_section_name=1000&federated_search_id=45fa6268-81bb-439d-b90a-0835a602a72d')

# Parsear el contenido de la página
soup = BeautifulSoup(response.content, 'html.parser')

# Usar un selector para identificar el elemento flotante
elemento_flotante = soup.select_one('a8jt5op')
rating = soup.find('span', class_='a8jt5op')

# Extraer el contenido
if elemento_flotante or rating:
    print("Contenido del elemento flotante:", elemento_flotante.text)
    print(rating.text)
else:
    print("F papa")

#script donde pruebo cosas raras