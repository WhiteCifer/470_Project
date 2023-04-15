from dbconnect import cursor, mydb
import datetime


class Window:
    def __init__(self,x,y):
        self.width = x
        self.height = y
        self.running = True

    def getDimensions(self):
        return self.width, self.height
    def setDimensions(self,x,y):
        self.height = x
        self.width = y
    def getState(self):
        return self.running
    def setState(self, bl):
        self.running = bl


class Player:
    def __init__(self):
        self.pLoc = "image/player/worm.png"
        self.size = (50,50)

    def get_player_location(self):
        return self.pLoc

    def get_player_size(self):
        return self.size

class Obstacle:
    def __init__(self):
        cursor.execute('select name,directory,dimensions from obstacles')
        self.objects = []
        for x in cursor.fetchall():
            self.objects.append(x)

    def getObjects(self):
        return self.objects

class Background:
    def __init__(self):
        self.bLoc = 'image/background/bg.jpg'
    def getBackground(self):
        return self.bLoc

class SavedGames:
    @staticmethod
    def saveGame(lst,score):
        date = datetime.datetime.now()
        dbDate = date.strftime('%Y-%m-%d %H:%M:%S')
        insDate = date.strftime('%Y-%m-%d %H-%M-%S')
        loc = f"instances/{str(insDate)}.txt"
        f = open(loc, 'x')
        f.write(f"{score}\n")
        for x in range(len(lst)):
            f.write(f"{str(lst[x][0])}, {str(lst[x][2][0])}x{str(lst[x][2][1])}\n")
        f.close()
        sql = 'insert into savedgames(loc, Date) values(%s,%s)'
        val = (loc,dbDate)
        cursor.execute(sql, val)
        mydb.commit()
    @staticmethod
    def getSaved():
        cursor.execute('select loc from savedgames order by Date asc limit 5')
        return [x for x in cursor]
    @staticmethod
    def loadGame(loc):
        f = open(loc[-1][0], 'r')
        lst = f.read().split('\n')
        return lst

class Settings:
    def __init__(self):
        self.sound = True
        self.music = True
        self.window_options = [(1000,1600), (800,1200), (700,1000)]
        self.window_current = 0

    def getSound(self):
        return self.sound

    def getMusic(self):
        return self.music

    def getWindowOptions(self):
        return self.window_options

    def getWindow(self):
        return self.window_options[self.window_current]

    def setSound(self):
        self.sound = not self.sound

    def setMusic(self):
        self.music = not self.music

    def setWindow(self,x):
        self.window_current = x

class Leaderboard:
    @staticmethod
    def getScoreBoard():
        cursor.execute('select * from leaderboard order by score desc')
        return cursor.fetchall()

    @staticmethod
    def getTenthScore():
        cursor.execute(
            'select score from (select * from leaderboard order by score asc) as temp order by score desc limit 1')
        return cursor.fetchall()
    @staticmethod
    def setScore(name, score):
        current = datetime.datetime.now()
        date = current.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'insert into leaderboard(name, score, Date) values(%s,%s,%s)'
        values = (name, score, date)
        cursor.execute(sql, values)
        mydb.commit()