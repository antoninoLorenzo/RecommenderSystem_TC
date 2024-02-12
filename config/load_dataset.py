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

    offers = []
    location_offer_jt = []
    required_skills_jt = []
    required_languages_jt = []
    lang_map = {'italiano': 1, 'inglese': 2, 'spagnolo': 3, 'francese': 4}

    with sqlite3.connect('../demo/datasets/skills_dataset.db') as skills_conn:
        skills_curs = skills_conn.cursor()

        skills_curs.execute('SELECT * FROM skills')
        skills = skills_curs.fetchall()



    with sqlite3.connect('../demo/datasets/offers_full.db') as offers_conn:
        offers_curs = offers_conn.cursor()

        offers_curs.execute('SELECT * FROM offers')
        offers_rows = offers_curs.fetchall()



        for offer_id, row in enumerate(offers_rows):
            offer_id += 1

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
                'location': row[OFFER_LOC] if row[OFFER_LOCTYPE] == 'OnSite' else 'NULL'
            })

    with sqlite3.connect('../demo/datasets/developers_dataset.db') as dev_conn:
        dev_curs = dev_conn.cursor()

        dev_curs.execute('SELECT * FROM developers')
        devs_rows = dev_curs.fetchall()

        devs = []
        devs_locations = []
        devs_skills_jt = []
        devs_langs_jt = []

        for i, row in enumerate(devs_rows):
            i += 1

            dev = {
                'id': i,
                'fname': row[DEV_NAME],
                'lname': row[DEV_SURNAME],
                'bio': row[DEV_BIO],
                'email': row[DEV_EMAIL],
                'password': row[DEV_PASS],
                'loc_id': row[DEV_LOC]
            }
            devs.append(dev)

            for skill_id in row[DEV_SKILLS].split(', '):
                devs_skills_jt.append({
                    'skill_id': int(skill_id) + 1,
                    'dev_id': i
                })

            for language in row[DEV_LANG].split(', '):
                devs_langs_jt.append({
                    'language': lang_map[language],
                    'dev_id': i
                })

    script = open('db_populator.sql', 'w')
    script.write('USE turing_careers;\n')

    script.write('INSERT INTO skill VALUES\n')
    for i, row in enumerate(skills):
        script.write(f'''({row[SKILL_ID] + 1}, "{row[SKILL_NAME]}", "{row[SKILL_TYPE]}")''')
        if i != len(skills) - 1:
            script.write(',')
        script.write('\n')
    script.write(';')

    script.write('INSERT INTO developer VALUES\n')
    for i, dev in enumerate(devs):
        script.write(f'''({dev['id']}, "{dev['fname']}", "{dev['lname']}", "{dev['bio']}", "{dev['email']}", "{dev['password']}", "{dev['loc_id']}")''')
        if i != len(devs) - 1:
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
        script.write(f'''({offer['id']}, "{name}", "OPEN", "{desc}", "{offer['type']}", 1, "{offer['location']}")''')
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

    script.write('INSERT INTO developerlanguage VALUES\n')
    for i, tup in enumerate(devs_langs_jt):
        script.write(f'''({tup['dev_id']}, {tup['language']})''')
        if i != len(devs_langs_jt) - 1:
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

    script.write('INSERT INTO developerskill VALUES\n')

    for i, tup in enumerate(devs_skills_jt):
        script.write(f'''({tup['dev_id']}, {tup['skill_id']})''')
        if i != len(devs_skills_jt) - 1:
            script.write(',')
        script.write('\n')
    script.write(';')

    script.close()
