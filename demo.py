# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

from gtts import gTTS
import string, math
from pygame import mixer, time  # Load the required library
import threading

pub = []
for p in string.punctuation:
    pub.append(p)

pub.append("，".decode("utf8"))
pub.append("。".decode("utf8"))
pub.append("、".decode("utf8"))
pub.append("”".decode("utf8"))
pub.append("？".decode("utf8"))
pub.append("：".decode("utf8"))
pub.append("！".decode("utf8"))

# print pub
# play_name = 'Speech.mp3'
# play_name_next = "Speechnext.mp3"
# save_name = "%s.%s" % (play_name, '.tmp')
mixer.init(frequency=30000)
list_free = ["Speech.mp3", "Speechnext.mp3"]
save_list = []


class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(526, 339), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(500, 200),
                                       wx.TE_MULTILINE)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.Point(11, 10), wx.Size(300, 50), 0)
        self.m_button1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))
        self.m_button1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        bSizer1.Add(self.m_button1, 0, wx.RIGHT, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button2, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.HORIZONTAL)

        # Connect Events
        self.m_button1.Bind(wx.EVT_LEFT_DOWN, self.showspeech)
        self.m_button2.Bind(wx.EVT_LEFT_DOWN, self.stopspeech)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def showspeech(self, event):
        event.Skip()

    def stopspeech(self, event):
        event.Skip()

# 播放
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print "t run"
        self.play()

    def play(self):
        f = open(self.name, 'rb')
        mixer.music.load(f)
        mixer.music.play(loops=0, start=0.0)
        while mixer.music.get_busy():  # still playing
            time.wait(600)
        f.close()
        list_free.append(self.name)

#存储
class myThread1(threading.Thread):
    def __init__(self,Stext):
        threading.Thread.__init__(self)
        self.text = Stext
        print Stext

    def run(self):
        print "t1 run"
        self.play()

    def play(self):
        try:
            self.text = self.text.encode("utf8")
        except Exception:
            pass
        text = gTTS(text=self.text, lang='en', slow=False)
        play_name = list_free.pop()
        text.save(play_name)
        save_list.append(play_name)
        print len(save_list)
        print "save finsh"


class SpeechFrame(MyFrame1):
    def __init__(self, parent):
        MyFrame1.__init__(self, parent)

    def play(self, filename):
        f = open(filename, 'rb')
        mixer.music.load(f)
        mixer.music.play()
        while mixer.music.get_busy():  # still playing
            time.wait(1000)
        f.close()
        list_free.append(filename)

    def voice(self, x):
        while len(x) > 0 or len(save_list)>0:
            print "while"
            # x = slist.pop()
            # 保存
            if list_free:
                print "save"
                t = myThread1(x.pop(0))
                t.start()
                t.join()
                # text = gTTS(text=x.pop(0).encode("utf8"), lang='zh', slow=False)
                # play_name = list_free.pop()
                # text.save(play_name)
                # save_list.append(play_name)

            if not mixer.music.get_busy() and len(save_list) > 0 :
                print "play music"
                # t1 = myThread(save_list.pop())
                # t1.start()
                # t1.join()
                self.play(save_list.pop())

    def showspeech(self, event):
        speechText = self.m_textCtrl1.GetValue()
        speechText = speechText.replace("\n",",")
        # 文件分段
        speechText_list = [" "]

        # maxNum = 60
        # num = int(math.ceil(len(speechText) / float(maxNum)))
        # print num
        # for x in range(0, num):
        #     speechText_list.append(speechText[x * maxNum + 0: x * maxNum + maxNum])

        tempNum = 0
        allNum = len(speechText)
        for x in range(allNum):
            if speechText[x] in pub:
                print x
                if len(speechText_list[-1])<40 :
                    speechText_list[-1] = speechText_list[-1]+","+  speechText[tempNum+1 :x]
                else:
                    speechText_list.append(","+speechText[tempNum+1 :x])
                tempNum = x



        if not speechText_list:
            maxNum = 80
            num = int(math.ceil(len(speechText) / float(maxNum)))
            print num
            for x in range(0, num):
                speechText_list.append(speechText[x * maxNum + 0: x * maxNum + maxNum])

        print speechText_list

        # for ss in speechText_list:
        self.voice(speechText_list)

        # while True:
        #     if len(list_free) == 1:
        #         pass
        #
        #     time.wait(1000)
        #     # self.play(play_name)

    def stopspeech(self, event):
        mixer.music.pause()


app = wx.App(False)
frame = SpeechFrame(None)
frame.Show(True)
# start the applications
app.MainLoop()
