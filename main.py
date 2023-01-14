import psycopg2

conn = psycopg2.connect(database='client_db', user='postgres', password='*****')


def create_table(cursor, name, structure):
    cursor.execute(f'create table if not exists {name}( id SERIAL primary key, {structure});')
    conn.commit()


def new_client(cursor, client_name, client_surname_name, client_email):
    cursor.execute(f'INSERT INTO client(name, surname_name, email) '
                   f'values{client_name, client_surname_name, client_email};')
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
            cursor.execute(f'INSERT INTO phone(number, client_id ) values{number, c[1]};')
            conn.commit()
            print(f'Номер добавлен к клиенту {c[0]} {c[2]}')

    else:
        print(f'Номер уже существует в базе!')


def change_data(cursor, name, surname_name, email, new_mail):
    cursor.execute("""
        select id from client where email = %s;
        """, (email,))
    x = cursor.fetchone()
    if x == None:
        print('Клиента с таким майлом нет')
    else:
        cursor.execute('update client set name= %s, surname_name = %s, email = %s where id = %s;'
                      , (name, surname_name, new_mail, x[0]))
        print('Данные изменены ')
    conn.commit()


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


def search_client(cursor, search):
    cursor.execute("""
                select name, surname_name, email, p.number from client c
                left join phone p on c.id = p.client_id
                where name ilike %s or surname_name ilike %s or email ilike %s or p.number ilike %s;
                """, (search, search, search, search))

    y = cursor.fetchall()
    print(y)


cur = conn.cursor()

#Функция, создающая структуру БД (таблицы)
# structure_1 = 'name VARCHAR (50) not null, surname_name VARCHAR (50) not null, email VARCHAR unique not null '
# structure_2 = 'number VARCHAR (50), client_id integer not null references client(id)'
# create_table(cur, 'client', structure_1)
# create_table(cur, 'phone', structure_2)
#Функция, позволяющая добавить нового клиента
# new_client(cur, 'Anzor', 'les', '002584@gmail.com')

#Функция, позволяющая добавить телефон для существующего клиента
# new_number(cur, '2345678', 'olo@gmail.com')

#Функция, позволяющая изменить данные о клиенте
# change_data(cur, 'Lex', 'f', '343434o@gmail.com', '123@gmail.com')

#Функция, позволяющая удалить телефон для существующего клиента
# delete_number(cur, 'zamd@gmail.com', '1002')

#Функция, позволяющая удалить существующего клиента
# delete_client(cur, 'Les@gmail.com')

#Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
# search_client(cur, 'f')

conn.close()
