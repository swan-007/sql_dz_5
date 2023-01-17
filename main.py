import psycopg2


def create_table(cursor, name, structure):
    gry = f"create table if not exists {name}(id SERIAL primary key, {structure});"
    cursor.execute(gry)
    conn.commit()


def new_client(cursor, client_name, client_surname_name, client_email):
    cursor.execute("""
                    INSERT INTO client(name, surname_name, email) 
                    values(%s,  %s, %s);
                    """, (client_name, client_surname_name, client_email))
    conn.commit()
    print('Клиент добавлен')


def new_number(cursor, number, client_email):
    x = f"{client_email}"
    cursor.execute("""
    select name, id, surname_name from client where email ilike %s;
    """, (x,))
    c = cursor.fetchone()
    y = number
    cursor.execute("""
        select number from phone where number ilike %s;
        """, (y,))
    n = cursor.fetchone()
    if n == None:
        if c == None:
            print('Клиента с таким майлом нет ')
        else:
            cursor.execute(""" INSERT INTO phone(number, client_id ) 
            values(%s, %s);""" % (number, c[1])
                           )

            print(f'Номер добавлен к клиенту {c[0]} {c[2]}')

    else:
        print(f'Номер уже существует в базе!')


def change_data(cursor, email, dict_t: dict):
    d = {}
    for key, val in dict_t.items():
        if val.strip():
            d[key] = val
    for key, val in d.items():
        v = (val, email)
        gry = (f"""update client set {key} = %s  where email = %s;
    """)
        cursor.execute(gry, v)
        print("Данные изменены")


def delete_number(cursor, email, number):
    cursor.execute("""
            select name from client c left join phone p on c.id = p.client_id where p.number = %s and c.email = %s;
            """, (number, email))
    x = cursor.fetchone()
    if x == None:
        print(f'Клиенту с почтой {email}, номер {number} не принадлежит')
    else:
        cursor.execute("""
                    DELETE FROM phone WHERE number=%s;
                    """, (number,))
        print("Номер удален")
    conn.commit()


def delete_client(cursor, email):
    cursor.execute("""
                select number from phone p 
                join client c on c.id = p.client_id
                where c.email= %s;
                """, (email, ))
    x = cursor.fetchone()
    if x == None:
        cursor.execute("""
                       DELETE FROM client WHERE email= %s;
                       """, (email,))
        print('Клиент удален')
    else:
        cursor.execute("""
                        DELETE FROM phone WHERE number= %s;
                        """, (x[0],))
        cursor.execute("""
                       DELETE FROM client WHERE email= %s;
                        """, (email,))
        print("Клиент удален")


def search_client(cursor, search: dict):
    d = {}
    for key, val in search.items():
        if val.strip():
            d[key] = val
    for key, val in d.items():
        v = (val,)
        gry = (f"""
        select name, surname_name, email, p.number from client c
        left join phone p on c.id = p.client_id
        where {key} ilike %s;
        """)
        cursor.execute(gry, v)
        print(cursor.fetchall()[0])


if __name__ == "__main__":
    with psycopg2.connect(database='client_db', user='postgres', password='wifi1993+') as conn:
        cur = conn.cursor()
#Функция, создающая структуру БД (таблицы)
        #structure_1 = 'name VARCHAR (50) not null, surname_name VARCHAR (50) not null, email VARCHAR unique not null '
    #     structure_2 = 'number VARCHAR (50), client_id integer not null references client(id)'
        # create_table(cur, 'client', structure_1)
    #     create_table(cur, "test_2", structure_2)
#Функция, позволяющая добавить нового клиента
        #new_client(cur, 'An', 's', '4@gmail.com')

#Функция, позволяющая добавить телефон для существующего клиента
        # new_number(cur, '55890', '123@gmail.com')

#Функция, позволяющая изменить данные о клиенте
        # new_dict = {'name': " lexa", 'surname_name': "maj", 'email': "  "}
        # change_data(cur, 'm@gmail.com', new_dict)

#Функция, позволяющая удалить телефон для существующего клиента
        # delete_number(cur, 'zamd@gmail.com', '1002')

#Функция, позволяющая удалить существующего клиента
        # delete_client(cur, 'Les@gmail.com')

#Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
        # d_1 = {"name": "", 'surname_name': "", 'email': "", 'number': "89434300400"}
        # search_client(cur, d_1)
