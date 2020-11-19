from flask import Flask, render_template, request, redirect, url_for
import DbManager
import ntplib
import sqlite3
from time import ctime
import base64
app = Flask(__name__)

@app.route('/')
def main():
    return redirect('game')

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
    now = ctime(cli.request("kr.pool.ntp.org").tx_time + 32400000)

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
    return redirect(url_for('showScoreBoard', name=name))

@app.route('/scoreboard', methods = ['GET'])
def showScoreBoard():
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
    return render_template('scoreboard.html', scores=tmp, name=name, n = len(tmp))

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
    app.run(host='0.0.0.0', port = 8000)
