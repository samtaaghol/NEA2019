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
from HashingAlgorithm import hash_string
from database import Database
import pymysql
import string
import random

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
        self.database = Database('localhost', 'root', 'rootpassword', 'NEA2019', 'utf8mb4', pymysql.cursors.DictCursor)

        self.title = 'Learn Python'
        self.titleFont = QFont('American Typewriter Light', 60, QFont.Bold)
        self.promptFont = QFont('Palatino', 20)
        self.username = ""

        # Set window background color
        self.setAutoFillBackground(True)

        self.init_background()
        self.set_style_sheets()

        # Setting the geometry of the screen.
        self.sw, self.sh = get_screen_dimensions()
        self.sw /= 3
        self.sh /= 3
        self.setFixedSize(self.sw, self.sh)
        self.widgets = []
        self.login_page()

    def set_style_sheets(self):

        """
        Sets the style sheets required for the application.
        """

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

        self.wrong_menu_input_style_sheet = "QLineEdit {background-color: rgb(90, 130, 255); " \
                                      "border-radius : 3px;" \
                                      "border-style: solid;" \
                                      "border-width: 2;" \
                                      "border-color: rgb(220, 100, 100);" \
                                      "color: rgb(230, 230, 230);" \
                                      "font-size: 15pt;" \
                                      "font-family: 'Quicksand';" \
                                      "font-weight: light;" \
                                      "selection-background-color: rgb(165, 135, 0);" \
                                      "selection-color: rgb(20, 20, 20)}"

        self.main_title_style_sheet = "QLabel {font-size: 50pt}"

        self.margin_style_sheet = "QLabel {background-color: rgb(20, 50 ,130)}"

        # "color: white;" \
        self.course_button_style_sheets = "QPushButton {background-color: rgb(90, 130, 255);" \
                                                        "font-size : 15px;"\
                                                        "color: white;" \
                                                        "font-family: 'Quicksand';" \
                                                        "border-width : 5px;" \
                                                        "border-color: black;" \
                                                        "border-radius: 30px}" \
                                          "QPushButton:hover {background-color: rgb(253, 253, 102);" \
                                                        "font-size : 15px;" \
                                                        "color: rgb(75,0,130);" \
                                                        "font-family: 'Comic Sans MS';" \
                                                        "font-weight: bold;" \
                                                        "border-width : 5px;" \
                                                        "border-radius: 30px;" \
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

        self.register_style_sheet = "QPushButton {background-color: transparent ;" \
                                                   "color : rgb(50,100,200);" \
                                                   "font-family:'Quicksand';" \
                                                   "font-size : 16pt}" \
                                      "QPushButton:hover {background-color: transparent ;" \
                                                   "color : rgb(50,120,220);" \
                                                   "font-family:'Quicksand';" \
                                                   "font-size : 16pt}"

    def init_background(self):

        """
        Initialises the interactive background.
        """

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

        """
        Changes the background slightly on each keystroke.
        """

        if (self.r + self.Rincrement > 255 or self.r + self.Rincrement < 200):
            self.Rincrement = -self.Rincrement

        print(self.r)

        self.r += self.Rincrement
        p = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(150, 200, 250))
        gradient.setColorAt(1.0, QColor(self.r, self.g, self.b))
        p.setBrush(self.backgroundRole(), QBrush(gradient))
        self.setPalette(p)

    def delete_current_widgets(self):

        """
        Deletes the current widgets in self.widgets.
        """

        for i in range(len(self.widgets)):
            if type(self.widgets[0]) is not str:
                self.widgets[0].deleteLater()
            self.widgets.remove(self.widgets[0])

    def check_creds(self, username, password):

        """
        Checks the credentials in the username and password widgets.
        """



        details = self.database.getDetails("credentials", username)

        if details == None:
            self.username.setStyleSheet(self.wrong_menu_input_style_sheet)
            return

        hashed, salt = details['password'], details['salt']

        if hash_string(password + salt) == hashed:
            self.username = username
            self.course_selection()

        else:
            self.username.setStyleSheet(self.wrong_menu_input_style_sheet)
            self.password.setStyleSheet(self.wrong_menu_input_style_sheet)

    def show_widgets(self):

        """
        This function shows all the widgets in the current widget buffer.
        """

        for widget in self.widgets:
            widget.show()

    def login_page(self):

        """
        Login page for users.
        """

        self.delete_current_widgets()

        button_width = self.sw / 4
        button_height = self.sh / 17

        button_x_offset = (self.sw - button_width)/2

        empty_y_space = self.sh - button_height*3
        y_gap = empty_y_space/4

        title = QLabel('Learn Python', self)
        title.resize(button_width, button_height)
        title.setGeometry(button_x_offset, y_gap, button_width, button_height*1.5)
        title.setStyleSheet(self.main_title_style_sheet)


        self.username = QLineEdit(self)
        self.username.setGeometry(button_x_offset, y_gap*1.6 + button_height, button_width, button_height)
        self.username.setStyleSheet(self.menu_input_style_sheet)
        self.username.setPlaceholderText("Username")
        self.username.textChanged.connect(self.change_background)

        self.password = QLineEdit(self)
        self.password.setGeometry(button_x_offset, y_gap*1.9 + button_height*2, button_width, button_height)
        self.password.setStyleSheet(self.menu_input_style_sheet)
        self.password.setPlaceholderText("Password")
        self.password.textChanged.connect(self.change_background)
        self.password.setEchoMode(self.password.Password);

        sign_up = QPushButton("Need an account ?",self)
        sign_up.setGeometry(button_x_offset, y_gap*1.9 + button_height* 3.2, button_width, button_height)
        sign_up.setStyleSheet(self.register_style_sheet)
        sign_up.clicked.connect(self.registration)

        self.username.returnPressed.connect(lambda: self.check_creds(self.username.text(), self.password.text()))
        self.password.returnPressed.connect(lambda: self.check_creds(self.username.text(), self.password.text()))

        self.widgets = [self.username, self.password, title, sign_up]
        self.show_widgets()
        self.show()

    def registration(self):

        """
        Account registration page is created here.
        """

        self.delete_current_widgets()

        button_width = self.sw / 4
        button_height = self.sh / 17

        button_x_offset = (self.sw - button_width) / 2

        empty_y_space = self.sh - button_height * 3
        y_gap = empty_y_space / 4

        title = QLabel('Sign Up', self)
        title.resize(button_width, button_height)
        title.setGeometry(button_x_offset * 1.125, y_gap, button_width, button_height * 1.5)
        title.setStyleSheet(self.main_title_style_sheet)

        self.username = QLineEdit(self)
        self.username.setGeometry(button_x_offset, y_gap * 1.6 + button_height, button_width, button_height)
        self.username.setStyleSheet(self.menu_input_style_sheet)
        self.username.setPlaceholderText("Username")
        self.username.textChanged.connect(self.change_background)

        self.password = QLineEdit(self)
        self.password.setGeometry(button_x_offset, y_gap * 1.9 + button_height * 2, button_width, button_height)
        self.password.setStyleSheet(self.menu_input_style_sheet)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(self.password.Password);

        self.username.returnPressed.connect(lambda: self.register(self.username.text(), self.password.text()))
        self.password.returnPressed.connect(lambda: self.register(self.username.text(), self.password.text()))

        login = QPushButton("Already have an account ?", self)
        login.setGeometry(button_x_offset, y_gap * 1.9 + button_height * 3.2, button_width, button_height)
        login.setStyleSheet(self.register_style_sheet)
        login.clicked.connect(self.login_page)

        self.widgets = [self.username, self.password, login, title]
        self.show_widgets()

    def register(self, username, password):

        """
        Handles the registration of a user.
        """

        if len(username) < 8:
            self.username.setStyleSheet(self.wrong_menu_input_style_sheet)

        if len(password) < 8:
            self.username.setStyleSheet(self.wrong_menu_input_style_sheet)


        if not self.database.getDetails("credentials", username):

            salt = ''.join(random.sample(string.ascii_lowercase, 10))

            self.database.insertRow("credentials", username, hash_string(password + salt), salt)

            self.course_selection()

        else:
            self.username.setStyleSheet(self.wrong_menu_input_style_sheet)

    def course_selection(self):

        """
        Course selection page is created here.
        """

        self.delete_current_widgets()
        self.temp_sh = self.sh / 0.75


        self.create_course("variables",0, 0)
        self.create_course("functions", 1, 0)
        self.create_course("classes", 2, 0)
        self.create_course("recursion", 3, 0)
        self.create_course("iteration", 4, 0)
        self.create_course("web scraping", 0, 1)
        self.create_course("imports", 1, 1)
        self.create_course("time", 2, 1)
        self.create_course("pygame", 3, 1)
        self.create_course("open-cv", 4, 1)
        self.create_course("objects", 0, -1)
        self.create_course("inheritance", 1, -1)
        self.create_course("code style", 2, -1)
        self.create_course("comments", 3, -1)
        self.create_course("sorting", 4, -1)

    def create_course(self, course_name, col, row):

        """
        Creates each individual course widget.
        """

        button_width = self.temp_sh / 5
        x_offset = self.sw / 5

        course = QPushButton(course_name, self)
        course.setGeometry(col * button_width + (self.sw - (4.8 * button_width)) / 2,  # x
                           row * button_width + (self.temp_sh * 1.5 - (5 * button_width)) / 2,  # y
                           button_width / 1.2,  # width
                           button_width / 1.2)  # height
        course.setStyleSheet(self.course_button_style_sheets)
        course.clicked.connect(lambda: self.load_course(course_name))
        course.setVisible(True)
        self.widgets.append(course)

    def load_course(self, course_name):

        """
        Loads a selected course and creates the page.
        """

        self.delete_current_widgets()

        self.current_line = 0
        self.question = False

        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(5,self.temp_sh/10 - 10 + self.sh/8, self.sw/10-10, self.temp_sh/10)
        self.setStyleSheet(self.back_button_style_sheet)
        self.back_button.pressed.connect(self.course_selection)

        self.next_button = QPushButton("Next", self)
        self.next_button.setGeometry(self.sw - self.sw/10 + 5,self.temp_sh/10 - 10 + self.sh/8, self.sw/10-10, self.temp_sh/10)
        self.setStyleSheet(self.back_button_style_sheet)
        self.next_button.pressed.connect(self.next_line)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(self.sw/10,
                         self.temp_sh/2.7,
                         self.sw - (self.sw/5),
                         self.temp_sh/3)

        title = QLabel(course_name, self)
        title.setGeometry((self.sw/2 - self.sw/8),
                          10,
                          self.sw/4,
                          self.temp_sh/15)
        title.setStyleSheet(self.course_title_style_sheet)
        title.setAlignment(Qt.AlignCenter)

        self.code_writer = QCodeWidget(self)
        self.console = QConsole(self)


        self.tabs.addTab(self.code_writer, "Code")
        self.tabs.addTab(self.console, "Console")

        run = QPushButton("Run",self)
        #run.setIcon(QIcon(self.root_path + "assets/run.jpg"))
        run.setGeometry(4,
                        self.temp_sh/2.5,
                        self.sw/10 - 10,
                        self.temp_sh/20)
        run.setStyleSheet(self.run_button_style_sheet)
        run.pressed.connect(self.run_code)

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
        self.display.setText(" \n" + self.course[0])

        self.widgets = [run, self.back_button, self.next_button, self.tabs, title,
                        self.code_writer, self.display, self.console]

        self.show_widgets()

    def run_code(self):

        """
        Runs the code in the code writer widget.
        """

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


    def get_course_name(self, count):

        """
        Gets course name given the count.
        """

        file_path = self.root_path + "/courses/" + str(count)
        if os.path.isfile(file_path):
            file = open(file_path, 'r')
            title = file.read().split("\n")[0]
            file.close()
            #print(title)
            return title

    def next_line(self):

        """
        Outputs the next line on the course file.
        """

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

        """
        Sets the style sheets required for the widgets.
        """

        self.code_writer_style_sheet = "QPlainTextEdit {background-color: rgb(75, 75, 75);" \
                                                  "color: white;" \
                                                  "font-family: 'Inconsolata';" \
                                                  "font-size: 26px;" \
                                                  "border-width: 10px;" \
                                                  "border-color: rgb(100,100,100);" \
                                                  "border-radius: 30px;" \
                                                  "border-style: solid}"


class QConsole(QTextEdit):

    """
    Custom made pyqt5 widget which creates a code console.
    """

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

        """
        Sets the style sheets required for the console.
        """

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