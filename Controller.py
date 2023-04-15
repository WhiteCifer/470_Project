import pygame
import Model
from View import view as v

class GameController:
    def __init__(self):
        self.window = Model.Window(1000,1600)
        self.saved = Model.SavedGames()
        self.view = v(self.window.height, self.window.width)
        self.pMovement = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.window.setState(False)
            elif event.type == pygame.KEYDOWN:
                if self.view.game == False:
                    if self.view.cur == 0: #Main Menu
                        if event.key == pygame.K_UP or event.key==pygame.K_DOWN:
                            self.view.menu_option = self.options(event.key, self.view.menu, self.view.menu_option)
                        elif event.key == pygame.K_RETURN:
                           if self.view.menu_option == 4:
                               pygame.quit()
                               self.window.setState(False)
                           else:
                               self.view.cur = (self.view.menu_option + 1) % 5
                    elif self.view.cur == 1: #Campaign
                        if event.key == pygame.K_UP or event.key==pygame.K_DOWN:
                            self.view.campaign_options = self.options(event.key, self.view.campaign, self.view.campaign_options)
                        elif event.key == pygame.K_RETURN:
                            if self.view.campaign_options == 0: #New Game
                                self.view.game = True
                                self.view.cur = 0
                            elif self.view.campaign_options == 1: #load game
                                self.view.game = True
                                self.view.cur = 4
                                self.view.data = Model.SavedGames.loadGame(Model.SavedGames.getSaved())
                            elif self.view.campaign_options == 2: #main menu
                                self.view.cur = 0
                    elif self.view.cur == 2: #Quick Play
                        if event.key == pygame.K_UP or event.key==pygame.K_DOWN:
                            self.view.quickplay_options = self.options(event.key, self.view.quickplay, self.view.quickplay_options)
                        elif event.key == pygame.K_RETURN:
                            if self.view.quickplay_options == 0: #Single Instance
                                self.view.game = True
                                self.view.cur = 0
                            elif self.view.quickplay_options == 1: #Time Attack
                                self.view.game = True
                                self.view.cur = 2
                            elif self.view.quickplay_options == 2: #main menu
                                self.view.cur = 0
                    elif self.view.cur == 4:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                            self.view.cur = 0
                    elif self.view.cur == 3: #Settings
                        if event.key == pygame.K_UP or event.key==pygame.K_DOWN:
                            self.view.settings_option = self.options(event.key, self.view.settings, self.view.settings_option)
                        elif event.key == pygame.K_RETURN:
                            #self.view.cur = (self.view.settings_option+1) % 4
                            pass

                elif self.view.game == True:
                    if self.view.cur == 0:
                        if event.key == pygame.K_ESCAPE:
                            self.view.cur = 5
                        else:
                            self.player_movement(event.key)
                            if self.collisionCheck() or self.goal():
                                self.view.cur = 1

                    elif self.view.cur == 1:
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            self.view.gameover_options = self.options(event.key, self.view.gameover,self.view.gameover_options)
                        elif event.key == pygame.K_RETURN:
                            Model.Leaderboard.setScore("Hasin",self.view.score)
                            self.view.cur = 0
                            self.view.score = 0
                            self.view.setPlayer()
                            if self.view.gameover_options == 0:  # Retry
                                pass
                            elif self.view.gameover_options == 1:  # New Game
                                self.view.obstacles_list = []
                                self.view.generated = False
                            elif self.view.gameover_options == 2:  # Main Menu
                                self.view.game = False
                                self.view.obstacles_list = []
                                self.view.generated = False
                    elif self.view.cur == 4:
                        if event.key == pygame.K_ESCAPE:
                            self.view.cur = 5
                        else:
                            self.player_movement(event.key)
                            if self.collisionCheck() or self.goal():
                                self.view.cur = 1
                    elif self.view.cur == 5:
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            self.view.continue1_options = self.options(event.key, self.view.continue1_game,self.view.continue1_options)
                        elif event.key == pygame.K_RETURN:
                            if self.view.continue1_options == 0:  # continue
                                self.view.cur = 0
                            elif self.view.continue1_options == 1: # Save
                                Model.SavedGames.saveGame(self.view.obstacles_list,self.view.score)
                                self.view.cur = 0
                            elif self.view.continue1_options == 2:
                                self.view.cur = 0
                                self.view.score = 0
                                self.view.setPlayer()
                                self.view.game = False
                                self.view.obstacles_list = []
                                self.view.generated = False
    def player_movement(self,key):
        if key == pygame.K_UP:
            self.view.pY -= 10
            self.view.score += 10
        elif key == pygame.K_DOWN:
            self.view.pY += 10
            self.view.score += 10
        elif key == pygame.K_LEFT:
            self.view.pX -= 10
            self.view.score += 10
        elif key == pygame.K_RIGHT:
            self.view.pX += 10
            self.view.score += 10



    def options(self, key, type, options):
        if key == pygame.K_UP:
            options = (options - 1) % len(type)
        elif key == pygame.K_DOWN:
            options = (options + 1) % len(type)
        return options

    def goal(self):
        return self.view.pX+20>=self.view.wWidth


    def collisionCheck(self):
        for x in self.view.obstacles_list:
            if x[0] == 'rottenApple' and (self.view.pX+20 in range(x[2][0],x[2][0]+50) and self.view.pY+20 in range(x[2][1], x[2][1]+50)):
                return True
            elif x[0] == 'plastic' and (self.view.pX+20 in range(x[2][0],x[2][0]+75) and self.view.pY+20 in range(x[2][1], x[2][1]+250)):
                return True
            elif x[0] == 'scrap' and (self.view.pX+20 in range(x[2][0],x[2][0]+20) and self.view.pY+20 in range(x[2][1], x[2][1]+20)):
                return True
            elif x[0] == 'medium_scrap' and (self.view.pX+20 in range(x[2][0],x[2][0]+100) and self.view.pY+20 in range(x[2][1], x[2][1]+100)):
                return True
            elif x[0] == 'large_scrap' and (self.view.pX+20 in range(x[2][0],x[2][0]+250) and self.view.pY+20 in range(x[2][1],x[2][1]+250)):
                return True
        return False

