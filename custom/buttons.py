import wx
import time
from wx import ColourDatabase as cdb
from wx.lib.agw import gradientbutton as GB

HOVER = 1
CLICK = 2

class MyButton(GB.GradientButton):
    def __init__(self, parent, id=wx.ID_ANY, bitmap=None, label="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER, align=wx.CENTER, validator=wx.DefaultValidator, name="gradientbutton"):
        super().__init__(parent, id, bitmap, label, pos, size, style, align, validator, name)
        self.SetTopStartColour(wx.Colour(81, 81, 81))
        self.SetTopEndColour(wx.Colour(181, 182, 185))
        self.SetBottomStartColour(wx.Colour(181, 182, 185))
        self.SetBottomEndColour(wx.Colour(81, 81, 81))
        self.SetForegroundColour(wx.Colour(wx.BLACK))
        self.SetPressedBottomColour(wx.Colour(172, 171, 173))
        self.SetPressedTopColour(wx.Colour(166, 168, 170))

        self._fade = False

    def OnMouseEnter(self, event):
        if not self.IsEnabled():
            return

        self._mouseAction = HOVER
        
        for i in range(0, 120, 20):
            # self.pen_color = wx.Colour(255, 100-i, 100-i)
            self.pen_color = wx.Colour(255, 0, 0, int(2.55*i))
            self.brush_colour = wx.Colour(255, 0, 0, int(0.15*i))
            self.Refresh()
            self.Update()
            time.sleep(0.03)
            event.Skip()
        self._fade = True

    def OnMouseLeave(self, event):
        self._mouseAction = None
        self.Refresh()
        # if self._fade:
        for i in reversed(range(0, 120, 20)):
            # self.pen_color = wx.Colour(255, 100-i, 100-i)
            self.pen_color = wx.Colour(255, 0, 0, int(2.55*i))
            self.brush_colour = wx.Colour(255, 0, 0, int(0.15*i))
            self.Refresh()
            self.Update()
            time.sleep(0.02)
            event.Skip()
        self._fade = False
        self.Refresh()

    def OnPaint(self, event):

        self.Refresh()
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()

        clientRect = self.GetClientRect()
        gradientRect = wx.Rect(*clientRect)
        capture = wx.Window.GetCapture()

        x, y, width, height = clientRect

        gradientRect.SetHeight(gradientRect.GetHeight()//2 + ((capture==self and [1] or [0])[0]))
        if capture != self:
            if self._mouseAction == HOVER:
                topStart, topEnd = self.LightColour(self._topStartColour, 10), self.LightColour(self._topEndColour, 10)
            else:
                topStart, topEnd = self._topStartColour, self._topEndColour

            rc1 = wx.Rect(x, y, width, height//2)
            path1 = self.GetPath(gc, rc1, 8)
            br1 = gc.CreateLinearGradientBrush(x, y, x, y+height/2, topStart, topEnd)
            gc.SetBrush(br1)
            gc.FillPath(path1) #draw main

            path4 = gc.CreatePath()
            path4.AddRectangle(x, y+height/2-8, width, 8)
            path4.CloseSubpath()
            gc.SetBrush(br1)
            gc.FillPath(path4)

            # ____________________________________#
            
                
            # _____________________________________#
                    

        else:

            rc1 = wx.Rect(x, y, width, height)
            path1 = self.GetPath(gc, rc1, 8)
            gc.SetPen(wx.Pen(self._pressedTopColour))
            gc.SetBrush(wx.Brush(self._pressedTopColour))
            gc.FillPath(path1)

        gradientRect.Offset((0, gradientRect.GetHeight()))

        if capture != self:

            if self._mouseAction == HOVER:
                bottomStart, bottomEnd = self.LightColour(self._bottomStartColour, 10), self.LightColour(self._bottomEndColour, 10)
            else:
                bottomStart, bottomEnd = self._bottomStartColour, self._bottomEndColour

            rc3 = wx.Rect(x, y+height//2, width, height//2)
            path3 = self.GetPath(gc, rc3, 8)
            br3 = gc.CreateLinearGradientBrush(x, y+height/2, x, y+height, bottomStart, bottomEnd)
            gc.SetBrush(br3)
            gc.FillPath(path3) #draw main

            path4 = gc.CreatePath()
            path4.AddRectangle(x, y+height/2, width, 8)
            path4.CloseSubpath()
            gc.SetBrush(br3)
            gc.FillPath(path4)

            shadowOffset = 0
            
        else:

            rc2 = wx.Rect(x+1, gradientRect.height//2, gradientRect.width, gradientRect.height)
            path2 = self.GetPath(gc, rc2, 8)
            gc.SetPen(wx.Pen(self._pressedBottomColour))
            gc.SetBrush(wx.Brush(self._pressedBottomColour))
            gc.FillPath(path2)
            shadowOffset = 1

        if self._mouseAction == HOVER and self._fade == False or self._mouseAction == None and self._fade == True:
                gc.SetPen(wx.Pen(self.pen_color))
                gc.SetBrush(wx.Brush(self.brush_colour))
                x, y = self.GetSize()
                gc.DrawRoundedRectangle(1, 1, x-2, y-2, 6)

        font = gc.CreateFont(self.GetFont(), self.GetForegroundColour())
        gc.SetFont(font)
        label = self.GetLabel()
        tw, th = gc.GetTextExtent(label)

        if self._bitmap:
            bw, bh = self._bitmap.GetWidth(), self._bitmap.GetHeight()
        else:
            bw = bh = 0

        if self._alignment == wx.CENTER:
            pos_x = (width-bw-tw)/2+shadowOffset # adjust for bitmap and text to centre
            if self._bitmap:
                pos_y =  (height-bh)/2+shadowOffset
                gc.DrawBitmap(self._bitmap, pos_x, pos_y, bw, bh) # draw bitmap if available
                pos_x = pos_x + 2 # extra spacing from bitmap
        elif self._alignment == wx.LEFT:
            pos_x = 3 # adjust for bitmap and text to left
            if self._bitmap:
                pos_y =  (height-bh)/2+shadowOffset
                gc.DrawBitmap(self._bitmap, pos_x, pos_y, bw, bh) # draw bitmap if available
                pos_x = pos_x + 3 # extra spacing from bitmap

        gc.DrawText(label, pos_x + bw + shadowOffset, (height-th)/2+shadowOffset)