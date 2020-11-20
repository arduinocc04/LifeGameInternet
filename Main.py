from flask import Flask, render_template, request, redirect, url_for, session
from flask import json
from flask_socketio import SocketIO, emit
import DbManager
import ntplib
import sqlite3
from time import ctime
import base64
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lisztlacampanella'
sio = SocketIO(app)

@app.route('/')
def main():
    if not session.get('logged_in'): return redirect('signin')
    return redirect('game')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/addUser', methods=['POST'])
def addUser():
    UsMan = DbManager.UserManager()
    jsonData = request.get_json()
    name = jsonData['name']
    nickName = jsonData['nickName']
    studentId = int(jsonData['studentId'])
    salt = jsonData['salt']
    uid = jsonData['uid']
    pw = jsonData['pw']
    showNs = 1 if jsonData['showNs'] == 'true' else 0
    UsMan.uploadUser(uid, pw, salt, nickName, name, studentId, showNs)
    UsMan.closeDb()
    return redirect(url_for('showProfile', uid=uid))

@app.route('/profile', methods=['GET'])
def showProfile():
    uid = request.args.get('uid')
    UsMan = DbManager.UserManager()
    tmp = UsMan.getInfo(uid)
    UsMan.closeDb()
    if tmp == None: return render_template('profileErr.html')
    _, _, _, nickName, name, studentId, showNs, maxScore = tmp
    add = ""
    #if not showNs:
        #if session['id'] == uid:
       #     add = "(not visible)"
        #else:
            #name="비밀"
           # studentId="비밀"
    return render_template('profile.html', uid=uid, studentId=studentId, name=name, nickName=nickName, maxScore=maxScore, add=add)


@app.route('/game')
def game():
    return render_template('life.html')

@app.route('/wating')
def wating():
    return render_template('wating.html')

@app.route('/score', methods=['POST'])
def uploadScore():
    DbMan = DbManager.DbManager()
    jsonData = request.get_json()
    name = jsonData['name']
    mCellCnt = int(jsonData['mCellCnt'])
    frame = int(jsonData['frame'])
    delayedTime = float(jsonData['delayedTime'])
    score = float(jsonData['score'])
    img = base64.b64decode(jsonData['image'][22:])

    cli = ntplib.NTPClient()
    now = ctime(cli.request("kr.pool.ntp.org").tx_time + 32400)

    try:
        DbMan.uploadScore(now, name, score, mCellCnt, frame, delayedTime)
        with open(f'static/image/{name}.jpg', 'wb') as f:
            f.write(img)
    except sqlite3.IntegrityError:
        if score > DbMan.getScoreByName(name):
            DbMan.updateScore(now, name, score, mCellCnt, frame, delayedTime)
            with open(f'static/image/{name}.jpg', 'wb') as f:
                f.write(img)
    DbMan.closeDb()
    return redirect(url_for('showLeaderBoard', name=name))

@app.route('/leaderboard', methods = ['GET'])
def showLeaderBoard():
    name = request.args.get('name')
    DbMan = DbManager.DbManager()
    tmp = DbMan.getTNSAll()
    DbMan.closeDb()
    tmp.sort(key = lambda x:-x[2])
    prev = -1
    prevPlace = -1
    for i in range(len(tmp)):
        tmp[i] = (tmp[i], (prevPlace if prev == tmp[i][2] else i+1),)
        prev = tmp[i][0][2]
        prevPlace = tmp[i][1]
    return render_template('leaderboard.html', scores=tmp, name=name, n = len(tmp))

@app.route('/image', methods = ['GET'])
def showImage():
    name = request.args.get('name')
    originalName = request.args.get('originalName')
    time = request.args.get('time')
    score = float(request.args.get('score'))
    rank = int(request.args.get('rank'))
    DbMan = DbManager.DbManager()
    _, _, _, mCellCnt, frame, delayedTime = DbMan.getRawInfo(name)
    return render_template('image.html', targetName = name, originalName=originalName, time=time, score=score, rank=rank, imgName=f'image/{name}.jpg', mCellCnt=mCellCnt, frame=frame, delayedTime=delayedTime)

if __name__ == "__main__":
    sio.run(app, host='0.0.0.0', port = 8000)
