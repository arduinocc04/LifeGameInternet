import os
import DbManager

if __name__ == '__main__':
    os.mkdir('./static/image')
    if(os.path.isfile('./Data.db')):
        os.remove('./Data.db')
    DbMan = DbManager()
    DbMan.makeDb()
    DbMan.closeDb()