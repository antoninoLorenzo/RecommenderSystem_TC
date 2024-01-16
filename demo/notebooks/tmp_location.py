import os
import pprint
import json
import re
import sqlite3

import requests


location_list = [
    'Padova,'
    'Veneto',
    '00034 Lazio',
    'Bari, Puglia',
    'Forlì, Emilia-Romagna',
    '20144 Milano',
    '84131 Salerno',
    'Pisa, Toscana',
    'Termoli, Molise',
    'Bologna, Emilia-Romagna',
    '00165 Roma',
    'Bolzano - Bozen, Trentino-Alto Adige',
    '70100 Bari',
    'Macerata, Marche',
    'Roma, Lazio',
    '48018 Faenza',
    'Taranto, Puglia',
    'Milano, Lombardia',
    '10152 Torino',
    'Basovizza, Friuli-Venezia Giulia',
    'Verona, Veneto',
    'Scandicci, Toscana',
    '20149 Milano',
    'Torino, Piemonte',
    'Pescara, Abruzzo',
    '66041 Atessa',
    '47122 Forlì',
    'Provincia di Torino, Piemonte',
    'Borgo Panigale, Emilia-Romagna',
    'Carugate, Lombardia',
    '81030 Falciano del Massico',
    '38123 Trento',
    'Italia',
    '00173 Roma',
    'Agrate Brianza, Lombardia',
    'Modena, Emilia-Romagna',
    '41123 Modena',
    '34170 Gorizia',
    'Provincia di Roma, Lazio',
    '84091 Battipaglia',
    'Nola, Campania',
    '07100 Sassari',
    '20100 Milano',
    'Lecce, Puglia',
    '16100 Genova',
    '10121 Torino',
    'Belluno, Veneto',
    'Vicenza, Veneto',
    'Provincia di Padova, Veneto',
    'Spoleto, Umbria',
    '80146 Napoli',
    '31020 Villorba',
    '37121 Verona',
    'Palermo, Sicilia',
    'Napoli, Campania',
    '00147 Roma',
    '00137 Roma',
    '31020 Chiarano',
    '80142 Napoli',
    'Misano Adriatico, Emilia-Romagna',
    '47814 Bellaria-Igea Marina',
    'Perugia, Umbria',
    '40033 Casalecchio di Reno',
    '25121 Brescia',
    'Provincia di Terni, Umbria',
    'Lucca, Toscana',
    'Pesaro, Marche',
    'Arè, Piemonte',
    '00149 Roma',
    '80121 Napoli',
    '55049 Viareggio',
    'Provincia di Forlì-Cesena, Emilia-Romagna',
    'Provincia di Treviso, Veneto',
    'Rovigo, Veneto',
    'Cuneo, Piemonte',
    'Fossacesia, Abruzzo',
    '44124 Ferrara',
    '10040 Rivalta di Torino',
    'Nardò, Puglia',
    '00185 Roma',
    '59100 Prato',
    'Provincia di Bologna, Emilia-Romagna',
    'Benevento, Campania',
    "Anzola dell'Emilia, Emilia-Romagna",
    '04011 Roma',
    'Biella, Piemonte',
    'Genova, Liguria',
    '06134 Perugia',
    '00144 Roma',
    'Fusaro, Campania',
    'Foggia, Puglia',
    'Solofra, Campania',
    '32100 Belluno',
    '26838 Tavazzano',
    '95131 Catania',
    'Formia, Lazio',
    'Battipaglia, Campania',
    'Avellino, Campania',
    '80143 Napoli',
    'Provincia di Genova, Liguria',
    'Pero, Lombardia',
    'Provincia di Novara, Piemonte',
    '20089 Rozzano',
    'Trieste, Friuli-Venezia Giulia',
    'Massarosa, Toscana',
    'Limena, Veneto',
    'Fabriano, Marche',
    'Cesena, Emilia-Romagna',
    'Ancona, Marche',
    '34133 Trieste',
    '42100 Reggio Emilia',
    '37045 Legnago',
    '70014 Conversano',
    '06128 Perugia',
    '73010 Veglie',
    'Provincia di Latina, Lazio',
    'Matera, Basilicata',
    '20124 Milano',
    '10015 Ivrea',
    '28100 Novara',
    'Pavia, Lombardia',
    '54011 Aulla',
    '40133 Bologna',
    'Treviso, Veneto',
    'Varese, Lombardia',
    '06055 Marsciano',
    '80035 Nola',
    '17027 Pietra Ligure',
    '36015 Schio',
    'Reggio Emilia, Emilia-Romagna',
    '95121 Catania',
    'Spilimbergo, Friuli-Venezia Giulia',
    'Savona, Liguria',
    '00178 Roma',
    '38122 Trento',
    '70056 Molfetta',
    'Piazza, Trentino-Alto Adige',
    'Villanova Mondovì, Piemonte',
    'Ascea, Campania',
    'Cascina, Toscana',
    'Scurzolengo, Piemonte',
    '20054 Segrate',
    '42025 Cavriago',
    'Latina, Lazio',
    'Firenze, Toscana',
    'Salerno, Campania',
    '35010 Vigonza',
    '20145 Milano',
    '35020 Ponte San Nicolò',
    'Rimini, Emilia-Romagna',
    '20121 Milano',
    'Cernusco sul Naviglio, Lombardia',
    '20025 Legnano',
    'Cosenza, Calabria',
    'Cagliari, Sardegna',
    '20871 Vimercate',
    '41015 Nonantola',
    'Ferrara, Emilia-Romagna',
    '20142 Milano',
    'Provincia di Lodi, Lombardia',
    'Bristol BS2',
    'London',
    'Knutsford',
    'Milton Keynes',
    'Nottingham',
    'Ipswich IP4',
    'Winsford CW7',
    'Lincoln',
    'Belfast',
    'Bristol',
    'Reading RG1',
    'Newcastle upon Tyne',
    'Darlington',
    'Edinburgh EH6',
    'Belfast BT1',
    'Great Malvern',
    'Warwick',
    'Worcestershire',
    'Cardiff CF10',
    'Stevenage',
    'Midlothian',
    'Cheltenham',
    'Newcastle upon Tyne NE15',
    'Cambridge',
    'Belfast BT2',
    'Havant',
    'Runcorn WA7',
    'Cambridge CB4',
    'Cambridgeshire',
    'Culham',
    'Manchester M13',
    'Stratford-upon-Avon',
    'Guildford',
    'Stoke-on-Trent ST1',
    'London EC4N',
    'Lichfield',
    'Street',
    'Killearn',
    'Gloucester',
    'Manchester M2',
    'Oundle',
    'North West',
    'Farnborough',
    'Didcot',
    'Edinburgh',
    'Corsham SN13',
    'Douglas',
    'Whiteley PO15',
    'London W4',
    'Southampton',
    'Reading',
    'Newtown',
    'London E14',
    'Manchester',
    'London TW11',
    'Cambridge CB1',
    'Abingdon',
    'Aylesford ME20',
    'Bedwas',
    'England',
    'Watford',
    'London EC3N',
    'Windsor SL4',
    'Basingstoke',
    'Bournemouth BH7',
    'Rugby CV21',
    'Coleshill',
    'High Wycombe',
    'Chester',
    'Melbourn SG8',
    'Dundee',
    'Brighton',
    'Leeds',
    'Batley',
    'London SE1',
    'Leicester LE19',
    'Billingham',
    'Crawley',
    'Wakefield WF1',
    'Birmingham',
    'Chesterfield S41',
    'Greater London',
    'Lowestoft NR33',
    'Glasgow',
    'Norwich',
    'Scotland',
    'Bristol BS16',
    'Ashby-De-La-Zouch LE65',
    'London NW9',
    'Salisbury',
    'Warton',
    'Basildon SS14',
    'Rotherham',
    'Solihull',
    'Wales',
    'West Sussex',
    'West Midlands',
    'London SW7',
    'Sunderland',
    'Leamington Spa CV32',
    'Barnard Castle',
    'Newcastle upon Tyne NE12',
    'Bournemouth BH2',
    'West Yorkshire',
    'Oxford',
    'Cambridge CB21',
    'Oxford OX1',
    'Swindon',
    'Birmingham B37',
    'Coventry',
    'Warwickshire',
    'Durham',
    'Aldershot',
    'Surrey',
    'Woking',
    'Worksop S81',
    'Laindon',
    'Stirling',
    'Kingston upon Thames',
    'Antrim',
    'Hook',
    'Hertford',
    'Jersey',
    'Nuneaton CV10',
    'West London',
    'Hampshire',
    'Stone',
    'Wirral',
    'Peterborough'
]


def autocomplete_location(query: str, key: str) -> tuple:
    """
    :param query: a string representing the location query
    :param key: googlemaps places api key
    :return: the first possible location as a tuple (City, Region, State)
    """
    pass


def extract_locations(lli: list) -> list:
    key = os.environ.get('PLACES_KEY')
    if not key:
        raise RuntimeError("PLACES_KEY Not Available: Please set Environment Variable PLACES_KEY")

    locations = []
    for loc in lli:
        locations.append(autocomplete_location(loc, key))
    return locations


def extraction():
    # -- Extract Locations
    out = extract_locations(location_list)
    locations_data = [
        (1, 'City', 'Region', 'State')
    ]

    # -- Persist Locations
    with sqlite3.connect('../datasets/locations_extracted.db') as conn:
        curs = conn.cursor()

        curs.execute('''
            CREATE TABLE IF NOT EXISTS Locations (
                ID INTEGER PRIMARY KEY,
                City TEXT,
                Region TEXT,
                Country TEXT
            )
        ''')

        curs.executemany('''
            INSERT INTO Locations (ID, City, Region, Country) VALUES (?, ?, ?, ?)
        ''', locations_data)

        conn.commit()
        conn.close()


if __name__ == "__main__":
    # extraction()
    key = os.environ.get('PLACES_KEY')
    if not key:
        raise RuntimeError("PLACES_KEY Not Available: Please set Environment Variable PLACES_KEY")

    link = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?'
    language = 'it'
    test_query = [
        'Bologna, Emilia-Romagna',
        '00165 Roma',
        'London SE1'
    ]

    # -- remove caps

    # -- query

    for query in test_query:
        try:
            out = requests.get(link + 'input=' + query + '&key=' + key)
            results = out.json()
            print(f'Query: {query}; Length: {len(results["predictions"])}')
            pprint.pprint(results["predictions"][1])

            print(results["predictions"][1]["structured_formatting"]["secondary_text"])
        except Exception as err:
            print(err)
