import mariadb
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


class MariaConn:
    def __init__(self):
        pass

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


    def return_table(self):
        self.cursor.execute("SELECT * FROM users")
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
        commandlet, operator = map(str, input().split(sep=" "))

        if commandlet == "del":
            maria.delete(operator)
        elif commandlet == "ret":
            maria.return_table()
        else:
            print("Дичь!")

maria.close()


