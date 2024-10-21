import random
import time
from airbnb_scraper import AirbnbScraper
from url_builder import URLBuilder

# Diccionario de ubicaciones con sus respectivos IDs
LOCATIONS = {
    "ANTONIO NARIÑO": "ChIJzYwoOMmeP44RF7iErav7Jg0",
    "BARRIOS UNIDOS": "ChIJ6WFCSP6aP44RIujZPPZisvY",
    "BOSA": "ChIJ6Sh07G-eP44RAdG49C4lxUY",
    "CANDELARIA": "ChIJy3nPRKiZP44RMROn2mQYjaU",
    "CHAPINERO": "ChIJgwW_iJ6QP44Rc7wFsOAC5M4",
    "CIUDAD BOLIVAR": "ChIJb2A-s-6hP44RCtQ56Pk_xgo",
    "ENGATIVA": "ChIJhTa7MamcP44R9A_fFp_Ee3c",
    "FONTIBON": "ChIJHaPSpV-cP44RRgySMYfH-aU",
    "KENNEDY": "ChIJeWMYwSCcP44RrHXiIb6MxHI",  
    "LOS MARTIRES": "ChIJGRtzwW-ZP44RyhT1aOU51Wc",
    "PUENTE ARANDA": "ChIJtbVi8lqZP44R4OCH4LRAv58",
    "RAFAEL URIBE URIBE": "ChIJM95Jj7eYP44RZP91dTHHG9Y",
    "SAN CRISTOBAL": "ChIJyTEmr4yYP44RyEyAcrR7BTk",
    "SANTA FE": "ChIJaU8k9SSaP44RoS6Stp4wY8g",
    "SUBA": "ChIJFwRwnVCEP44RFE_5QOlpzcc",
    "SUMAPAZ": "ChIJH0gDNhn3Po4RfgRfL2zF9wU",
    "TEUSAQUILLO": "ChIJN3NkpeqbP44RWZMQLjdYo28",
    "TUNJUELITO": "ChIJKyHw51afP44RlL4iA4jg4as",
    "USAQUEN": "ChIJ61tOXYCPP44Rb3xHQhxhUwg",
    "USME": "ChIJt9qBZPmjP44R4KJ7vKBwMqQ"
}

def scrape_location_data(location_name, group_size, max_pages):
    """Realiza el scraping de una localidad específica."""
    search_url = URLBuilder.build_search_url(
        city=location_name,
        state='Bogotá DC'
    )
    print(f"URL de búsqueda personalizada: {search_url}")

    scraper = AirbnbScraper(base_url=search_url)
    scraper.run(group_size=group_size, max_pages=max_pages, output_filename="airbnb_listings.csv")

    return scraper.residuales

def iterate_over_locations(group_size):
    """Itera sobre todas las localidades y ejecuta el scraper en cada una."""
    contador_iter = 0

    for location in LOCATIONS:
        print(f"Iteración {contador_iter} para la localidad: {location}")

        marg_sites = 6
        while marg_sites > 5:
            contador_iter += 1
            delay = random.randrange(0, 60)
            print(f"Esperando {delay} segundos antes de la próxima ejecución...")

            marg_sites = scrape_location_data(location, group_size, max_pages=3)
            print(f"Residuales: {marg_sites}")
            
            time.sleep(delay)

def main(flag_use, group_size, max_pages):
    """
    Controla la ejecución del scraping:
    - Si flag_use es True, itera sobre todas las localidades.
    - Si flag_use es False, ejecuta el scraping solo para 'Localidad'.
    """
    if flag_use:
        iterate_over_locations(group_size)
    else:
        scrape_location_data('KENNEDY', group_size, max_pages)

if __name__ == "__main__":
    main(flag_use=False, group_size=6, max_pages=3)

    

                
            


