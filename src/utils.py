import urllib.parse
url="rooms/1238435975213252968?adults=1&children=0&enable_m3_private_room=true&infants=0&pets=0&search_mode=regular_search&check_in=2024-10-16&check_out=2024-10-21&source_impression_id=p3_1727716584_P3FjtxhgXvBysSRi&previous_page_section_name=1000&federated_search_id=14f9fd82-791f-439a-a28e-8c465913810a"

path = urllib.parse.urlparse(url).path
print(path.split('/')[-1])


