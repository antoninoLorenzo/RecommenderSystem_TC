"""
Checklist:
- [DONE] firstName
- [DONE] lastName
- [DONE] email
- [DONE] password
- [] biography
- [] professions TODO
- [WIP] skills TODO: improve skills and offer dataset
- [DONE] languages TODO
- [] location TODO
"""

import sqlite3
import random
import re
import exrex

from faker import Faker
from faker.providers import BaseProvider
from utils import create_table, insert_data

# --- Setup resources

DATASET_SIZE = 5000
LANGUAGES = {'Italian': 'it_IT', 'English': 'en_US'}
EMAIL_SUFFIX = ['@gmail.com', '@outlook.com', '@gmail.com', '@yahoo.com']
REMOVAL_NAME = ['Sig.', 'Sig.ra', 'Dott.', 'Mr.', 'MD']

SKILLS_TMP = set()
with sqlite3.connect('./datasets/skills_dataset.db') as skills_conn:
    skills_curs = skills_conn.cursor()
    skills_curs.execute('SELECT SKILL FROM skills')
    rows = skills_curs.fetchall()
    for skill in rows:
        SKILLS_TMP.add(skill[0])
SKILLS = list(SKILLS_TMP)

SKILL_SETS = []
with sqlite3.connect('./datasets/skill_sets.db') as sk_sets_conn:
    sk_sets_curs = sk_sets_conn.cursor()
    sk_sets_curs.execute('SELECT * FROM SkillSets')
    rows = sk_sets_curs.fetchall()
    for sk_set in rows:
        SKILL_SETS.append(sk_set[1].split(', '))


# --- Setup Faker

class SkillProvider(BaseProvider):
    """
    There is where skill "random" generation happens.
    It is based on the relationships found in ./skill_relationships.ipynb
    """

    def developer_skills(self) -> set:
        """
        :return: a set of skills
        """
        generated_skills = set()
        for _ in range(1, random.randint(2, 5)):
            n = random.randint(0, len(SKILLS) - 1)
            random_skill = SKILLS[n]

            # get skill sets containing skill
            skills_subsets = []
            for i, sset in enumerate(SKILL_SETS):
                if random_skill.lower() in sset:
                    skills_subsets.append(i)

            # randomly add related skills (orribile)
            if skills_subsets:
                for j in skills_subsets:
                    if random.randint(0, 1) == 1:
                        # print(f'The Set {SKILL_SETS[j]} was chosen')
                        for chosen_one in SKILL_SETS[j]:
                            # print(f'Chosen Skill: {chosen_one}')
                            for corresponding in SKILLS:
                                if chosen_one == corresponding.lower():
                                    generated_skills.add(corresponding)
                                    break
                        break

            generated_skills.add(random_skill)
        return generated_skills


FAKE: Faker = Faker([LANGUAGES['Italian'], LANGUAGES['English']])
FAKE_SKILLS: Faker = Faker()
FAKE_SKILLS.add_provider(SkillProvider)


# --- Generation Utils

def generate_names(): # -> tuple
    """
    :return: (NAME, SURNAME)
    """

    locales = list(LANGUAGES.values())
    
    for _ in range(0, DATASET_SIZE):
        locale = locales[random.randint(0, len(locales) - 1)]
        raw_name = FAKE[locale].name().split()
        out_name = []
        
        for word in raw_name:
            if word not in REMOVAL_NAME:
                out_name.append(word)
        
        yield out_name[0], out_name[-1], locale
        


def generate_password(): # -> str:
    """
    TODO: add password
    :return:
    regex r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    """
    pass


def generate_basic_info(): # -> dict:
    """
    TODO: add password
    :return: {'name': NAME, 'surname': SURNAME, 'email': EMAIL, 'password': PASSWORD}
    """
    
    languages = [(k, v) for k, v in LANGUAGES.items()]
    for name, surname, locale in generate_names():
        mail = []
        email_provider = EMAIL_SUFFIX[random.randint(0, len(EMAIL_SUFFIX) - 1)]
        num = None
        lower_name = False
        lower_surname = False
        spoken_languages = []

        if random.randint(0, 1) == 1:
            num = random.randint(1900, 2024)

        if random.randint(0, 1) == 1:
            lower_name = True

        if random.randint(0, 1) == 1:
            lower_surname = True

        if lower_name:
            mail.append(name.lower())
        else:
            mail.append(name)

        if lower_surname:
            mail.append(surname.lower())
        else:
            mail.append(surname)

        if num:
            mail.append(str(num))

        mail.append(email_provider)

        password = name + surname + "123_" #goofy ahh 
        
        if random.randint(0, len(languages)) == 0:
            spoken_languages = [k for k, _ in languages]
        else:
            spoken_languages = [k for k, v in languages if v == locale]
        
        yield {'name': name, 'surname': surname, 'email': "".join(mail), "password": password, "locale" : locale, "spoken_languages": spoken_languages}


if __name__ == "__main__":

    for dev in generate_basic_info():
        fake_skills = FAKE_SKILLS.developer_skills()
        print(f'''
        Name: {dev["name"]} {dev["surname"]}
        Email: {dev["email"]}
        Password: {dev["password"]}
        Skills: {fake_skills}
        Locale: {dev["locale"]}
        Spoken Languages {dev["spoken_languages"]}
        ''')
