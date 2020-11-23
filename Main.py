from flask import Flask, render_template, request, redirect, url_for, session
import DbManager
import ntplib
import sqlite3
from time import ctime
import base64
import random
import string
import re

app = Flask(__name__)
with open('secret.txt', 'r', encoding='utf8') as f:
    app.config['SECRET_KEY'] = f.readline().rstrip()
    app.secret_key = f.readline().rstrip().encode()

ekn = re.compile('[a-zA-Zㄱ-ㅎ가-힣\d]+')

@app.route('/')
def main():
    if not 'uid' in session: return redirect(url_for('signin'))
    return redirect(url_for('genQrcode'))

@app.route('/signout')
def signout():
    session.pop('uid')
    return redirect(url_for('signin'))

@app.route('/signin')
def signin():
    prev = request.args.get('prev')
    return render_template('signinId.html', prev=prev)

@app.route('/signinPw')
def signinPw():
    prev = ekn.match(request.args.get('prev')).group()
    salt = ekn.match(request.args.get('salt')).group()
    uid = ekn.match(request.args.get('uid')).group()
    return render_template('signinPw.html', prev=prev, salt=salt, uid=uid)

@app.route('/signinId', methods=['GET'])
def signinId():
    prev = request.args.get('prev')
    uid = ekn.match(request.args.get('uid')).group()
    UsMan = DbManager.UserManager()
    tmp = UsMan.getSalt(uid)
    if tmp == None: return render_template('idNotExist.html')
    UsMan.closeDb()
    return redirect(url_for('signinPw', prev=prev, uid=uid, salt=tmp))
    

@app.route('/signinUser', methods=['POST'])
def login():
    UsMan = DbManager.UserManager()
    uid = ekn.match(request.form['uid']).group()
    pw = request.form['pw']
    prev = request.form['prev']
    tmp = UsMan.getPw(uid)
    UsMan.closeDb()
    if tmp != None:
        if pw == tmp:
            session['uid'] = uid
            if prev != "None": return redirect(prev)
            return redirect(url_for('showProfile', uid=uid))
        else:
            UsMan = DbManager.UserManager()
            tmp = UsMan.getSalt(uid)
            UsMan.closeDb()
            return redirect(url_for('signinPw', prev=prev, salt=tmp, uid=uid))
    else:
        return redirect(url_for('signin'))

@app.route('/signup')
def signup():
    prev = request.args.get('prev')
    return render_template('signup.html', prev = prev)

@app.route('/info')
def goNotion():
    return redirect('https://www.notion.so/LifeGameInternet-976cac5fd76846b9b057db8b25277bcb')

@app.route('/err')
def error():
    return render_template('Error.html')

@app.route('/addUser', methods=['POST'])
def addUser():
    print(request.form)
    UsMan = DbManager.UserManager()
    DbMan = DbManager.DbManager()
    name = ekn.match(request.form['name']).group()
    studentId = int(ekn.match(request.form['studentId']).group())
    salt = ekn.match(request.form['salt']).group()
    uid = ekn.match(request.form['uid']).group()
    pw = ekn.match(request.form['pw']).group()
    prev = request.form['prev']
    #showNs = 1 if request.form['showNs'] == 'on' else 0
    showNs = 1
    try:
        UsMan.uploadUser(uid, pw, salt, name, studentId, showNs)
    except sqlite3.IntegrityError:
        return redirect(url_for('idErr'))
    DbMan.uploadScore(0, uid, 0, 0, 0, 0)
    DbMan.closeDb()
    UsMan.closeDb()
    return redirect(url_for('signin', prev=prev))

@app.route('/idErr')
def idErr():
    return render_template('idErr.html')

@app.route('/profile', methods=['GET'])
def showProfile():
    uid = ekn.match(request.args.get('uid')).group()
    UsMan = DbManager.UserManager()
    DbMan = DbManager.DbManager()
    tmp = UsMan.getInfo(uid)
    UsMan.closeDb()
    if tmp == None: return render_template('profileErr.html')
    _, _, _, name, studentId, showNs = tmp
    maxScore = DbMan.getMScoreByName(uid)
    return render_template('profile.html', uid=uid, studentId=studentId, name=name, maxScore=maxScore, yourId=session['uid'])

@app.route('/gqrcode')
def genQrcode():
    tmp = '' #8자리 랜덤 문자열
    for _ in range(8):
        tmp += random.choice(string.ascii_letters)
    cli = ntplib.NTPClient()
    now = ctime(cli.request("kr.pool.ntp.org").tx_time + 32400)
    GmMan = DbManager.GameManger()
    GmMan.uploadGame(tmp, '', now)
    GmMan.closeDb()
    url = "http://www.arduinocc04.live/game?gid=" + tmp
    imgSrc = f'https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={url}'
    return render_template('qr.html', url = url, url2="/game?gid="+tmp, yourId=session['uid'], imgSrc=imgSrc)

@app.route('/scoreboard', methods=['GET'])
def showScoreboard():
    GmMan = DbManager.GameManger()
    DbMan = DbManager.DbManager()
    gid = ekn.match(request.args.get('gid')).group()
    name = request.args.get('name')
    tmp = GmMan.getInfo(gid)
    if tmp == None: return redirect(url_for('error'))
    _, players, t = tmp
    players = players.split(',')
    tmp = [DbMan.getLTNS(p) for p in players]
    tmp.sort(key = lambda x:-x[2])
    prev = -1
    prevPlace = -1
    for i in range(len(tmp)):
        tmp[i] = (tmp[i], (prevPlace if prev == tmp[i][2] else i+1),)
        prev = tmp[i][0][2]
        prevPlace = tmp[i][1]
    return render_template('scoreboard.html', scores=tmp, name=name, n = len(tmp), gid=gid, yourId=session['uid'])


@app.route('/game', methods=['GET'])
def game():
    gid = ekn.match(request.args.get('gid')).group()
    if not 'uid' in session:
        return redirect(url_for('signin', prev=url_for('game', gid=gid)))
    return render_template('life.html', gid=gid, yourId=session['uid'])

@app.route('/appendUser', methods=['GET'])
def appendUser():
    gid = ekn.match(request.args.get('gid')).group()
    uid = session['uid']
    # uid = request.args.get('uid')
    print(f'gid:{gid}uid:{uid}')
    GmMan = DbManager.GameManger()
    _, ps, _ = GmMan.getInfo(gid)
    if not uid in ps.split(','):
        GmMan.appendPlayer(gid, uid)
    GmMan.closeDb()
    return redirect(url_for('showScoreboard', gid=gid, name=uid))

@app.route('/score', methods=['POST'])
def uploadScore():
    DbMan = DbManager.DbManager()
    jsonData = request.get_json()
    name = session['uid']
    #name = jsonData['name']
    mCellCnt = int(jsonData['mCellCnt'])
    frame = int(jsonData['frame'])
    delayedTime = float(jsonData['delayedTime'])
    score = float(jsonData['score'])
    img = base64.b64decode(jsonData['image'][22:])

    cli = ntplib.NTPClient()
    now = ctime(cli.request("kr.pool.ntp.org").tx_time + 32400)
    with open(f'static/image/{name}_last.jpg', 'wb') as f:
        f.write(img)
    DbMan.updateLScore(now, name, score, mCellCnt, frame, delayedTime)
    if score > DbMan.getMScoreByName(name):
        DbMan.updateMScore(now, name, score, mCellCnt, frame, delayedTime)
        with open(f'static/image/{name}.jpg', 'wb') as f:
            f.write(img)
    DbMan.closeDb()
    return redirect(url_for('showLeaderBoard', name=name))

@app.route('/leaderboard', methods = ['GET'])
def showLeaderBoard():
    name = ekn.match(request.args.get('name')).group()
    DbMan = DbManager.DbManager()
    tmp = DbMan.getMTNSAll()
    DbMan.closeDb()
    tmp.sort(key = lambda x:-x[2])
    prev = -1
    prevPlace = -1
    for i in range(len(tmp)):
        tmp[i] = (tmp[i], (prevPlace if prev == tmp[i][2] else i+1),)
        prev = tmp[i][0][2]
        prevPlace = tmp[i][1]
    return render_template('leaderboard.html', scores=tmp, name=name, n = len(tmp), yourId=session['uid'])

@app.route('/image', methods = ['GET'])
def showImage():
    name = ekn.match(request.args.get('name')).group()
    originalName = ekn.match(request.args.get('originalName')).group()
    time = request.args.get('time')
    score = float(request.args.get('score'))
    rank = int(request.args.get('rank'))
    DbMan = DbManager.DbManager()
    _, _, _, mCellCnt, frame, delayedTime = DbMan.getMRawInfo(name)
    return render_template('image.html', targetName = name, originalName=originalName, time=time, score=score, rank=rank, imgName=f'image/{name}.jpg', mCellCnt=mCellCnt, frame=frame, delayedTime=delayedTime, yourId=session['uid'])

@app.route('/imageScore', methods = ['GET'])
def showImageScore():
    name = ekn.match(request.args.get('name')).group()
    gid = ekn.match(request.args.get('gid')).group()
    originalName = ekn.match(request.args.get('originalName')).group()
    time = request.args.get('time')
    score = float(request.args.get('score'))
    rank = int(request.args.get('rank'))
    DbMan = DbManager.DbManager()
    _, _, _, mCellCnt, frame, delayedTime = DbMan.getLRawInfo(name)
    return render_template('image_score.html', targetName = name, originalName=originalName, time=time, score=score, rank=rank, imgName=f'image/{name}_last.jpg', mCellCnt=mCellCnt, frame=frame, delayedTime=delayedTime, gid=gid, yourId=session['uid'])

if __name__ == "__main__":
    import setup
    #setup.setup()
    app.run(host='0.0.0.0', port = 80)