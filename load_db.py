import csv
import psycopg2


conn = psycopg2.connect("host=localhost dbname=med user=postgres password=1386waxedoff")
cur = conn.cursor()

def pop_table(query):
    with open('csv/med.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            print(row)
            cur.execute(query, row)
            conn.commit()
    return


q = """INSERT INTO med_mj (strain, species, rate, effect, flavor) VALUES (%s, %s, %s, %s, %s)"""
pop_table(q)

q = """INSERT INTO effect (effect) VALUES (%s)"""
pop_table(q)

q = """INSERT INTO flavor (flavor_id, flavor) VALUES (%s, %s)"""
pop_table(q)

q = """INSERT INTO species (species_id, species) VALUES (%s, %s)"""
pop_table(q)

q = """INSERT INTO strain (strain_id, strain, species_id, rate) VALUES (%s, %s, %s, %s)"""
pop_table(q)



cur.close()
conn.close()