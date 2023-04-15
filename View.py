import pygame
import random

import Model
from Model import Background, Obstacle, Player, Leaderboard

class view:
    def __init__(self, x, y):
        self.wWidth = x
        self.wHeight = y
        self.obstacles = Obstacle().getObjects()
        self.obstacles_list = []
        self.generated = False
        self.leaderboard = Leaderboard()
        p = Player()
        self.player = pygame.transform.scale(pygame.image.load(p.get_player_location()), p.get_player_size())
        self.setPlayer()
        pygame.init()
        self.screen = pygame.display.set_mode((self.wWidth, self.wHeight))
        self.bg = pygame.transform.scale(pygame.image.load(Background().getBackground()), (self.wWidth,self.wHeight))
        pygame.display.set_caption("Reborn As an Earthworm")
        self.font1 = pygame.font.SysFont(None, 50)
        self.font2 = pygame.font.SysFont(None, 100)
        self.data = None
        self.settingsObj = Model.Settings()
        pygame.mixer.init()
        pygame.mixer.music.load('audio/game.wav')
        pygame.mixer.music.play()
        self.menu = ["Campaign", "Quick Play", "Settings", "Highscores", "Exit"] #cur = 0
        self.menu_option = 0
        self.continue1_game = ["Continue", "Save Game", "Back to Main Menu"]
        self.continue1_options = 0
        self.campaign = ["New Game", "Load Game", "Back to Main Menu"] #cur = 1
        self.campaign_options = 0
        self.quickplay = ["Single Instance", "Time Attack", "Back to Main Menu"] #cur = 2
        self.quickplay_options = 0
        self.settings = ["Sound", "Music", "Window Size", "Back to Main Menu"] #cur = 3
        self.settings_option = 0
        self.loadgame = ["Sound", "Music", "Window Size", "Back to Main Menu"] #cur = 4
        self.load_option = 0
        self.gameover = ["Retry", "New Game", "Back to Main Menu"]  # cur = 4
        self.gameover_options = 0
        self.score = 0
        self.game = False
        self.cur = 0

    def setPlayer(self):
        self.pX, self.pY = self.wWidth * 0.01, self.wHeight * 0.5
    def render_base(self,type,options):
        title = self.font2.render("Reborn As an Earthworm", True, (255,255,255))
        title_rect = title.get_rect(center=(self.wWidth / 2, self.wHeight / 2 - 200))
        self.screen.blit(title, title_rect)
        for i, option in enumerate(type):
            if i == options:
                text = self.font1.render(option, True, (0, 0, 0))
            else:
                text = self.font1.render(option, True, (50, 50, 50))
            text_rect = text.get_rect(center=(self.wWidth / 2, self.wHeight / 2 + i * 50))
            self.screen.blit(text, text_rect)

    def render_gameover(self):
        gameover = self.font2.render("GAME OVER", True, (255, 0, 0))
        score = self.font1.render(f"Your score this run:{self.score}", True, (255,255,255))
        gameover_rect = gameover.get_rect(center=(self.wWidth / 2, self.wHeight / 2 - 200))
        score_rect = score.get_rect(center=(self.wWidth / 2, self.wHeight / 2 - 50))
        self.screen.blit(gameover, gameover_rect)
        self.screen.blit(score, score_rect)
        for i, option in enumerate(self.gameover):
            if i == self.gameover_options:
                text = self.font1.render(option, True, (0, 0, 0))
            else:
                text = self.font1.render(option, True, (50, 50, 50))
            text_rect = text.get_rect(center=(self.wWidth / 2, self.wHeight / 2 + i * 50))
            self.screen.blit(text, text_rect)
    def render_highscore(self):
        i = 30
        column_space = 500
        head1 = self.font1.render(f'PLAYER', True, (3, 255, 112))
        head2 = self.font1.render(f'SCORE', True, (3, 255, 112))
        h1_rect = head1.get_rect(center=([self.wWidth / 3, (700 / 4) + 5]))
        h2_rect = head2.get_rect(center=([(self.wWidth / 3) + column_space + 50, (700 / 4) + 5]))
        self.screen.blit(head1, h1_rect)
        self.screen.blit(head2, h2_rect)
        rows = self.leaderboard.getScoreBoard()
        for row in rows:
            column1 = self.font1.render('{:>3}'.format(row[0]), True, (3, 255, 112))
            column2 = self.font1.render('{}'.format(row[1]), True, (3, 255, 112))
            c1_rect = column1.get_rect(center=([self.wWidth / 3, (700 / 4) + i + 5]))
            c2_rect = column2.get_rect(center=([(self.wWidth / 3) + column_space + 50, (700 / 4) + i + 5]))
            self.screen.blit(column1, c1_rect)
            self.screen.blit(column2, c2_rect)
            i += 30
        text = self.font1.render("Back to main menu", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.wWidth / 2, self.wHeight / 2 + i+30))
        self.screen.blit(text, text_rect)

    def updateWindow(self, width, height):
        self.wWidth = width
        self.wHeight = height
        self.screen = pygame.display.set_mode((self.wWidth, self.wHeight))

    def update_display(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.bg, (0, 0))
        if self.game == False:
            if self.cur == 0:
                self.render_base(self.menu,self.menu_option)
            elif self.cur == 1:
                self.render_base(self.campaign,self.campaign_options)
            elif self.cur == 2:
                self.render_base(self.quickplay,self.quickplay_options)
            elif self.cur == 4:
                self.render_highscore()
            elif self.cur == 3:
                self.render_base(self.settings,self.settings_option)
        elif self.game:
            if self.cur == 0:
                self.draw_instance()
            elif self.cur == 1:
                self.render_gameover()
            elif self.cur == 4:
                self.draw_instance()
            elif self.cur == 5:
                self.render_base(self.continue1_game, self.continue1_options)
        pygame.display.update()
        # code to update the display with current game state

    def new_time_attack(self):
        pass

    def draw_instance(self):
        score = self.font2.render(f"SCORE:{self.score}", True, (255,255,255))
        self.screen.blit(score, (0,0))
        self.screen.blit(self.player, (self.pX, self.pY))
        if self.cur == 0:
            if not self.generated:
                self.generateRandomObjects()
                self.generated = True
            else:
                for obj in self.obstacles_list:
                    self.screen.blit(obj[1], obj[2])
        else:
            if not self.generated:
                self.loadPreviousInstance()
                self.generated = True
            else:
                for obj in self.obstacles_list:
                    self.screen.blit(obj[1], obj[2])


    def generateRandomObjects(self):
        tempList=[]
        for x in self.obstacles:
            temp = pygame.transform.scale(pygame.image.load(x[1]), tuple(int(i) for i in x[2].split('x')))
            tempList.append((x[0],temp))
        c = 0
        while c!=5:
            if tempList[c][0] == 'rottenApple':
                limit = 3
                for x in range(limit):
                    loc = (random.randint(100,1400),random.randint(100,900))
                    self.obstacles_list.append((tempList[c][0],tempList[c][1],loc))
                    self.screen.blit(tempList[c][1], loc)
                c+=1
            elif tempList[c][0] == 'plastic':
                limit = 1
                for x in range(limit):
                    loc = (random.randint(100,1000),random.randint(100,900))
                    self.obstacles_list.append((tempList[c][0],tempList[c][1],loc))
                    self.screen.blit(tempList[c][1], loc)
                c+=1
            elif tempList[c][0] == 'scrap':
                limit = 3
                for x in range(limit):
                    loc = (random.randint(100,1000),random.randint(100,900))
                    self.obstacles_list.append((tempList[c][0],tempList[c][1],loc))
                    self.screen.blit(tempList[c][1], loc)
                c+=1
            elif tempList[c][0] == 'medium_scrap':
                limit = 2
                for x in range(limit):
                    loc = (random.randint(100,1000),random.randint(100,900))
                    self.obstacles_list.append((tempList[c][0],tempList[c][1],loc))
                    self.screen.blit(tempList[c][1], loc)
                c+=1
            elif tempList[c][0] == 'large_scrap':
                limit = 1
                for x in range(limit):
                    loc = (random.randint(100,1000),random.randint(100,900))
                    self.obstacles_list.append((tempList[c][0],tempList[c][1],loc))
                    self.screen.blit(tempList[c][1], loc)
                c+=1

    def loadPreviousInstance(self):
        tempList = []
        for x in self.obstacles:
            temp = pygame.transform.scale(pygame.image.load(x[1]), tuple(int(i) for i in x[2].split('x')))
            tempList.append((x[0], temp))
        self.score = int(self.data[0])
        for x in range(1,len(self.data)-1):
            n,d = self.data[x].split(',')
            if n == 'rottenApple':
                loc = tuple(int(i) for i in d.split('x'))
                self.obstacles_list.append((tempList[1][0], tempList[1][1], loc))
                self.screen.blit(tempList[1][1], loc)
            elif n == 'plastic':
                loc = tuple(int(i) for i in d.split('x'))
                self.obstacles_list.append((tempList[0][0], tempList[0][1], loc))
                self.screen.blit(tempList[0][1], loc)
            elif n == 'scrap':
                loc = tuple(int(i) for i in d.split('x'))
                self.obstacles_list.append((tempList[2][0], tempList[2][1], loc))
                self.screen.blit(tempList[2][1], loc)
            elif n == 'medium_scrap':
                loc = tuple(int(i) for i in d.split('x'))
                self.obstacles_list.append((tempList[3][0], tempList[3][1], loc))
                self.screen.blit(tempList[3][1], loc)
            elif n == 'large_scrap':
                loc = tuple(int(i) for i in d.split('x'))
                self.obstacles_list.append((tempList[4][0], tempList[4][1], loc))
                self.screen.blit(tempList[4][1], loc)

