import os
import re
import requests

AUTOCOMPLETE_API_LINK = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?'
DETAILS_API_LINK = 'https://maps.googleapis.com/maps/api/place/details/json?'


def extract_locations(locations_list: list) -> dict:
    """
    Run extraction of full addresses for each location
    :param locations_list:
    :return: a dict Location: Address
    """
    key = os.environ.get('PLACES_KEY')
    if not key:
        with open('../../.keys.txt', 'r') as fp:
            content = fp.read()
            key = re.match(r'PLACES_KEY=(\S+)', content).group(1)
            if not key:
                raise RuntimeError("PLACES_KEY Not Available: Please set Environment Variable PLACES_KEY")

    extracted_addresses = {}
    for query in locations_list:
        try:
            # Get Place ID
            autocomplete_response = requests.get(AUTOCOMPLETE_API_LINK + 'input=' + query + '&key=' + key)
            autocomplete_parsed = autocomplete_response.json()
            place_id = autocomplete_parsed["predictions"][1]["place_id"]

            # Get Address Components
            details_request = requests.get(DETAILS_API_LINK + 'place_id=' + place_id + '&key=' + key)
            details_parsed = details_request.json()
            address_components = details_parsed["result"]["address_components"]

            extracted_components = []
            for element in address_components:
                if 'route' not in element['types'] and 'postal_code' not in element['types']:
                    if 'Metropolitan City of ' in element['long_name']:
                        new = element['long_name'][21:]
                    else:
                        new = element['long_name']

                    if len(extracted_components) > 0:
                        for n in extracted_components:

                            if new not in n and n not in new:
                                extracted_components.append(new)
                    else:
                        extracted_components.append(new)

            extracted_addresses[query] = ', '.join(extracted_components[:len(extracted_components)-1])
        except Exception as err:
            print(err)

    return extracted_addresses

