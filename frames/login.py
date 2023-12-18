import wx
import db_controller


class LoginDialog(wx.Dialog):
    """
    Класс диалогового окна входа пользователя
    """
 
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Вход в систему",size=(300, 180))
        self.login = False
 
        # Ввод имени пользователя
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user_lbl = wx.StaticText(self, label="Пользователь: ")
        self.user = wx.TextCtrl(self)
        user_sizer.Add(user_lbl, 0, wx.ALL|wx.CENTER, 5)
        user_sizer.Add(self.user, 0, wx.ALL, 5)
 
        # Ввод пароля пользователя
        p_sizer = wx.BoxSizer(wx.HORIZONTAL)
        p_lbl = wx.StaticText(self, label="Пароль:            ")
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.password.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        p_sizer.Add(p_lbl, 0, wx.ALL|wx.CENTER, 6)
        p_sizer.Add(self.password, 0, wx.ALL, 5)
 
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(user_sizer, 0, wx.ALL, 5)
        main_sizer.Add(p_sizer, 0, wx.ALL, 5)
 
        btn = wx.Button(self, label="Войти")
        btn.Bind(wx.EVT_BUTTON, self.onLogin)
        main_sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
 
        self.SetSizer(main_sizer)
        self.Center()
 
    def onLogin(self, event):
        user_name = self.user.GetValue()
        user_password = self.password.GetValue()
        self.login = db_controller.login(user_name, user_password)
        if self.login == None:
            wx.MessageBox('Ошибка подключения к базе данных!', 'Ошибка!', wx.OK | wx.ICON_ERROR)
        elif self.login:
            self.Close() 
        else:
            wx.MessageBox('Неверные имя пользователя или пароль!', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        
        