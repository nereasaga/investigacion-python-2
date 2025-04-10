import sqlite3


con = sqlite3.connect("users.db")
cur = con.cursor()

# Paso 1: Crear nueva tabla con columna ID autoincremental
cur.execute("""
    CREATE TABLE movie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year INTEGER,
        score REAL
    )
""")

# Insertar dos filas
cur.execute("""
    INSERT INTO movie VALUES
        (NULL, 'Monty Python and the Holy Grail', 1975, 8.2),
        (NULL, 'And Now for Something Completely Different', 1971, 7.5)
""")
con.commit()

data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
cur.executemany("INSERT INTO movie (title, year, score) VALUES (?, ?, ?)", data)
con.commit()  # Guardar cambios

# Verificar si los datos fueron insertados
for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):

    print(row)

cur.execute("""
    CREATE TABLE profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bio TEXT,
        movie_id INTEGER,
        avatar_path TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (movie_id) REFERENCES movie(id)
    )
""")

cur.execute(
    "INSERT INTO profile (user_id, bio, movie_id) VALUES (?, ?, ?)",
    (5, "¡Muerde mi brillante trasero metálico!", 1)
)
con.commit()
con.close() # Cerrar conexión

