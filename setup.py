import os
import DbManager

if __name__ == '__main__':
    if(not os.path.isdir('./static/image')): os.mkdir('./static/image')
    if(os.path.isfile('./Data.db')): os.remove('./Data.db')
    DbMan = DbManager.DbManager()
    DbMan.makeDb()
    DbMan.closeDb()