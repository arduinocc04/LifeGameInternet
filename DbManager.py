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
	        "Name"	TEXT,
	        "MTime"	TEXT,
            "LTime" TEXT,
	        "MScore"	REAL,
	        "MMaxCellCnt"	INTEGER,
	        "MFrame"	INTEGER,
	        "MDelayedTime"	REAL,
	        "LScore"	REAL,
	        "LMaxCellCnt"	INTEGER,
	        "LFrame"	INTEGER,
	        "LDelayedTime"	REAL,
	        PRIMARY KEY("Name")
        );"""
        self.c.execute(query)
        self.conn.commit()

    def deleteAll(self) -> None:
        query = "DROP TABLE Scores"
        self.c.execute(query)
        self.conn.commit()

    def uploadScore(self, time:str, name:str, score:float, mCellCnt:int, frame:int, delayedTime:float) -> None:
        query = f'INSERT INTO Scores (Name, MTime, LTime, MScore, MMaxCellCnt, MFrame, MDelayedTime, LScore, LMaxCellCnt, LFrame, LDelayedTime) VALUES ("{name}", "{time}", "{time}",{score}, {mCellCnt}, {frame}, {delayedTime}, {score}, {mCellCnt}, {frame}, {delayedTime})'
        self.c.execute(query)
        self.conn.commit()

    def updateMScore(self, time:str, name:str, score:float, mCellCnt:int, frame:int, delayedTime:float) -> None:
        query = f'UPDATE Scores SET MScore = {score}, MTime = "{time}", MMaxCellCnt = {mCellCnt}, MFrame = {frame}, MDelayedTime = {delayedTime} WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()

    def updateLScore(self, time:str, name:str, score:float, mCellCnt:int, frame:int, delayedTime:float) -> None:
        query = f'UPDATE Scores SET LScore = {score}, LTime = "{time}", LMaxCellCnt = {mCellCnt}, LFrame = {frame}, LDelayedTime = {delayedTime} WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()

    def getMTNSAll(self) -> typing.List:
        query = 'SELECT MTime, Name, MScore FROM Scores'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchall()

    def getMScoreByName(self, name:str) -> float:
        query = f'SELECT MScore FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        try: return self.c.fetchone()[0]
        except TypeError: return None
    
    def getMTNS(self, name:str) -> typing.Tuple:
        query = f'SELECT MTime, Name, MScore FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def getLTNSAll(self) -> typing.List:
        query = 'SELECT LTime, Name, LScore FROM Scores'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchall()

    def getLScoreByName(self, name:str) -> float:
        query = f'SELECT LScore FROL Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        try: return self.c.fetchone()[0]
        except TypeError: return None
    
    def getLTNS(self, name:str) -> typing.Tuple:
        query = f'SELECT LTime, Name, LScore FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def getMRawInfo(self, name:str) -> typing.Tuple:
        query = f'SELECT Name, MTime, Mscore, MMaxCellCnt, MFrame, MDelayedTime FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def getLRawInfo(self, name:str) -> typing.Tuple:
        query = f'SELECT Name, LTime, Lscore, LMaxCellCnt, LFrame, LDelayedTime FROM Scores WHERE Name = "{name}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def getInfo(self, name:str) -> typing.Tuple:
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
        	"Name"	TEXT NOT NULL,
        	"StudentId"	TEXT NOT NULL UNIQUE,
        	"ShowNS"	INTEGER NOT NULL,
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

    def uploadUser(self, uid:str, pw:str, salt:str, name:str, studentId:int, showNS:int) -> None:
        query = f'INSERT INTO Users (ID, PW, Salt, Name, StudentId, ShowNS) VALUES ("{uid}", "{pw}", "{salt}", "{name}", {studentId}, {showNS})'
        self.c.execute(query)
        self.conn.commit()

    def updatePw(self, uid:str, pw:str) -> None:
        query = f'UPDATE Users SET PW = "{pw}" WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit(query)

    def updateStudentId(self, uid:str, studentId:int) -> None:
        query = f'UPDATE Users SET StudentId = {studentId} WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()

    def getPw(self, uid:str) -> str:
        query = f'SELECT PW FROM Users WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()
        try: return self.c.fetchone()[0]
        except TypeError: return None

    def getSalt(self, uid:str) -> str:
        query = f'SELECT Salt FROM Users WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()
        try: return self.c.fetchone()[0]
        except TypeError: return None

    def getInfo(self, uid:str) -> typing.Tuple:
        query = f'SELECT * FROM Users WHERE ID = "{uid}"'
        self.c.execute(query)
        self.conn.commit()
        return self.c.fetchone()

    def closeDb(self) -> None:
        self.conn.commit()
        self.c.close()
        self.conn.close()

class GameManger:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('Game.db')
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
        query = f'INSERT INTO Games (Gid, Players, MadeTime) VALUES ("{gid}", "{players}", "{time}")'
        self.c.execute(query)
        self.conn.commit()

    def appendPlayer(self, gid:str, player:str) -> None:
        _, pre, _ = self.getInfo(gid)
        if pre == "": query = f'UPDATE Games SET players = "{player}" WHERE Gid = "{gid}"'
        else: query = f'UPDATE Games SET players = "{pre},{player}" WHERE Gid = "{gid}"'
        self.c.execute(query)
        self.conn.commit()
    
    def getInfo(self, gid:str) -> typing.Tuple:
        query = f'SELECT * FROM Games WHERE Gid = "{gid}"'
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