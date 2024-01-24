import sqlite3

PROFESSIONS: list[str] = ['IT Technician', 'Support specialist', 'Quality assurance tester', 'Web developer',
                          'IT security specialist', 'Systems analyst', 'Network engineer', 'Software engineer',
                          'User experience designer', 'Database administrator', 'Data scientist', 'Computer scientist',
                          'IT director', 'Applications Engineer', 'Cloud system engineer', 'Data quality manager',
                          'Web administrator', 'Back end developer', 'Front end developer', 'Full stack developer',
                          'DevOps engineer', 'Cloud security specialist', 'Project manager', 'Product manager']

if __name__ == "__main__":
    with sqlite3.connect("./datasets/professions_dataset.db") as conn:
        out_curs = conn.cursor()
        out_curs.execute("DROP TABLE IF EXISTS Professions")
        out_curs.execute('''
                CREATE TABLE IF NOT EXISTS Professions (
                    ID INTEGER PRIMARY KEY,
                    Profession TEXT
                )    
            ''')

        id = 0
        for profession in PROFESSIONS:
            print(f"Query #{id}: INSERT INTO Professions VALUES ({id}, \"{profession}\")")
            out_curs.execute(f"INSERT INTO Professions VALUES ({id}, \"{profession}\")")
            id += 1

        conn.commit()
