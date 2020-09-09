import base64
import os

from flask import Flask, render_template, redirect, request, url_for
import API.Data
import API.APICalls
from API import Sender, APICalls

app = Flask(__name__)

@app.route('/')
def start():
    if not os.path.exists("Credentials"):
        return redirect(url_for('signin'))
    else:
        return redirect(url_for('checkin'))


@app.route('/new/<name>/<badge>/<int:amount>', methods=['GET', 'POST'])
def enterItems(name, badge, amount):
    if request.method == 'POST':
        message = ""
        for i in range(amount):
            message += "returned a " + str(request.form['number ' + str(i)]) + " asset number " + str(request.form['items ' + str(i)] + "\n")

        keyboard = request.form.get('keyboard')
        mouse = request.form.get('mouse')
        headset = request.form.get('headset')

        if keyboard == "on":
            message += "keyboard "
        if mouse == "on":
            message += "mouse "
        if headset == "on":
            message += "headset "

        message += " Were also returned"
        print(message)

        data = API.Data.data(str(name), str(badge), message)
        Sender.send(APICalls.makeIssue(data), "https://vivint.atlassian.net/rest/api/3/issue")

        return redirect(url_for('checkin'))


    return render_template('EnterItems.html', name=name, badge=badge, amount=int(amount))

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    error = ""
    if request.method == 'POST':
        name = request.form['name']
        badge = request.form['badge']
        amount = request.form['amount']

        if len(name) == 0 or len(badge) == 0:
            error = "failed"
        else:
            return redirect(url_for('enterItems', name=name, badge=badge, amount=amount))

    return render_template('StartCheckIn.html', message=error)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        API = request.form['API']

        if len(email) == 0 or len(API) == 0:
            error = "failed"
        else:
            f = open("Credentials", "w+")
            f.write(base64.b64encode(str(email).encode()).decode() + "\n")
            f.write(base64.b64encode(str(API).encode()).decode())
            f.close()

            if not Sender.auth().status_code == 200:
                os.remove("Credentials")
            else:
                return redirect(url_for('checkin'))
            return redirect(url_for('signin'))

    return render_template('sign-in.html', message=error)

if __name__ == '__main__':
    app.run()
