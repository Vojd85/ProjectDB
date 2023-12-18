import wx
import db_controller
from validators.not_empty import NotEmptyValidator


class PasswordChange(wx.Dialog):
    def __init__(self, obj):
        """Constructor"""
        wx.Dialog.__init__(self, None, title=f"Смена пароля пользователя {obj.surname}", size=(300, 180))
        self.obj = obj
 
        pass_lbl = wx.StaticText(self, label="Введите пароль:    ")
        self.passwrd = wx.TextCtrl(self, style=wx.TE_PASSWORD, validator=NotEmptyValidator())
        re_pass_lbl = wx.StaticText(self, label="Повторите пароль:")
        self.re_pass = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER, validator=NotEmptyValidator())
        self.re_pass.Bind(wx.EVT_TEXT_ENTER, self.change_pass)
        btn = wx.Button(self, label="Изменить пароль")
        btn.Bind(wx.EVT_BUTTON, self.change_pass)

        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        re_pass_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        password_sizer.Add(pass_lbl, 0, wx.ALL|wx.CENTER, 5)
        password_sizer.Add(self.passwrd, 0, wx.ALL, 9)
        
        re_pass_sizer.Add(re_pass_lbl, 0, wx.ALL|wx.CENTER, 5)
        re_pass_sizer.Add(self.re_pass, 0, wx.ALL, 5) 
        
        main_sizer.Add(password_sizer, 0, wx.ALL, 5)
        main_sizer.Add(re_pass_sizer, 0, wx.ALL, 5)
        main_sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
 
        self.SetSizer(main_sizer)
        self.Center()

    def change_pass(self, event):
        if self.Validate():
            if self.passwrd.GetValue() == self.re_pass.GetValue():
                data = self.obj.id, self.passwrd.GetValue()
                res = db_controller.change_password(data)
                if res:
                    wx.MessageBox('Пароль изменён!', 'Успешно!', wx.OK)
                    self.Destroy()
                else:
                    wx.MessageBox('Ошибка изменения пароля!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                    return
            else:
                wx.MessageBox('Пароли не совпадают!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                self.passwrd.Clear()
                self.re_pass.Clear()
                return