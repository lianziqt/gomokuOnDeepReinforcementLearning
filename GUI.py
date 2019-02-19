import numpy as np
import random

import loggers as lg

from game import Game, GameState
from model import Residual_CNN

from agent import Agent, User

import config

import tkinter
import tkinter.messagebox as messagebox
import time
import threading

class GUI():
    def __init__(self):
        self.BALCK = "#000000"    #黑棋
        self.WHITE = "#ffffff"    #白棋
        self.RED = "#ff0000"        #红色标志   
        self.top = tkinter.Tk()               #对话框对象
        self.top.title("**自己画的五子棋**")   #对话框名称
        self.top.geometry('600x600')          #对话框初始大小
        self.canvas = tkinter.Canvas(self.top,width=480,height=480,background="white")  #画布长、高、颜色
        self.vs = [[0 for col in range(15)] for row in range(15)]
    
    def board_initial(self):
        self.canvas.delete('all')    #删除画布全部内容   
        self.last_x1, self.last_x2, self.last_y1, self.last_y2=0,0,0,0
        #self.red_a1, self.red_a2, self.red_b1, self.red_b2=0,0,0,0 
        for num in range(1,16):     #棋盘线
            self.canvas.create_line(num*30,30,num*30,450,width=1)
        for num in range(1,16):
            self.canvas.create_line(30,num*30,450,num*30,width=1)
            self.canvas.create_oval(117,117,123,123,fill=self.BALCK)  #棋盘方位点
            self.canvas.create_oval(357,117,363,123,fill=self.BALCK)
            self.canvas.create_oval(117,357,123,363,fill=self.BALCK)
            self.canvas.create_oval(357,357,363,363,fill=self.BALCK)
            self.canvas.create_oval(236,236,244,244,fill=self.BALCK)
        self.canvas.pack()    #画布打包进对话框
    
    def bind_button(self, text, command):
        A = tkinter.Button(self.top,text=text, command=command)
        A.pack()
    
    def bind_click(self, text, command):
        self.canvas.bind(text,command)

    def paint_chessman(self, clickx, clicky, color):
        self.current_x1, self.current_y1=(clickx-8), (clicky-8)  #棋子大小
        self.current_x2, self.current_y2=(clickx+8), (clicky+8)
        self.canvas.create_oval(self.current_x1, self.current_y1, self.current_x2, self.current_y2, fill=color) #落白子

    def paint_mark(self, clickx, clicky):
        red_a1, red_b1=(clickx-3), (clicky-3)  #红色标记标记大小
        red_a2, red_b2=(clickx+3), (clicky+3)
        self.canvas.create_oval(red_a1, red_b1, red_a2, red_b2, fill=self.RED)   #标记最新落子处

    
    def paint_with_click(self, clickx, clicky, color):
        index_x = clickx//30-1        #像素点480*480换算成坐标点15*15
        index_y = clicky//30-1

        if(self.vs[index_x][index_y] != 0): return
        self.vs[index_x][index_y] = 1

        last_color = self.BALCK if color == self.WHITE else self.WHITE

        self.paint_chessman(clickx, clicky, color=color) #落子
        self.paint_mark(clickx, clicky)   #标记最新落子处
        
        self.canvas.create_oval(self.last_x1, self.last_y1, self.last_x2, self.last_y2, fill=last_color) #覆盖上一次的标记

        self.last_x1, self.last_y1 = self.current_x1, self.current_y1
        self.last_x2, self.last_y2 = self.current_x2, self.current_y2

        


    def paint_with_action(self, action, color):
        click_x = ((action // 15) + 1) * 30
        click_y = ((action % 15) + 1) * 30
        self.paint_with_click(click_x, click_y, color)

class PlayWithAI():

    def __init__(self, player1, playerAI, logger, turns_until_tau0, memory = None):
        self.window = GUI()
        self.player1 = player1
        self.playerAI = playerAI
        self.logger = logger
        self.turns_until_tau0 = turns_until_tau0
        self.memory = memory
        self.env = Game()
        self.scores = {player1.name:0, "drawn": 0, playerAI.name:0}
        self.sp_scores = {'sp':0, "drawn": 0, 'nsp':0}
        self.points = {player1.name:[], playerAI.name:[]}
        self.color = {-1:'#000000', 1:'#ffffff'}
    
    def end_game(self):
        if self.done == 1:
            if self.state.playerTurn == 1:
                messagebox.askokcancel('结束','黑棋胜！点击"重新开始"再战一局')
            else:
                messagebox.askokcancel('结束','白棋胜！点击"重新开始"再战一局')
            self.reload()
            return True
        return False

    def reload(self):
        self.window.board_initial()
        self.state = self.env.reset()
        
        self.done = 0
        self.turn = 0
        self.playerAI.mcts = None
        self.playerAI.act(self.state, 0)

    def click(self, event):
        
        flag_x = event.x % 30       #将鼠标点击坐标转换至交点位置下棋
        flag_y = event.y % 30
        if(flag_x > 15):  
            clickx = event.x + (30 - flag_x)
        else:
            clickx = event.x - flag_x
        if(flag_y > 15):
            clicky = event.y + (30 - flag_y)
        else:
            clicky = event.y - flag_y
        if(clickx < 25 or clickx >455 or clicky <25 or clicky > 455): #规定在棋盘内落子
            return
        if(self.window.vs[clickx // 30 - 1][clicky // 30 - 1] == 0):  #只能在空白处落子
            action = ((clickx // 30 - 1) * 15) + ( clicky // 30 - 1 )

            self.action, self.pi, self.MCTS_value, self.NN_value = self.player1.act(action, self.state, 1)
            self.state, self.value, self.done, _ = self.env.step(action)
            self.window.paint_with_click(clickx, clicky, self.color[self.state.playerTurn])
            if self.end_game() :
                return
            self.start_AI_threading()
            self.turn = self.turn + 1
        return
    def start_AI_threading(self):
        self.thread=threading.Thread(target=self.AI_act,args=())
        self.thread.start()

    def AI_act(self):
        if self.turn < self.turns_until_tau0:
            self.action, pi, MCTS_value, NN_value = self.playerAI.act(self.state, 1)
        else:
            self.action, pi, MCTS_value, NN_value = self.playerAI.act(self.state, 0)
            
        self.state, self.value, self.done, _ = self.env.step(self.action)
        self.window.paint_with_action(self.action, self.color[self.state.playerTurn])
        self.end_game()


    def initial(self):
        self.state = self.env.reset()
        
        self.done = 0
        self.turn = 0
        self.playerAI.mcts = None
        self.playerAI.act(self.state, 0)
        
        self.window.board_initial()
        self.window.bind_button('重新开始', self.reload)
        self.window.bind_button('AI落子', self.start_AI_threading)
        self.window.bind_click('<Button-1>', self.click)

    def loop(self):
        self.window.top.mainloop()

