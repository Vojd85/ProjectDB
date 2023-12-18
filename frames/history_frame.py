import wx
import os
import logging
from wx import adv
import datetime as dt
import db_controller
from ObjectListView import ObjectListView, ColumnDefn, Filter
from .panel import MyPanel
from models import Record
from print_controller import Printer
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), format='{asctime} {levelname} {funcName}->{lineno}: {msg}', style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("templates/test.html")


class HistoryFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title="История", size=(1400, 800))
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.GetParent().Show(False)
        self.setUI()
        self.printer = Printer(self)
        self.Center()
        self.Show()
        
    def setUI(self):
        panel = MyPanel(self)
        self.data = self.type = self.names = self.order = self.inv = self.req =  []
        self.history = ObjectListView(panel, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.history.SetEmptyListMsg('Тут пока пусто...')
        self.setColumns()
        self.history.AutoSizeColumns()
        self.update_search_fields()
        self.name_filter = None
        self.type_filter = None
        self.order_filter = None
        self.invoice_filter = None
        self.requirement_filter = None
        self.filter1 = None
        self.filter2 = None
        
        staticbox = wx.StaticBox (panel, wx.NewId(), label="Критерии поиска")
        sizer_1 = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
        search_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        staticbox2 = wx.StaticBox (panel, wx.NewId(), label="Операции")
        right_sizer = wx.StaticBoxSizer(staticbox2, wx.VERTICAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.ch1=wx.ComboBox(panel, value='Наименование',choices=self.names,style=wx.CB_SORT)
        self.ch1.Bind(wx.EVT_TEXT, self.name_search)
        self.ch2=wx.ComboBox(panel, value='Тип',choices=self.type,style=wx.CB_SORT|wx.TE_PROCESS_ENTER)
        self.ch2.Bind(wx.EVT_TEXT, self.type_search)
        self.ch3= wx.ComboBox(panel, value='Заказ №',choices=self.order,style=wx.CB_DROPDOWN)
        self.ch3.Bind(wx.EVT_COMBOBOX, self.order_search)
        self.date_begin = adv.DatePickerCtrl(panel, style=adv.DP_DROPDOWN)
        self.date_begin.Bind(adv.EVT_DATE_CHANGED, self.date_filter_begin)
        self.date_end = adv.DatePickerCtrl(panel, style=adv.DP_DROPDOWN)
        self.date_end.Bind(adv.EVT_DATE_CHANGED, self.date_filter_end)
        self.ch4 = wx.ComboBox(panel, value='Накладная №', choices=self.inv, style=wx.CB_SORT, size=(200, -1))
        self.ch4.Bind(wx.EVT_TEXT, self.invoice_search)
        self.ch5 = wx.ComboBox(panel, value='Требование №', choices=self.req, style=wx.CB_SORT, size=(200, -1))
        self.ch5.Bind(wx.EVT_TEXT, self.requirement_search)
        btn_update = wx.Button(panel, wx.NewId(), "Обновить базу", size=(120, 60))
        btn_update.Bind(wx.EVT_BUTTON, self.update_history)
        btn_print = wx.Button(panel, wx.NewId(), "Печать\nнакладной", size=(120, 60))
        btn_print.Bind(wx.EVT_BUTTON, self.print_invoice)
        

        search_sizer_1.Add(self.ch1, 1, wx.ALL|wx.FIXED_MINSIZE, 10)
        search_sizer_1.Add(self.ch2, 1, wx.ALL|wx.FIXED_MINSIZE, 10)
        search_sizer_1.Add(self.ch3, 1, wx.ALL|wx.FIXED_MINSIZE, 10)
        search_sizer_1.Add(self.date_begin, 0, wx.ALL|wx.FIXED_MINSIZE, 10)
        search_sizer_1.Add(self.date_end, 0, wx.ALL|wx.FIXED_MINSIZE, 10)
        search_sizer_2.Add(self.ch4, 1, wx.ALL|wx.FIXED_MINSIZE, 10)
        search_sizer_2.Add(self.ch5, 1, wx.ALL|wx.FIXED_MINSIZE, 10)
        sizer_1.Add(search_sizer_1, 1, wx.EXPAND|wx.ALL)
        sizer_1.Add(search_sizer_2, 1,)
        left_sizer.Add(sizer_1, 1, wx.EXPAND|wx.ALL, 5)
        left_sizer.Add(self.history, 8, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
        right_sizer.Add(btn_update, 0, wx.SHAPED|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        right_sizer.Add(btn_print, 0, wx.SHAPED|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_sizer, 8, wx.ALL|wx.FIXED_MINSIZE, 5)
        main_sizer.Add(right_sizer, 1, wx.EXPAND|wx.ALL, 10)

        panel.SetSizer(main_sizer)

        self.update_history()

    def setColumns(self, data=None):
        self.history.SetColumns([
            ColumnDefn("Чертеж", "left", 120, "plan"),
            ColumnDefn("Наименование", "left", 120, "name"),
            ColumnDefn("Тип", "left", 150, "type"),
            ColumnDefn("Материал", "left", 100, "mat"),
            ColumnDefn("Размер", "left", 80, "size"),
            ColumnDefn("Количество(шт)", "left", 110, "count"),
            ColumnDefn("Длина(м)", "left", 80, "length"),
            ColumnDefn("Накладная", "left", 80, "invoice"),
            ColumnDefn("Требование", "left", 80, "requirement"),
            ColumnDefn("Заказ №", "left", 100, "order"),
            ColumnDefn("Мастер", "left", 100, "master"),
            ColumnDefn("Получил", "left", 100, "receive"),
            ColumnDefn("Чертёж по СП", "left", 100, "plan_order"),
            ColumnDefn("Время", "left", 100, "date"),
            ColumnDefn("Работник", "left", 100, "worker")
            
        ])

    def update_history(self, event=None):
        session = db_controller.connect_to_DB()
        if session:
            query = "SELECT history.id, plan, name, type, material, size, history.count, history.length, \
                weigth, datetime, invoice, requirement, history.order, plan_order, history.master, receive, worker \
                FROM material INNER JOIN history ON material.id = history.item_id"
            try:
                with session.conn.cursor() as cursor:
                    cursor.execute(query)
                    self.data = [Record(*item) for item in cursor.fetchall()]
                    self.history.SetObjects(self.data)
                    self.history.SetFilter(None)
                    self.history.RepopulateList()
                    self.ch1.SetLabel('Наименование')
                    self.ch2.SetLabel('Тип')
                    self.ch3.SetLabel('Заказ №')
                    self.ch4.SetLabel('Накладная №')
                    self.ch5.SetLabel('Требование №')
                    self.date_begin.Value = wx.DateTime.Now()
                    self.date_end.Value = wx.DateTime.Now()
            except Exception as e:
                print(e)
                logger.exception('Ошибка БД')
            finally:
                session.conn.close()
        else:
            wx.MessageBox('Ошибка загрузки данных', 'Внимание!', wx.OK | wx.ICON_ERROR)

    def update_search_fields(self):
        try:
            self.names, self.type, self.order, self.inv, self.req = db_controller.update_search_fields('history')
            if '' in self.names:
                self.names.remove('')
            if '' in self.type:
                self.type.remove('')
            if '' in self.order:
                self.order.remove('')
            if None in self.order:
                self.order.remove(None)
            if None in self.inv:
                self.inv.remove(None)
            if None in self.req:
                self.req.remove(None)
        except Exception as e:
            logger.exception(f'Ошибка получения полей из контроллера: {e}')

    def print_invoice(self, event):
        if self.history.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.history.GetSelectedObject()
        data = db_controller.get_invoice_obj(obj)
        if data:
            html_invoice = template.render({'items': data[:6],'order': data[0][7], 
                                            'invoice': data[0][6], 'master': data[0][8], 
                                            'worker': data[0][9], 
                                            'date': dt.date.today().strftime('%d.%m.%y')})
            self.printer.preview_text(html_invoice)

    def name_search(self, category):
        
        keyword = self.ch1.GetValue()
        self.name_filter = Filter.TextSearch(self.history, columns=self.history.columns[1:2], text=keyword)
        self.filter_refresh()

    def type_search(self, category):
        
        keyword = self.ch2.GetValue()
        self.type_filter = Filter.TextSearch(self.history, columns=self.history.columns[2:3], text=keyword)
        self.filter_refresh()

    def order_search(self, category):
        
        keyword = self.ch3.GetValue()
        self.order_filter = Filter.TextSearch(self.history, columns=self.history.columns[9:10], text=keyword)
        self.filter_refresh()

    def invoice_search(self, category):
        keyword = self.ch4.GetValue()
        self.invoice_filter = Filter.TextSearch(self.history, columns=self.history.columns[7:8], text=keyword)
        self.filter_refresh()

    def requirement_search(self, category):
        keyword = self.ch5.GetValue()
        self.requirement_filter = Filter.TextSearch(self.history, columns=self.history.columns[8:9], text=keyword)
        self.filter_refresh()

    def filter_refresh(self):
        filters = set([self.name_filter, self.type_filter, self.order_filter, self.invoice_filter, self.requirement_filter, self.filter1, self.filter2])
        filters.discard(None)
        self.history.SetFilter(Filter.Chain(*filters))
        self.history.RepopulateList()

    def date_filter_begin(self, event):
        wxdate = self.date_begin.GetValue().Format("%Y-%m-%d")
        self.begin_date = dt.datetime(*map(int, wxdate.split('-')))
        self.filter1 = Filter.Predicate(self.more)
        self.filter_refresh()
    
    def date_filter_end(self, event):
        wxdate = self.date_end.GetValue().Format("%Y-%m-%d")
        self.end_date = dt.datetime(*map(int, wxdate.split('-')), hour=23, minute=59, second=59)
        self.filter2 = Filter.Predicate(self.less)
        self.filter_refresh()

    def less(self, obj):
        return obj.date <= self.end_date
    
    def more(self, obj):
        return obj.date >= self.begin_date

    def onClose(self, event):
        self.GetParent().Show(True)
        self.Destroy()