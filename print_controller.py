import os
import sys
import wx
import wx.html2
from wx.html import HtmlEasyPrinting


app_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
html_file = os.path.join(app_dir, "templates/test.html")

class Printer(HtmlEasyPrinting):
    """
    Класс Printer наследуется от wx.HtmlEasyPrinting, созданного 
    для упрощения печати страниц в HTML формате
    """
    def __init__(self, parent):

        # Задаём имя окна
        name = "Invoice"

        # Инициализация принтера через родительский класс
        HtmlEasyPrinting.__init__(self, name, parent)

        # Получение рабочего каталога
        self.current_dir = os.path.normpath(os.path.dirname(__file__))

        # Установка первоначальных настроек принтера и страницы печати
        self.GetPrintData().SetPaperId(wx.PAPER_A4) 
        self.GetPrintData().SetOrientation(wx.PORTRAIT)
        self.GetPrintData().SetColour(False)
        self.GetPageSetupData().SetMarginTopLeft((20, 10))
        self.GetPageSetupData().SetMarginBottomRight((20, 20))

    # Настройки печати 
    def page_setup(self):
        self.PageSetup()

    def print_text(self, text): # Печать текста
        return self.PrintText(text, basepath=self.current_dir)

    def preview_text(self, text): # Просмотр текста
        return self.PreviewText(text, basepath=self.current_dir)

    def print_file(self, file): # Печать файла
        return self.PrintFile(file)

    def preview_file(self, file): # Просмотр файла
        return self.PreviewFile(file)