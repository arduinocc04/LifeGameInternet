import sqlite3
from time import ctime
import typing
class DbManager:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('Data.db')
        self.c = self.conn.cursor()

    def makeDb(self) -> None:
        query = """
        CREATE TABLE "Scores" (
	        "Time"	TEXT,
	        "Name"	TEXT,
	        "Score"	REAL,
	        "MaxCellCnt"	INTEGER,
	        "Frame"	INTEGER,
	        "DelayedTime"	REAL,
	        PRIMARY KEY("Name")
        );"""
        self.c.execute(query)
        self.conn.commit()

    def deleteAll(self) -> None:
        query = "DROP TABLE Scores"
        self.c.execute(query)
        self.conn.commit()

    def uploadScore(self, time:str, name:str, score:float, mCellCnt:int, frame:int, delayedTime:float) -> None:
        query = f'INSERT INTO Scores (Time, Name, Score, MaxCellCnt, Frame, DelayedTime) VALUES ("{time}", "{name}", {score}, {mCellCnt}, {frame}, {delayedTime})'
        self.c.execute(query)
        self.conn.commit()

    def updateScore(self, time:str, name:str, score:float, mCellCnt:int, frame:int, delayedTime:float) -> None:
        query = f'UPDATE Scores SET Score = {score}, Time = "{time}", MaxCellCnt = {mCellCnt}, Frame = {frame}, DelayedTime = {delayedTime} WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()

    def getTNSAll(self) -> typing.List:
        query = 'SELECT Time, Name, Score FROM Scores'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchall()

    def getScoreByName(self, name:str) -> float:
        query = f'SELECT Score FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()[0]
    
    def getTNS(self, name:str) -> typing.Tuple:
        query = f'SELECT Time, Name, Score FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def getRawInfo(self, name:str) -> typing.Tuple:
        query = f'SELECT * FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def closeDb(self) -> None:
        self.conn.commit()
        self.c.close()
        self.conn.close()

if __name__ == '__main__':
    import time
    a = DbManager()
    TIMESTAMP = ctime(time.time())
    #a.uploadScore(TIMESTAMP, 'Daniel Cho', 1e9)
    #print(a.getTNS())
    #print(a.readInfo('조다니엘'))
    #print(a.getScoreByName('조다니엘'))
    #print(a.getScoreByName('10222 조다니엘'))
    #a.updateScore(TIMESTAMP, '10222 조다니엘', 0)
    #print(a.getScoreByName('10222 조다니엘'))
    a.deleteAll()
    a.makeDb()
    a.closeDb()