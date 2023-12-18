import wx
import os
import db_controller
import logging
from frames.panel import MyPanel
from validators.not_empty import NotEmptyValidator

logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), format='{asctime} {levelname} {funcName}->{lineno}: {msg}', style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class EditDialog(wx.Dialog):
    def __init__(self, obj):
        wx.Dialog.__init__(self, None, title='Редактирование записи...', size=(400, 280))
        self.obj = obj
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

        self.plan = wx.TextCtrl(panel, value=f"{self.obj.plan}", size=(200, -1))
        self.name = wx.TextCtrl(panel, value=f"{self.obj.name}", validator=NotEmptyValidator(), size=(200, -1))
        self.type = wx.TextCtrl(panel, value=f"{self.obj.type}", validator=NotEmptyValidator(), size=(200, -1))
        self.mat = wx.TextCtrl(panel, value=f"{self.obj.mat}", validator=NotEmptyValidator())
        self.size = wx.TextCtrl(panel, value=f"{self.obj.size}")
        self.comment = wx.TextCtrl(panel, value=f"{self.obj.comments}", size=(200, -1))
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
        right_sizer.Add(self.comment, 1, wx.ALL)

        sizer_1.Add(left_sizer, 1, wx.ALL, 5)
        sizer_1.Add(right_sizer, 2, wx.ALL, 5)

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)

        ok_btn = wx.Button(panel, label='Подтвердить')
        ok_btn.Bind(wx.EVT_BUTTON, self.edit_record)
        cnl_btn = wx.Button(panel, label='Отмена')
        cnl_btn.Bind(wx.EVT_BUTTON, self.on_close)
        sizer_btn.Add(ok_btn)
        sizer_btn.AddSpacer(20)
        sizer_btn.Add(cnl_btn)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(sizer_1, 1, wx.TOP|wx.LEFT|wx.RIGHT, 10)
        main_sizer.Add(sizer_btn, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=20)

        panel.SetSizer(main_sizer)

    def edit_record(self, event):
        if self.Validate():
            new_plan = self.plan.GetValue()
            new_name = self.name.GetValue()
            new_type = self.type.GetValue()
            new_mat = self.mat.GetValue()
            new_size = self.size.GetValue()
            new_comment = self.comment.GetValue()
            data = self.obj.id, new_plan, new_name, new_type, new_mat, new_size, new_comment
            res = db_controller.edit(data)
            if res:
                wx.MessageBox('Редактирование завершено!', 'Успешно!', wx.OK)
                self.Destroy()
            else:
                wx.MessageBox('Ошибка выполнения операции!', 'Внимание!', wx.OK | wx.ICON_ERROR)
                return
            
    def on_close(self, event):
        self.Destroy()