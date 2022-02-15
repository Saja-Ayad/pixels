from flask import Flask, render_template, request, redirect, flash,session
from cs50 import SQL
from flask_session import Session

app = Flask(__name__) 
DB = SQL("sqlite:///database.db")
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get("user_id", None):
        return redirect("/login")
    else:
        brands = DB.execute("SELECT * from brands order by review desc")
        return render_template("blogs.html", brands=brands)


@app.route("/login", methods=['GET','POST'])
def login():
    if session.get("user_id", None):
        return redirect("/")

    if request.method == 'POST':
        email = request.form.get("email", None)
        password = request.form.get("pass", None)

        if not email or not password:
            flash("Please fill all Fields", "danger")
            return redirect("/login")

        row = DB.execute("select * from users1 where email= ?", email)
        if len(row) < 1:
            flash("Users does not exist", "danger")
            return redirect("/login")
        
        if password != row[0]['password']:
            flash("Check Your info", "danger")
            return redirect("/login")

        session['user_id'] = row[0]['id']
        flash("Welcome", "success")
        return redirect("/")

    else:
        return render_template("/login.html")


@app.route("/register" , methods=['GET','POST'])
def register():
    if session.get("user_id", None):
        return redirect("/")

    if request.method == 'POST':
        email = request.form.get("email", None)
        password = request.form.get("pass", None)
        name = request.form.get("name", None)

        if not email or not password or not name:
            flash("Please Fill all Filds", "danger")
            return redirect("/register.html")

        row = DB.execute("select * from users1 where email = ?", email)
        if len(row) > 1:
            flash("User alradey exist LOGIN please", "danger")
            return redirect("/login.html")

        row = DB.execute("insert into users1 (name, email, password) VALUES (?,?,?)", name, email, password)
        session['user_id'] = row
        flash("Welcome", "success")
        return redirect("/")

    else:
        return render_template("/register.html") 


@app.route("/logout")
def logout():
    if not session.get("user_id", None):
        return redirect("/lognin")
    del session['user_id']
    return redirect("/login")

@app.route("/buy_pixel")
def view():
    if not session.get("user_id", None):
        return redirect("/lognin")

@app.route("/review")
def update():
    if not session.get("user_id", None):
        return redirect("/lognin")

@app.route("/delete?id=1")
def delete():
    if not session.get("user_id", None):
        return redirect("/lognin")

    # id = request.args.get('id')
    # SELECT * FROM blogs where id=?",id
    # DELETE FROM blogs where id =
    


@app.route("/new")
def new():
    pass

if __name__ == '__main__':
    app.run(debug=True)