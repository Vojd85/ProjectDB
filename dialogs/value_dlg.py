import wx
import db_controller
from frames.panel import MyPanel
from validators.not_empty import NotEmptyValidator



class ChooseValueDialog(wx.Dialog):
    def __init__(self, obj):
        wx.Dialog.__init__(self, None, title="Выбор значения",size=(300, 180))

        self.obj = obj

        panel = MyPanel(self)

        statictext = wx.StaticText(panel, label="Выберите единицу измерения:")
        self.choice = wx.ComboBox(panel, value='Выбор',choices=['Количество(шт)', 'Длина(м)'],style=wx.CB_SORT|wx.CB_READONLY, validator=NotEmptyValidator())
        self.choice.SetHelpText("Выбор...")

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)

        ok_btn = wx.Button(panel, label='Подтвердить')
        ok_btn.Bind(wx.EVT_BUTTON, self.add_record)
        cnl_btn = wx.Button(panel, label='Отмена')
        cnl_btn.Bind(wx.EVT_BUTTON, self.on_close)
        sizer_btn.Add(ok_btn)
        sizer_btn.AddSpacer(20)
        sizer_btn.Add(cnl_btn)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(statictext, 1, wx.TOP|wx.BOTTOM|wx.CENTER, 20)
        main_sizer.Add(self.choice, 0, wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.Add(sizer_btn, 1, wx.TOP|wx.BOTTOM|wx.CENTER, 20)

        panel.SetSizer(main_sizer)

    def add_record(self, event):
        if self.Validate():
            # flag = ''
            if self.choice.GetValue() == 'Количество(шт)':
                flag = 'count'
            if self.choice.GetValue() == 'Длина(м)':
                flag = 'length'
            res = db_controller.add_to_base(self.obj.id, flag)
            if res:
                wx.MessageBox('Операция выполнена!', 'Успешно!', wx.OK)
                self.Destroy()
            else:
                wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return


    def on_close(self, event):
        self.Destroy()
