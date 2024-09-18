from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service  # Usar el servicio de Firefox
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import pandas as pd
import time 
import tkinter as tk
from tkinter import ttk

# Function to wait for a specific amount of time
def wait_for_page_load(driver, seconds):
    time.sleep(seconds)  # Waits for a specified amount of time
# Gets the navigation component, title and icons
def get_navigation():
        # Use WebDriverWait to ensure specific elements are loaded
    wait = WebDriverWait(driver, 4)
    navs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c1abgzgs")))
    # Print the count of elements found
    for nav in navs: 
        title = nav.find_element(By.CLASS_NAME, "t192ua0c ")
        image = nav.find_element(By.CLASS_NAME, "i181yxiv")
        print(title.text)
        print(image.get_attribute("src"))
#This function extracts the data from the current page 
def extract_listings():
    cards_data = []
    cards = driver.find_elements(By.CLASS_NAME, "cy5jw6o")
    for card in cards:
        link_component = card.find_element(By.CLASS_NAME, "bn2bl2p")
        location = card.find_element(By.CLASS_NAME, "t1jojoys")
        description = card.find_element(By.CLASS_NAME, "s1cjsi4j")
        image = card.find_element(By.CLASS_NAME, "itu7ddv")
        price = card.find_element(By.CLASS_NAME, "pquyp1l")
        rating = card.find_element(By.CLASS_NAME, "r4a59j5")
        for card in cards:
            card.click()  # Click on the first card

            # Wait for the new tab to open
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, "")
            # Switch to the most recently opened tab (which should be the new one)
        driver.switch_to.window(driver.window_handles[-1])
        # Close the current tab (the one that was clicked)
        driver.close()
        # Switch back to the original window (first window)
        driver.switch_to.window(driver.window_handles[0])
    
        data = {
            "link": link_component.get_attribute("href"),
            "location": location.text,
            "description": description.text,
            "image": image.get_attribute("src"),
            "price": price.text,
            "rating": rating.text
        }

        cards_data.append(data)
    return cards_data    

def show_table(dataframe):
    # Sanitize column names for Tkinter Treeview
    sanitized_columns = [col.replace(" ", "_").replace(".", "_") for col in dataframe.columns]

    # Create a window
    root = tk.Tk()
    root.title("DataFrame Viewer")
    
    # Create a frame for the table
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)
    
    # Create a treeview to display the DataFrame
    tree = ttk.Treeview(frame, columns=sanitized_columns, show="headings", height=25)
    tree.pack(side="left", fill="both", expand=True)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscroll=scrollbar.set)

    # Define columns
    for col in sanitized_columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Insert data into the treeview
    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

    # Start the Tkinter main loop
    root.mainloop()
# Set up the WebDriver


def extract_descriptions(driver):
    # Lista para almacenar los datos extraídos
    listings_data = []

    # Espera hasta que las publicaciones estén presentes
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cy5jw6o")))

    # Encuentra todas las publicaciones en la página
    listings = driver.find_elements(By.CLASS_NAME, "cy5jw6o")
    print(f"Se encontraron {len(listings)} publicaciones.")

    # Para cada publicación en la lista
    for index, listing in enumerate(listings):
        print(f"Procesando publicación {index + 1} de {len(listings)}")

        # Intenta obtener el enlace de la publicación
        try:
            link_element = listing.find_element(By.CLASS_NAME, "bn2bl2p")
            link = link_element.get_attribute('href')
        except Exception as e:
            print(f"Error al obtener el enlace de la publicación {index + 1}: {e}")
            continue  # Pasa a la siguiente publicación si hay un error

        # Abre el enlace en una nueva pestaña
        driver.execute_script("window.open(arguments[0], '_blank');", link)
        # Cambia a la nueva pestaña
        driver.switch_to.window(driver.window_handles[-1])

        # Volver a localizar el elemento body y presionar ESC
        try:
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
            print("Ventana emergente cerrada con tecla ESC.")
        except Exception as e:
            print(f"No se pudo enviar ESC al body: {e}")

        # Espera a que la descripción esté presente
        try:
            # Espera hasta que el elemento de descripción principal esté presente
            description_element = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-section-id="DESCRIPTION_DEFAULT"]')))
            description = description_element.text
            print(f"Descripción extraída de la publicación {index + 1}")

            # Volver a localizar el elemento body y presionar ESC
            try:
                body = driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.ESCAPE)
                print("Ventana emergente cerrada con tecla ESC.")
            except Exception as e:
                print(f"No se pudo enviar ESC al body: {e}")

            # Ahora, busca el botón con el texto "Mostrar los X servicios"
            try:
                # Encuentra y hace clic en el botón usando XPath con el texto
                services_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(text(), "Mostrar los")]')))
                services_button.click()
                print("Botón de servicios clickeado.")

                # Esperamos el elemento del popup
                popup_dialog = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//div[@role="dialog"]')))

                # Ahora encuentra todos los elementos que contienen los servicios
                service_elements = popup_dialog.find_elements(By.CLASS_NAME, 'twad414')

                # Extrae el texto de cada elemento
                services = [service.text for service in service_elements]

                # Combina los servicios en una cadena o almacénalos como lista
                additional_info = '\n'.join(services)
                print("Información adicional extraída.")

                # Cerrar la ventana emergente de servicios
                try:
                    # Intentar cerrar enviando ESC al popup
                    popup_dialog.send_keys(Keys.ESCAPE)
                    print("Ventana emergente de servicios cerrada con tecla ESC.")
                except Exception as e:
                    print(f"No se pudo cerrar la ventana emergente enviando ESC: {e}")

                # Si aún está abierta, intentar hacer clic en el botón de cerrar
                try:
                    if popup_dialog.is_displayed():
                        close_button = popup_dialog.find_element(
                            By.XPATH, './/button[@aria-label="Cerrar"]')
                        close_button.click()
                        print("Ventana emergente de servicios cerrada haciendo clic en el botón de cerrar.")
                except Exception as e:
                    print(f"No se pudo cerrar la ventana emergente con el botón de cerrar: {e}")

            except Exception as e:
                print(f"Error al extraer información adicional: {e}")
                additional_info = ""

            # Desplazar la página hacia abajo lentamente durante 1 segundo
            scroll_pause_time = 0.5  # Tiempo entre cada desplazamiento
            total_scroll_time = 1    # Tiempo total de desplazamiento
            scrolls = int(total_scroll_time / scroll_pause_time)
            for _ in range(scrolls):
                driver.execute_script("window.scrollBy(0, document.body.scrollHeight / %d);" % scrolls)
                time.sleep(scroll_pause_time)
            print("Página desplazada hacia abajo lentamente.")

            # Intentar arrastrar el Pegman hasta 3 veces
            latitude = ""
            longitude = ""
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    print(f"Intentando arrastrar el Pegman, intento {attempt + 1} de {max_attempts}")
                    # Esperar brevemente para asegurar que el mapa cargue
                    time.sleep(2)

                    # Encontrar el elemento del mapa usando el selector proporcionado
                    map_element = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '[data-testid="map/GoogleMap"]')))

                    # Desplazar el mapa a la vista
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", map_element)
                    print("Mapa desplazado al centro de la vista.")

                    # Esperar un poco después de desplazar
                    time.sleep(1)

                    # Crear una instancia de ActionChains
                    actions = ActionChains(driver)

                    # Encontrar el Pegman (el hombrecito)
                    pegman = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button[aria-label="Arrastra Pegman al mapa"]')))
                    print("Pegman encontrado.")

                    # Mover el cursor al Pegman
                    actions.move_to_element(pegman).perform()
                    time.sleep(0.5)

                    # Hacer clic y mantener presionado en el Pegman
                    actions.click_and_hold(pegman).perform()
                    time.sleep(0.5)

                    # Obtener las coordenadas del Pegman
                    pegman_location = pegman.location
                    pegman_x = pegman_location['x']
                    pegman_y = pegman_location['y']

                    # Obtener las coordenadas del centro del mapa
                    map_location = map_element.location
                    map_size = map_element.size
                    center_x = map_location['x'] + map_size['width'] / 2
                    center_y = map_location['y'] + map_size['height'] / 2

                    # Calcular el desplazamiento necesario
                    offset_x = center_x - pegman_x
                    offset_y = center_y - pegman_y

                    # Mover el Pegman al centro del mapa
                    actions.move_by_offset(offset_x, offset_y).perform()
                    time.sleep(0.5)

                    # Soltar el Pegman
                    actions.release().perform()
                    print("Pegman arrastrado al centro del mapa.")

                    # Esperar a que se cargue Street View o la nueva vista
                    time.sleep(5)

                    # Si se abre una nueva pestaña, cambiar a ella
                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])

                    # Obtener la URL actual
                    current_url = driver.current_url

                    # Extraer las coordenadas de la URL
                    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', current_url)
                    if match:
                        latitude = match.group(1)
                        longitude = match.group(2)
                        print(f"Coordenadas extraídas: Latitud = {latitude}, Longitud = {longitude}")
                    else:
                        print("No se pudieron extraer las coordenadas de la URL.")
                        latitude = ""
                        longitude = ""

                    # Si abrimos una nueva pestaña, cerrarla y volver a la original
                    if len(driver.window_handles) > 1:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[-1])

                    # Salir del ciclo si se logra arrastrar el Pegman y obtener las coordenadas
                    break

                except Exception as e:
                    print(f"Error al arrastrar el Pegman en el intento {attempt + 1}: {e}")
                    if attempt == max_attempts - 1:
                        latitude = ""
                        longitude = ""
                    else:
                        time.sleep(2)  # Esperar antes de reintentar

            # Agrega los datos a la lista
            listings_data.append({
                'link': link,
                'description': description,
                'additional_info': additional_info,
                'latitude': latitude,
                'longitude': longitude
            })

        except Exception as e:
            print(f"Error al extraer datos de la publicación {index + 1}: {e}")
        finally:
            # Cierra la pestaña actual
            driver.close()
            # Regresa a la pestaña original
            driver.switch_to.window(driver.window_handles[0])

            # Pequeña pausa para evitar sobrecargar el servidor
            time.sleep(1)

    return listings_data



# Configura el WebDriver
driver = webdriver.Firefox() 
os.system("clear")
try:
    # Abre la página de Airbnb
    driver.get("https://www.airbnb.com.co/s/Bogot%C3%A1--Colombia/homes")
    data = extract_listings()
    df = pd.DataFrame(data)
    show_table(df)


finally:
    time.sleep(5)
    driver.quit()
# Boton de servicios> twad414
# Todos los servicios: f16mr5nx
# # NO dispnible añadir id pdp_unavailable
#Disponible con class 19xnuo97

#VAloraciones c18arpj7 
# Reseñas b7zir4z

# Google pages: gm-iv-address-link pero primero toca colocar el muñeco en el apuntador del airbnb