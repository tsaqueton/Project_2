import csv
from PyQt5.QtWidgets import *
from To_Do import *


def read_list(dict):
    """
    function updates a dictionary (dict) by reading "to_do.csv" file.
    :param dict: dictionary (self.to_do_dict)
    """
    try:
        with open("to_do.csv", "r") as file_dict:
            csvFile = csv.reader(file_dict)
            for lines in csvFile:
                key = lines[0]
                value = lines[1]
                dict.update({int(key): value})
            for key in dict.keys():
                if '!@#$%' in dict[key]:
                    dict[key] = dict[key].replace('!@#$%', '\n    ')
    except FileNotFoundError:
        pass


def save_list(dict):
    """
    function writes the contents of a dictionary (dict) to "to_do.csv" file.
    :param dict: dictionary (self.temp_to_do_dict)
    """
    with open('to_do.csv', 'w') as csvfile:
        for key in dict.keys():
            if '\n    ' in dict[key]:
                dict[key] = dict[key].replace('\n    ', '!@#$%')
            csvfile.write("%s,%s\n" % (key, dict[key]))


class Controller(QMainWindow, Ui_MainWindow):
    """
    class creates a controller to control To_Do.py GUI.
    """

    def __init__(self, *args, **kwargs):
        """
        method initializes controller class; it sets up buttons and creates dictionaries.
        """
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.button_Add.clicked.connect(lambda: self.add_item())
        self.button_Del.clicked.connect(lambda: self.del_item())
        self.button_clear.clicked.connect(lambda: self.clear_list())

        self.temp_to_do_dict = {}
        self.to_do_dict = {}
        read_list(self.to_do_dict)
        self.update_list()

    def add_item(self):
        """
        method adds text from the text box (self.textEdit_Descripton) to a dictionary (self.to_do_dict).
        """
        if self.textEdit_Descripton.toPlainText() == '':
            pass
        else:
            num = self.spinBox_itemNum.value()
            if num == 0:
                if self.listWidget.count() == 0:
                    num = 1
                    self.to_do_dict.update({num: self.textEdit_Descripton.toPlainText().replace('\n', '\n    ')})
                else:
                    num = len(self.to_do_dict) + 1
                    self.to_do_dict.update({num: self.textEdit_Descripton.toPlainText().replace('\n', '\n    ')})
                self.update_list()
            elif num in self.to_do_dict or num == len(self.to_do_dict) + 1:
                temp_dict = {}
                for key in range(num, len(self.to_do_dict) + 1):
                    temp_dict[key + 1] = self.to_do_dict[key]
                self.to_do_dict.update(temp_dict)
                self.to_do_dict.update({num: self.textEdit_Descripton.toPlainText().replace('\n', '\n    ')})
                self.update_list()
            else:
                self.label_error.setText(f"ERROR: Item number {str(num)}\nis not on the list")

    def del_item(self):
        """
        method deletes item number (which is from self.spinBox_itemNum) from a dictionary (self.to_do_dict).
        """
        try:
            num = self.spinBox_itemNum.value()
            if num == 0:
                num = len(self.to_do_dict)
                self.to_do_dict.pop(num)
                self.update_list()
            elif num in self.to_do_dict:
                for key in range(num, len(self.to_do_dict)):
                    self.to_do_dict[key] = self.to_do_dict[key + 1]
                self.to_do_dict.pop(len(self.to_do_dict))
                self.update_list()
            else:
                self.label_error.setText(f"ERROR: Item number {str(num)}\nis not on the list")
        except KeyError:
            self.label_error.setText(f"ERROR: There are no items\nto delete.")

    def clear_list(self):
        """
        method clears the dictionary and the GUI list widget (self.to_do_dict and self.listWidget).
        """
        self.to_do_dict.clear()
        self.temp_to_do_dict.clear()
        save_list(self.temp_to_do_dict)
        self.listWidget.clear()

    def update_list(self):
        """
        method updates the GUI list widget (self.listWidget) by displaying the keys and items of a dictionary.
        (self.to_do_dict).
        """
        self.listWidget.clear()
        self.textEdit_Descripton.clear()
        for num in range(1, len(self.to_do_dict) + 1):
            self.listWidget.addItem(f'{str(num)}. {self.to_do_dict[num]}')
        self.temp_to_do_dict.clear()
        self.temp_to_do_dict.update(self.to_do_dict)
        save_list(self.temp_to_do_dict)
        self.label_error.setText("Note:\"Add Item\"\\\"Delete\nItem\" adds\\deletes the item\nat the end of the list "
                                 "when\n\"Item Number\" is set to 0.")
