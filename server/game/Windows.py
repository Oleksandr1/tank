#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, pygame
from pygame import *

#**************************** Класс окна (основное window, окно Game_Window, окно Results_Window, окно Chat_Window)

class Windows():

    def __init__(self, gw=None):
    #**************************** окно Game_Window
        self.rect_color_GW = (0,100,0)# цвет окна
        self.rect_rect_GW = ((0,0),(800,700))#расположение и размер
        self.rect_width_GW = 0# заливка

    #**************************** окно Results_Window
        self.rect_color_RW = (0,0,139)# цвет окна
        self.rect_rect_RW = ((800,0),(224,350))#расположение и размер
        self.rect_width_RW = 0# заливка

    #**************************** окно Chat_Window
        self.rect_color_CW = (152,251,152)# цвет окна
        self.rect_rect_CW = ((800,350),(224,350))#расположение и размер
        self.rect_width_CW = 0# заливка

    #****************************рисуем окна
    def draw_windows(self, screen):
        pygame.draw.rect(screen,self.rect_color_GW,self.rect_rect_GW,self.rect_width_GW)#рисуем окно Game_Window
        pygame.draw.rect(screen,self.rect_color_RW,self.rect_rect_RW,self.rect_width_RW)#рисуем окно Results_Window
        pygame.draw.rect(screen,self.rect_color_CW,self.rect_rect_CW,self.rect_width_CW)#рисуем окно Chat_Window


    def showChatText(self, text = 'Hi'):
        self.text = font.render(text,True,black)
        pygame.draw.rect(self.text, (200,300))
