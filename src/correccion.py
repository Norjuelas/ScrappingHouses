from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options

from urllib.parse import urlparse

import pandas as pd
import os
import requests, re, time

from urllib.parse import urlparse
from bs4 import BeautifulSoup

class AirbnbScraper:
    def __init__(self, base_url):
        """
        Inicializa el scraper con las configuraciones necesarias.
        """
        self.driver = self.init_driver(True)
        self.base_url = base_url
        self.master_df = pd.DataFrame()
        print("WebDriver inicializado.")

    def init_driver(self,process:bool):
        """Inicializa el WebDriver con las opciones necesarias."""
        if not process:
            options = Options() 
            options.add_argument("--headless")
            return webdriver.Firefox(options=options)
        else:
            webdriver.Firefox()


    def navigate_to(self, url):
        """Navega a una URL específica y espera a que la página cargue."""
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'cy5jw6o')))
        print(f"Navegando a {url}")

    def extract_listings(self):
        """Extrae los datos de las tarjetas en la página actual utilizando BeautifulSoup."""
        soup = self.get_soup()
        cards = self.find_cards(soup)
        return [self.extract_card_data(card) for card in cards if self.extract_card_data(card)]
 
    def get_soup(self):
        """Obtiene el HTML de la página actual y lo convierte en BeautifulSoup."""
        try:
            page_source = self.driver.page_source
            return BeautifulSoup(page_source, 'html.parser')
        except Exception as e:
            print(f"Error al obtener el HTML: {e}")
            return None

    def find_cards(self, soup):
        """Encuentra todas las tarjetas de listados en la página."""
        try:
            return soup.find_all('div', class_='cy5jw6o')
        except Exception as e:
            print(f"Error al encontrar las tarjetas: {e}")
            return []

    def extract_card_data(self, card):
        """Extrae los datos de una tarjeta individual."""
        try:
            link_component = card.find('a', class_='bn2bl2p')
            id_publication = self.extract_id_publication(link_component)
            if not id_publication:
                return None
            
            TypeDescription = card.find('div', class_='t1jojoys').get_text(strip=True)
            description = card.find('div', class_='s1cjsi4j').get_text(strip=True)
            image = card.find('img', class_='itu7ddv')['src']
            price = card.find('span', class_='_11jcbg2').get_text(strip=True)
            rating = card.find('span', class_='r4a59j5').get_text(strip=True)
            
            lat, lon = self.extract_lat_lon(id_publication)
            #ListaComentarios = self.extract_first_comment(id_publication)

            return {
                "link": link_component['href'] if link_component else None,
                "TypeDescription": TypeDescription,
                "description": description,
                "image": image,
                "price": price,
                "rating": rating,
                "idPublication": id_publication,
                "lat": lat,
                "lon": lon,
                "TypeRoomOrHouse": self.roomOrHouse(TypeDescription),
                "ListaComentarios": ListaComentarios
                #"PrimerComentario": ListaComentarios[0] if ListaComentarios else None
            }
        except Exception as e:
            print(f"Error al extraer un card: {e}")
            return None

    def extract_id_publication(self, link_component):
        """Extrae el idPublication del enlace del componente."""
        try:
            return urlparse(link_component['href']).path.split('/')[-1]
        except (AttributeError, IndexError):
            return None

    def extract_next_links(self):
        """Extrae los enlaces para las próximas páginas desde la página actual."""
        try:
            wait = WebDriverWait(self.driver, 10)
            buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c1ackr0h")))
            return [button.get_attribute("href") for button in buttons if button.get_attribute("href")]
        except TimeoutException:
            print("Tiempo de espera excedido al extraer enlaces.")
            return []
        except Exception as e:
            print(f"Error al extraer los enlaces: {e}")
            return []

    def extract_lat_lon(self, idPublication):
        """Extrae la latitud y longitud de la página del listado."""
        URL = f'https://www.airbnb.com.co/rooms/{idPublication}'
        try:
            r = requests.get(URL)
            lat = re.search(r'"lat":([-0-9.]+),', r.text).group(1)
            lon = re.search(r'"lng":([-0-9.]+),', r.text).group(1)
            return lat, lon
        except Exception:
            return 0, 0

    def roomOrHouse(self, TypeDescription):
        """Clasifica la propiedad como habitación o casa según la descripción."""
        return "room" if TypeDescription.startswith("Habitación") else "house"

    def save_to_csv(self, filename="airbnb_listings.csv"):
        """Guarda el DataFrame acumulado en un archivo CSV sin sobrescribir, eliminando duplicados."""
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            existing_df = pd.read_csv(filename)
        else:
            existing_df = pd.DataFrame()

        combined_df = pd.concat([existing_df, self.master_df], ignore_index=True)
        combined_df.drop_duplicates(subset=['idPublication'], inplace=True)
        combined_df.to_csv(filename, index=False)

    def run(self, group_size=3, max_pages=15, output_filename="airbnb_listings.csv"):
        """Ejecuta el proceso completo de scraping."""
        self.navigate_to(self.base_url)
        starting_links = self.extract_next_links()
        if not starting_links:
            print("No se encontraron enlaces iniciales.")
            return

        self.master_df = self.extract_data_in_groups(starting_links, group_size, max_pages)
        self.save_to_csv(output_filename)

    def extract_first_comment(self, idPublication: str) -> list:
        """
        Extrae todas las fechas de los comentarios de la publicación dada.

        :param idPublication: ID de la publicación de Airbnb.
        :return: Lista de fechas de los comentarios en formato de cadena, o una lista vacía si no hay comentarios.
        """
        try:
            # Acceder a la página de comentarios de la publicación
            self.driver.get(f'https://www.airbnb.com.co/rooms/{idPublication}/reviews')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 's78n3tv')))
            
            # Obtener el HTML de la página
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source,'html.parser')

            # Intentar extraer las fechas de los comentarios
            datesComments = soup.find_all('div', class_='s78n3tv')
            comment_dates = []

            if datesComments:
                # Extraer todas las fechas y añadirlas a la lista
                for date in datesComments:
                    date_text = date.get_text(strip=True)
                    comment_dates.append(date_text)
                return comment_dates
            else:
                print(f"No se encontraron comentarios en la publicación {idPublication}.")
                return []
            
        except Exception as e:
            print(f"Error al extraer las fechas de los comentarios de la publicación {idPublication}: {e}")
            return []
        
    def extract_data_in_groups(self, starting_links, group_size=3, max_pages=15):
        """Extrae datos en grupos de pestañas."""
        links_to_process = starting_links.copy()
        page_count = 0

        while links_to_process and page_count < max_pages:
            current_group = links_to_process[:group_size]
            links_to_process = links_to_process[group_size:]

            for link in current_group:
                self.driver.execute_script(f"window.open('{link}', '_blank');")
                print(f"Abriendo nueva pestaña: {self.extract_id_publication(link)}")
                self.wait_for_page_load()

            for handle in self.driver.window_handles[1:]:  # Ignorar la pestaña principal
                self.driver.switch_to.window(handle)
                print(f"Procesando pestaña")
                self.wait_for_page_load()

                cards_data = self.extract_listings()
                print(f"Datos extraídos: {len(cards_data)} cards")
                
                if cards_data:
                    df_current = pd.DataFrame(cards_data)
                    self.master_df = pd.concat([self.master_df, df_current], ignore_index=True)

                # Extraer nuevos enlaces solo desde la última pestaña procesada
                if page_count == 0:
                    new_links = self.extract_next_links()
                    if new_links:
                        links_to_process.extend(new_links)

                self.driver.close()
                page_count += 1
                print(f"Páginas procesadas: {page_count}/{max_pages}")

                if page_count >= max_pages:
                    break

            self.driver.switch_to.window(self.driver.window_handles[0])
            print("Volviendo a la pestaña principal.")

        return self.master_df

