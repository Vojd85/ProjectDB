import wx
from wx import adv
import os
import logging
from history_logger import history_logger
import datetime as dt
import db_controller
from frames.panel import MyPanel
from validators.numbers_only import NumberValidator
from validators.not_empty import NotEmptyValidator

logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), format='{asctime} {levelname} {funcName}->{lineno}: {msg}', style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExtraditionDialog(wx.Dialog):
    def __init__(self, obj, user):
        wx.Dialog.__init__(self, None, title='Выдача материала...', size=(400, 460))
        self.obj = obj
        self.user = user
        self.setUI()

    def setUI(self):
        panel = MyPanel(self)

        item = wx.StaticText(panel, label=f"{self.obj.name} {self.obj.type}")
        font = item.GetFont()
        item.SetFont(font.Bold())
        choice = wx.StaticText(panel, label=f"Единица:")
        value_lbl = wx.StaticText(panel, label=f"Значение:")
        self.users = [item[0] for item in db_controller.get_users()]
        # last_invoice = controller.get_last_invoice()
        if self.obj.count != None:
            self.choice = wx.StaticText(panel, label="Количество(шт)")
            self.option = 'count'
        else:
            self.choice = wx.StaticText(panel, label="Длина(м)")
            self.option = 'length'
        self.value = wx.TextCtrl(panel, size=(80, -1), validator=NumberValidator())
        order = wx.StaticText(panel, label="Заказ №:        ")
        invoice = wx.StaticText(panel, label="Требование №:")
        date = wx.StaticText(panel, label="Дата: ")
        self.date = adv.DatePickerCtrl(panel, style=adv.DP_DROPDOWN)
        master = wx.StaticText(panel, label="Затребовал:  ")
        worker = wx.StaticText(panel, label="Получил:      ")
        self.worker = wx.TextCtrl(panel, validator=NotEmptyValidator())
        plan = wx.StaticText(panel, label="Чертёж по СП:")
        self.order = wx.ComboBox(panel, value='Выбор',choices=['02483','02484', '02460', '02461', '08022', '01619'],style=wx.CB_SORT|wx.CB_READONLY)
        self.invoice = wx.TextCtrl(panel)
        # if last_invoice:
        #     if last_invoice.split('-')[0] != dt.date.today().strftime('%d/%m'):
        #         self.invoice.SetValue(dt.date.today().strftime('%d/%m') + '-1')
        #     else:
        #         self.invoice.SetValue(last_invoice.split('-')[0] + '-' + str(int(last_invoice.split('-')[1]) + 1))
        # else:
        #     self.invoice.SetValue(dt.date.today().strftime('%d/%m') + '-1')
        self.master = wx.ComboBox(panel, value='Выбор', choices=self.users, style=wx.CB_SORT|wx.CB_READONLY)
        self.plan = wx.TextCtrl(panel)
    
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(choice, 1,  wx.ALL|wx.EXPAND, 10)
        sizer_1.AddSpacer(30)
        sizer_1.Add(value_lbl, 1, wx.ALL|wx.EXPAND, 10)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.choice, wx.CENTER)
        sizer_2.AddSpacer(20)
        sizer_2.Add(self.value)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(order, 1, wx.ALL|wx.CENTER, 10)
        sizer_3.Add(self.order, 2, wx.ALL, 10)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(invoice, 0, wx.ALL|wx.CENTER, 10)
        sizer_4.Add(self.invoice, 0, wx.CENTER)
        sizer_4.Add(date, 0, wx.ALL|wx.CENTER, 10)
        sizer_4.Add(self.date, 0, wx.ALL, 10)

        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(master, 1, wx.ALL|wx.CENTER, 10)
        sizer_5.Add(self.master, 2, wx.ALL, 10)

        sizer_5_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_1.Add(worker, 1, wx.ALL|wx.CENTER, 10)
        sizer_5_1.Add(self.worker, 2, wx.ALL, 12)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(plan, 1, wx.ALL|wx.CENTER, 10)
        sizer_6.Add(self.plan, 2, wx.ALL|wx.CENTER, 2)

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
        main_sizer.Add(sizer_1, 1, wx.CENTRE)
        main_sizer.Add(sizer_2, 1, wx.CENTRE)
        main_sizer.Add(wx.StaticLine(panel), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        main_sizer.Add(sizer_3, 1)
        main_sizer.Add(sizer_4, 1)
        main_sizer.Add(sizer_5, 1)
        main_sizer.Add(sizer_5_1, 1)
        main_sizer.Add(sizer_6, 1)
        main_sizer.Add(wx.StaticLine(panel), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        main_sizer.Add(sizer_btn, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=15)

        panel.SetSizer(main_sizer)

    def update_record(self, event):
        if self.Validate():
            try:
                if self.option == 'count' and int(self.value.GetValue()) > self.obj.count or \
                    self.option == 'length' and float(self.value.GetValue().replace(',', '.')) > self.obj.length:
                    wx.MessageBox('Недостаток материала', 'Внимание!', wx.OK | wx.ICON_ERROR)
                    self.value.Clear()
                    return
                if self.option == 'count':
                    value = int(self.value.GetValue())
                    obj_value = int(self.obj.count)
                elif self.option == 'length':
                    value = float(self.value.GetValue().replace(',', '.'))
                    obj_value = float(self.obj.length)
            except ValueError as e:
                print(e)
                wx.MessageBox(f'Неправильное значение {self.value.GetValue()}', 'Ошибка!', wx.OK | wx.ICON_ERROR)
                logger.exception(f'Неправильное значение {self.value.GetValue()}')
                return
            requirement = self.date.GetValue().Format("%m/%d") + '-' + self.invoice.GetValue()
            data = self.obj.id, self.option, value, self.order.GetValue(), requirement, self.master.GetValue(), self.plan.GetValue(), self.user, self.worker.GetValue()
            res = db_controller.update(data, predicat='-')
            if res:
                wx.MessageBox('Операция выполнена!', 'Успешно!', wx.OK)
                history_logger.info(f"Выдача позиции {self.obj.plan} {self.obj.name} {self.obj.type} {self.obj.mat} {self.obj.size} в кол-ве {value}. Остаток: {obj_value - value}. Оформил: {self.user}")
                self.Destroy()
            else:
                wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return

    def on_close(self, event):
        self.Destroy()


if __name__ == "__main__":
    
    app = wx.App(False)
    frame = ExtraditionDialog()
    app.MainLoop()