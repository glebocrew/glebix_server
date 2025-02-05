import mariadb
import random
import os

from hashlib import sha256


conn_params= {
    "user" : "root",
    "password" : "glebocrew",
    "host" : "localhost",
    "database" : "glebix"
}

queries = {
    "username": "SELECT username FROM users WHERE username = ?",
    "password": "SELECT password FROM users WHERE username = ?",
    "delete": "DELETE FROM users WHERE username = ?",
    "add": "INSERT INTO users (username, password) VALUES (?, ?)"
}

queries_for_codes = {
    "passcode": "SELECT code FROM codes WHERE username = ?",
    "delete": "DELETE FROM codes WHERE username = ?",
    "add": "INSERT INTO codes (username, code) VALUES (?, ?)"
}

alphabet = "mark gleb kuptsov proga list python fullstack developer top programmer of moscow lychse guitar metal 1999 2021 2025 2023 zaurus zaorus hatfield".split(sep=' ')

class MariaConn:
    def __init__(self):
        pass

    def _create_passcode(self):
        passcode = ""
        for x in range(0, 5):
            passcode += random.choice(alphabet)

        return passcode

    def connect(self, conn_params: map):
        self.connection = mariadb.connect(**conn_params)
        self.cursor = self.connection.cursor()

    def check_password(self, username, password):
        if not self.invalid(username) and not (" " in password):
            self.cursor.execute(queries["password"], tuple([username]))
            pwd = self.cursor.fetchone()

            pwd_hash = sha256()
            pwd_hash.update(password.encode("utf-8"))

            print(pwd)
            print(pwd_hash.hexdigest())

            if pwd_hash.hexdigest() in pwd:
                return True
            else:
                return False
        return False

    def invalid(self, username):
        if " " in username or "'" in username:
            return True
        
        self.cursor.execute(queries["username"], tuple([username]))
        if self.cursor.fetchone() == None:
            return True
        else:
            return False

    def add(self, username, password):
        pwd_hash = sha256()
        pwd_hash.update(password.encode("utf-8"))

        self.cursor.execute(queries['add'], (username, pwd_hash.hexdigest()))
        self.connection.commit()

    def delete(self, username):
        self.cursor.execute(queries['delete'], tuple([username]))
        self.connection.commit()



    def add_code(self, username, passcode):
        self.cursor.execute(queries_for_codes['add'], (username, passcode))
        self.connection.commit()

    def delete_code(self, username):
        self.cursor.execute(queries_for_codes['delete'], tuple([username]))
        self.connection.commit()

    def check_code(self, username, code):
        if not self.invalid(username) and not (" " in code):
            self.cursor.execute(queries_for_codes["passcode"], tuple([username]))
            cd = self.cursor.fetchone()

            print(cd)
            print(code)

            if code in cd:
                return True
            else:
                return False
        return False



    def return_table(self):
        self.cursor.execute("SELECT * FROM users")
        print(self.cursor.fetchall())
    
    
    def return_table_codes(self):
        self.cursor.execute("SELECT * FROM codes")
        print(self.cursor.fetchall())

    def close(self):
        self.cursor.close()
        self.connection.close()


# add("glebocrew", "123")
# return_table()

    
maria = MariaConn()
maria.connect(conn_params)
# maria.return_table()
# maria.delete("glebocrew")

if (input("debug?")).lower() == "y":
    while True:
        
        try:
            commandlet, operator = map(str, input().split(sep=" "))
            if commandlet == "del":
                maria.delete(operator)
            elif commandlet == "add":
                maria.add(operator)
            else:
                print("Дичь!")
        except:
            print(maria.return_table())
            print(maria.return_table_codes())

maria.close()


