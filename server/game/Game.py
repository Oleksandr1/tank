#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys, os, pygame
from pygame import *
from Windows import *
from Level import *
from Tank import *
from twisted.internet import reactor

from netgame.connection import ClientConnection, ClientConnFactory
#****************************ID процессов игры

#(MENU,NEW_GAME,CONTINUE,RESULTS,OPTIONS,EXIT)=(1,2,3,4,5,6)
HOST = 'localhost'
PORT = 3113


class Game():
    def __init__(self):
        print "INIT GAME"
    #**************************** основное window
        self.win_width = 1024#Ширина создаваемого окна
        self.win_height = 700# Высота
        self.win_display = (self.win_width,self.win_height)# Группируем ширину и высоту в одну переменную
        self.timer = pygame.time.Clock()
        self.online = True
    #**************************** инициализация

        self.left = self.right = self.up = self.down = self.space = False
        self.exit_ = True# флаг для выхода
        self.windows = Windows()# инициализируем Windows
        self.player = Player((100,100))# инициализируем Tank
        #self.bul = self.player.shot_bull()
        self.level1 = Level('level1.txt')#Инициализируем level1
        self.level1.load_level()
        self.platforms = self.level1.ret_tiles()

#******************************* свойства для сетевого взаимодействия
        self.id = None
        self.data = {}
        self.data['type'] = 'game'
        self.data['shoot'] = False
        self.move_coord = (0,0,0,0)
        self.stop_coord = (0,0,0,0)

    #**************************** блоки спрайтов

        self.block_list = pygame.sprite.Group() #Это список спрайтов. Каждый блок добавляется в этот список.
        self.all_sprites_list = pygame.sprite.Group()# # Это список каждого спрайта. Все блоки, а также блок игрока.
        self.bullet_list = pygame.sprite.Group()#тес массив спрайтов пули

        self.block_list.add(self.platforms)
        self.all_sprites_list.add(self.player)

        self.cf = ClientConnFactory(self)
        reactor.connectTCP(HOST,PORT,self.cf)
        reactor.run()
    #****************************инициализируем pygame (получаем screen)
    def init_window(self):
        pygame.init()#инициализируем pygame
        self.screen = pygame.display.set_mode(self.win_display)# Создаем окошко
        pygame.display.set_caption('Tanks')#название шапки "капчи"

    #****************************обработка процессов и действий (обработка нажатий (mouse and keyboard и др.))
    def tick(self):
        self.timer.tick(60)
    #****************************обработка
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.left = True

                #self.sendData("left = True")
                self.data['coordinate'] = (1,0,0,0)
                self.sendData(self.data)
            if event.type == KEYUP and event.key == K_LEFT:
                self.left = False
                self.data['coordinate'] = self.stop_coord
                self.sendData(self.data)

            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.right = True
                #self.sendData('self.right = True')
                self.data['coordinate'] = (0,1,0,0)
                self.sendData(self.data)

            if event.type == KEYUP and event.key == K_RIGHT:
                self.right = False
                #self.sendData('self.right = False')
                self.data['coordinate'] = self.stop_coord
                self.sendData(self.data)


            if event.type == KEYDOWN and event.key == K_UP:
                self.up = True
                #self.sendData('self.up = True')
                self.data['coordinate'] = (0,0,1,0)
                self.sendData(self.data)

            if event.type == KEYUP and event.key == K_UP:
                self.up = False
                #self.sendData('self.up = False')
                self.data['coordinate'] = self.stop_coord
                self.sendData(self.data)


            if event.type == KEYDOWN and event.key == K_DOWN:
                self.down = True
                self.data['coordinate'] = (0,0,0,1)
                self.sendData(self.data)

                #self.sendData('self.down = True')
            if event.type == KEYUP and event.key == K_DOWN:
                self.down = False
                #self.sendData('self.down = False')
                self.data['coordinate'] = self.stop_coord
                self.sendData(self.data)


            if event.type == KEYDOWN and event.key == K_SPACE:
                self.space = True
                #self.sendData('self.space = True')
                self.data['shoot'] = True
                self.sendData(self.data)
            if event.type == KEYUP and event.key == K_SPACE:
                self.shot_bull_game()
                self.space = False
                self.data['shoot'] = False
                self.sendData(self.data)

            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.sendData("GOODBYE!!!!!!!")
                reactor.stop()
                sys.exit(0)

        self.draw_game()
        self.update_game()


    #****************************отобрыжение процессов
    def draw_game(self):
        self.windows.draw_windows(self.screen)#рисуем окна
        self.all_sprites_list.draw(self.screen)
        self.block_list.draw(self.screen)
        self.bullet_list.draw(self.screen)
        pygame.display.update()# обновление и вывод всех изменений на экран

    #****************************shot
    def shot_bull_game(self):
        self.player.shot_bull()
        self.bullet_list.add(self.player.ret_bull())

    #**************************** при столкновении пули с объектом удаление пули
    def destroy_bull_game(self):

        sprite.groupcollide(self.block_list,self.bullet_list,0,1)

    #**************************** update
    def update_game(self):
        self.player.tank_update(self.left,self.right,self.up,self.down,self.space,self.platforms)
        self.destroy_bull_game()
        self.player.bull_move()

    #****************************удаление данных (destroy data here)
    def end_pygame():
        pygame.quit()

    #****************************ЗАПУСК ИГРЫ
    def play_game(self):
        print 'play_game'
        self.init_window()
        #self.end_pygame()

    #****************************фунция запуска

    def sendData(self, data):
        self.cf.conn.send(data)

    def getData(self, data):
        print "INCOMING: ", data
        self.parseData(data)

    def parseData(self, data):
        print type(data)
        if isinstance(data, dict):
            print "PARSING"
            print data['id']
            if data.get('type') == 'start':
                print 'START  THE GAME'
            for k in data:
                print "KEY: ",k," VALUE: ",data[k]

"""
    def parseData(self, data):
        if data['type'] == 'registration':
            self.registration(self)

        if data['type'] == 'game':
            self.parseGameData(self, data)


    def parseGameData(self, data):
        print "Parse Game Data"

"""
def main():
    play=Game()
if __name__ == '__main__': main()


    #while(!exit_&&SgIsActive())
	#	{
	#		start_draw();
	#		Process();
	#		end_draw();
	#	}
