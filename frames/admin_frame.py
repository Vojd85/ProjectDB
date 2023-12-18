import wx
import db_controller
from ObjectListView import ObjectListView, ColumnDefn, Filter
from .panel import MyPanel
from models import User
from validators.not_empty import NotEmptyValidator
from validators.numbers_only import OneDigitValidator
from dialogs.change_pass import PasswordChange
from dialogs.change_level import ChangeLevelDialog




class AdminFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title="Администрирование", size=(600, 450))
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.GetParent().Show(False)
        self.setUI()
        self.setColumns()
        self.update_users()
        self.Center()
        self.Show()

    def setUI(self):
        panel = MyPanel(self)
        
        static_users = wx.StaticText(panel, label="Пользователи:")
        self.del_check = wx.CheckBox(panel, label="Удалённые")
        self.del_check.Bind(wx.EVT_CHECKBOX, self.filter)
        self.users = ObjectListView(panel, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.users.SetEmptyListMsg('Тут пока пусто...')
        static_create = wx.StaticText(panel, label="Создать пользователя")
        name = wx.StaticText(panel, label="Имя:")
        password = wx.StaticText(panel, label="Пароль:")
        re_pass = wx.StaticText(panel, label="Повторите:")
        level = wx.StaticText(panel, label="Уровень:")
        self.name = wx.TextCtrl(panel, validator=NotEmptyValidator())
        self.password = wx.TextCtrl(panel, style=wx.TE_PASSWORD, validator=NotEmptyValidator())
        self.re_pass = wx.TextCtrl(panel, style=wx.TE_PASSWORD, validator=NotEmptyValidator())
        self.level = wx.TextCtrl(panel, validator=OneDigitValidator())
        add_btn = wx.Button(panel, label='Добавить', size=(100,30))
        add_btn.Bind(wx.EVT_BUTTON, self.add_user)
        del_btn = wx.Button(panel, label='Удалить', size=(100,30))
        del_btn.Bind(wx.EVT_BUTTON, self.del_user)
        change_passwrd_btn = wx.Button(panel, label="Сменить пароль", size=(100,30))
        change_passwrd_btn.Bind(wx.EVT_BUTTON, self.change_password)
        change_level_btn = wx.Button(panel, label="Сменить уровень\nдоступа", size=(120,40))
        change_level_btn.Bind(wx.EVT_BUTTON, self.change_level)
        recover_btn = wx.Button(panel, label="Восстановить", size=(100,30))
        recover_btn.Bind(wx.EVT_BUTTON, self.recover_user)
        vert_line = wx.StaticLine(panel, size=(2, 400), style=wx.LI_VERTICAL)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        left_hor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer_4 = wx.BoxSizer(wx.HORIZONTAL)

        left_hor_sizer.Add(static_users, 1, wx.EXPAND|wx.ALL, 5)
        left_hor_sizer.Add(self.del_check, 1, wx.EXPAND|wx.ALL, 5)

        left_sizer.Add(left_hor_sizer, 1, wx.EXPAND|wx.ALL, 5)
        left_sizer.Add(self.users, 12, wx.EXPAND|wx.ALL, 5)

        hor_sizer_1.Add(name, 1, wx.ALL, 5)
        hor_sizer_1.Add(self.name, 1, wx.ALL, 5)
        hor_sizer_2.Add(password, 1, wx.ALL, 5)
        hor_sizer_2.Add(self.password, 1, wx.ALL, 5)
        hor_sizer_3.Add(re_pass, 1, wx.ALL, 5)
        hor_sizer_3.Add(self.re_pass, 1, wx.ALL, 5)
        hor_sizer_4.Add(level, 1, wx.ALL, 5)
        hor_sizer_4.Add(self.level, 1, wx.ALL, 5)

        right_sizer.Add(static_create, 0, wx.ALL, 5)
        right_sizer.Add(hor_sizer_1, 0, wx.EXPAND|wx.ALL, 5)
        right_sizer.Add(hor_sizer_2, 0, wx.EXPAND|wx.ALL, 5)
        right_sizer.Add(hor_sizer_3, 0, wx.EXPAND|wx.ALL, 5)
        right_sizer.Add(hor_sizer_4, 0, wx.EXPAND|wx.ALL, 5)
        right_sizer.Add(add_btn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        right_sizer.Add(wx.StaticLine(panel), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        right_sizer.Add(change_level_btn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        right_sizer.Add(change_passwrd_btn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        right_sizer.Add(recover_btn, wx.ALIGN_CENTER|wx.ALL, 5)
        right_sizer.Add(del_btn, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        main_sizer.Add(left_sizer, 1, wx.ALL, 5)
        main_sizer.Add(vert_line, -1, wx.TOP|wx.BOTTOM, 10)
        main_sizer.Add(right_sizer, 1, wx.ALL, 5)

        panel.SetSizer(main_sizer)

    def setColumns(self, data=None):
        self.users.SetColumns([
            ColumnDefn("Фамилия", "left", 200, "surname"),
            ColumnDefn("Уровень", "left", 80, "level")
        ])

    def update_users(self):
        self.users.SetObjects([User(*item) for item in db_controller.get_users('all')])
        self.user_filter = Filter.Predicate(self.active)
        self.users.SetFilter(self.user_filter)
        self.users.RepopulateList()

    def filter(self, event):
        if self.del_check.IsChecked():
            self.users.SetFilter(None)
        else:
            self.users.SetFilter(self.user_filter)
        self.users.RepopulateList()

    def add_user(self, event):
        if self.Validate():
            user_list = [item[0] for item in db_controller.get_users('all')]
            if self.name.GetValue() not in user_list:
                if self.password.GetValue() == self.re_pass.GetValue():
                    data = self.name.GetValue(), self.password.GetValue(), self.level.GetValue()
                    res = db_controller.add_user(data)
                    if res:
                        wx.MessageBox('Пользователь добавлен!', 'Успешно!', wx.OK | wx.ICON_INFORMATION)
                        self.clear_fields()
                        if self.del_check.IsChecked():
                            self.del_check.SetValue(False)
                        self.update_users()
                        self.users.RepopulateList()
                        return
                    else:
                        wx.MessageBox('Ошибка добавления пользователя', 'Внимание!', wx.OK | wx.ICON_ERROR)
                        return
                else:
                    wx.MessageBox('Пароли не совпадают!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                    self.password.Clear()
                    self.re_pass.Clear()
                    return
            else:
                wx.MessageBox('Пользователь уже существует!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                self.clear_fields()
                return
        else:
            return
        
    def del_user(self, event):
        if self.users.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали пользователя...', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.users.GetSelectedObject()
        dlg = wx.MessageDialog(self, 'Вы действительно хотите удалить?', 'Внимание!', wx.YES_NO|wx.ICON_EXCLAMATION)
        confirm = dlg.ShowModal()
        if confirm == wx.ID_YES:
            res = db_controller.delete_user(obj.id)
            if res:
                wx.MessageBox('Пользователь удалён!', 'Успешно!', wx.OK)
                self.update_users()
            else:
                wx.MessageBox('Ошибка удаления пользователя!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return
        elif confirm == wx.ID_NO:
            return
        
    def change_password(self, event):
        if self.users.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали пользователя...', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.users.GetSelectedObject()
        dlg = PasswordChange(obj)
        dlg.ShowModal()
        dlg.Destroy()

    def change_level(self, event):
        if self.users.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали пользователя...', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.users.GetSelectedObject()
        dlg = ChangeLevelDialog(obj)
        dlg.ShowModal()
        dlg.Destroy()

    def active(self, obj):
        return obj.active
    
    def clear_fields(self):
        self.name.Clear()
        self.password.Clear()
        self.re_pass.Clear()
        self.level.Clear()        

    def onClose(self, event):
        self.GetParent().Show(True)
        self.Destroy()

    def recover_user(self, event):
        if self.users.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали пользователя', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.users.GetSelectedObject()
        dlg = wx.MessageDialog(self, 'Вы действительно хотите восстановить пользователя?', 'Внимание!', wx.YES_NO|wx.ICON_EXCLAMATION)
        confirm = dlg.ShowModal()
        if confirm == wx.ID_YES:
            res = db_controller.recover_user(obj.id)
            if res:
                wx.MessageBox('Пользователь восстановлен!', 'Успешно!', wx.OK)
                self.update_users()
            else:
                wx.MessageBox('Ошибка восстановления пользователя!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return
        elif confirm == wx.ID_NO:
            return