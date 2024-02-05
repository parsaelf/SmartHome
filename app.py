from flask import Flask, render_template, request, jsonify, session, url_for, redirect, g
import os
import mysql.connector
import random
import string
from datetime import datetime
from datetime import datetime, timedelta
import pytz

current_datetime = datetime.now()
hour = current_datetime.hour
minute = current_datetime.minute

print("hours : ", hour, "minute : ", minute)

app = Flask(__name__)
app.secret_key = os.urandom(24)

host = "localhost" # parsahome.mysql.pythonanywhere-services.com
database = "smarthome" # parsahome$smarthome
user = "root"# parsahome
password = ""# mysqlroot
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

def time_iran():
    iran_timezone = pytz.timezone('Asia/Tehran')
    iran_now = datetime.now(iran_timezone)
    formatted_date_time = iran_now.strftime("%Y/%m/%d_%H/%M")
    return formatted_date_time      
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
                                                    param1 = (token, first_name, phone_number, email, password, 0, 0)
                                                    param2 = (token, 0, 0, 0, 0, 0)
                                                    param3 = (token, 0, 0, 0)
                                                    param4 = (token, 0, 0, 0, 0)
                                                    param5 = (token, 0, 0, 0)
                                                    param6 = (token, 0, 0, 0, 0)
                                                    param7 = (token, 0, 0, 0)
                                                    param8 = (token, 0, 0, 0)
                                                    param9 = (token, 0, 0, 0)
                                                    param10 = (token, 0)
                                                    param11 = (token, 0, 0, 0)
                                                    param12 = (token, 0,0,0)
                                                    cur.execute("INSERT INTO users(token, name, phone, email, password, telegram, gmail) VALUES (%s,%s,%s,%s,%s,%s,%s)", param1)
                                                    cur.execute("INSERT INTO sensor(token, pir, strike, temp, saving, lcd) VALUES (%s,%s,%s,%s,%s,%s)", param2)
                                                    cur.execute("INSERT INTO night(token, router, lamps, security) VALUES (%s,%s,%s,%s)", param3)
                                                    cur.execute("INSERT INTO mode(token, ECO, Night, HomeO, Home) VALUES (%s,%s,%s,%s,%s)", param4)
                                                    cur.execute("INSERT INTO logs(token, pir, strike, temp) VALUES (%s,%s,%s,%s)", param5)
                                                    cur.execute("INSERT INTO lamp(token, lamp1, lamp2, lamp3, lamp4) VALUES (%s,%s,%s,%s,%s)", param6)
                                                    cur.execute("INSERT INTO homeout(token, router, lamps, security) VALUES (%s,%s,%s,%s)", param7)
                                                    cur.execute("INSERT INTO home(token, router, lamps, security) VALUES (%s,%s,%s,%s)", param8)
                                                    cur.execute("INSERT INTO eco(token, router, lamps, security) VALUES (%s,%s,%s,%s)", param9)
                                                    cur.execute("INSERT INTO data(token, temp) VALUES (%s,%s)", param10)
                                                    cur.execute("INSERT INTO settings(token, temp, pir, strike) VALUES (%s,%s,%s,%s)", param11)
                                                    cur.execute("INSERT INTO energy(token, data, today, month) VALUES (%s,%s,%s,%s)", param12)
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
    session.pop("token", None)
    phone_number = data.get('phoneNumber')
    email = data.get('email')
    password = data.get('password')
    result = check_info(data)
    if result:
        return result, 400
    else :
        cur.execute(f"SELECT token FROM users WHERE phone = {data.get("phoneNumber")}")
        a = cur.fetchone()
        session["token"] = a[0]
        session["phoneNumber"] = data.get('phoneNumber')
        session["email"] = data.get('email')
        response = {"status" : "Register Successful"}
        return response, 200


def check(token):
    cur.execute(f"SELECT token FROM users")
    a = cur.fetchall()
    for i in a:
        for t in i:
            if int(t) == int(token):
                return True
            else:
                return False
def sensor(data):
    token = data.get("token")
    date = data.get("time")
    pir = data.get("pir")
    strike = data.get("strike")
    l = []
    if pir and strike:
        cur.execute(f"SELECT pir,strike FROM logs WHERE token = {token}")
        a = cur.fetchone()
        if a:
            b = a[0]
            c = a[1]
            if b == "0":
                q = f"{date}:{pir}"
                param = (q, token)
                cur.execute("UPDATE logs SET pir = %s WHERE token = %s", param)
                con.commit()
                l.append("pir")
            else:
                q = f"{b}-{date}:{pir}"
                param = (q, token)
                cur.execute("UPDATE logs SET pir = %s WHERE token = %s", param)
                con.commit()
                l.append("pir")
            if c == "0":
                q = f"{date}:{strike}"
                param = (q, token)
                cur.execute("UPDATE logs SET strike = %s WHERE token = %s", param)
                con.commit()
                l.append("strike")
            else :
                q = f"{c}-{date}:{strike}"
                param = (q, token)
                cur.execute("UPDATE logs SET strike = %s WHERE token = %s", param)
                con.commit()
                l.append("strike")
            if bool(l):
                q = l[0]
                w = l[1]
                if q == "pir" and w == "strike":
                    return "Save logs PIR,STRIKE"
        else :
            return "Problem : Database > Logs > PIR"
    else:    
        if pir:
            cur.execute(f"SELECT pir FROM logs WHERE token = {token}")
            a = cur.fetchone()
            if a:
                b = a[0]
                if b == "0":
                    q = f"{date}:{pir}"
                    param = (q, token)
                    cur.execute("UPDATE logs SET pir = %s WHERE token = %s", param)
                    con.commit()
                    return "Save logs PIR"
                else:
                    q = f"{b}-{date}:{pir}"
                    param = (q, token)
                    cur.execute("UPDATE logs SET pir = %s WHERE token = %s", param)
                    con.commit()
                    return "Save logs PIR"
            else:
                return "Problem : Database > Logs > PIR"
        if strike:
            cur.execute(f"SELECT strike FROM logs WHERE token = {token}")
            a = cur.fetchone()
            if a:
                b = a[0]
                if b == "0":
                    q = f"{date}:{strike}"
                    param = (q, token)
                    cur.execute("UPDATE logs SET strike = %s WHERE token = %s", param)
                    con.commit()
                    return "Save logs STRIKE"
                else :
                    q = f"{b}-{date}:{strike}"
                    param = (q, token)
                    cur.execute("UPDATE logs SET strike = %s WHERE token = %s", param)
                    con.commit()
                    return "Save logs STRIKE"
            else :
                return "Problem : Database > Logs > STRIKE"
            
def board(data):
    current_datetime = datetime.now()
    hour = current_datetime.hour
    minute = current_datetime.minute
    l = []
    m = []
    token = data.get("token")
    cur.execute(f"SELECT temp FROM data WHERE token = {token}")
    tyu = cur.fetchone()
    temperature = tyu[0]
    cur.execute(f"SELECT pir,strike,temp,saving,lcd FROM sensor WHERE token = {token}")
    a = cur.fetchone()
    cur.execute(f"SELECT lamp1, lamp2, lamp3, lamp4 FROM lamp WHERE token = {token}")
    b = cur.fetchone()
    if a:
        pir = a[0]
        strike = a[1]
        temp  = a[2]
        saving = a[3]
        lcd = a[4]
        lamp1 = b[0]
        lamp2 = b[1]
        lamp3 = b[2]
        lamp4 = b[3]
        if int(pir) == 1:
            l.append("pir")
        if int(strike) == 1:
            l.append("strike")
        if int(temp) == 1:
            l.append("temp")
        if int(saving) == 1:
            l.append("saving")
        if int(lcd) == 1:
            l.append("lcd")
        if int(lamp1) == 1:
            l.append("lamp1")
        if int(lamp2) == 1:
            l.append("lamp2")
        if int(lamp3) == 1:
            l.append("lamp3")
        if int(lamp4) == 1:
            l.append("lamp4")
        if bool(l):
            if "pir" in l:
                cur.execute(f"SELECT pir FROM settings WHERE token = {token}")
                q = cur.fetchone()
                if q:
                    bq = q[0]
                    if bq == "0":
                        m.append("pir>1")
                    else:
                        s = bq.split(":")
                        date = s[0]
                        status = s[1]
                        if "_" in date:
                            we = date.split("_")[0]
                            er = date.split("_")[1]
                            if int(hour) >= int(we) and int(hour) < int(er) :
                                m.append(f"pir>{status}")
                            else:
                                if int(status) == 1:
                                    m.append("pir>0")
                                else :
                                    m.append("pir>1")
                        else:
                            if int(hour) == int(date):
                                m.append(f"pir>{status}")
                            else:
                                if int(status) == 0:
                                    m.append("pir>1")
                                else:
                                    m.append("pir>0")
                else:
                    return "Problem in Database : Settings > PIR"
            if "strike" in l:
                cur.execute(f"SELECT strike FROM settings WHERE token = {token}")
                a = cur.fetchone()
                if a:
                    b = a[0]
                    if b == "0":
                        m.append("strike>1")
                    else:
                        if ":" in b:
                            c = b.split(":")
                            date = c[0]
                            status = c[1]
                            if "_" in date :
                                w = date.split("_")[0]
                                e = date.split("_")[1]
                                if int(hour) >= int(w) and int(hour) < int(e) :
                                    m.append(f"strike>{status}")
                                else:
                                    if int(status) == 1:
                                        m.append("strike>0")
                                    else:
                                        m.append("strike>1")
                            else :
                                if int(hour) == int(date):
                                    m.append(f"strike>{status}")
                                else:
                                    if int(status) == 0:
                                        m.append("strike>1")
                                    else:
                                        m.append("strike>0")
                else:
                    return "Problem in Database : Settings > STRIKE"
            if "temp" in l:
                cur.execute(f"SELECT temp FROM settings WHERE token = {token}")
                a = cur.fetchone()
                if a:
                    b = a[0]
                    if ":" in b:
                        q = b.split(":")
                        date = q[0]
                        temp = q[1]
                        if "_" in date:
                            we = date.split("_")[0]
                            er = date.split("_")[1]
                            if int(hour) >= int(we) and int(hour) < int(er):
                                m.append(f"temp>{temp}")
                            else:
                                m.append("temp>1")
                        else:
                            if int(hour) == int(date):
                                m.append(f"temp>{temp}")
                            else:
                                m.append("temp>1")
                    else :
                        if int(b) == int(0):
                            m.append("temp>1")
                else:
                    return "Problem in Database : Settings > TEMP"
        lk = []
        if "pir" in m and int(m.count("pir>0")) == 1 or int(m.count("pir>1")) == 0 or int(
            m.count("pir>0") == 0) or int(m.count("pir>1")) == 1:
            if int(m.count("pir>1")) == 1:
                lk.append("1")
            else:
                if int(m.count("pir>0")) == 1:
                    lk.append("0")
                else :
                    lk.append("0")
        if "strike" in m and int(m.count("strike>0")) == 1 or int(m.count("strike>1")) == 0 or int(
            m.count("strike>0") == 0) or int(m.count("strike>1")) == 1 :
            if int(m.count("strike>1")) == 1:
                lk.append("1")
            else:
                if int(m.count("strike>0")) == 1:
                    lk.append("0")
                else :
                    lk.append("0")
        if "temp" in m or "temp" in l:
            df = []
            for i in m:
                if "temp" in i or "temp>" in i:
                    df.append(i)
                else:
                    pass
            lk.append(f"{df[0].split('>')[1]}")   
        else :
            lk.append(f"0")
        if "saving" in l and int(l.count("saving")) == 1 or l.count("saving") == "1" or l.count("saving") == 1 :
            lk.append(f"{1}")
        else :
            if "saving" not in l and int(l.count("saving")) == 0 or l.count("saving") == "0" or l.count("saving") == 0:
                lk.append(f"{0}")
        if "lcd" in l and int(l.count("lcd")) == 1 or l.count("lcd") == "1" or l.count("lcd") == 1:
            lk.append(f"{1}")
        else :
            if "lcd" not in l and int(l.count("lcd")) == 0 or l.count("lcd") == "0" or l.count("lcd") == 0:
                lk.append(f"{0}")
        if "lamp1" in l and int(l.count("lamp1")) == 1 or l.count("lamp1") == "1" or l.count("lamp1") == 1:
            lk.append(f"{1}")
        else :
            if "lamp1" not in l and int(l.count("lamp1")) == 0 or l.count("lamp1") == "0" or l.count("lamp1") == 0:
                lk.append(f"{0}")
        if "lamp2" in l and int(l.count("lamp2")) == 1 or l.count("lamp2") == "1" or l.count("lamp2") == 1:
            lk.append(f"{1}")
        else :
            if "lamp2" not in l and int(l.count("lamp2")) == 0 or l.count("lamp2") == "0" or l.count("lamp2") == 0:
                lk.append(f"{0}")
        if "lamp3" in l and int(l.count("lamp3")) == 1 or l.count("lamp3") == "1" or l.count("lamp3") == 1:
            lk.append(f"{1}")
        else :
            if "lamp3" not in l and int(l.count("lamp3")) == 0 or l.count("lamp3") == "0" or l.count("lamp3") == 0:
                lk.append(f"{0}")
        if "lamp4" in l and int(l.count("lamp4")) == 1 or l.count("lamp4") == "1" or l.count("lamp4") == 1:
            lk.append(f"{1}")
        else :
            if "lamp4" not in l and int(l.count("lamp4")) == 0 or l.count("lamp4") == "0" or l.count("lamp4") == 0:
                lk.append(f"{0}")
        result = {"pir": f"{lk[0]}",
                  "strike":f"{lk[1]}",
                  "temp":f"{lk[2]}",
                  "saving":f"{lk[3]}",
                  "lcd":f"{lk[4]}",
                  "lamp1":f"{lk[5]}",
                  "lamp2":f"{lk[6]}",
                  "lamp3":f"{lk[7]}",
                  "lamp4":f"{lk[8]}",
                  "temperature":f"{temperature}"}
        return result
                                 
def status(data):
    token = data.get("token")
    pir = data.get("pir")
    strike = data.get("strike")
    temp = data.get("temp")
    saving = data.get("saving")
    lcd = data.get("lcd")
    lamps = data.get("lamps")
    modes = data.get("modes")
    r = []
    if modes:
        r.append("mode")
        if modes.get("ECO"):
            param = (1,0,0,0, token)
            cur.execute("UPDATE mode SET ECO = %s , Home = %s, HomeO = %s, Night = %s WHERE token = %s", param)
            if (modes.get("ECO")).get("lamps") :
                param = ((modes.get("ECO")).get("lamps"), token)
                cur.execute("UPDATE eco SET lamps = %s WHERE token = %s", param)
                con.commit()
                if ((modes.get("ECO")).get("lamps")) == "1":
                    param1 = (1,1,1,1, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param1)
                    con.commit()
                    r.append("lamps")
                else:
                    param1 = (0,0,0,0, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param1)
                    con.commit()
                    r.append("lamps")
            if (modes.get("ECO")).get("router") :
                param = ((modes.get("ECO")).get("router"), token)
                cur.execute("UPDATE eco SET router = %s WHERE token = %s", param)
                con.commit()
                r.append("router")
            if (modes.get("ECO")).get("security") :
                param = ((modes.get("ECO")).get("security"), token)
                cur.execute("UPDATE eco SET security = %s WHERE token = %s", param)
                con.commit()
                if ((modes.get("ECO")).get("security")) == "1":
                    param = (1,1, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")
                else:
                    param = (0,0, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")
        if modes.get("Home"):
            param = (1,0,0,0, token)
            cur.execute("UPDATE mode SET Home = %s, HomeO = %s, Night = %s, ECO = %s WHERE token = %s", param)
            con.commit()
            if (modes.get("Home")).get("lamps") :
                param = ((modes.get("Home")).get("lamps"), token)
                cur.execute("UPDATE home SET lamps =%s WHERE token = %s", param)
                con.commit()
                if (modes.get("Home")).get("lamps") == "1":
                    param = (1,1,1,1, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param)
                    con.commit()
                    r.append("lamps")
                else :
                    param = (0,0,0,0, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param)
                    con.commit()
                    r.append("lamps")
            if (modes.get("Home")).get("router") :
                param = ((modes.get("Home")).get("router"), token)
                cur.execute("UPDATE home SET router = %s WHERE token = %s", param)
                con.commit()
                r.append("router")
            if (modes.get("Home")).get("security"):
                param = ((modes.get("Home")).get("security"), token)
                cur.execute("UPDATE home SET security = %s WHERE token = %s", param)
                con.commit()
                if (modes.get("Home")).get("security") == "1":
                    param = (1,1, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")
                else:
                    param = (1,1, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")
        if modes.get("HomeO"):
            param = (1,0,0,0, token)
            cur.execute("UPDATE mode SET HomeO = %s, Home = %s, Night = %s, ECO = %s WHERE token = %s", param)
            con.commit()
            if (modes.get("HomeO")).get("lamps") :
                param = ((modes.get("HomeO")).get("lamps"), token)
                cur.execute("UPDATE homeout SET lamps =%s WHERE token = %s", param)
                con.commit()
                if (modes.get("HomeO")).get("lamps") == "1":
                    param = (1,1,1,1, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param)
                    con.commit()
                    r.append("lamps")
                else :
                    param = (0,0,0,0, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param)
                    con.commit()
                    r.append("lamps")
            if (modes.get("HomeO")).get("router") :
                param = ((modes.get("HomeO")).get("router"), token)
                cur.execute("UPDATE homeout SET router = %s WHERE token = %s", param)
                con.commit()
                r.append("router")
            if (modes.get("HomeO")).get("security"):
                param = ((modes.get("HomeO")).get("security"), token)
                cur.execute("UPDATE homeout SET security = %s WHERE token = %s", param)
                con.commit()
                if (modes.get("HomeO")).get("security") == "1":
                    param = (1,1, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")
                else:
                    param = (1,1, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")
        if modes.get("Night"):
            param = (1,0,0,0, token)
            cur.execute("UPDATE mode SET Night = %s, HomeO = %s, Home = %s, ECO = %s WHERE token = %s", param)
            con.commit()
            if (modes.get("Night")).get("lamps") :
                param = ((modes.get("Night")).get("lamps"), token)
                cur.execute("UPDATE night SET lamps = %s WHERE token = %s", param)
                con.commit()
                if (modes.get("Night")).get("lamps") == "1":
                    param = (1,1,1,1, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param)
                    con.commit()
                    r.append("lamps")
                else :
                    param = (0,0,0,0, token)
                    cur.execute("UPDATE lamp SET lamp1 = %s, lamp2 = %s, lamp3 = %s, lamp4 = %s WHERE token = %s", param)
                    con.commit()
                    r.append("lamps")
            if (modes.get("Night")).get("router") :
                param = ((modes.get("Night")).get("router"), token)
                cur.execute("UPDATE night SET router = %s WHERE token = %s", param)
                con.commit()
                r.append("router")
            if (modes.get("Night")).get("security"):
                param = ((modes.get("Night")).get("security"), token)
                cur.execute("UPDATE night SET security = %s WHERE token = %s", param)
                con.commit()
                if (modes.get("Night")).get("security") == "1":
                    param = (1,1, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")
                else:
                    param = (0,0, token)
                    cur.execute("UPDATE sensor SET pir = %s , strike = %s WHERE token = %s", param)
                    con.commit()
                    r.append("security")        
    else:
        param = (0,0,0,0, token)
        cur.execute("UPDATE mode SET Home = %s, HomeO = %s, Night = %s, ECO = %s WHERE token = %s", param)
        con.commit()
        r.append("manual")
        if pir:
            if pir != "0" and pir != "1" and pir.get("limit"):
                limit = pir.get("limit")
                param = (limit, token)
                param1 = (pir.get("status"), token)
                cur.execute("UPDATE settings SET pir = %s WHERE token = %s", param)
                con.commit()
                cur.execute("UPDATE sensor SET pir = %s WHERE token = %s", param1)
                con.commit()
                r.append("pir")
            else :
                param = (pir, token)
                param1 = (0, token)
                cur.execute("UPDATE sensor SET pir = %s WHERE token = %s", param)
                con.commit()
                cur.execute("UPDATE settings SET pir = %s WHERE token = %s", param1)
                con.commit()
                r.append("pir")
        if strike:
            if strike != "0" and strike != "1" and strike.get("limit"):
                limit = strike.get("limit")
                param = (limit, token)
                param1 = (strike.get("status"), token)
                cur.execute("UPDATE settings SET strike = %s WHERE token = %s", param)
                con.commit()
                cur.execute("UPDATE sensor SET strike = %s WHERE token = %s", param1)
                con.commit()
                r.append("strike")
            else :
                param = (strike, token)
                param1 = (0, token)
                cur.execute("UPDATE sensor SET strike = %s WHERE token = %s", param)
                con.commit()
                cur.execute("UPDATE settings SET strike = %s WHERE token = %s", param1)
                con.commit()
                r.append("strike")
        if temp:
            if temp != "0" and temp != "1" and temp.get("limit"):
                limit = temp.get("limit")
                param = (limit, token)
                param1 = (temp.get("status"), token)
                cur.execute("UPDATE settings SET temp = %s WHERE token = %s", param)
                con.commit()
                cur.execute("UPDATE sensor SET temp = %s WHERE token = %s", param1)
                con.commit()
                r.append("temp")
            else :
                param = (temp, token)
                param1 = (0, token)
                cur.execute("UPDATE sensor SET temp = %s WHERE token = %s", param)
                con.commit()
                cur.execute("UPDATE settings SET temp = %s WHERE token = %s", param1)
                con.commit()
                r.append("temp")
        if saving :
            if saving == "1" :
                param = (1,0,1,1, token)
                cur.execute("UPDATE sensor SET saving = %s , lcd = %s , pir = %s , strike = %s WHERE token = %s", param)
                con.commit()
                r.append("saving")
            else :
                if lcd:
                    if lcd == "1":
                        param = (1,0, token)
                        cur.execute("UPDATE sensor SET lcd = %s , saving = %s WHERE token = %s", param)
                        con.commit()
                        r.append("lcd")
                    else :
                        param = (0,0, token)
                        cur.execute("UPDATE sensor SET lcd = %s , saving = %s WHERE token = %s", param)
                        con.commit()
                        r.append("lcd")
        if lamps :
            if lamps == 1 or lamps == "1" or lamps == 0 or lamps == "0":
                param = (lamps, lamps, lamps, lamps, token)
                cur.execute("UPDATE lamp SET lamp1 = %s , lamp2 = %s , lamp3 = %s, lamp4 = %s WHERE token = %s", param)
                con.commit()
                r.append("lamps")
            if lamps != "0" and lamps != "1" and lamps.get("lamp1"):
                param = (lamps.get("lamp1"), token)
                cur.execute("UPDATE lamp SET lamp1 = %s WHERE token = %s", param)
                con.commit()
                r.append("lamp1")
            if lamps != "0" and lamps != "1" and lamps.get("lamp2"):
                param = (lamps.get("lamp2"), token)
                cur.execute("UPDATE lamp SET lamp2 = %s WHERE token = %s", param)
                con.commit()
                r.append("lamp2")
            if lamps != "0" and lamps != "1" and lamps.get("lamp3"):
                param = (lamps.get("lamp3"), token)
                cur.execute("UPDATE lamp SET lamp3 = %s WHERE token = %s", param)
                con.commit()
                r.append("lamp3")
            if lamps != "0" and lamps != "1" and lamps.get("lamp4"):
                param = (lamps.get("lamp4"), token)
                cur.execute("UPDATE lamp SET lamp4 = %s WHERE token = %s", param)
                con.commit()
                r.append("lamp4")
    if bool(r):
        if int(r.count("mode")) == 1:
            if int(r.count("lamps")) == 1 and int(r.count("router")) == 1 and int(r.count("security")) == 1 :
                return "Mode Data Save"
            else :
                return "Error in Data save Mode"
        else :
            if int(r.count("manual")) == 1:
                return "Data Manual Save"
            else :
                return "Error in Save Data on Manual"
    else :
        return "Error in Database"
            
        
@app.route('/api/<path>', methods=['POST'])
def api(path):
    data = request.get_json()
    token = data.get("token")
    a = check(token)
    if a == True:
        if path == "sensor_logs":
            b = sensor(data)
            return b
        else:
            if path == "data":
                c = board(data)
                return c
            else:
                if path == "status":
                    d = status(data)
                    return d
                else:
                    if path == "temp":
                        param = (data.get("temp"), token)
                        cur.execute("UPDATE data SET temp = %s WHERE token = %s", param)
                        con.commit()
                        temp = data.get("temp")
                        return f"Save Data : {temp}"
                    else :
                        if path == "energy":
                            pass
                        else:
                            if path == "notification":
                                qw = []
                                tel = data.get("telegram")
                                em = data.get("email")
                                if tel:
                                    param = (tel, token)
                                    cur.execute("UPDATE users SET telegram = %s WHERE token = %s", param)
                                    con.commit()
                                    qw.append("telegram")
                                if em :
                                    param = (em, token)
                                    cur.execute("UPDATE users SET gmail = %s WHERE token = %s", param)
                                    con.commit()
                                    qw.append("email")
                                if bool(qw):
                                    return "Save Data"
                                else :
                                    return "Problem in save data api notification"
                            else :
                                if path == "get_time":
                                    a = time_iran()
                                    return a
                                else :
                                    return "Path is not available"
    else :
        return "Access Denied"
@app.route('/register', methods=['POST'])
def register():
    session.pop("email", None)
    session.pop("number", None)
    session.pop("token", None)
    session.pop("phoneNumber", None)
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
        cur.execute(f"SELECT token FROM users WHERE phone = {data.get("phoneNumber")}")
        a = cur.fetchone()
        session["token"] = a[0]
        session["phoneNumber"] = data.get('phoneNumber')
        session["email"] = data.get('email')
        response = {"status" : "Register Successful"}
        return response, 200
    
@app.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("number", None)
    session.pop("phoneNumber", None)
    session.pop("token", None)
    g.token = None
    g.user = None
    g.phone = None
    return "ok"
@app.before_request
def before():
    g.user = None
    g.phone = None
    g.token = None
    print(session)
    if "email" in session:
        g.user = session["email"]
    if "phoneNumber" in session:
        g.phone = session["phoneNumber"]
    if "token" in session:
        g.token = session["token"]

@app.route('/account', methods=["GET", "POST"])
def account():
    if g.user and g.token :
        cur.execute(f"SELECT name FROM users WHERE token = {session["token"]}")
        a = cur.fetchone()
        name = a[0]
        return render_template("index.html",email=session["email"], token=session["token"], phone=session["phoneNumber"], name=name)
    
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