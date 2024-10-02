# main.py

from airbnb_scraper import AirbnbScraper
from url_builder import URLBuilder

def main():
    # Construir una URL de búsqueda personalizada
    search_url = URLBuilder.build_search_url(
        city='Chapinero',
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
    
    # Inicializar el scraper con la Url solicitada
    scraper = AirbnbScraper(base_url=search_url)

    # Ejecutar el scraper
    scraper.run(group_size=3, max_pages=15, output_filename="airbnb_listings.csv")

if __name__ == "__main__":
    main()


