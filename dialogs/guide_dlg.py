import wx
import os
import logging
import db_controller
from ObjectListView import ObjectListView, ColumnDefn, Filter
from frames.panel import MyPanel
from models import Material
from .value_dlg import ChooseValueDialog
from .edit_dlg import EditDialog
from .insert_dlg import InsertDialog


logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), format='{asctime} {levelname} {funcName}->{lineno}: {msg}', style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GuideDialog(wx.Dialog):
    def __init__(self, user):
        wx.Dialog.__init__(self, None, title='Справочник материалов', size=(900, 500))
        self.user = user
        self.filter = None
        self.setUI()

    def setUI(self): 
        panel = MyPanel(self)

        self.material = ObjectListView(panel, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.material.SetEmptyListMsg('Тут пока пусто...')
        self.setColumns()
        self.material.AutoSizeColumns()

        self.search_field = wx.SearchCtrl(panel)
        self.search_field.SetDescriptiveText("Введите что-нибудь...")
        btn_add = wx.Button(panel, wx.NewId(), "Добавить\nна склад", size=(100, 60))
        btn_add.Bind(wx.EVT_BUTTON, self.add_record)
        btn_insert = wx.Button(panel, wx.NewId(), "Новая\nзапись", size=(100, 60))
        btn_insert.Bind(wx.EVT_BUTTON, self.insert_record)
        btn_edit = wx.Button(panel, wx.NewId(), "Редактировать", size=(100, 60))
        btn_edit.Bind(wx.EVT_BUTTON, self.edit_record)
        btn_delete = wx.Button(panel, wx.NewId(), "Удалить\nзапись", size=(100, 60))
        btn_delete.Bind(wx.EVT_BUTTON, self.delete_record)

        search_staticbox = wx.StaticBox (panel, wx.NewId(), label="Поиск")
        search_sizer = wx.StaticBoxSizer(search_staticbox, wx.HORIZONTAL)
        search_sizer.Add(self.search_field, 1, wx.ALL, 5)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(search_sizer, 1, wx.EXPAND|wx.BOTTOM, 10)
        left_sizer.Add(self.material, 8, wx.EXPAND|wx.FIXED_MINSIZE)

        btn_staticbox = wx.StaticBox (panel, wx.NewId(), label="Операции")
        right_sizer = wx.StaticBoxSizer(btn_staticbox, wx.VERTICAL)
        right_sizer.Add(btn_add, 0, wx.SHAPED|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        right_sizer.Add(btn_insert, 0, wx.SHAPED|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        right_sizer.Add(btn_edit, 0, wx.SHAPED|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        right_sizer.Add(btn_delete, 0, wx.SHAPED|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_sizer, 6, wx.ALL|wx.FIXED_MINSIZE, 10)
        main_sizer.Add(right_sizer, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.BOTTOM, 10)

        panel.SetSizer(main_sizer)

        self.update_guide()

    def setColumns(self, data=None):
        self.material.SetColumns([
            ColumnDefn("Чертеж", "left", 120, "plan"),
            ColumnDefn("Наименование", "left", 200, "name"),
            ColumnDefn("Тип", "left", 180, "type"),
            ColumnDefn("Материал", "left", 100, "mat"),
            ColumnDefn("Размер", "left", 80, "size"),
            ColumnDefn("Комментарии", "left", 190, "comments")
            
            ])
        
    def update_guide(self, event=None):
        session = db_controller.connect_to_DB()
        if session:
            query = "SELECT id, plan, name, type, material, size, count, length, comments FROM material WHERE is_active = false"
            try:
                with session.conn.cursor() as cursor:
                    cursor.execute(query)
                    self.data = [Material(*item) for item in cursor.fetchall()]
                    self.material.SetObjects(self.data)
                    self.material.SetFilter(None)
                    self.material.RepopulateList()
            except Exception as e:
                print(e)
                logger.exception('Ошибка загрузки справочника из БД')
            finally:
                session.conn.close()
        else:
            wx.MessageBox('Ошибка загрузки данных', 'Внимание!', wx.OK | wx.ICON_ERROR)

    def add_record(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        dlg = ChooseValueDialog(obj)
        dlg.ShowModal()
        self.update_guide()
        dlg.Destroy()

    def insert_record(self, event):
        dlg = InsertDialog()
        dlg.ShowModal()
        self.update_guide()
        dlg.Destroy()

    def edit_record(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        dlg = EditDialog(obj)
        dlg.ShowModal()
        self.update_guide()
        dlg.Destroy()

    def delete_record(self, event):
        if self.material.GetSelectedObject() == None:
            wx.MessageBox('Вы не выбрали позицию', 'Внимание!', wx.OK | wx.ICON_INFORMATION)
            return
        obj = self.material.GetSelectedObject()
        dlg = wx.MessageDialog(self, 'Вы действительно хотите удалить?', 'Внимание!', wx.YES_NO|wx.ICON_EXCLAMATION)
        confirm = dlg.ShowModal()
        if confirm == wx.ID_YES:
            res = db_controller.delete(obj.id)
            if res:
                wx.MessageBox('Операция удаления выполнена!', 'Успешно!', wx.OK)
                self.update_guide()
            else:
                wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return
        elif confirm == wx.ID_NO:
            return
        
    def search(self, event):
        keyword = self.search_field.GetValue().replace('*','х')
        self.filter = Filter.TextSearch(self.material, columns=self.material.columns[0:5], text=keyword)        
        self.material.SetFilter(self.filter)
        self.material.RepopulateList()





        
