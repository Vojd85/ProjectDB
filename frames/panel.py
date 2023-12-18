import wx


class MyPanel(wx.Panel):
    """"""
 
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(186, 184, 177))