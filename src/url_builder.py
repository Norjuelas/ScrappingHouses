# url_builder.py

from urllib.parse import urlencode, quote_plus

class URLBuilder:
    def __init__(self, base_url):
        self.base_url = base_url
        self.params = {}

    def add_param(self, key, value):
        """Agrega un parámetro a la URL si el valor no está vacío."""
        if value is not None:
            self.params[key] = value

    def add_list_param(self, key, values):
        """Agrega un parámetro de lista a la URL."""
        if values:
            self.params[key] = values.split(',')

    def build(self):
        """Construye la URL completa con los parámetros codificados."""
        query_string = urlencode(self.params, doseq=True, quote_via=quote_plus)
        return f"{self.base_url}?{query_string}"

    @staticmethod
    def build_search_url(**kwargs):
        """Construye una URL de búsqueda de Airbnb con los parámetros proporcionados."""
        base_url = 'https://www.airbnb.com.co/s/homes'
        builder = URLBuilder(base_url)

        # Agregar parámetros de ubicación
        if kwargs.get('city') and kwargs.get('state'):
            location = f"{kwargs['city']}, {kwargs['state']}"
            builder.add_param('query', location)
        if kwargs.get('place_id'):
            builder.add_param('place_id', kwargs['place_id'])

        # Agregar fechas
        if kwargs.get('checkin'):
            builder.add_param('checkin', kwargs['checkin'])
        if kwargs.get('checkout'):
            builder.add_param('checkout', kwargs['checkout'])

        # Agregar huéspedes
        builder.add_param('adults', kwargs.get('adults', 0))
        builder.add_param('children', kwargs.get('children', 0))
        builder.add_param('infants', kwargs.get('infants', 0))
        builder.add_param('pets', kwargs.get('pets', 0))

        # Tipo de búsqueda y fechas flexibles
        builder.add_param('search_type', kwargs.get('search_type', 'AUTOSUGGEST'))
        if kwargs.get('flexible_dates', True):
            builder.add_param('date_picker_type', 'flexible_dates')

        # Agregar listas de parámetros
        builder.add_list_param('amenities[]', kwargs.get('amenities'))
        builder.add_list_param('accessibilities[]', kwargs.get('accessibilities'))
        builder.add_list_param('facilities[]', kwargs.get('facilities'))
        builder.add_list_param('property_type_id[]', kwargs.get('property_types'))
        builder.add_list_param('house_rules[]', kwargs.get('house_rules'))
        builder.add_list_param('neighborhood_ids[]', kwargs.get('neighborhoods'))

        return builder.build()

    @staticmethod
    def build_room_url(room_id, **kwargs):
        """Construye una URL para una habitación específica de Airbnb."""
        base_url = f'https://www.airbnb.com.co/rooms/{room_id}'
        builder = URLBuilder(base_url)

        # Agregar parámetros de huéspedes
        builder.add_param('adults', kwargs.get('adults', 1))
        builder.add_param('children', kwargs.get('children', 0))
        builder.add_param('infants', kwargs.get('infants', 0))
        builder.add_param('pets', kwargs.get('pets', 0))

        # Agregar fechas
        if kwargs.get('check_in'):
            builder.add_param('check_in', kwargs['check_in'])
        if kwargs.get('check_out'):
            builder.add_param('check_out', kwargs['check_out'])

        # Otros parámetros
        builder.add_param('enable_m3_private_room', kwargs.get('enable_m3_private_room', True))
        builder.add_param('search_mode', kwargs.get('search_mode', 'regular_search'))
        builder.add_param('source_impression_id', kwargs.get('source_impression_id'))
        builder.add_param('previous_page_section_name', kwargs.get('previous_page_section_name'))
        builder.add_param('federated_search_id', kwargs.get('federated_search_id'))

        return builder.build()
