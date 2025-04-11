import sqlite3

# Crear una conexión a la base de datos SQLite
# Si la base de datos no existe, se crea una nueva
con = sqlite3.connect("./SQLite/tutorial.db")

# Crear un cursor
# Un cursor es un objeto que permite ejecutar comandos SQL y recuperar resultados
# de una base de datos SQLite
cur = con.cursor() 

# Crear tabla
cur.execute("CREATE TABLE movie(title, year, score)")

# Verificar si la tabla fue creada
res = cur.execute("SELECT name FROM sqlite_master")

print(res.fetchone())

# Verificar si una tabla no existente existe
res = cur.execute("SELECT name FROM sqlite_master WHERE name='spam'")

print(res.fetchone())

# Insertar dos filas
cur.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
""")
con.commit()

# Verificar si los datos fueron insertados
res = cur.execute("SELECT score FROM movie")

print(res.fetchall())

res = cur.execute("SELECT title FROM movie")

print(res.fetchall())

# Insertar varias filas
data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
con.commit()  # Guardar cambios

# Verificar si los datos fueron insertados
for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):

    print(row)


con.close() # Cerrar conexión

new_con = sqlite3.connect("tutorial.db") # Reabrir conexión

new_cur = new_con.cursor() # Crear nuevo cursor

res = new_cur.execute("SELECT title, year FROM movie ORDER BY score DESC") # Obtener la película con mayor puntuación

title, year = res.fetchone() # Obtener el título y año de la película con mayor puntuación
# Mostrar el resultado
print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')

""" # Eliminar una fila
new_cur.execute("DELETE FROM movie WHERE title = 'Monty Python and the Holy Grail'")
new_con.commit()

# Eliminar todas las filas
new_cur.execute("DELETE FROM movie")
new_con.commit()

# Verificar si los datos fueron eliminados
new_cur.execute("SELECT * FROM movie")
filas = new_cur.fetchall()

if not filas:
    print("Filas eliminadas.")
else:
    print("Aún hay filas en la tabla:", filas)


# Borrar la tabla 'movie'
new_cur.execute("DROP TABLE IF EXISTS movie")
new_con.commit()


# Verificar si la tabla existe
new_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movie'")
resultado = new_cur.fetchone()

if resultado is None:
    print("La tabla 'movie' ha sido borrada.")
else:
    print("La tabla 'movie' todavía existe.")

# Cerrar conexión
new_con.close() """