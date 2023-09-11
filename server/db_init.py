import sqlite3

conn = sqlite3.connect('face_recognize.db')

c = conn.cursor()
c.execute("""Drop table if exists PERSON""")
c.execute("""Drop table if exists PERSON_RECORD""")

c.execute("""CREATE TABLE PERSON (
        person_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        picture_path TEXT NOT NULL,
        created_time DATETIME DEFAULT CURRENT_TIMESTAMP
)""")

c.execute("""CREATE TABLE PERSON_RECORD (
        record_id INTEGER PRIMARY KEY,
        person_id INTEGER,
        created_time DATETIME DEFAULT CURRENT_TIMESTAMP
)""")
          
          
# c.execute('INSERT INTO PERSON (person_id, name, picture_path) VALUES (?, ?, ?)', (1,"Zhang Ruolin", "C:/Users/smyrz1/Desktop/project/subpicture/Zhang_Ruolin",))
c.execute('INSERT INTO PERSON (name, picture_path) VALUES (?, ?)', ("Zhang Ruolin", "C:/Users/smyrz1/Desktop/project/subpicture/Zhang_Ruolin",))

c.execute('INSERT INTO PERSON_RECORD (person_id) VALUES (?)', (1,))
c.execute('INSERT INTO PERSON_RECORD (person_id) VALUES (?)', (1,))
c.execute('select * from PERSON')
rows = c.fetchall()
print(rows)

conn.commit()

conn.close()