import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS Phone;
        DROP TABLE IF EXISTS Client;
        """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Client(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL UNIQUE
                );
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Phone(
                number_id SERIAL NOT NULL,
                number DECIMAL UNIQUE CHECK(number <= 99999999999),
                client_id INTEGER REFERENCES Client(client_id 
                ));
                """)
        conn.commit()


def add_client(conn, name, last_name, email):
    conn.execute("""
        INSERT INTO Client(name, last_name, email)
        VALUES(%s, %s, %s)
        RETURNING client_id, name, last_name, email;
        """, (name, last_name, email))
    print(cur.fetchone())


def add_phone(conn, client_id, number):
    conn.execute("""
        INSERT INTO Phone(client_id, number)
        VALUES(%s, %s)
        RETURNING client_id, number;
        """, (client_id, number))
    print(cur.fetchall())


def change_client(conn, client_id, name=None, last_name=None, email=None):
    conn.execute("""
        UPDATE Client
        SET name=%s, last_name=%s, email=%s
        WHERE client_id=%s
        RETURNING client_id, name, last_name, email;
        """, (name, last_name, email, client_id))


def delete_phone(conn, client_id):
    conn.execute("""
        DELETE FROM Phone
        WHERE client_id=%s;
        """, (client_id))


def delete_client(conn, client_id):
    conn.execute("""
            DELETE FROM Phone
            WHERE client_id=%s;
            """, (client_id))

    conn.execute("""
        DELETE FROM Client
        WHERE client_id=%s;
        """, (client_id))


def find_client(conn, name=None, last_name=None, email=None, number=None):
    conn.execute("""
        SELECT c.name, c.last_name, c.email, p.number FROM Client AS c
        LEFT JOIN Phone AS p ON c.client_id = p.client_id
        WHERE c.name=%s OR c.last_name=%s OR c.email=%s OR p.number=%s;
        """, (name, last_name, email, number,))
    return cur.fetchall()


with psycopg2.connect(database="testol", user="postgres", password="Onagron_64") as conn:
    with conn.cursor() as cur:
        create_db(conn)
        add_client(cur, 'Oleg', 'Nagornyy', 'olehanter@gmail.com')
        add_client(cur, 'Olga', 'Antonova', 'antonova.o@mail.ru')
        conn.commit()
        add_phone(cur, '1', '79035055200')
        add_phone(cur, '1', '79067125722')
        add_phone(cur, '2', '+79108101010')
        conn.commit()
        change_client(cur, '1', 'Olga', 'Tamarova', 'tamarova.o@mail.ru')
        conn.commit()
        delete_phone(cur, '1')
        conn.commit()
        delete_client(cur, '1')
        conn.commit()
        print(find_client(cur, '', 'Antonova'))
conn.close()
