from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from dbops import MariaConn


conn_params= {
    "user" : "root",
    "password" : "glebocrew",
    "host" : "localhost",
    "database" : "glebix"
}

app = Flask("__name__",
            static_folder="static")

maria = MariaConn()
maria.connect(conn_params)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        if maria.is_valid(username):
            if password == repeat:
                if password != "" and username != "":
                    for p in password:
                        if p != " ":
                            maria.add(username, password)
                            print("logged!")
                            return redirect("/login")
                    else:
                        return render_template("signin.html", message="only spaces can't be a pwd")
                else:
                    return render_template("signin.html", message="empty pwd field")
            else:
                return render_template("signin.html", message="passwords don't match")
        else:
            return render_template("signin.html", message="this username is already taken")
    return render_template("signin.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")


        if maria.check_password(username, password):
            return render_template("home.html")
        else:
            return render_template("login.html", message="Incorrect data!")
    return render_template("login.html")

if __name__ == "__main__":
    app.run()