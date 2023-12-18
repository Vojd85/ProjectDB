import wx
import db_controller
from validators.numbers_only import OneDigitValidator


class ChangeLevelDialog(wx.Dialog):
    def __init__(self, obj):
        """Constructor"""
        wx.Dialog.__init__(self, None, title=f"Смена уровня пользователя {obj.surname}", size=(300, 140))
        self.obj = obj

        lvl_lbl = wx.StaticText(self, label="Введите уровень:    ")
        self.level = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, validator=OneDigitValidator())
        self.level.Bind(wx.EVT_TEXT_ENTER, self.change_lvl)
        btn = wx.Button(self, label="Изменить уровень")
        btn.Bind(wx.EVT_BUTTON, self.change_lvl)

        level_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        level_sizer.Add(lvl_lbl, 0, wx.ALL|wx.CENTER, 5)
        level_sizer.Add(self.level, 0, wx.ALL, 9)

        main_sizer.Add(level_sizer, 0, wx.ALL, 5)
        main_sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)

        self.SetSizer(main_sizer)
        self.Center()

    def change_lvl(self, event):
        if self.Validate():
            value = int(self.level.GetValue())
            if value > 9:
                wx.MessageBox('Уровень не может быть более 9!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return
            data = self.obj.id, value
            res = db_controller.change_lvl(data)
            if res:
                wx.MessageBox('Уровень изменён!', 'Успешно!', wx.OK)
                self.Destroy()
            else:
                wx.MessageBox('Ошибка изменения уровня!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return