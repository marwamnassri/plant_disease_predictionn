import sqlite3

def init_db():
    conn = sqlite3.connect("plant_diseases.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS history (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 plant TEXT,
                 symptoms TEXT,
                 disease TEXT,
                 treatment TEXT
                 )""")
    conn.commit()
    conn.close()

def insert_history(plant, symptoms, disease, treatment):
    conn = sqlite3.connect("plant_diseases.db")
    c = conn.cursor()
    c.execute("INSERT INTO history (plant, symptoms, disease, treatment) VALUES (?, ?, ?, ?)",
              (plant, symptoms, disease, treatment))
    conn.commit()
    conn.close()
