from PyQt5.QtWidgets import *
import python_syntax_highlighter
from PyQt5.QtGui import *
from PIL import ImageGrab
from PyQt5.QtCore import *
import os
import traceback
import subprocess
import sys
import code
import subprocess

def get_screen_dimensions():

    """
    This function returns a double of the width and height of the screen.
    """

    screen = ImageGrab.grab()
    return screen.size

class mainGui(QWidget):

    def __init__(self):

        """
        Runs when class is instantiated, here it assigns fonts and resolution.
        """
        super().__init__()

        self.root_path = os.path.dirname(os.path.abspath(__file__))[0:-7]

        self.title = 'Learn Python'
        self.titleFont = QFont('American Typewriter Light', 60, QFont.Bold)
        self.promptFont = QFont('Palatino', 20)

        # Set window background color
        self.setAutoFillBackground(True)

        self.init_background()
        self.set_style_sheets()

        # Setting the geometry of the screen.
        self.sw, self.sh = get_screen_dimensions()
        self.sw /= 1.5
        self.sh /= 1.5
        self.setFixedSize(self.sw, self.sh)
        self.login_page()

    def set_style_sheets(self):

        self.menu_input_style_sheet = "QLineEdit {background-color: rgb(90, 130, 255); " \
                                 "border-radius : 3px;" \
                                 "border-style: solid;" \
                                 "border-width: 3px;" \
                                 "border-color: rgb(90, 130, 255);" \
                                 "color: rgb(230, 230, 230);" \
                                 "font-size: 15pt;" \
                                 "font-family: 'Quicksand';" \
                                 "font-weight: light;" \
                                 "selection-background-color: rgb(165, 135, 0);" \
                                 "selection-color: rgb(20, 20, 20)}"

        self.main_title_style_sheet = "QLabel {font-size: 50pt}"

        self.margin_style_sheet = "QLabel {background-color: rgb(20, 50 ,130)}"

        self.course_button_style_sheets = "QPushButton {background-color: rgb(200,100,100);" \
                                                        "color: white;" \
                                                        "font-family: 'Quicksand';" \
                                                        "border-width : 5px;" \
                                                        "border-color: black;" \
                                                        "border-radius: 38px}" \
                                          "QPushButton:hover {background-color: rgb(180, 90, 90);" \
                                                        "color: white;" \
                                                        "font-family: 'Quicksand';" \
                                                        "border-width : 5px;" \
                                                        "border-radius: 20px;" \
                                                        "border-color: black}"
        self.course_title_style_sheet = "QLabel {color: white;" \
                                                "font-size : 30px;" \
                                                "background-color: rgb(90, 130, 255);" \
                                                "border-radius: 9px;" \
                                                "font-family: 'Quicksand';" \
                                                "font-size: 40pt}"

        self.run_button_style_sheet = "QPushButton {background-color: rgb(50,205,50) ;" \
                                                   "color : white;" \
                                                   "border-radius: 9px;" \
                                                   "font-family:'Quicksand';" \
                                                   "font-size : 20pt}" \
                                      "QPushButton:pressed {background-color: rgb(20,170,20) ;" \
                                                   "color : white;" \
                                                   "border-radius: 9px;" \
                                                   "font-family:'Quicksand'}" \
                                      "QPushButton:hover {background-color: rgb(30,180,30) ;" \
                                                   "color : white;" \
                                                   "border-radius: 9px;" \
                                                   "font-family:'Quicksand';" \
                                                   "font-size : 20pt}"

        self.display_style_sheet = "QTextEdit {background-color: white;" \
                                       "color: black;" \
                                       "font-family: 'SF Mono';" \
                                       "font-size: 20px;" \
                                       "border-width: 5px;" \
                                       "border-color: rgb(100,100,100);" \
                                       "border-radius: 30px;" \
                                       "border-style: solid}"

        self.back_button_style_sheet = "QPushButton {background-color: rgb(80,80,205) ;" \
                                                   "color : white;" \
                                                   "border-radius: 9px;" \
                                                   "font-family:'Quicksand';" \
                                                   "font-size : 20pt}" \
                                      "QPushButton:pressed {background-color: rgb(80,80,220) ;" \
                                                   "color : white;" \
                                                   "border-radius: 9px;" \
                                                   "font-family:'Quicksand'}" \
                                      "QPushButton:hover {background-color: rgb(70,79,205) ;" \
                                                   "color : white;" \
                                                   "border-radius: 9px;" \
                                                   "font-family:'Quicksand';" \
                                                   "font-size : 20pt}"

    def init_background(self):
        self.r = 240
        self.g = 160
        self.b = 160
        self.Rincrement = 5
        p = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(150, 200, 250))
        gradient.setColorAt(1.0, QColor(self.r, self.g, self.b))
        p.setBrush(self.backgroundRole(), QBrush(gradient))
        self.setPalette(p)

    def change_background(self):

        if (self.r + self.Rincrement > 255 or self.r + self.Rincrement < 200): self.Rincrement = -self.Rincrement
        self.r += self.Rincrement
        p = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(150, 200, 250))
        gradient.setColorAt(1.0, QColor(self.r, self.g, self.b))
        p.setBrush(self.backgroundRole(), QBrush(gradient))
        self.setPalette(p)

    def delete_current_widgets(self):
        for i in range(len(self.widgets)):
            if type(self.widgets[0]) is not str:
                self.widgets[0].deleteLater()
            self.widgets.remove(self.widgets[0])

    def check_creds(self):
        # TODO: write check.
        self.course_selection()

    def login_page(self):

        """
        Login page for users.
        """

        button_width = self.sw / 4
        button_height = self.sh / 17

        button_x_offset = (self.sw - button_width)/2

        empty_y_space = self.sh - button_height*3
        y_gap = empty_y_space/4

        title = QLabel('Learn Python', self)
        title.resize(button_width, button_height)
        title.setGeometry(button_x_offset, y_gap, button_width, button_height*1.5)
        title.setStyleSheet(self.main_title_style_sheet)

        username = QLineEdit(self)
        username.setGeometry(button_x_offset, y_gap*1.6 + button_height, button_width, button_height)
        username.setStyleSheet(self.menu_input_style_sheet)
        username.setPlaceholderText("Username")
        username.textChanged.connect(self.change_background)
        username.returnPressed.connect(self.check_creds)

        password = QLineEdit(self)
        password.setGeometry(button_x_offset, y_gap*1.9 + button_height*2, button_width, button_height)
        password.setStyleSheet(self.menu_input_style_sheet)
        password.setPlaceholderText("Password")
        password.setEchoMode(password.Password);
        password.returnPressed.connect(self.check_creds)

        self.widgets = [username, password, title]

        self.show()

    def course_selection(self):
        self.delete_current_widgets()
        self.temp_sh = self.sh / 0.75


        self.create_course("variables",0, 0)
        self.create_course("functions", 1, 0)
        self.create_course("classes", 2, 0)
        self.create_course("recursion", 3, 0)


    def create_course(self, course_name, col, row):

        button_width = self.temp_sh / 5
        x_offset = self.sw / 5

        course = QPushButton(course_name, self)
        course.setGeometry(col * button_width + (self.sw - (5 * button_width)) / 2,  # x
                           row * button_width + (self.temp_sh * 1.5 - (5 * button_width)) / 2,  # y
                           button_width / 1.2,  # width
                           button_width / 1.2)  # height
        course.setStyleSheet(self.course_button_style_sheets)
        course.clicked.connect(lambda: self.load_course(course_name))
        course.setVisible(True)
        self.widgets.append(course)

    def load_course(self, course_name):
        self.delete_current_widgets()

        self.current_line = 0
        self.question = False

        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(5,self.temp_sh/10 - 10 + self.sh/8, self.sw/10-10, self.temp_sh/10)
        self.setStyleSheet(self.back_button_style_sheet)
        self.back_button.pressed.connect(self.course_selection)
        self.back_button.show()
        self.widgets.append(self.back_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.setGeometry(self.sw - self.sw/10 + 5,self.temp_sh/10 - 10 + self.sh/8, self.sw/10-10, self.temp_sh/10)
        self.setStyleSheet(self.back_button_style_sheet)
        self.next_button.pressed.connect(self.next_line)
        self.next_button.show()
        self.widgets.append(self.next_button)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(self.sw/10,
                         self.temp_sh/2.7,
                         self.sw - (self.sw/5),
                         self.temp_sh/3)
        self.widgets.append(self.tabs)

        #title = QLabel(self)
        title = QLabel(course_name, self)
        title.setGeometry((self.sw/2 - self.sw/8),
                          10,
                          self.sw/4,
                          self.temp_sh/15)
        title.setStyleSheet(self.course_title_style_sheet)
        title.setAlignment(Qt.AlignCenter)
        title.show()
        self.widgets.append(title)

        self.code_writer = QCodeWidget(self)
        self.console = QConsole(self)
        self.widgets.append(self.code_writer)
        self.widgets.append(self.console)

        self.tabs.addTab(self.code_writer, "Code")
        self.tabs.addTab(self.console, "Console")
        self.tabs.show()

        run = QPushButton("Run",self)
        #run.setIcon(QIcon(self.root_path + "assets/run.jpg"))
        run.setGeometry(4,
                        self.temp_sh/2.5,
                        self.sw/10 - 10,
                        self.temp_sh/20)
        run.setStyleSheet(self.run_button_style_sheet)
        run.pressed.connect(self.run_code)
        run.show()

        self.widgets.append(run)
        print(self.root_path + "courses/" + course_name)

        self.course = open(self.root_path + "courses/" + course_name, "r")
        self.course = self.course.read().split("$")

        self.display = QTextEdit(self)
        self.display.setReadOnly(True)
        self.display.setGeometry(self.sw/10,
                         self.temp_sh/15 + 40,
                         self.sw - (self.sw/5),
                         self.temp_sh/4)
        self.display.setStyleSheet(self.display_style_sheet)
        self.display.show()
        self.display.setText(" \n" + self.course[0])
        self.widgets.append(self.display)

    def run_code(self):

        if not self.question:
            return
        self.tabs.setCurrentIndex(1)
        self.console.setPlainText(">> This is the python console")
        text = self.code_writer.toPlainText()

        text += "\n" + self.code

        file = open("temp_file.py", "w")
        file.write(text)
        file.close()

        with open('output.txt', 'w') as f:
            subprocess.call([sys.executable, 'temp_file.py'], stdout=f, stderr=subprocess.STDOUT)
            f.close()
        file = open('output.txt', 'r')

        content = file.read()

        if "T" in content:
            self.console.setText(">> " + content + "Correct")
            self.question = False
        else:
            self.console.setText(">> " + content + "Incorrect")


        #for piece in text.split("\n"):
        #    self.console.append(">> " + piece)

    def get_course_name(self, count):
        file_path = self.root_path + "/courses/" + str(count)
        if os.path.isfile(file_path):
            file = open(file_path, 'r')
            title = file.read().split("\n")[0]
            file.close()
            #print(title)
            return title

    def next_line(self):
        if self.question:
            return
        self.current_line += 1
        try:
            if "@" in self.course[self.current_line]:
                self.question = True
                parts = self.course[self.current_line].split("@")
                message = parts[0]
                self.code = parts[1]
            else:
                self.question = False
                message = self.course[self.current_line]

            self.display.setText(" " + message)
        except IndexError:
            self.display.setText(" " + "course complete")


class QCodeWidget(QPlainTextEdit):
    """
    This is a custom made pyqt5 widget which creates a code interface.
    """
    def __init__(self, canvas):

        QWidget.__init__(self, parent=canvas)
        self.interpreter = code.InteractiveConsole()
        self.setStyleSheets()
        self.highlight = python_syntax_highlighter.PythonHighlighter(self.document())
        self.qCursor = QTextCursor(self.document())
        self.setGeometry(canvas.sw/10,
                         canvas.sh/2.7,
                         canvas.sw - (canvas.sw/5),
                         canvas.sh/3)
        self.setStyleSheet(self.code_writer_style_sheet)
        self.show()

    def setStyleSheets(self):
        self.code_writer_style_sheet = "QPlainTextEdit {background-color: rgb(75, 75, 75);" \
                                                  "color: white;" \
                                                  "font-family: 'Inconsolata';" \
                                                  "font-size: 26px;" \
                                                  "border-width: 10px;" \
                                                  "border-color: rgb(100,100,100);" \
                                                  "border-radius: 30px;" \
                                                  "border-style: solid}"


class QConsole(QTextEdit):

    def __init__(self, canvas):
        QWidget.__init__(self, parent = canvas)
        self.setStyleSheets()
        self.setGeometry(canvas.sw / 10,
                         canvas.sh / 2.7,
                         canvas.sw - (canvas.sw / 5),
                         canvas.sh / 3)
        self.setStyleSheet(self.console_style_sheet)
        self.setText(">> This is the python console")
        self.setReadOnly(True)

    def setStyleSheets(self):
        self.console_style_sheet = "QTextEdit {background-color: rgb(120, 120, 120);" \
                                       "color: white;" \
                                       "font-family: 'SF Mono';" \
                                       "font-size: 20px;" \
                                       "border-width: 10px;" \
                                       "border-color: rgb(100,100,100);" \
                                       "border-radius: 30px;" \
                                       "border-style: solid}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainGui()
    sys.exit(app.exec_())