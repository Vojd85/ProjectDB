import wx


class NotEmptyValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self):
        return NotEmptyValidator()

    def Validate(self, win):
        # Определение поля для проверки из окна, которому назначен валидатор
        field = self.GetWindow()
        # Получение значения из поля проверки
        text = field.GetValue()

        if len(text) == 0:
            wx.MessageBox("Поле должно содержать символы!", "Ошибка!")
            field.SetBackgroundColour("pink")
            field.SetFocus()
            field.Refresh()
            return False
        else:
            field.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            field.Refresh()
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True