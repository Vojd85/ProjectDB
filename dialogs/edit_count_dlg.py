import wx
import db_controller
from validators.numbers_only import NumberValidator


class EditCountDialog(wx.Dialog):
    def __init__(self, obj):
        wx.Dialog.__init__(self, None, title="Редактирование количества")
        self.obj = obj
        if self.obj.count != None:
            self.choice = wx.StaticText(self, label=f"Количество")
            self.option = 'count'
        else:
            self.choice = wx.StaticText(self, label=f"Длина")
            self.option = 'length'
        self.value = wx.TextCtrl(self, validator=NumberValidator())
        ok_btn = wx.Button(self, label='Подтвердить')
        ok_btn.Bind(wx.EVT_BUTTON, self.update_record)
        cnl_btn = wx.Button(self, label='Отмена')
        cnl_btn.Bind(wx.EVT_BUTTON, self.on_close)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.choice, 0, wx.ALL|wx.CENTER, 15)
        sizer_1.Add(self.value, 0, wx.ALL, 15)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(ok_btn)
        btn_sizer.AddSpacer(20)
        btn_sizer.Add(cnl_btn)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(sizer_1, 0, wx.ALL, 5)
        main_sizer.Add(btn_sizer, 0, wx.ALL, 5)
 
        self.SetSizer(main_sizer)
        self.Center()

    def update_record(self, event):
        if self.option == 'count':
                try:
                    value = int(self.value.GetValue())
                except ValueError:
                    wx.MessageBox('Количество должно быть целым числом!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                    return
        elif self.option == 'length':
            value = float(self.value.GetValue().replace(',', '.'))
        data = self.obj.id, self.option, value
        res = db_controller.edit_record(data)
        if res:
            wx.MessageBox('Операция выполнена!', 'Успешно!', wx.OK)
            self.Destroy()
        else:
            wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
            return
        
    def on_close(self, event):
        self.Destroy()