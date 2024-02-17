from flask import Flask, render_template, request, make_response
import database

app = Flask(__name__, instance_path="/home/stian/Documents/2023-2024-dokumenter/Brukerstøtte/Social-engineering/cookie_test/flask_eksempel/app.py")


@app.route("/")
def root_route():
    cookie = request.cookies.get("cookie_id")
    
    if not cookie:
        new_cookie = database.create_new_cookie()
        database.add_cookie(new_cookie, request.base_url)
        resp = make_response(render_template("index.html", cookie_login_ID=""))
        resp.set_cookie('cookie_id', new_cookie)
        return resp
    return render_template("index.html", cookie_login_ID=cookie)


@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    
    if request.method == 'POST':
        
        resp = make_response(render_template('readcookie.html'))
        
        return resp

@app.route('/getcookie')
def getcookie():

    cookieID = request.cookies.get('cookie_id')
    number = database.get_number_of_people()
    if cookieID:
        html = f"""<h1>Your cookie: {cookieID}</h1>
        <p>You are our visitor number: {number[0]}</p>"""
        #database.delete_cookie(request.cookies.get("cookie_id"))
        response = make_response(html)
        database.delete_cookie(cookieID)
        response.set_cookie("cookie_id", max_age=0)
        
        return response
    return f'<h1>No cookies for you! You are however our visitor number {number[0]}</h1>'

if __name__ == "__main__":
    
    app.run("0.0.0.0", port=5000, debug=True)
