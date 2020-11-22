import os
import DbManager
import random
import string
import shutil
def setup():
    if(os.path.isdir('./static/image')): shutil.rmtree('./static/image')
    os.mkdir('./static/image')
    cmd = int(input("Del Score Db? yes->1 no->0 >>>"))
    if cmd == 1:
        if(os.path.isfile('./Data.db')): os.remove('./Data.db')
        DbMan = DbManager.DbManager()
        DbMan.makeDb()
        DbMan.closeDb()
    cmd = int(input("Del User Db? yes ->1 no ->0 >>>"))
    if cmd == 1:
        if(os.path.isfile('./User.db')): os.remove('./User.db')
        DbMan = DbManager.UserManager()
        DbMan.makeDb()
        DbMan.closeDb()
    cmd = int(input("Del Game Db? yes ->1 no ->0 >>>"))
    if cmd == 1:
        if(os.path.isfile('./Game.db')): os.remove('./Game.db')
        DbMan = DbManager.GameManger()
        DbMan.makeDb()
        DbMan.closeDb()

    tmp = ''
    tmp2 = ''
    for _ in range(10):
        tmp += random.choice(string.ascii_letters)
        tmp2 += random.choice(string.ascii_letters)
    with open('secret.txt', 'w', encoding='utf8') as f:
        f.write(tmp + '\n')
        f.write(tmp2 + '\n')

if __name__ == '__main__':
    setup()