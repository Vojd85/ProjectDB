import wx
from wx import adv
import os
import db_controller
import logging
from history_logger import history_logger
from frames.panel import MyPanel
from validators.numbers_only import NumberValidator

logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), format='{asctime} {levelname} {funcName}->{lineno}: {msg}', style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReceivingDialog(wx.Dialog):
    def __init__(self, obj, user):
        wx.Dialog.__init__(self, None, title='Приход материала...', size=(400, 280))
        self.user = user
        self.obj = obj
        self.setUI()

    def setUI(self):
        panel = MyPanel(self)

        item = wx.StaticText(panel, label=f"{self.obj.name} {self.obj.type}")
        font = item.GetFont()
        item.SetFont(font.Bold())
        choice = wx.StaticText(panel, label=f"Единица:")
        value = wx.StaticText(panel, label=f"Значение:")
        self.value = wx.TextCtrl(panel, size=(80, -1), validator=NumberValidator())
        invoice = wx.StaticText(panel, label=f"Накладная №:  ")
        self.invoice = wx.TextCtrl(panel)
        date = wx.StaticText(panel, label="Дата: ")
        self.date = adv.DatePickerCtrl(panel, style=adv.DP_DROPDOWN)
        if self.obj.count != None:
            self.choice = wx.StaticText(panel, label=f"Количество(шт)")
            self.option = 'count'
        else:
            self.choice = wx.StaticText(panel, label=f"Длина(м)")
            self.option = 'length'

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(choice, 1,  wx.ALL|wx.EXPAND, 10)
        sizer_1.AddSpacer(30)
        sizer_1.Add(value, 1, wx.ALL|wx.EXPAND, 10)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.choice)
        sizer_2.AddSpacer(20)
        sizer_2.Add(self.value)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(invoice, 1, wx.ALL|wx.CENTER, 5)
        sizer_3.Add(self.invoice, 1, wx.ALL|wx.CENTER, 5)
        sizer_3.Add(date, 1, wx.ALL|wx.CENTER, 5)
        sizer_3.Add(self.date, 1, wx.ALL|wx.CENTER, 5)
                

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, label='Подтвердить')
        ok_btn.Bind(wx.EVT_BUTTON, self.update_record)
        cnl_btn = wx.Button(panel, label='Отмена')
        cnl_btn.Bind(wx.EVT_BUTTON, self.on_close)
        sizer_btn.Add(ok_btn)
        sizer_btn.AddSpacer(20)
        sizer_btn.Add(cnl_btn)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(item,1, wx.ALL|wx.ALIGN_CENTRE, 20)
        main_sizer.Add(wx.StaticLine(panel), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        main_sizer.Add(sizer_1, 1, wx.ALL|wx.CENTRE, 5)
        main_sizer.Add(sizer_2, 1, wx.ALL|wx.CENTRE, 5)
        main_sizer.Add(sizer_3, 1, wx.ALL|wx.CENTRE, 5)
        main_sizer.Add(wx.StaticLine(panel), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        main_sizer.Add(sizer_btn, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=20)

        panel.SetSizer(main_sizer)

    def update_record(self, event):
        if self.Validate():
            if self.option == 'count':
                try:
                    value = int(self.value.GetValue())
                    obj_value = int(self.obj.count)
                except ValueError:
                    wx.MessageBox('Количество должно быть целым числом!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                    logger.exception(f'Неправильное значение {self.value.GetValue()}')
                    return
            elif self.option == 'length':
                value = float(self.value.GetValue().replace(',', '.'))
                obj_value = float(self.obj.length)
            invoice = self.date.GetValue().Format("%m/%d") + '-' + self.invoice.GetValue()
            data = self.obj.id, self.option, value, None, invoice, None, None, self.user, None
            res = db_controller.update(data, predicat='+')
            if res:
                wx.MessageBox('Операция выполнена!', 'Успешно!', wx.OK)
                history_logger.info(f"Приход позиции {self.obj.plan} {self.obj.name} {self.obj.type} {self.obj.mat} {self.obj.size} в кол-ве {value}. Остаток: {obj_value + value}. Оформил: {self.user}")
                self.Destroy()
            else:
                wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return

    def on_close(self, event):
        self.Destroy()