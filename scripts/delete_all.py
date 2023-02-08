import psycopg2

con = psycopg2.connect(
    database="postgres", 
    user="postgres", 
    password="1029", 
    host="127.0.0.1", 
    port="5432"
)

cur=con.cursor()

tables=["cars", "drivers",  "fuel" ,  "transportations", "cars_drivers", "archive" ]
for i in tables[::-1]:
    cur.execute(f'DELETE FROM "{i}" *')
con.commit()
con.close()
print("Deleted ALL fields!\nDone!")
