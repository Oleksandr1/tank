#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import cPickle
import sys

class GameData():
    def __init__(self,type = 'start game', gw=None):
        self.gw = gw
        self.data = {'type':type}


    def show(self):
        print self.data

    def serialize(self):
        s = cPickle.dumps(self.data,2)
        return s

    def deserialize(self, data):
        return cPickle.loads(data)

    def sendData(self, cf):
        cf.conn.send(self.serialize())

    def parseData(self):
        if self.data['type'] == 'start game':
            print 'parsing is work'
            print self.data.keys()


    def setInstance(self):
        pass

def main():
    data = GameData()
    data.show()
    data.data['id'] = 12
    data.show()
    data.data['coordinate'] = (244,123)
    data.show()
    data.data['bullet']  = {'id':11,'coord':(11, 12)}
    data.show()
    print 'Serialize and deserialize'
    print 'Original', sys.getsizeof(data.data)
    a = data.serialize()
    print 'Pickled', sys.getsizeof(a)
    print data.deserialize(a)

    print data.parseData()

if __name__ == '__main__':
    main()


"""

Данные для передачи между клиентом и сервером.
При создании игры
    какая игра(2*2, 4*4)
    id создателя
    какой уровень


От игрока:
    состояние: в игре, пауза, вышел, сервер не отвечает(чтоб отключаль игра, специфика библиотекм)
    id
    координаты
    выстрел
    список пуль
    направление движения?
    ?как вариант сообщения в чат

от Бота:
    id
    координаты(кортеж)
    выстрел

от сервера возвращается:
    ВСЕМ ПОЛЬЗОВАТЛЯМ:
        кол-во игроков на поле
        координаты каждого игрока (массив)
        координаты пуль (массив)
        ?соощения чата
        время на сервере
    КАЖДОМУ ОТДЕЛЬНО:
        здоровье
        очки


на сервере должно отображаться:
    запущен ли
    сколько игроков в игре
    сколько в ожидании
    сколько полей играется
    сколько полей свободно






"""
