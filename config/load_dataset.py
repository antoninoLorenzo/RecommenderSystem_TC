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
            if row[OFFER_LOCTYPE] == 'OnSite':
                locations.append({
                    'name': row[OFFER_LOC],
                    'lat': row[OFFER_LAT],
                    'lon': row[OFFER_LON]
                })

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
                'location': 'optional_location_foreign_key'
            })

    # for off in offers:
    #    print(f'Offer:{off["name"]}')
    # print(f'Locations:\n{locations}\n')
    # print(f'OfferSkills JoinTable:\n{required_skills_jt}\n')
    print(f'OfferLanguages JoinTable: \n{required_languages_jt}\n')
