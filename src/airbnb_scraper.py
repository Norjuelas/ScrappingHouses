# airbnb_scraper.py

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

        :param base_url: URL principal para iniciar el scraping.
        """
        self.driver = self.init_driver() 
        self.base_url = base_url
        self.master_df = pd.DataFrame()
        self.residuales = None
        print("WebDriver inicializado.")
    
    def init_driver(self):
        """Inicializa el WebDriver con las opciones necesarias."""
        options = Options() 
        options.add_argument("--headless")
        return webdriver.Firefox(options=options)
    
    def wait_for_page_load(self, seconds=3, element=None, by=By.CLASS_NAME):
        """
        Espera a que la página cargue completamente o hasta que un elemento específico esté presente.
        
        :param seconds: Tiempo máximo de espera (en segundos).
        :param element: Nombre del elemento a esperar (opcional).
        :param by: Tipo de localizador de elementos (opcional, predeterminado By.CLASS_NAME).
        :return: True si se encuentra el elemento o si la página carga dentro del tiempo, False si ocurre un Timeout.
        """
        try:
            if element is None:
                # Espera hasta que expire el tiempo indicado
                WebDriverWait(self.driver, seconds).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            else:
                # Espera hasta que el elemento esté presente en el DOM
                WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located((by, element)))
            return True
        except TimeoutException:
            print(f"Tiempo de espera agotado después de {seconds} segundos.")
            return False
    
    def get_soup(self):
        """Obtiene el HTML de la página actual y lo convierte en BeautifulSoup."""
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            return soup
        except Exception as e:
            print(f"Error al obtener el HTML: {e}")
            return None
        
    def find_cards(self, soup):
        """Encuentra todas las tarjetas de listados (cards) en la página."""
        try:
            return soup.find_all('div', class_='cy5jw6o')
        except Exception as e:
            print(f"Error al encontrar las tarjetas de listado: {e}")
            return []
    def scroll_to_bottom(self):
        """Desplaza la página hasta el final para cargar todo el contenido."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait_for_page_load()
        
    def extract_listings(self):
        """Extrae los datos de las tarjetas en la página actual utilizando BeautifulSoup."""
        cards_data = []
        try:
            soup = self.get_soup()  # Llamada a la función para obtener el BeautifulSoup
            cards = self.find_cards(soup)  # Llamada a la función para encontrar las cards
            print(f"Encontrados {len(cards)} cards en la página.")
            
            for card in cards:
                card_data = self.extract_card_data(card)
                if card_data:
                    cards_data.append(card_data)
        
        except Exception as e:
            print(f"Error al encontrar las cards: {e}")
        
        return cards_data

    def extract_card_data(self, card):
        """Extrae los datos de una tarjeta individual."""
        try:
            link_component, TypeDescription, description, image, price, rating, idPublication = self.parse_card(card)
            
            # Obtener latitud y longitud
            lat, lon = self.extract_lat_lon(idPublication)
            #Obtener primer comentario
            ListaComentarios = self.extract_first_comment(idPublication)            
            # Crear diccionario con la información extraída
            data = {
                "link": link_component['href'] if link_component else None,
                "TypeDescription": TypeDescription.get_text(strip=True) if TypeDescription else None,
                "description": description.get_text(strip=True) if description else None,
                "image": image['src'] if image else None,
                "price": price.get_text(strip=True) if price else None,
                "rating": rating.get_text(strip=True) if rating else None,
                "idPublication": idPublication if idPublication else None,
                "lat": lat if lat else None,
                "lon": lon if lon else None,
                "TypeRoomOrHouse": self.roomOrHouse(TypeDescription.get_text(strip=True)) if TypeDescription else None,
                "ListaComentarios": ListaComentarios if ListaComentarios else None,
                "PrimerComentario": ListaComentarios[0] if ListaComentarios else None
            }
            return data
        
        except Exception as e:
            print(f"Error al extraer un card: {e}")
            return None
 
    def extract_next_links(self):
        """Extrae los enlaces para las próximas páginas desde la página actual."""
        try:
            wait = WebDriverWait(self.driver, 10)
            buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c1ackr0h")))
            links = [button.get_attribute("href") for button in buttons if button.get_attribute("href")]
            print(f"Enlaces extraídos exitosamente")
            return links
        except TimeoutException:
            print("Tiempo de espera excedido al extraer enlaces.")
            return []
        except Exception as e:
            print(f"Error al extraer los enlaces: {e}")
            return []
    def extractIdpublication(self, link_component: str) -> str:
        # Verificar si el link_component es válido
        if link_component:
            # Extraer el idPublication del link
            idPublication = urlparse(link_component).path.split('/')[-1]
        else:
            # Si el link no es válido, retorna None
            idPublication = None

        return idPublication


    def extract_data_in_groups(self, starting_links, group_size=3, max_pages=15):
        """Extrae datos en grupos de pestañas."""
        links_to_process = starting_links.copy()
        page_count = 0

        while links_to_process and page_count < max_pages:
            current_group = links_to_process[:group_size]
            links_to_process = links_to_process[group_size:]

            for link in current_group:
                self.driver.execute_script(f"window.open('{link}', '_blank');")
                print(f"Abriendo nueva pestaña: {self.extractIdpublication(link)}")
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
    
    def extract_lat_lon(self, idPublication):
        attempts = 0
        success = False

        while not success and attempts < 10:
            try:
                URL = 'https://www.airbnb.com.co/rooms/'
                r = requests.get(URL + idPublication)
                p_lat = re.compile(r'"lat":([-0-9.]+),')
                p_lon = re.compile(r'"lng":([-0-9.]+),')
                lat = p_lat.findall(r.text)[0]
                lon = p_lon.findall(r.text)[0]
                success = True
                return lat , lon
            except:
                print('no existe cordenada')
                attempts += 1
        return 0 , 0
    def extract_comment_datesss(self, idPublication: str) -> list:
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
    
    def extract_first_comment(self, idPublication: str) -> list:
        """
        Extrae la fecha del primer comentario de la publicación dada.

        :param idPublication: ID de la publicación de Airbnb.
        :return: Fecha del primer comentario en formato de cadena, o None si no hay comentarios.
        """
        try:
            # Acceder a la página de comentarios de la publicación
            self.driver.get(f'https://www.airbnb.com.co/rooms/{idPublication}/reviews')
            self.wait_for_page_load()

            # Obtener el HTML de la página
            soup = self.get_soup

            # Intentar extraer las fechas de los comentarios
            datesComments = soup.find_all('div', class_='s78n3tv')
            lista = []
            if datesComments:
                # Tomar la fecha del primer comentario
                FirstCommentDate = datesComments[0].get_text(strip=True)
                return lista.append(FirstCommentDate)
            else:
                print(f"No se encontraron comentarios en la publicación {idPublication}.")
                return None
        except Exception as e:
            print(f"Error al extraer el primer comentario de la publicación {idPublication}: {e}")
            return None
    
    def roomOrHouse(self,TypeDescription:str)->str:
        """
        clasifica descripciones si es habitacion o apto
        """
        if TypeDescription.startswith("Habitación"):
            return "room"
        else: return "house"

    def parse_card(self, card):
        """Parsea una tarjeta y extrae los componentes individuales."""
        try:
            link_component = card.find('a', class_='bn2bl2p')
            TypeDescription = card.find('div', class_='t1jojoys')
            description = card.find('div', class_='s1cjsi4j')
            image = card.find('img', class_='itu7ddv')
            price = card.find('span', class_='_11jcbg2')
            rating = card.find('span', class_='r4a59j5')
            
            # Obtener idPublication del link
            if link_component and 'href' in link_component.attrs:
                idPublication = urlparse(link_component['href']).path.split('/')[-1]
            else:
                idPublication = None
            
            return link_component, TypeDescription, description, image, price, rating, idPublication
        
        except Exception as e:
            print(f"Error al parsear la tarjeta: {e}")
            return None, None, None, None, None, None, None
    def filterRoomOrHouse(self,df: pd.DataFrame) -> pd.DataFrame:
        """
        Añade una columna 'TypeRoomOrHouse' al DataFrame según el contenido de 'TypeDescription'.
        Si el valor de 'TypeDescription' comienza con 'Habitación', asigna 'room', de lo contrario 'house'.
        """
        print("añadiendo columna 'TypeRoomOrHouse' inexistente... ")
        # Crear una nueva columna 'TypeRoomOrHouse' basada en 'TypeDescription'
        #df['TypeRoomOrHouse'] = df['TypeDescription'].apply(lambda x: 'room' if x.startswith('Habitación') else 'house')        
        return df

    def run(self, group_size=3, max_pages=15, output_filename="airbnb_listings.csv"):
        """Ejecuta el proceso completo de scraping."""
        start_time = time.time()
        try:
            # Abrir la página principal
            self.driver.get(self.base_url)
            print(f"Navegando a {self.base_url}")
            self.wait_for_page_load()

            # Extraer los primeros enlaces
            starting_links = self.extract_next_links()
            if not starting_links:
                print("No se encontraron enlaces iniciales. Terminando el scraping.")
                return

            # Extraer datos en grupos de pestañas
            self.master_df = self.extract_data_in_groups(starting_links, group_size, max_pages)

            # Mostrar información del DataFrame
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', 20)
            pd.set_option('display.width', 1000)
            pd.set_option('display.colheader_justify', 'center')
            print("\nDatos acumulados:")
            print(self.master_df)

            print(f"\nDimensiones del DataFrame: {self.master_df.shape}")

            # Identificar datos duplicados
            duplicates = self.master_df[self.master_df.duplicated()]
            num_duplicates = duplicates.shape[0]
            print(f"\nDatos duplicados encontrados: {num_duplicates}")

            # Guardar los datos en CSV
            self.save_to_csv(output_filename)

        finally:
            self.driver.quit()
            print("WebDriver cerrado.")

            # Calcular y mostrar el tiempo total transcurrido
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"\nTiempo total de ejecución: {elapsed_time:.2f} segundos")

    def save_to_csv(self, filename="airbnb_listings.csv"):
        self.master_df, original_size = self.verificar_archivo_existente(filename)
        self.master_df = self.inicializar_dataframe(self.master_df)
        current_date = time.strftime('%Y-%m-%d %H:%M:%S')
        #self.master_df = self.actualizar_historial_precios(self.master_df, current_date)
        combined_df = self.eliminar_duplicados(self.master_df)
        self.actualizar_estadisticas(original_size, combined_df)
        self.guardar_dataframe(combined_df, filename)

    def inicializar_dataframe(self, master_df):
        current_date = time.strftime('%Y-%m-%d %H:%M:%S')
        master_df['last_read_date'] = current_date        
        return master_df

    def verificar_archivo_existente(self, filename):
        if os.path.exists(filename):
            original_size = self.master_df.shape[0]
            print(f"\nEl archivo existente tiene {original_size} registros.")
        else:
            self.master_df = pd.DataFrame()
            original_size = 0
            print("\nNo se encontró archivo existente. Se creará uno nuevo.")
        return self.master_df, original_size

    def actualizar_estadisticas(self, original_size, combined_df):
        final_size = combined_df.shape[0]
        new_data_count = final_size - original_size
        print(f"Nuevos datos añadidos: {new_data_count}")
        print(f"El DataFrame ha crecido de {original_size} a {final_size} registros.")
        self.residuales = new_data_count


    def guardar_dataframe(self, combined_df, filename):
        combined_df.to_csv(filename, index=False)
        file_path = os.path.join(os.getcwd(), filename)
        print(f"Datos exportados a: {file_path}")

    def eliminar_duplicados(self, master_df):
        return master_df.drop_duplicates(subset=['idPublication'], keep='last')

    def actualizar_historial_precios(self, master_df, current_date):
        for i, row in master_df.iterrows():
            matching_row = master_df[self.master_df['idPublication'] == row['idPublication']]
            
            if not matching_row.empty:
                index = matching_row.index[0]
                price_history = self.master_df.at[index, 'price_history']
                new_entry = (row['price'], current_date)
                price_history.append(new_entry)
                self.master_df.at[index, 'price_history'] = price_history
            else:
                new_price_history = [(row['price'], current_date)]
                row['price_history'] = new_price_history
                self.master_df = pd.concat([self.master_df, pd.DataFrame([row])], ignore_index=True)

        return master_df





