import wx
 
class CustomButton(wx.Control):
    def __init__(self, parent, label):
        wx.Control.__init__(self, parent)
        self.label = label
         
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
         
    def onPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
         
        # отрисовка фона кнопки
        dc.SetBrush(wx.Brush(wx.Colour(240, 240, 240)))
        dc.SetPen(wx.Pen(wx.Colour(200, 200, 200), width=1))
        dc.DrawRectangle(0, 0, self.GetSize().width, self.GetSize().height)
         
        # отрисовка рамки кнопки
        dc.SetPen(wx.Pen(wx.Colour(150, 150, 150), width=2))
        dc.DrawLine(0, 0, 0, self.GetSize().height)
        dc.DrawLine(0, 0, self.GetSize().width, 0)
        dc.DrawLine(self.GetSize().width-1, 0, self.GetSize().width-1, self.GetSize().height)
        dc.DrawLine(0, self.GetSize().height-1, self.GetSize().width, self.GetSize().height-1)
         
        # отрисовка надписи на кнопке
        dc.SetTextForeground(wx.Colour(0, 0, 0))
        dc.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
         
        textWidth, textHeight = dc.GetTextExtent(self.label)
        textX = (self.GetSize().width - textWidth) // 2
        textY = (self.GetSize().height - textHeight) // 2
        dc.DrawText(self.label, textX, textY)
         
    def onLeftDown(self, event):
        self.CaptureMouse()
         
    def onLeftUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
            if self.GetClientRect().Contains(event.GetPosition()):
                print("Кнопка была нажата")
 
app = wx.App()
frame = wx.Frame(None, title="Пример кастомной кнопки", size=(300, 200))
panel = wx.Panel(frame)
button = CustomButton(panel, label="Нажми меня")
frame.Show()
app.MainLoop()