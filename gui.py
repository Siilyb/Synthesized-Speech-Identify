#!/bin/python
import wave
import wx
from pydub import AudioSegment
from PIL import Image
import numpy as np
import tensorflow._api.v2.compat.v1 as tf

import useModel

tf.disable_v2_behavior()
import matplotlib.pyplot as plt
import os
import re
import sys


class HelloFrame(wx.Frame):
    global project_root

    def __init__(self,*args,**kw):
        super(HelloFrame,self).__init__(*args,**kw)
        self.project_root = os.getcwd()


        pnl = wx.Panel(self)

        self.pnl = pnl
        st = wx.StaticText(pnl, label="检测", pos=(400, 0))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        st = wx.StaticText(pnl, label="要求音频长度1~5秒", pos=(450, 40))
        font = st.GetFont()
        font.PointSize += 6

        st.SetFont(font)

        # 选择图像文件按钮
        btn = wx.Button(pnl, -1, "select")
        btn.Bind(wx.EVT_BUTTON, self.OnSelect)

        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText("text test")

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                                    "123")
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)



        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")


        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)



    def OnExit(self, event):
        self.Close(True)

    def OnHello(self, event):
        wx.MessageBox("hello world...")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("sample,only for test",
                      wx.OK | wx.ICON_INFORMATION)

    def OnSelect(self, event):
        wildcard = "audio source(*.wav)|*.wav|" \
                   "All file(*.*)|*.*"

        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(),
                               "", wildcard, wx.ID_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            print(dialog.GetPath())



        print(self.project_root)
        os.chdir(self.project_root)


        spectrum(dialog.GetPath(), "TestFigure")
        print(useModel.useModel2("data/savefig/TestFigure.jpg"))
        textresult=str(useModel.useModel2("data/savefig/TestFigure.jpg"))
        result_text = wx.StaticText(self.pnl, label=textresult, pos=(100, 700))
        font = result_text.GetFont()
        font.PointSize += 8
        result_text.SetFont(font)
        result_text = wx.StaticText(self.pnl, label=str(dialog.GetPath()), pos=(100, 600))
        font = result_text.GetFont()
        font.PointSize += 8
        result_text.SetFont(font)
        result_text = wx.StaticText(self.pnl, label=textresult[2:6], pos=(700, 200))
        font = result_text.GetFont()
        font.PointSize += 16
        font = font.Bold()
        result_text.SetFont(font)


        self.initimage(name="data/savefig/TestFigure.jpg")



        # 生成图片控件
    def initimage(self, name):
        os.chdir(self.project_root)
        imageShow = wx.Image(name, wx.BITMAP_TYPE_ANY)
        sb = wx.StaticBitmap(self.pnl, -1, imageShow.ConvertToBitmap(), pos=(0,45))
        return sb



def spectrum(path, name):
    filename = path

    f = wave.open(filename, 'rb')

    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)
    waveData = np.fromstring(strData, dtype=np.short)
    waveData = waveData * 1.0 / max(abs(waveData))
    waveData = np.reshape(waveData, [nframes, nchannels]).T
    f.close()
    framelength = 0.025  # 帧长
    framesize = framelength * framerate

    nfftdict = {}
    lists = [32, 64, 128, 256, 512, 1024]
    for i in lists:
        nfftdict[i] = abs(framesize - i)
    sortlist = sorted(nfftdict.items(), key=lambda x: x[1])
    framesize = int(sortlist[0][0])

    NFFT = framesize
    overlapSize = 1.0 / 3 * framesize
    overlapSize = int(round(overlapSize))
    print("帧长为{},帧叠为{},傅里叶变换点数为{}".format(framesize, overlapSize, NFFT))
    spectrum, freqs, ts, fig = plt.specgram(waveData[0], NFFT=NFFT, Fs=framerate, window=np.hanning(M=framesize),
                                            noverlap=overlapSize, mode='psd', scale_by_freq=True, sides='default',
                                            scale='dB', xextent=None)  # 绘制频谱图


    plt.ylabel('Frequency')
    plt.xlabel('Time')
    plt.title("Spectrogram")
    plt.savefig("data/savefig/" + name + ".jpg")
    plt.clf()

if __name__ == '__main__':

    app = wx.App()
    frm = HelloFrame(None, title='合成语音检测', size=(1200,900))
    frm.Show()
    app.MainLoop()

