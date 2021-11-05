import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QFrame, QWidget
from PyQt5.QtWidgets import QScrollArea, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from Main_window import MyWidget
from ViewOlympWindow import MyOlymp
from CreateOlympWindow import CreateOlymp, CreateOlympWithSubject

from classes import OlympiadsAll, Olympiad


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('MainWindow')
        self.olympiadsAll = OlympiadsAll()
        self.program = self
        self.show_main_window()

    def show_main_window(self):
        self.main_w = MyWidget(self.olympiadsAll, self)
        self.main_w.show()
        self.main_w.addButton.clicked.connect(self.show_create_olymp_window_with_subj)
        self.clicked_for_olymp()

    def clicked_for_olymp(self):
        self.olymp_label_class = {}  # словарь ключ: QLabel олимпиады, значение: объект Olympiads
        self.current_olymps = None
        self.current_olymp = None
        self.flag_subject = False
        for frame in self.main_w.scrollArea.findChildren(QFrame):  # привязка события на все олимпиады (QLabel)
            if type(frame) == QFrame:
                for count, olymp in enumerate(frame.findChildren(QLabel)):
                    if count == 0:
                        self.flag_subject = True
                        self.current_olymps = self.main_w.current_olymps[olymp.text()]

                    else:
                        self.current_olymp = self.current_olymps[count - 1]
                        self.olymp_label_class[olymp] = self.current_olymp
                    olymp.installEventFilter(self)

    def eventFilter(self, obj, e):  # для подлкючения события clicked на QLabel
        if e.type() == 2:
            if obj in self.olymp_label_class:
                self.show_olymp_window(self.olymp_label_class[obj])
            else:
                self.show_create_olymp_window(obj.text())
        return super(QMainWindow, self).eventFilter(obj, e)

    def show_olymp_window(self, olympiad: Olympiad):
        subject = olympiad.subject
        self.olymp_view_w = MyOlymp(olympiad, self.olympiadsAll, self.main_w, self, subject)
        self.olymp_view_w.setWindowModality(Qt.ApplicationModal)
        self.olymp_view_w.show()
        self.olympiadsAll.update_all_olymp_dict()

    def show_create_olymp_window(self, subject):
        self.create_olymp_w = CreateOlymp(subject, self.olympiadsAll, self.main_w, self)
        self.create_olymp_w.setWindowModality(Qt.ApplicationModal)
        self.create_olymp_w.show()

    def show_create_olymp_window_with_subj(self, subject):
        self.create_olymp_w = CreateOlympWithSubject(subject, self.olympiadsAll, self.main_w, self)
        self.create_olymp_w.setWindowModality(Qt.ApplicationModal)
        self.create_olymp_w.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()

    sys.exit(app.exec_())
