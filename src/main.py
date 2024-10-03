# main.py

from airbnb_scraper import AirbnbScraper
from url_builder import URLBuilder
import random
import time

def main():

    for localidad in locations:

        # Construir una URL de búsqueda personalizada
        search_url = URLBuilder.build_search_url(
            city=localidad,
            state='Bogotá DC',
            place_id=None,
            checkin=None,
            checkout=None,
            adults=None,
            children=None,
            amenities=None,
            flexible_dates=None
        )
        
        print(f"URL de búsqueda personalizada: {search_url}")

        marg_sites = 6

        while marg_sites > 5:
            

            x = random.randrange(0,60)
            print(x)
            
            # Inicializar el scraper con la Url solicitada
            scraper = AirbnbScraper(base_url=search_url)

            # Ejecutar el scraper
            scraper.run(group_size=6, max_pages=3, output_filename="airbnb_listings.csv")
                        
            marg_sites = scraper.residuales
            print(marg_sites)
            time.sleep(x)




locations = {
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

# if __name__ == "__main__":


#     for i in locations:
        
#         marg_sites = 6

#         while marg_sites > 5:

#             x = random.randrange(0,60)
#             print(x)
            
#             main(i)
#             marg_sites = AirbnbScraper.residuales
#             time.sleep(x)



if __name__ == "__main__":

    main()

    

                
            


