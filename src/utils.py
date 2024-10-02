import urllib.parse
url="rooms/1238435975213252968?adults=1&children=0&enable_m3_private_room=true&infants=0&pets=0&search_mode=regular_search&check_in=2024-10-16&check_out=2024-10-21&source_impression_id=p3_1727716584_P3FjtxhgXvBysSRi&previous_page_section_name=1000&federated_search_id=14f9fd82-791f-439a-a28e-8c465913810a"

path = urllib.parse.urlparse(url).path
print(path.split('/')[-1])


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
