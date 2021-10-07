import pygame as pg
from settings import *

class Timer:
    def __init__(self,time):

        self.sec=0
        self.min=0
        self.hour=0
        if time[0]=='s':
            self.sec=int(time[1])
        elif time[0]=='m':
            self.min=int(time[1])
        elif time[0]=='h':
            self.hour=int(time[1])
        elif len(time)>2:
            time_s=time.split(':')
            self.hour=int(time_s[0])
            self.min=int(time_s[1])
            self.sec=int(time_s[2])
        self.curr_time=0
    def update_sec(self):
        now=pg.time.get_ticks()
        if self.sec==0 and self.min==0 and self.hour!=0:
            self.hour-=1
            self.min=60
            self.sec=0
        if self.sec==0 and self.min!=0:
            self.min-=1
            self.sec=60
        if now-self.curr_time>1000:
            self.curr_time=now
            self.sec-=1
    def return_time(self):
        return f"{self.hour}:{self.min}:{self.sec}"

class FirstQuest:
    def __init__(self,game):
        self.timer=Timer('3:0:0')
        self.game = game
        self.name = 'The first quest'
        self.text={"1":"Wait for a little while: ",
                   "2":"Eat 3 apples:#"

                   }
        self.quest_running=True
    def update(self):
        self.timer.update_sec()
        if self.timer.sec==0:
            self.quest_running=False
        return self.quest_running

    def draw(self):
        self.game.draw_text(self.text['1']+self.timer.return_time(), self.game.title_font, 20, WHITE,
                            WIDTH/20, HEIGHT/12,
                            align='sw')




class QuestManager:

    def __init__(self, game):
        self.game=game
        self.quest_complete = []
        self.quest = None
        self.quest_running = False

        # Drawing variables
        self.window_size = 0

    def start_quest(self, quest):
        if quest.name not in self.quest_complete:
            self.quest_complete.append(quest.name)
            self.quest = quest
            self.quest_running = True

    def end_quest(self):
        self.quest= None
        self.quest_running = False

    def update(self):

        if self.quest_running:
            # if self.window_size < self.game.screen.get_height() * 0.3 and self.quest.field_drawing:
            #     self.window_size += 6
            self.quest_running = self.quest.update()
        else:
            self.end_quest()

    def draw(self):
        if self.quest_running:
            # Draw specific cut scene details
            self.quest.draw()