from flask import Flask, render_template, request, jsonify, session, url_for, redirect, g
import os
import mysql.connector
import random
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)

host = "parsahome.mysql.pythonanywhere-services.com" # parsahome.mysql.pythonanywhere-services.com
database = "parsahome$smarthome" # parsahome$smarthome
user = "parsahome"# parsahome
password = "mysqlroot"# mysqlroot
con = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password)

if con.is_connected():
    print("ok")
else:
    print("Not ok")
    con.close()
cur = con.cursor()

@app.route('/')
def index():
    return "ok"

@app.route("/singup")
def singup():
    return render_template("Register.html")

@app.route("/sigin")
def singin():
    return render_template("login.html")

def create_id():
    num = random.randint(1, 10)
    id_text = ''.join(random.choice(string.digits) for _ in range(num))
    return id_text
           
def check_register(data):
    r = []
    payload = {}
    first_name = data.get('firstName')
    phone_number = data.get('phoneNumber')
    email = data.get('email')
    password = data.get('password')
    notif = data.get('notif')
    telegram = data.get('telegram')
    if first_name:
        if phone_number:
            if phone_number.startswith("09"):
                if len(phone_number) == 11:
                    if email:
                        if "-" in email:
                            return jsonify({'error': 'please correct email'})
                        else :
                            if "/" in email:
                                return jsonify({'error': 'please correct email'})
                            else :
                                if "@gmail.com" in email:
                                    pass
                                else :
                                    return jsonify({'error': 'please correct email'})
                                if password:
                                    if notif == "true":
                                        payload["notification"] = 1
                                    else :
                                        if notif == "false":
                                            payload["notification"] = 0
                                        else :
                                            if notif == None:
                                                payload["notification"] = 0
                                        if telegram == "true":
                                            payload["telegram"] = 1
                                        else:
                                            if telegram == "false":
                                                payload["telegram"] = 0
                                            else :
                                                if telegram == None:
                                                    payload['telegram'] = 0
                                            cur.execute("SELECT email FROM users")
                                            a = cur.fetchall()
                                            cur.execute("SELECT phone FROM users")
                                            s = cur.fetchall()
                                            if a:
                                                for i in a:
                                                    if email in i:
                                                        r.append(2)
                                                        return jsonify({'error': 'email is ready'})
                                                    else :
                                                        r.append(1)
                                            if s:
                                                for n in s:
                                                    if phone_number in n:
                                                        r.append(2)
                                                        return jsonify({'error': 'phone is ready'})
                                                    else:
                                                        r.append(1)      
                                            if r:
                                                if 2 in r:
                                                    return jsonify({'error': 'email or phone is ready'})
                                                else:
                                                    token = create_id()
                                                    param = (first_name, email, phone_number, password, token, payload['telegram'], payload['notification'])
                                                    cur.execute("INSERT INTO users(name, email, phone, password, token, telegram, notif) VALUES (%s,%s,%s,%s,%s,%s,%s)", param)
                                                    con.commit()
                                                    params = (token, 0,0,0,0,0,0,0,0,0,0)
                                                    cur.execute("INSERT INTO sensor(token, statuspir, alarmpir, datapir, statussensor, alarmsensor, datasensor, statustemp, limittemp, datatemp, statuslamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", params)
                                                    con.commit()
                                                    r.clear()
                                else:
                                    return jsonify({'error': 'please input password'})
                    else :
                        return jsonify({'error': 'please input email'})
                else :
                    return jsonify({'error': 'please correct phone'})
            else :
                return jsonify({'error': 'phone must be start with 09'})
        else :
            return jsonify({'error': 'please type phone'})
    else:
        return jsonify({'error': 'please type name'})

def check_info(data):
    phone_number = data.get('phoneNumber')
    email = data.get('email')
    password = data.get('password')
    cur.execute(f"SELECT email, password FROM users WHERE phone = {phone_number}")
    a = cur.fetchone()
    if email and password in a:
        pass
    else :
        return jsonify({'error': 'password or email or phone not correct'})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    session.pop("email", None)
    session.pop("number", None)
    phone_number = data.get('phoneNumber')
    email = data.get('email')
    password = data.get('password')
    result = check_info(data)
    if result:
        return result, 400
    else :
        session["phoneNumber"] = data.get('phoneNumber')
        session["email"] = data.get('email')
        response = {"status" : "Register Successful"}
        return response, 200
    
@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    return 200
@app.route('/register', methods=['POST'])
def register():
    session.pop("email", None)
    session.pop("number", None)
    data = request.get_json()
    first_name = data.get('firstName')
    phone_number = data.get('phoneNumber')
    email = data.get('email')
    password = data.get('password')
    remember = data.get('notif')
    receive_updates = data.get('telegram')
    result = check_register(data)
    if result :
        return result, 400
    else :
        session["phoneNumber"] = data.get('phoneNumber')
        session["email"] = data.get('email')
        response = {"status" : "Register Successful"}
        return response, 200

@app.before_request
def before():
    g.user = None
    g.phone = None
    print(session)
    if "email" in session:
        g.user = session["email"]
    if "phoneNumber" in session:
        g.phone = session["phoneNumber"]

@app.route('/account', methods=["GET", "POST"])
def account():
    if g.user:
        return render_template("index.html")
        return session["phoneNumber"]
    
    else:
        return redirect(url_for("singup"))
    # email = session.get('email')
    # phoneNumber = session.get('phoneNumber')
    # print(email, phoneNumber)
    # if email and phoneNumber:
    #     return render_template("file:///C:/Users/Lenovo_irG/PycharmProjects/Smart-Home/Site/Front-end/Register/templates/account.html")
    # else :
    #     return "no data"

if __name__ == '__main__':
    app.run(port=5000,debug=True)




