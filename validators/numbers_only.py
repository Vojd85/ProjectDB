import wx
import string


class OneDigitValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return OneDigitValidator()

    def Validate(self, win):
        field = self.GetWindow()
        text = field.GetValue()

        if len(text) != 1:
            wx.MessageBox("Поле должно содержать одну цифру!", "Ошибка!")
            field.SetBackgroundColour("pink")
            field.SetFocus()
            field.Refresh()
            return False
        else:
            field.SetBackgroundColour(wx.SystemSettings.GetColour
                                      (wx.SYS_COLOUR_WINDOW))
            field.Refresh()
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def OnChar(self, evt):
        key = evt.GetKeyCode()
        if chr(key) not in string.digits and key != 8:
            return
        evt.Skip()


class NumberValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return NumberValidator()

    def Validate(self, win):
        field = self.GetWindow()
        text = field.GetValue().replace(',', '.')
        try:
            if len(text) < 1:
                wx.MessageBox("Поле не должно быть пустым!", "Ошибка!")
                field.SetBackgroundColour("pink")
                field.SetFocus()
                field.Refresh()
                return False
            temp = float(text)
            return True
        except Exception:
            wx.MessageBox("Поле должно быть числом!", "Ошибка!")
            field.SetBackgroundColour("pink")
            field.SetFocus()
            field.Refresh()
            return False

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def OnChar(self, evt):
        key = evt.GetKeyCode()
        if chr(key) not in string.digits and key != 8 and chr(key) != ',' and chr(key) != '.':
            return
        evt.Skip()