import wx
import os
import db_controller
import logging
from history_logger import history_logger
from frames.panel import MyPanel
from validators.not_empty import NotEmptyValidator
from validators.numbers_only import NumberValidator

logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), format='{asctime} {levelname} {funcName}->{lineno}: {msg}', style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class InsertDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title='Добавление материала...', size=(400, 280))
        self.setUI()

    def setUI(self):
        panel = MyPanel(self)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        plan_lbl = wx.StaticText(panel, label="Чертёж:")
        name_lbl = wx.StaticText(panel, label="Наименование:")
        type_lbl = wx.StaticText(panel, label="Тип:")
        mat_lbl = wx.StaticText(panel, label="Материал:")
        size_lbl = wx.StaticText(panel, label="Размер:")
        comment_lbl = wx.StaticText(panel, label="Комментарий:")
        left_sizer.Add(plan_lbl, 1, wx.ALL, 5)
        left_sizer.Add(name_lbl, 1, wx.ALL, 5)
        left_sizer.Add(type_lbl, 1, wx.ALL, 5)
        left_sizer.Add(mat_lbl, 1, wx.ALL, 5)
        left_sizer.Add(size_lbl, 1, wx.ALL, 5)
        left_sizer.Add(comment_lbl, 1, wx.ALL, 5)

        self.plan = wx.TextCtrl(panel, size=(200, -1))
        self.name = wx.TextCtrl(panel, validator=NotEmptyValidator(), size=(200, -1))
        self.type = wx.TextCtrl(panel, validator=NotEmptyValidator(), size=(200, -1))
        self.mat = wx.TextCtrl(panel, validator=NotEmptyValidator())
        self.size = wx.TextCtrl(panel)
        self.comment = wx.TextCtrl(panel, size=(200, -1))
        right_sizer.Add(self.plan, 1, wx.ALL)
        right_sizer.AddSpacer(3)
        right_sizer.Add(self.name, 1, wx.ALL)
        right_sizer.AddSpacer(3)
        right_sizer.Add(self.type, 1, wx.ALL)
        right_sizer.AddSpacer(3)
        right_sizer.Add(self.mat, 1, wx.ALL|wx.ALIGN_LEFT)
        right_sizer.AddSpacer(3)
        right_sizer.Add(self.size, 1, wx.ALL|wx.ALIGN_LEFT)
        right_sizer.AddSpacer(3)
        right_sizer.Add(self.comment, 1, wx.ALL|wx.ALIGN_LEFT)

        sizer_1.Add(left_sizer, 1, wx.ALL, 5)
        sizer_1.Add(right_sizer, 2, wx.ALL, 5)

        # sizer_6 = wx.BoxSizer(wx.HORIZONTAL)

        # choice = wx.StaticText(panel, label=f"Выбор единицы:")
        # value = wx.StaticText(panel, label=f"Значение:")
        # sizer_6.Add(choice, 1,  wx.ALL|wx.EXPAND, 5)
        # sizer_6.AddSpacer(30)
        # sizer_6.Add(value, 1, wx.ALL|wx.EXPAND, 5)

        # sizer_6_1 = wx.BoxSizer(wx.HORIZONTAL)

        # self.choice = wx.ComboBox(panel, value='Выбор',choices=['Количество', 'Длина'],style=wx.CB_SORT|wx.CB_READONLY, validator=NotEmptyValidator())
        # self.value = wx.TextCtrl(panel, validator=NumberValidator())
        # sizer_6_1.Add(self.choice)
        # sizer_6_1.AddSpacer(30)
        # sizer_6_1.Add(self.value)

        # sizer_7 = wx.BoxSizer(wx.HORIZONTAL)

        # invoice_lbl = wx.StaticText(panel, label="Накладная №:")
        # self.invoice = wx.TextCtrl(panel)
        # sizer_7.Add(invoice_lbl, 1, wx.ALL|wx.CENTER, 5)
        # sizer_7.Add(self.invoice, 2, wx.ALL, 5)

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)

        ok_btn = wx.Button(panel, label='Подтвердить')
        ok_btn.Bind(wx.EVT_BUTTON, self.add_record)
        cnl_btn = wx.Button(panel, label='Отмена')
        cnl_btn.Bind(wx.EVT_BUTTON, self.on_close)
        sizer_btn.Add(ok_btn)
        sizer_btn.AddSpacer(20)
        sizer_btn.Add(cnl_btn)
        

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(sizer_1, 1, wx.TOP|wx.LEFT|wx.RIGHT, 10)
        # main_sizer.Add(sizer_6, 1, wx.CENTRE)
        # main_sizer.Add(sizer_6_1, 1, wx.CENTRE)
        # main_sizer.Add(sizer_7)
        main_sizer.Add(sizer_btn, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=20)

        panel.SetSizer(main_sizer)

    def add_record(self, event):
        if self.Validate():
            # if self.choice.GetValue() == 'Количество':
            #     choice = 'count'
            #     try:
            #         value = int(self.value.GetValue())
            #     except ValueError:
            #         wx.MessageBox('Количество должно быть целым числом!', 'Внимание!', wx.OK | wx.ICON_ERROR)
            #         logger.exception(f'Неправильное значение {self.value.GetValue()}')
            #         return
            # elif self.choice.GetValue() == 'Длина':
            #     choice = 'length'
            #     value = float(self.value.GetValue().replace(',', '.'))
            data = self.plan.GetValue(), self.name.GetValue(), self.type.GetValue(), self.mat.GetValue(), self.size.GetValue(), self.comment.GetValue()
            res = db_controller.insert(data)
            if res:
                wx.MessageBox('Операция выполнена!', 'Успешно!', wx.OK)
                # history_logger.info(f"Добавление позиции {data[0]} {data[1]} {data[2]} {data[3]} {data[4]} в кол-ве {value}. Оформил: {self.user}")
                self.Destroy()
            else:
                wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return
        
    def on_close(self, event):
        self.Destroy()