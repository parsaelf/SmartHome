# from flask import Flask, session, render_template, request, redirect, g, url_for
# import os 

# app = Flask(__name__)

# app.secret_key = os.urandom(24)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         session.pop("user", None)
#         if request.form["password"] == "password":
#             session["user"] = request.form["username"]
#             session["password"] = request.form["password"]
#             return redirect(url_for("acc"))
#     return render_template("index.html")

# @app.route("/acc")
# def acc():
#     if g.user:
#         return session["user"]
#     return redirect(url_for("index"))

# @app.before_request
# def before():
#     g.user = None
    
#     if "user" in session:
#         g.user = session["user"]
#     if "password" in session:
#         g.password = session["password"]
        
# if __name__ == "__main__":
#     app.run(debug=True)


import requests
import json
import string
payload = {
    "token":"2",
    "lamp1":"0"
}

response = requests.post(url="http://parsahome.pythonanywhere.com/api",data=json.dumps(payload))
print(response.status_code)


