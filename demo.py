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
from pygame import mixer  # Load the required library
import threading
import gevent,time

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
play_name = 'Speech{0}.mp3'
# play_name_next = "Speechnext.mp3"
# save_name = "%s.%s" % (play_name, '.tmp')
mixer.init(frequency=30000)
# list_free = ["Speech.mp3", "Speechnext.mp3"]
# save_list = []
speechText_list = [" "]

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

def task_play(x):
    ff = open(play_name.format(str(x)),"rb")
    mixer.music.load(ff)
    mixer.music.play(0)
    while mixer.music.get_busy():  # still playing
        time.sleep(0.5)
    ff.close()
    



# x数字
def task_save(x):

    if x == 1:
        print "播放：" +str(0)
        task_play(0)

    if x > 1 :
        print "播放: "+str(x-1)
        # mixer.music.queue(play_name.format(str(x-1)))
        task_play((str(x-1)))

    print "save: " + str(x)
    text = gTTS(text=speechText_list[x].encode("utf8"), lang='zh', slow=False)
    text.save(play_name.format(str(x)))



        

class SpeechFrame(MyFrame1):
    def __init__(self, parent):
        MyFrame1.__init__(self, parent)


    def showspeech(self, event):
        speechText = self.m_textCtrl1.GetValue()
        speechText = speechText.replace("\n",",")
        # 文件分段
        

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
            # print num
            for x in range(0, num):
                speechText_list.append(speechText[x * maxNum + 0: x * maxNum + maxNum])

        threads = []
        threads.append(gevent.spawn(task_save, 0))
        for x in range(1,len(speechText_list)):

            threads.append(gevent.spawn(task_save, x))
            # threads.append(gevent.spawn(task_play, x-1))

        
        # for x in range(len(speechText_list)):
        #     # task_play(x)
        #     threads.append(gevent.spawn(task_play, x))

        gevent.joinall(threads)
        task_play(len(speechText_list)-1)



    def stopspeech(self, event):
        mixer.music.pause()


app = wx.App(False)
frame = SpeechFrame(None)
frame.Show(True)
# start the applications
app.MainLoop()
