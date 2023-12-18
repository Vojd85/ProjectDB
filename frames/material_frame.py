import wx
import os
import logging
from ObjectListView import ObjectListView, ColumnDefn, Filter
import db_controller
from .panel import MyPanel
from models import Material
from dialogs.extradition_dlg import ExtraditionDialog
from dialogs.insert_dlg import InsertDialog
from dialogs.receiveing_dlg import ReceivingDialog
from dialogs.edit_dlg import EditDialog
from dialogs.edit_count_dlg import EditCountDialog
from dialogs.guide_dlg import GuideDialog

logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), format='{asctime} {levelname} {funcName}->{lineno}: {msg}', style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SecondFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title="Полный перечень материалов", size=(1360, 800))
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.GetParent().Show(False)
        self.setUI()
        if self.GetParent().level > 1:
            self.btn_del.Disable()
        if self.GetParent().level > 2:
            self.btn_receive.Disable()
            self.btn_add.Disable()
            self.btn_edit.Disable()
        if self.GetParent().level > 3:
            self.btn_extrad.Disable()
            

    def setUI(self):    
        panel = MyPanel(self)
        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.type = self.names = self.mat = []
        self.plan_filter = None
        self.name_filter = None
        self.type_filter = None
        self.mat_filter = None
        self.material = ObjectListView(panel, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.material.SetEmptyListMsg('Тут пока пусто...')
        self.setColumns()
        self.update_search_fields()
        
        staticbox = wx.StaticBox (panel, wx.NewId(), label="Критерии поиска")
        sizer_1 = wx.StaticBoxSizer(staticbox, wx.HORIZONTAL)

        self.ch = wx.ComboBox(panel, value="Чертёж", choices=['ИМЛТ', 'ТЛИШ', 'ГОСТ', 'ДВИЕ', 'КЛИГ'], size=(80, 20),style=wx.CB_SORT)
        self.ch.Bind(wx.EVT_TEXT, self.plan_search)
        self.ch1=wx.ComboBox(panel, value='Наименование',choices=self.names,style=wx.CB_SORT)
        self.ch1.Bind(wx.EVT_TEXT, self.name_search)
        self.ch2=wx.ComboBox(panel, value='Тип',choices=self.type,style=wx.CB_SORT)
        self.ch2.Bind(wx.EVT_TEXT, self.type_search)
        self.ch3=wx.ComboBox(panel, value='Материал',choices=self.mat,style=wx.CB_SORT)
        self.ch3.SetSize(120, 20)
        self.ch3.Bind(wx.EVT_TEXT, self.mat_search)
        btn_all = wx.Button(panel, wx.NewId(), "Обновить базу")
        btn_all.SetSize(130, 20)
        btn_all.Bind(wx.EVT_BUTTON, self.update_base)

        # self.btn_edit_count = wx.Button(panel, wx.NewId(), "Изменить\nколичество")
        # self.btn_edit_count.Bind(wx.EVT_BUTTON, self.edit_value)
        self.btn_extrad = wx.Button(panel, wx.NewId(), "Выдать\nматериал", size=(120, 60))
        self.btn_extrad.Bind(wx.EVT_BUTTON, self.extradition)
        self.btn_receive = wx.Button(panel, wx.NewId(), "Приход\nматериала", size=(120, 60))
        self.btn_receive.Bind(wx.EVT_BUTTON, self.receiving)
        # self.btn_add = wx.Button(panel, wx.NewId(), "Добавить\nпозицию")
        # self.btn_add.Bind(wx.EVT_BUTTON, self.insert)
        # self.btn_edit = wx.Button(panel, wx.NewId(), "Редактировать\nпозицию")
        # self.btn_edit.Bind(wx.EVT_BUTTON, self.edit)
        self.btn_del = wx.Button(panel, wx.NewId(), "Удалить", size=(120, 60))
        self.btn_del.Bind(wx.EVT_BUTTON, self.remove)

        sizer_1.Add(self.ch, 0, wx.ALL|wx.FIXED_MINSIZE, 10)
        sizer_1.Add(self.ch1, 1, wx.ALL|wx.FIXED_MINSIZE, 10)
        sizer_1.Add(self.ch2, 1, wx.ALL|wx.FIXED_MINSIZE, 10)
        sizer_1.Add(self.ch3, 0, wx.ALL|wx.FIXED_MINSIZE, 10)
        sizer_1.Add(btn_all, 0, wx.ALL|wx.EXPAND, 5)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(sizer_1, 1, wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM, 20)
        left_sizer.Add(self.material, 8, wx.EXPAND|wx.LEFT|wx.BOTTOM, 20)

        staticbox2 = wx.StaticBox (panel, wx.NewId(), label="Операции")
        right_sizer = wx.StaticBoxSizer(staticbox2, wx.VERTICAL)

        # right_sizer.Add(self.btn_edit_count, 1, wx.ALL|wx.CENTER|wx.EXPAND, 5)
        right_sizer.Add(self.btn_extrad, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        right_sizer.Add(self.btn_receive, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        # right_sizer.Add(self.btn_add, 1, wx.ALL|wx.CENTER|wx.EXPAND, 5)
        right_sizer.Add(self.btn_del, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        # right_sizer.Add(self.btn_edit, 1, wx.ALL|wx.CENTER|wx.EXPAND, 5)

        boxsizer.Add(left_sizer, 6)
        boxsizer.Add(right_sizer, 1, wx.EXPAND|wx.ALL, 20)
        panel.SetSizer(boxsizer)
        self.update_base()
        self.Center()
        self.Show()

    def setColumns(self, data=None):
        self.material.SetColumns([
            ColumnDefn("№ п/п", "left", 60, "id"),
            ColumnDefn("Чертеж", "left", 140, "plan"),
            ColumnDefn("Наименование", "left", 160, "name"),
            ColumnDefn("Тип", "left", 140, "type"),
            ColumnDefn("Материал", "left", 100, "mat"),
            ColumnDefn("Размер", "left", 100, "size"),
            ColumnDefn("Количество(шт)", "left", 110, "count"),
            ColumnDefn("Длина(м)", "left", 100, "length"),
            ColumnDefn("Комментарии", "left", 190, "comments")
        ])
        # self.material.SetObjects(self.data)

    def update_base(self, event=None):
        session = db_controller.connect_to_DB()
        if session:
            query = "SELECT id, plan, name, type, material, size, count, length, comments FROM material WHERE is_active = true"
            try:
                with session.conn.cursor() as cursor:
                    cursor.execute(query)
                    self.data = [Material(*item) for item in cursor.fetchall()]
                    self.material.SetObjects(self.data)
                    self.material.SetFilter(None)
                    self.material.RepopulateList()
                    self.ch.SetLabel('Чертёж')
                    self.ch1.SetLabel('Наименование')
                    self.ch2.SetLabel('Тип')
                    self.ch3.SetLabel('Материал')
            except Exception as e:
                print(e)
                logger.exception('Ошибка БД')
            finally:
                session.conn.close()
        else:
            wx.MessageBox('Ошибка загрузки данных', 'Внимание!', wx.OK | wx.ICON_ERROR)
        
    def update_search_fields(self):
        try:
            self.names, self.type, self.mat = db_controller.update_search_fields('material')
            if '' in self.names:
                self.names.remove('')
            if '' in self.type:
                self.type.remove('')
            if '' in self.mat:
                self.mat.remove('')
        except Exception as e:
            print(e)
            logger.exception(f'Ошибка получения полей из контроллера: {e}')

    def onClose(self, event):
        self.GetParent().Show(True)
        self.Destroy()

    def plan_search(self, category):
        keyword = self.ch.GetValue()
        self.plan_filter = Filter.TextSearch(self.material, columns=self.material.columns[1:2], text=keyword)        
        self.filter_refresh()

    def name_search(self, category):
        keyword = self.ch1.GetValue().replace('*','х')
        self.name_filter = Filter.TextSearch(self.material, columns=self.material.columns[2:6], text=keyword)        
        self.filter_refresh()

    def type_search(self, category):
        keyword = self.ch2.GetValue()
        self.type_filter = Filter.TextSearch(self.material, columns=self.material.columns[3:4], text=keyword)
        self.filter_refresh()

    def mat_search(self, category):
        keyword = self.ch3.GetValue()
        self.mat_filter = Filter.TextSearch(self.material, columns=self.material.columns[4:5], text=keyword)
        self.filter_refresh()

    def filter_refresh(self):
        filters = set([self.plan_filter, self.name_filter, self.type_filter, self.mat_filter])
        filters.discard(None)
        self.material.SetFilter(Filter.Chain(*filters))
        self.material.RepopulateList()

    def extradition(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        if obj.count == 0 or obj.length == 0:
            wx.MessageBox('Недостаток материала для выдачи', 'Внимание!', wx.OK | wx.ICON_ERROR)
            return
        dlg = ExtraditionDialog(obj, self.GetParent().user)
        dlg.ShowModal()
        self.update_base()
        dlg.Destroy()

    def receiving(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        dlg = ReceivingDialog(obj, self.GetParent().user)
        dlg.ShowModal()
        self.update_base()
        dlg.Destroy()

    def insert(self, event):
        dlg = GuideDialog(self.GetParent().user)
        dlg.ShowModal()
        self.update_base()
        dlg.Destroy()

    def remove(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        if obj.length == None and obj.count > 0 or obj.count == None and obj.length > 0:
            wx.MessageBox('Вы не можете удалить материал с остатком', 'Внимание!', wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.MessageDialog(self, 'Вы действительно хотите удалить?', 'Внимание!', wx.YES_NO|wx.ICON_EXCLAMATION)
        confirm = dlg.ShowModal()
        if confirm == wx.ID_YES:
            res = db_controller.remove_from_base(obj.id)
            if res:
                wx.MessageBox('Операция удаления выполнена!', 'Успешно!', wx.OK)
                self.update_base()
            else:
                wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return
        elif confirm == wx.ID_NO:
            return
        
    def edit(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        dlg = EditDialog(obj)
        dlg.ShowModal()
        self.update_base()
        dlg.Destroy()

    def edit_value(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        dlg = EditCountDialog(obj)
        dlg.ShowModal()
        self.update_base()
        dlg.Destroy()
        
    def printing(self, event):
        pass