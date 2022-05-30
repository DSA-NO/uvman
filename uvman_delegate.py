from PyQt5.QtWidgets import QApplication, QStyledItemDelegate, QStyle

class PasswordDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        style = option.widget.style() or QApplication.style()
        hint = style.styleHint(QStyle.SH_LineEdit_PasswordCharacter)
        option.text = chr(hint) * 5

class ChannelFormatDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):        
        formattedNum = locale.toString(float(value), 'f', 5)
        return formattedNum