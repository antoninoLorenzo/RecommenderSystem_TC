"""
Checklist:
- [DONE] firstName
- [DONE] lastName
- [DONE] email
- [] biography
- [] professions
- [WIP] skills TODO: improve skills and offer dataset
- [] languages
- [] location
"""

import sqlite3
import random

from faker import Faker
from faker.providers import BaseProvider
from utils import create_table, insert_data

# --- Setup resources

DATASET_SIZE = 100
LANGUAGES = {'Italian': 'it_IT', 'English': 'en_US'}
EMAIL_SUFFIX = ['@gmail.com', '@outlook.com', '@gmail.com', '@yahoo.com']
REMOVAL_NAME = ['Sig.', 'Sig.ra', 'Dott.', 'Mr.', 'MD']
SKILLS = set()
with sqlite3.connect('./datasets/skills_short.db') as skills_conn:
    skills_curs = skills_conn.cursor()
    skills_curs.execute('SELECT Skill FROM skills')
    rows = skills_curs.fetchall()
    for skill in rows:
        SKILLS.add(skill[0])

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
        for _ in range(1, random.randint(1, 5)):
            n = random.randint(0, len(SKILLS) - 1)
            random_skill = list(SKILLS)[n]

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

            generated_skills.add(random_skill)
        return generated_skills


FAKE: Faker = Faker([LANGUAGES['Italian'], LANGUAGES['English']])
FAKE_SKILLS: Faker = Faker()
FAKE_SKILLS.add_provider(SkillProvider)


# --- Generation Utils

def generate_names() -> tuple:
    """
    :return: (NAME, SURNAME)
    """
    for _ in range(0, DATASET_SIZE):
        raw_name = FAKE.name().split()
        out_name = []

        for n in raw_name:
            if n not in REMOVAL_NAME:
                out_name.append(n)

        yield out_name[0], out_name[1]


def generate_password() -> str:
    """
    TODO: add password
    :return:
    """


def generate_basic_info() -> dict:
    """
    TODO: add password
    :return: {'name': NAME, 'surname': SURNAME, 'email': EMAIL, 'password': PASSWORD}
    """
    for name, surname in generate_names():
        mail = []
        email_provider = EMAIL_SUFFIX[random.randint(0, len(EMAIL_SUFFIX) - 1)]
        num = None
        lower_name = False
        lower_surname = False

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

        # Generate Password
        yield {'name': name, 'surname': surname, 'email': "".join(mail)}


if __name__ == "__main__":
    for dev in generate_basic_info():
        fake_skills = FAKE_SKILLS.developer_skills()
        print(f'Name: {dev["name"]} {dev["surname"]}\nEmail: {dev["email"]}\nSkills: {fake_skills}\n')
