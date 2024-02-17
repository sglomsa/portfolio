from flask import Flask, render_template, Response, request, redirect, url_for

import database as db

app = Flask(__name__)

dbase = db.db_connect()


@app.route("/")
def index():
<<<<<<< Updated upstream
    cookie = request.cookies.get("cookie_id")
    if not cookie:
=======
    if "SESSION" in request.cookies.keys():
>>>>>>> Stashed changes
        return render_template("index.html")
    else:
        cookie_id = db.create_new_cookie()
        res = Response(render_template("index.html"), status=200)
        res.set_cookie(key="SESSION", value=cookie_id)
        db.add_cookie(cookie_id=cookie_id, url=request.url)
        return res


@app.route("/hva-vi-kunne-gjort")
def melding_fare():
    return render_template("melding_fare.html")


@app.route("/du-har-blitt-lurt")
def melding_index():
    kjeks = request.cookies.get("cookie_id")
    print(kjeks)
    if kjeks:
        db.click_cookie_update(kjeks)
        return render_template("melding_index.html")
    return render_template("melding_index.html")


@app.route("/tips")
def melding_tips():
    return render_template("melding_tips.html")


@app.route("/info-phishing")
def phishing():
    return render_template("phishing.html")


@app.route("/superadmin")
def superadmin():
    res = Response(f"Folk: {db.get_number_of_people_mcdonalds()}")
    return res


if __name__ == "__main__":
    app.run(debug=True)
