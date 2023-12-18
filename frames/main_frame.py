import wx
from frames import __version__
# from wx.lib import colourdb
from custom.buttons import MyButton
from .panel import MyPanel
from .login import LoginDialog
from .material_frame import SecondFrame
from .history_frame import HistoryFrame
from .admin_frame import AdminFrame
from dialogs.guide_dlg import GuideDialog


class MainFrame(wx.Frame):
    """"""
 
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Учёт материалов", size=(600, 450))
        panel = MyPanel(self)
        loc = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(wx.Icon(loc))
        dlg = LoginDialog()
        dlg.ShowModal()
        dlg.Destroy()
        if not isinstance(dlg.login, tuple):
            self.Destroy()
        else:
            self.user, self.level = dlg.login
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        hor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        btn_all_base = wx.Button(panel, label="Все\nматериалы", size=(100, 100))
        btn_log = wx.Button(panel, label="Журнал\nсобытий", size=(100, 100))
        btn_admin = wx.Button(panel, label="Админ", size=(100, 100))
        btn_guide = wx.Button(panel, label="Справочник", size=(100, 100))

        btn_all_base.Bind(wx.EVT_BUTTON, self.to_all)
        btn_log.Bind(wx.EVT_BUTTON, self.to_history)
        btn_admin.Bind(wx.EVT_BUTTON, self.to_admin)
        btn_guide.Bind(wx.EVT_BUTTON, self.to_guide)

        hor_sizer.Add(btn_all_base, 0, wx.LEFT|wx.TOP, 20)
        hor_sizer.Add(btn_log, 0, wx.LEFT|wx.TOP, 20)
        hor_sizer.Add(btn_admin, 0, wx.LEFT|wx.TOP, 20)
        hor_sizer2.Add(btn_guide, 0, wx.LEFT|wx.TOP, 20)
        

        version = wx.StaticText(panel, label=f"version: {__version__}")
        develop = wx.StaticText(panel, label="Vojd-py_development (C) 2023")
        hor_sizer3.Add(version, 0, wx.ALIGN_BOTTOM)
        hor_sizer3.AddSpacer(300)
        hor_sizer3.Add(develop, 0, wx.ALIGN_BOTTOM)
        main_sizer.Add(hor_sizer, wx.ALL, 10)
        main_sizer.Add(hor_sizer2, wx.ALL, 10)
        main_sizer.Add(hor_sizer3, 1, wx.ALL, 10)
        
        panel.SetSizer(main_sizer)
        # if self.level != 1:
        #     btn_admin.Disable()
        # if self.level > 2:
        #     btn_guide.Disable()
        # if self.level > 3:
        #     btn_log.Disable()
        self.Center()
        self.Show()

    def to_all(self, event):
        sec = SecondFrame()

    def to_history(self, event):
        history = HistoryFrame()

    def to_admin(self, event):
        admin = AdminFrame()

    def to_guide(self, event):
        dlg = GuideDialog(self.user)
        dlg.ShowModal()
        dlg.Destroy()

    # def OnSetFocus(self, e):
    #     print(e.GetEventObject().GetSize())

    

    