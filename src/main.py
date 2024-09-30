# main.py

#from driver_builder import driver_builder
from airbnb_scraper import AirbnbScraper
from url_builder import URLBuilder

def main():
    # Construir una URL de búsqueda personalizada
    search_url = URLBuilder.build_search_url(
        city='Chapinero',
        state='Bogotá DC',
        place_id='ChIJgwW_iJ6QP44Rc7wFsOAC5M4',
        checkin='2024-10-10',
        checkout='2024-10-15',
        adults=2,
        children=1,
        amenities='wifi,kitchen',
        flexible_dates=True
    )
    print(f"URL de búsqueda personalizada: {search_url}")
    
    # Inicializar el scraper con la Url solicitada
    scraper = AirbnbScraper(base_url=search_url)

    # Ejecutar el scraper
    scraper.run(group_size=3, max_pages=15, output_filename="airbnb_listings.csv")

if __name__ == "__main__":
    main()
