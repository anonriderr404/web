import sqlite3
import bcrypt

db = sqlite3.connect('flask.db', check_same_thread=False)
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY,
        img TEXT UNIQUE,
        title TEXT,
        description TEXT,
        date TEXT,
        place TEXT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS memo(
        id INTEGER PRIMARY KEY,
        img TEXT UNIQUE,
        title TEXT UNIQUE,
        date TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS alert(
        id INTEGER PRIMARY KEY,
        user TEXT UNIQUE,
        title TEXT UNIQUE,
        date TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY,
               username TEXT UNIQUE,
               email TEXT UNIQUE,
               password TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS profile(
               id INTEGER PRIMARY KEY,
               username TEXT UNIQUE,
               image TEXT
)''')



def create_user(username: str, email: str, password: str):
    try:
        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        data = (username, email, hashed_password.decode('utf-8'))
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', data)
        db.commit()
    except Exception as e:
        print(e)
        return False
    return True

def edit_record(table, field, field_value, **fields):
    # Update a record in the specified table based on a field and its value
    keys_in_order, values_in_order, amount = '', '', 0
    for key, value in fields.items():
        keys_in_order = keys_in_order + key + ' = ?, '
        amount += 1
    keys_in_order = keys_in_order[:len(keys_in_order) - 2]

    for key, value in fields.items():
        values_in_order = values_in_order + ',' + value
    values_in_order = values_in_order.removeprefix(',')

    data = values_in_order.split(',')
    data.append(field_value)
    data = tuple(data)

    try:
        cursor.execute(f"UPDATE {table} SET {keys_in_order} WHERE {field} = ?", data)
        db.commit()
        return True
    except:
        pass
    return False




def authenticate(username, password):
    # Authenticate a user by checking the username and password against stored data
    user = get_record('users', 'username', username)
    if user:
        hashed_password = user[3].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return False


def add_to_memo(path,title,date):
        try:
            data = (path,title,date)
            cursor.execute('INSERT INTO memo (img,title,date) VALUES (?,?,?)',data)
            db.commit()
            return True
        except sqlite3.IntegrityError:
            db.commit()
            return 'exists'
        except Exception as e:
            print(e)
            db.commit()
            return False

def get_record(table, field, value):
    # Retrieve a specific record from the specified table based on a field and its value
    cursor.execute(f'SELECT * FROM {table} WHERE {field} = ?', (value,))
    record = cursor.fetchone()
    if record is not None:
        return record
    else:
        return None

def delete_record(table, field, value):
    try:
        # Delete a record from the specified table based on a field and its value
        cursor.execute(f'DELETE FROM {table} WHERE {field} = ?', (value,))
        db.commit()
        record = get_record(table, field, value)
        if record is None:
            return True
    except:
        pass
    return False


def add_to_memories(path,title,description,date,place=None):
        try:
            if place is not None:
                data = (path,title,description,date,place)
                cursor.execute('INSERT INTO memories (img,title,description,date,place) VALUES (?,?,?,?,?)',data)
            else:
                data = (path,title,description,date)
                cursor.execute('INSERT INTO memories (img,title,description,date) VALUES (?,?,?,?)',data)
            db.commit()
            return True
        except sqlite3.IntegrityError:
            db.commit()
            return 'exists'
        except Exception as e:
            print(e)
            db.commit()
            return False

def retrieve_data(table_name):
    try:
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
    except:
        print(f'No such a table named {table_name} in db')
        return None
    return data

def get_from_pk(primary_key):
    cursor.execute('SELECT * FROM memories WHERE id = ?', (primary_key,))
    return cursor.fetchone()

def get_memo_from_pk(primary_key):
    cursor.execute('SELECT * FROM memo WHERE id = ?', (primary_key,))
    return cursor.fetchone()


def filterFromQuery(query):
    try:
        cursor.execute("SELECT * FROM memories WHERE title LIKE ? OR description LIKE ? OR place LIKE ?", ('%'+query+'%', '%'+query+'%','%'+query+'%'))
        data = cursor.fetchall()
        db.commit()
        return data
    except:
        data = []
        return data

def filterFromMemoQuery(query):
    try:
        cursor.execute("SELECT * FROM memo WHERE title LIKE ? OR date LIKE ?", ('%'+query+'%', '%'+query+'%'))
        data = cursor.fetchall()
        db.commit()
        return data
    except:
        data = []
        return data

def add_record(table, **fields):
    # Constructing the INSERT query to add a new record
    keys_in_order, values_in_order, amount = '', '', 0
    for key, value in fields.items():
        keys_in_order = keys_in_order + ',' + key
        amount += 1
    keys_in_order = keys_in_order.removeprefix(',')

    for key, value in fields.items():
        values_in_order = values_in_order + ',' + value
    values_in_order = values_in_order.removeprefix(',')
    try:
        # Attempt to insert data into the specified table
        data = tuple(values_in_order.split(','))
        cursor.execute(f'INSERT INTO {table} ({keys_in_order}) VALUES ({str("?," * amount).removesuffix(",")})', data)
        db.commit()
    except:
        return False
    return True

db.commit()