import sqlite3

OFFER_NAME = 0
OFFER_DESC = 1
OFFER_LOC = 2
OFFER_SKILLS = 3
OFFER_LOCTYPE = 4
OFFER_LANG = 5
OFFER_LAT = 6
OFFER_LON = 7

if __name__ == "__main__":
    with sqlite3.connect('../demo/datasets/offers_full.db') as offers_conn:
        offers_curs = offers_conn.cursor()

        offers_curs.execute('SELECT * FROM offers')
        rows = offers_curs.fetchall()

        offers = []
        locations = []
        location_offer_jt = []
        required_skills_jt = []
        required_languages_jt = []

        for offer_id, row in enumerate(rows):

            loc = {
                'offer_id': offer_id,
                'name': row[OFFER_LOC],
                'lat': row[OFFER_LAT],
                'lon': row[OFFER_LON],
                'type': row[OFFER_LOCTYPE]
            }
            locations.append(loc)

            for skill_id in row[OFFER_SKILLS].split(', '):
                required_skills_jt.append({
                    'skill_id': skill_id,
                    'offer_id': offer_id
                })

            for language in row[OFFER_LANG].split(', '):
                required_languages_jt.append({
                    'language': language,
                    'offer_id': offer_id
                })

            offers.append({
                'id': offer_id,
                'name': row[OFFER_NAME],
                'description': row[OFFER_DESC],
                'type': row[OFFER_LOCTYPE],
                'location': offer_id if row[OFFER_LOCTYPE] == 'OnSite' else None
            })


    to_delete = set()
    for i, location in enumerate(locations):
        if location['type'] == 'OnSite':
            for j in range(i + 1, len(locations)):
                if (locations[j]['type'] == 'OnSite') and (location['lat'] == locations[j]['lat']) and (location['lon'] == locations[j]['lon']):
                    print(f'Location {location["lat"], location["lon"]} == {locations[j]["lat"], locations[j]["lon"]}')

                    offers[locations[j]['offer_id']]['location'] = location['offer_id']
                    to_delete.add(locations[j]['offer_id'])
        else:
            to_delete.add(location['offer_id'])

    print(to_delete)

    for id in to_delete:
        locations.remove([l for l in locations if l['offer_id'] == id][0])

    print(f'dopo rimozione {len(locations)}')


    # for off in offers:
    #    print(f'Offer:{off["name"]}')
    # print(f'Locations:\n{locations}\n')
    # print(f'OfferSkills JoinTable:\n{required_skills_jt}\n')
    #print(f'OfferLanguages JoinTable: \n{required_languages_jt}\n')
