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

class UserManager:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('User.db')
        self.c = self.conn.cursor()

    def makeDb(self) -> None:
        query = """
        CREATE TABLE "Users" (
        	"ID"	TEXT,
        	"PW"	TEXT NOT NULL,
        	"Salt"	TEXT NOT NULL,
        	"NickName"	TEXT NOT NULL,
        	"Name"	TEXT NOT NULL,
        	"StudentId"	TEXT NOT NULL UNIQUE,
        	"ShowNS"	INTEGER NOT NULL,
        	"MaxScore"	REAL DEFAULT 0,
        	PRIMARY KEY("ID")
        );
        """
        self.c.execute(query)
        self.conn.commit()

    def deleteAll(self) -> None:
        query = "DROP TABLE Users"
        self.c.execute(query)
        self.conn.commit()
    
    def deleteUser(self, uid:str) -> None:
        query = f'DELETE FROM Users WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()

    def uploadUser(self, uid:str, pw:str, salt:str, nickName:str, name:str, studentId:int, showNS:int, MaxScore:float=0) -> None:
        query = f'INSERT INTO Users (ID, PW, Salt, NickName, Name, StudentId, ShowNS, MaxScore) VALUES ("{uid}", "{pw}", "{salt}", "{nickName}", "{name}", {studentId}, {showNS}, {MaxScore})'
        self.c.execute(query)
        self.conn.commit()

    def updatePw(self, uid:str, pw:str) -> None:
        query = f'UPDATE Users SET PW = "{pw}" WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit(query)

    def updateNickName(self, uid:str, nickname:str) -> None:
        query = f'UPDATE Users SET NickName = "{nickname}" WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()

    def updateStudentId(self, uid:str, studentId:int) -> None:
        query = f'UPDATE Users SET StudentId = {studentId} WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()

    def updateMaxScore(self, uid:str, score:float) -> None:
        query = f'UPDATE Users SET MaxScore = {score} WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()

    def getPw(self, uid:str) -> str:
        query = f'SELECT PW FROM Users WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()[0]

    def getSalt(self, uid:str) -> str:
        query = f'SELECT Salt FROM Users WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()[0]

    def getInfo(self, uid:str) -> typing.Tuple:
        query = f'SELECT * FROM Users WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def getNNameMScoreAll(self) -> typing.List:
        query = 'SELECT NickName, MaxScore FROM Users'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchall()
    
    def closeDb(self) -> None:
        self.conn.commit()
        self.c.close()
        self.conn.close()

class GameManger:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('Games.db')
        self.c = self.conn.cursor()

    def makeDb(self)-> None:
        query = """
        CREATE TABLE "Games" (
        	"Gid"	TEXT,
        	"Players"	TEXT,
        	"MadeTime"	TEXT,
        	PRIMARY KEY("Gid")
        );
        """
        self.c.execute(query)
        self.conn.commit()

    def deleteAll(self) -> None:
        query = "DROP TABLE Games"
        self.c.execute(query)
        self.conn.commit()

    def deleteGame(self, gid:str) -> None:
        query = f'DELETE FROM Games WHERE Gid = "{gid}"'
        self.c.execute(query)
        self.conn.commit()

    def uploadGame(self, gid:str, players:str, time:str) -> None:
        query = f'INSERT INTO Games (Gid, Players, MadeTime) VALUES ("{gid}", "{players}", "{time}"'
        self.c.execute(query)
        self.conn.commit()
    
    def getInfo(self, gid:str) -> typing.Tuple:
        query = f'SELECT * FROM Games WHERE Gid = "{gid}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()
    
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