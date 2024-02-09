import sqlite3

OFFER_NAME = SKILL_ID = DEV_NAME = 0
OFFER_DESC = SKILL_NAME = DEV_SURNAME = 1
OFFER_LOC = SKILL_TYPE = DEV_LOC = 2
OFFER_SKILLS = DEV_SKILLS = 3
OFFER_LOCTYPE = DEV_BIO = 4
OFFER_LANG = DEV_EMAIL = 5
OFFER_LAT = DEV_PASS = 6
OFFER_LON = DEV_LANG = 7
DEV_LAT = 8
DEV_LON = 9

if __name__ == "__main__":
    script = open('db_populator.sql', 'w')
    script.write('USE turing_careers;\n')

    with sqlite3.connect('../demo/datasets/skills_dataset.db') as skills_conn:
        skills_curs = skills_conn.cursor()

        skills_curs.execute('SELECT * FROM skills')
        rows = skills_curs.fetchall()

        script.write('INSERT INTO skill VALUES\n')
        for i, row in enumerate(rows):
            script.write(f'''({row[SKILL_ID] + 1}, "{row[SKILL_NAME]}", "{row[SKILL_TYPE]}")''')
            if i != len(rows) - 1:
                script.write(',')
            script.write('\n')
        script.write(';')


    with sqlite3.connect('../demo/datasets/offers_full.db') as offers_conn:
        offers_curs = offers_conn.cursor()

        offers_curs.execute('SELECT * FROM offers')
        rows = offers_curs.fetchall()

        offers = []
        locations = []
        location_offer_jt = []
        required_skills_jt = []
        required_languages_jt = []
        lang_map = {'italiano' : 1, 'inglese' : 2, 'spagnolo' : 3, 'francese' : 4}

        for offer_id, row in enumerate(rows):
            offer_id += 1
            loc = {
                'offer_id': offer_id,
                'name': row[OFFER_LOC],
                'lat': row[OFFER_LAT],
                'lon': row[OFFER_LON],
                'type': row[OFFER_LOCTYPE],
                'tbd' : False
            }
            locations.append(loc)

            for skill_id in row[OFFER_SKILLS].split(', '):
                required_skills_jt.append({
                    'skill_id': int(skill_id) + 1,
                    'offer_id': offer_id
                })

            for language in row[OFFER_LANG].split(', '):
                required_languages_jt.append({
                    'language': lang_map[language],
                    'offer_id': offer_id
                })

            offers.append({
                'id': offer_id,
                'name': row[OFFER_NAME],
                'description': row[OFFER_DESC],
                'type': row[OFFER_LOCTYPE],
                'location': offer_id if row[OFFER_LOCTYPE] == 'OnSite' else 'NULL'
            })


    to_delete = set()
    for i, location in enumerate(locations):
        i += 1
        if location['type'] == 'OnSite' and not location['tbd']:
            for j in range(i + 1, len(locations)):
                other = locations[j - 1]
                if (not other['tbd']) and (other['type'] == 'OnSite') and (location['lat'] == other['lat']) and (location['lon'] == other['lon']):
                    #print(f'Location {location["lat"], location["lon"]} == {locations[j]["lat"], locations[j]["lon"]}')

                    offers[other['offer_id'] - 1]['location'] = location['offer_id']
                    other['tbd'] = True
                    to_delete.add(other['offer_id'])
        else:
            to_delete.add(location['offer_id'])




    for id in to_delete:
        locations.remove([l for l in locations if l['offer_id'] == id][0])


    for offer in offers:
        found = False
        for location in locations:
            if offer['location'] == location['offer_id']:
                #print(f'offer {offer["id"]} -> location {offer["location"]}')
                found = True
                break
        if not found and offer['type'] == 'OnSite':
            print(f'offer {offer["id"]} is on site but does not have a valid location ({offer["location"]})')


    script.write('INSERT INTO location VALUES\n')
    for i, location in enumerate(locations):
        if location['type'] == 'OnSite':
            script.write(f'''({location['offer_id']}, "{location['name']}", {location['lat']}, {location['lon']})''')
            if i != len(locations) - 1:
                script.write(',')
            script.write('\n')
    script.write(';')

    script.write('INSERT INTO employer VALUES (1, "John", "Doe", "john.doe@tc.com", "password", "Turing Careers");\n')

    script.write('INSERT INTO offer VALUES\n')
    for i, offer in enumerate(offers):
        desc = offer['description'].encode(errors='ignore')
        desc = str(desc).replace('\"', '\\"')
        name = offer['name'].encode(errors='ignore')
        name = str(name).replace('\"', '\\"')
        script.write(f'''({offer['id']}, "{name}", "OPEN", "{desc}", "{offer['type']}", 1, {offer['location']})''')
        if i != len(offers) - 1:
            script.write(',')
        script.write('\n')
    script.write(';')

    script.write('''INSERT INTO language VALUES
    (1, "it_IT"),
    (2, "en_UK"),
    (3, "es_ES"),
    (4, "fr_FR");\n''')

    script.write('INSERT INTO offerlanguage VALUES\n')

    for i, tup in enumerate(required_languages_jt):
        script.write(f'''({tup['offer_id']}, {tup['language']})''')
        if i != len(required_languages_jt) - 1:
            script.write(',')
        script.write('\n')
    script.write(';')

    script.write('INSERT INTO offerskill VALUES\n')

    for i, tup in enumerate(required_skills_jt):
        script.write(f'''({tup['offer_id']}, {tup['skill_id']})''')
        if i != len(required_skills_jt) - 1:
            script.write(',')
        script.write('\n')
    script.write(';')

    with sqlite3.connect('../demo/datasets/developers_dataset.db') as dev_conn:
        dev_curs = dev_conn.cursor()

        dev_curs.execute('SELECT * FROM developers')
        rows = dev_curs.fetchall()


