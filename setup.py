import os
import DbManager

if __name__ == '__main__':
    if(not os.path.isdir('./static/image')): os.mkdir('./static/image')
    cmd = int(input("Del Score Db? yes->1 no->0"))
    if cmd == 1:
        if(os.path.isfile('./Data.db')): os.remove('./Data.db')
        DbMan = DbManager.DbManager()
        DbMan.makeDb()
        DbMan.closeDb()
    cmd = int(input("Del User Db? yes ->1 no ->0"))
    if cmd == 1:
        if(os.path.isfile('./User.db')): os.remove('./User.db')
        DbMan = DbManager.UserManager()
        DbMan.makeDb()
        DbMan.closeDb()