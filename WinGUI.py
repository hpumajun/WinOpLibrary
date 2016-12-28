# -*- coding: utf-8 -*-

'''
    created by JunMa 2016-11-2
'''
__version__ = '0.1'


from win32gui import *
from win32con import *
from win32process import *
from win32api import *
import time 
import string
from robot.api import logger
import os

class windowinfo():
    def __init__(self):
        self.classname = ''
        self.title = ''

class ScreenSolution():
    def __init__(self):
        self.width = GetSystemMetrics(SM_CXSCREEN)
        self.height = GetSystemMetrics(SM_CYSCREEN)

class WindowRect():
    def __init__(self):
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
class WindowPosition:
    x = 0
    y = 0

class WindowSize:
    width = 0
    height = 0
                
class WinGUIOperate(object):
    def __init__(self):
        self.titles = []
        self.ScrSolution = ScreenSolution()
        self.WinRec = WindowRect()
        
    def CallBackWindowsName(self,hwnd,titles):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and GetWindowText(hwnd):
            wininfo = windowinfo()
            wininfo.classname = GetClassName(hwnd)
            wininfo.title = GetWindowText(hwnd)
            dict = {}
            dict = {hwnd : wininfo}
            titles.append(dict)
#             time.sleep(0.1)
    
    def EnumAllVisableWindowName(self):
        """
        Get All the name of visiable window, and reture the name list
        usage:
        | ${namelist}|EnumAllWindowName| the handle of the window                                 |
        
        """
        titles = []
        EnumWindows(self.CallBackWindowsName,titles)
#         lt = [t for t in titles if t]
#         lt.sort()
#         return lt
        for t in titles:
            for key, value in t.items():
                classname = value.classname
                title = value.title
                print "%d--->classname is %s, window title is %s " % (key, classname, title.decode('GB2312','ignore'))
        return titles
    def EnumAllWindowByNameAndClass(self,name,clname):
        list1 = []
        EnumWindows(self.CallBackWindowsName,list1)
#        print ("find name is %s,clname is %s") % (name,clname)
        hwnd = []
        for t in list1:
            for key, value in t.items():
#                 classname = value.classname
#                 title = value.title
#                 print "%d--->classname is %s, window title is %s ,visibility is" % (key, classname, title.decode('GB2312','ignore'))
                if (clname == str(value.classname).decode('utf-8') and name == str(value.title).decode('utf-8')):
                    hwnd.append(key)
        return hwnd
                
    def EnumChildWindowByParentHwnd(self,parenthwnd):
        """
        Get all the child window info by parent hwnd
        """
        titles = []
        EnumChildWindows(parenthwnd,self.CallBackWindowsName,titles)
#         for t in titles:
#             for key, value in t.items():
#                 classname = value.classname
#                 title = value.title
#                 visable = value.visibility
#                 print "%d--->classname is %s, window title is %s ,visibility is %d" % (key, classname, title.decode('GB2312','ignore'),visable)
        return titles
    def GetHwndByParentAndText(self,Phwnd,text):
        info = self.EnumChildWindowByParentHwnd(Phwnd)
#        print text
        for t in info :
            for key, value in t.items():
                tl = str(value.title)
                print "hwnd = %d , window title is %s\n" % (key, tl.decode('GB2312','ignore'))
                if (text.decode("utf-8") == tl.decode("utf-8")):
                    return key
        return 0    
    
    def GetHwndByNameAndClass(self,name,classname):
        """
        Get the handle of the windown whose name is ${name}
        usage:
        | ${hwnd}|GetHwndByNameAndClass| the handle of the window                                 |
        
        """
        try:
            hwnd = FindWindow(classname,name)
        except Exception:
            print "Find the windows %s failed, please check it" % name.decode('GB2312')
            return 0 
        if(hwnd):
            return hwnd
    def GetHwndByParentAndInfo(self,parent,name,clname):
        allhwnd = self.EnumAllWindowByNameAndClass(name, clname)
        print "same class and name hwnd is %s" % allhwnd
        for t in allhwnd :
            print GetWindowLong(t,GWL_HWNDPARENT)
            if (int(parent) == GetWindowLong(t,GWL_HWNDPARENT)):
                print "get hwnd is %d" % t
                return t
        return 0
                
    def SetWindowTopFront(self,hwnd):
        """
        this keyword is used to set the windows as the topest window 
        usage:
        | SetWindowTopFront|${hwnd}| the handle of the window                                 |
        
        """
        assert hwnd > 0
        threadid = GetCurrentThreadId()
        forehwnd = GetForegroundWindow()
        forceId = GetWindowThreadProcessId(forehwnd)
         
        AttachThreadInput(threadid, forceId[0],TRUE)
        time.sleep(0.1)
        ShowWindow(hwnd,SW_SHOWNORMAL)
        SetWindowPos(hwnd,HWND_TOPMOST,0,0,0,0,SWP_NOSIZE|SWP_NOMOVE)
        SetWindowPos(hwnd,HWND_NOTOPMOST,0,0,0,0,SWP_NOSIZE|SWP_NOMOVE)
        SetForegroundWindow(hwnd)
        time.sleep(0.1)
        AttachThreadInput(threadid, forceId[0], FALSE)
        
    def ShowWindowsByName(self,hwnd,flag=1):
        """
        this keyword is used to set the windows to show max or min, show max means,the window will filled with your screen show min means\
        the windowns will hide from the screen,on the other words,max show equal you click the maxinum button and min show you click the min\
        button,by default if no change the size of the windows
        usage:
        |hwnd = <int>  | the handle of the window                                 |
        |flag = 0      | if flag is 2, the window will min,flag is 3 means max it |
        
        """
        ShowWindow(hwnd,flag)
    def GetScreenSolution(self):
        """
        This keyword can get your screen's resolution ratio like 1920*1080, it return the value of width and height of your screen
        |${width} |${hight}| GetScreenSolution            |
        """
        return (self.ScrSolution.width, self.ScrSolution.height)
    
    def GetWindowClientRect(self,hwnd):
        """
        This keyword can get your window's Rect size,the window is specified by hwnd
        |${width} |${hight}| GetWindowClientRect|${hwnd}     |
        
        """
        assert hwnd != 0
        (left,top,right,bot) = GetClientRect(hwnd)
#         print ("%d,%d,%d,%d") % (left,top,right,bot)
        return right,bot
    
    def GetWindowRection(self,hwnd):
        """
        get the Rect of windows, return the left,top, right and bottom position of your screen
        |${left}|${top}|${right}|${bottom}|GetWindowRect|${hwnd}|
        
        """
        (left,top,right,bot) = GetWindowRect(hwnd)
        WindowPosition.x = left
        WindowPosition.y = top
        WindowSize.width = right - left
        WindowSize.height = bot - top
        return WindowPosition.x,WindowPosition.y, WindowSize.width,WindowSize.height
    
    def SetWindowPosCenter(self,hwnd):
        """
        set the window you specified in the center of your screen, but it doesn't change the size of the window.
        |SetWindowPosCenter|${hwnd}|
        
        """
        width,height = self.GetScreenSolution()
        (right,bot) = self.GetWindowClientRect(hwnd)
        nX = (width - right)/2
        nY = (height - bot)/2
        SetWindowPos(hwnd,HWND_TOP,nX,nY,0,0,SWP_NOSIZE)
        
    def ClickButton(self,hwnd):
        # here we can't use SendMessage, or it will block until the hwnd return.
        assert hwnd != 0
        assert hwnd is not None
        PostMessage(hwnd,WM_LBUTTONDOWN,0,0)
        PostMessage(hwnd,WM_LBUTTONUP,0,0)
    
    def ClickButtonByText(self,Phwnd,text):
        hwnd = self.GetHwndByParentAndText(Phwnd, text)
        print "the hwnd you want to click is %d" % hwnd    
        self.ClickButton(hwnd)
        
if __name__ == "__main__":
    GUI = WinGUIOperate()
     
#     (right, bot) = GUI.GetWindowClientRect(198278)
#     print ("%d,%d") % (right,bot)
    time.sleep(3)
#    print GUI.GetActiveWindows()
#    WinInfoList = GUI.EnumAllVisableWindowName()
    Name = u"iVMS-4200"
    clname = "QWidget"
    hwnd = GUI.GetHwndByNameAndClass(Name,clname)
    print ("hwnd is %d, class name is %s") %(hwnd,GetClassName(hwnd))
    GUI.SetWindowTopFront(hwnd)
    GUI.ClickButtonByText(hwnd,'m_pBtnRemoteCfg')
    time.sleep(1)
#     info = GUI.EnumChildWindowByParentHwnd(hwnd)
    WinInfoList = GUI.EnumAllVisableWindowName()
     
    pwnd = GUI.GetHwndByNameAndClass("iVMS-4200", "QWidget")  
    print pwnd
    WindowPosition.x,WindowPosition.y,WindowSize.height, WindowSize.width = GUI.GetWindowRection(pwnd)
     
#     print ("%d,%d,%d,%d") % (left,right,top,bottom)
    print ("%d,%d,%d,%d") % (WindowPosition.x,WindowPosition.y,WindowSize.height,WindowSize.width)
    WinInfoList = GUI.EnumAllVisableWindowName()
#     GUI.SetWindowTopFront(pwnd)
#     GUI.ClickButtonByText(pwnd,'m_pPortLEdit')
#     GUI.SetWindowTopFront(hwnd)
#     GUI.GetScreenSolution()
#     (right,bot) = GUI.GetWindowClientRect(hwnd)
#     print ("%d,%d") % (right,bot)
     
#     GUI.SetWindowPosCenter(hwnd)
#     time.sleep(5)
#     info = GUI.EnumChildWindowByParentHwnd(hwnd)
#     for t in info:
#         for key, value in t.items():
#             classname = value.classname
#             title = value.title
# #            visable = value.visibility
#             print "%d--->classname is %s, window title is %s ,visibility is" % (key, classname, title.decode('GB2312','ignore'))
# #       
