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
import pygame
from examples import *

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
        self.profile_name = ""

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

    def mouseMoveEvent(self, e):

        self.r = 240
        self.g = 160
        self.b = 160

        p = self.palette()
        gradient = QLinearGradient(0, 0, 0, abs(e.y()))
        gradient.setColorAt(0.0, QColor(150, 200, 250))
        gradient.setColorAt(1.0, QColor(self.r, self.g, self.b))
        p.setBrush(self.backgroundRole(), QBrush(gradient))
        self.setPalette(p)

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
                                 "selection-background-color: rgb(200, 200, 255);" \
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
                                      "selection-background-color: rgb(200, 200, 255);" \
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
                                          "QPushButton:hover {background-color: rgb(255,127,80);" \
                                                        "font-size : 15px;" \
                                                        "color: white;" \
                                                        "font-family: 'Quicksand';" \
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

        self.main_menu_button_style_sheet = "QPushButton {background-color: rgb(90, 130, 255);" \
                                                        "font-size : 15px;"\
                                                        "color: white;" \
                                                        "font-family: 'Quicksand';" \
                                                        "border-width : 5px;" \
                                                        "border-color: black;" \
                                                        "border-radius: 3px}" \
                                            "QPushButton:hover {background-color: rgb(173, 216, 255);" \
                                                        "font-size : 15px;" \
                                                        "color: white;" \
                                                        "font-family: 'Quicksand';" \
                                                        "border-width : 5px;" \
                                                        "border-radius: 3px;" \
                                                        "border-color: black}"

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

    def create_back_button(self, prev_page):

        backbutton = QPushButton("Back", self)
        backbutton.setGeometry(5,
                               5,
                               self.sw/10,
                               self.sh/20)
        backbutton.setStyleSheet(self.main_menu_button_style_sheet)
        backbutton.pressed.connect(prev_page)
        self.widgets.append(backbutton)

    def change_background(self):

        """
        Changes the background slightly on each keystroke.
        """

        if (self.r + self.Rincrement > 255 or self.r + self.Rincrement < 0):
            self.Rincrement = -self.Rincrement

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
            self.setMouseTracking(True)
            self.init_background()
            self.profile_name = username
            self.main_menu()

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

        self.password_shower = QCheckBox(self)
        self.password_shower.move(button_x_offset + button_width, y_gap * 1.9 + button_height * 2.3)

        sign_up = QPushButton("Need an account ?",self)
        sign_up.setGeometry(button_x_offset, y_gap*1.9 + button_height* 3.2, button_width, button_height)
        sign_up.setStyleSheet(self.register_style_sheet)
        sign_up.clicked.connect(self.registration)

        self.username.returnPressed.connect(lambda: self.check_creds(self.username.text(), self.password.text()))
        self.password.returnPressed.connect(lambda: self.check_creds(self.username.text(), self.password.text()))
        self.password_shower.stateChanged.connect(self.show_password)

        self.widgets = [self.username, self.password, title, sign_up, self.password_shower]
        self.show_widgets()
        self.show()

    def show_password(self):

        """
        Shows the password when activated.
        """

        if self.password_shower.isChecked():
            self.password.setEchoMode(self.password.Normal)
        else:
            self.password.setEchoMode(self.password.Password)

    def main_menu(self):

        """
        Main menu where the user can decide what to do.
        """

        self.delete_current_widgets()

        button_width = self.sw / 4
        button_height = self.sh / 17

        button_x_offset = (self.sw - button_width) / 2

        empty_y_space = self.sh - button_height * 3
        y_gap = empty_y_space / 4

        self.courses = QPushButton("Courses",self)
        self.courses.setGeometry(button_x_offset, y_gap * 1.4 + button_height, button_width, button_height)
        self.courses.setStyleSheet(self.main_menu_button_style_sheet)
        self.courses.pressed.connect(self.course_selection)

        self.league_table = QPushButton("Leaderboard", self)
        self.league_table.setGeometry(button_x_offset, y_gap * 1.6 + button_height * 2, button_width, button_height)
        self.league_table.setStyleSheet(self.main_menu_button_style_sheet)
        self.league_table.pressed.connect(self.leaderboard)

        self.examples = QPushButton("Examples", self)
        self.examples.setGeometry(button_x_offset, y_gap * 1.8 + button_height * 3, button_width, button_height)
        self.examples.setStyleSheet(self.main_menu_button_style_sheet)
        self.examples.pressed.connect(self.examples_menu)

        self.settings = QPushButton("Settings", self)
        self.settings.setGeometry(button_x_offset, y_gap * 2.0 + button_height * 4, button_width, button_height)
        self.settings.setStyleSheet(self.main_menu_button_style_sheet)
        self.settings.pressed.connect(self.change_background)

        self.widgets = [self.courses, self.examples, self.settings, self.league_table]
        self.create_back_button(self.login_page)
        self.show_widgets()

    def examples_menu(self):

        """
        Example applications are shown here.
        """

        button_width = self.sw / 4
        button_height = self.sh / 17

        button_x_offset = (self.sw - button_width) / 2

        empty_y_space = self.sh - button_height * 3
        y_gap = empty_y_space / 4

        self.delete_current_widgets()

        self.queens = QPushButton("8 Queens problem", self)
        self.queens.setGeometry(button_x_offset, y_gap * 1.4 + button_height, button_width, button_height)
        self.queens.setStyleSheet(self.main_menu_button_style_sheet)
        self.queens.pressed.connect(self.eight_queens_test)

        self.dijkstra = QPushButton("Dijkstras algorithm", self)
        self.dijkstra.setGeometry(button_x_offset, y_gap * 1.6 + button_height * 2, button_width , button_height)
        self.dijkstra.setStyleSheet(self.main_menu_button_style_sheet)
        self.dijkstra.pressed.connect(self.eight_queens)

        self.bubble_sort = QPushButton("Bubble sort", self)
        self.bubble_sort.setGeometry(button_x_offset, y_gap * 1.8 + button_height * 3, button_width, button_height)
        self.bubble_sort.setStyleSheet(self.main_menu_button_style_sheet)
        self.bubble_sort.pressed.connect(self.eight_queens)

        self.widgets = [self.queens, self.dijkstra, self.bubble_sort]
        self.create_back_button(self.main_menu)
        self.show_widgets()

    def eight_queens_test(self):

        """
        This function sets up the eight queens lesson.
        """

        self.display = QTextEdit(self)
        self.display.setReadOnly(True)
        self.display.setGeometry(self.sw/15,
                                 self.sh/7,
                                 self.sw - (self.sw / 7.5),
                                 self.sh / 1.5)
        self.display.setPlainText("Difficulty : 5  requires knowledge of functions, recursion, objects" +
                                  "\n" + "The 8 queen problem involes putting 8 queens on the board where they each don't attack each other." +
                                  "\n" + "\n" + "The queen can move diagonally and horizontally/vertically" +
                                  "\n" + "\n" +  "The chess board is 8x8." +
                                  "\n" + "\n" +  "Here is a simulation of the Recursive algorithm I wrote. You will then asked" +
                                  "\n" + "questions about the code which will be provide.")


        self.display.setStyleSheet(self.display_style_sheet)

        self.widgets = [self.display]

        self.show_widgets()

    def eight_queens(self):

        self.delete_current_widgets()

        try:
            eightQueensGUI()
        except pygame.error:
            pass

        code = QCodeWidget(self)
        code.setPlainText("""    def recursivley_solve(self):
        for x in range(8):
            for y in range(8):
                if not self.game.in_check(x, y):
                    # choose
                    self.game.add_queen(x, y)

                    self.board_positions.append(str(self.game.board))
                    # explore
                    self.recursivley_solve()
                    if self.game.queen_count == 8:
                        return
                    # unchoose
                    self.game.remove_queen(x, y)""")
        code.setGeometry(self.sw/15,
                         self.sh/7,
                         self.sw - (self.sw / 7.5),
                         self.sh / 1.5)

        self.widgets = [code, self.display]
        self.create_back_button(self.examples_menu)
        self.show_widgets()


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

        self.password_shower = QCheckBox(self)
        self.password_shower.move(button_x_offset + button_width, y_gap * 1.9 + button_height * 2.3)

        self.username.returnPressed.connect(lambda: self.register(self.username.text(), self.password.text()))
        self.password.returnPressed.connect(lambda: self.register(self.username.text(), self.password.text()))

        self.phone_slider = QSlider(Qt.Horizontal, self)
        self.phone_slider.setMinimum(100000000)
        self.phone_slider.setMaximum(999999999)
        self.phone_slider.setGeometry(button_x_offset, y_gap * 1.9 + button_height * 5, button_width, button_height)
        self.phone_slider.valueChanged.connect(self.update_slider)

        self.phone_label = QLineEdit(self)
        self.phone_label.setPlaceholderText("Phone Number")
        self.phone_label.setStyleSheet(self.menu_input_style_sheet)
        self.phone_label.setGeometry(button_x_offset, y_gap * 1.9 + button_height * 4.1, button_width, button_height)
        self.phone_label.setEnabled(False)

        login = QPushButton("Already have an account ?", self)
        login.setGeometry(button_x_offset, y_gap * 1.9 + button_height * 6, button_width, button_height)
        login.setStyleSheet(self.register_style_sheet)
        login.clicked.connect(self.login_page)

        self.password_shower.stateChanged.connect(self.show_password)

        self.widgets = [self.username, self.password, self.phone_slider, self.phone_label, login, title, self.password_shower]
        self.show_widgets()

    def update_slider(self):

        """
        This function updates the phone number slider.
        """

        self.phone_label.setText("0" + str(self.phone_slider.value()))

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
            self.database.insertRow("leaderboard", username, 0)
            self.profile_name = username
            self.main_menu()

        else:
            self.username.setStyleSheet(self.wrong_menu_input_style_sheet)

    def course_selection(self):

        """
        Course selection page is created here.
        """

        self.delete_current_widgets()

        self.create_back_button(self.main_menu)
        self.temp_sh = self.sh / 0.75


        self.create_course("variables",0, -1)
        self.create_course("imports", 1, -1)
        self.create_course("time", 2, -1)
        self.create_course("iteration", 3, -1)
        self.create_course("code style", 4, -1)
        self.create_course("arrays", 0, 0)
        self.create_course("functions", 1, 0)
        self.create_course("sorting", 2, 0)
        self.create_course("classes", 3, 0)
        self.create_course("objects", 4, 0)
        self.create_course("pygame", 0, 1)
        self.create_course("inheritance", 1, 1)
        self.create_course("recursion", 2, 1)
        self.create_course("webscraping", 3, 1)
        self.create_course("challenge", 4, 1)

        self.create_back_button(self.main_menu)

        self.show_widgets()

    def create_course(self, course_name, col, row):

        """
        Creates each individual course widget.
        """

        button_width = self.temp_sh / 5
        x_offset = self.sw / 5

        course = QPushButton(course_name, self)
        course.setGeometry(col * button_width + (self.sw - (4.8 * button_width)) / 2,  # x
                           row * button_width + (self.temp_sh * 1.5 - (5 * button_width)) / 1.75,  # y
                           button_width / 1.2,  # width
                           button_width / 1.2)  # height
        course.setStyleSheet(self.course_button_style_sheets)
        course.clicked.connect(lambda: self.load_course(course_name))
        self.widgets.append(course)

    def load_course(self, course_name):

        """
        Loads a selected course and creates the page.
        """

        self.delete_current_widgets()
        self.setMouseTracking(False)

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
        run.setGeometry(self.sw - self.sw/10,
                         self.sh / 1.75,
                         self.sw/10 - 5,
                         self.sh / 3)
        run.setStyleSheet(self.run_button_style_sheet)
        run.pressed.connect(self.run_code)

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

        self.widgets = [self.back_button, self.next_button, self.tabs, title,
                        self.code_writer, self.display, self.console, run]
        self.create_back_button(self.course_selection)
        self.show_widgets()

    def leaderboard(self):

        """
        This generates the leader board and displays it.
        """

        self.delete_current_widgets()
        self.data = self.database.custom_query("SELECT username, score FROM leaderboard ORDER BY score DESC")

        self.table = QTableWidget(self)

        self.table.setRowCount(len(self.data) * 10)
        self.table.setColumnCount(2)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        for i in range(len(self.data)):
            self.table.setItem(i,  0, QTableWidgetItem(self.data[i]["username"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.data[i]["score"])))

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["Username", "Score"])

        self.table.setGeometry(self.sw / 10,
                               self.sh / 10,
                               (8 * self.sw) / 10,
                               (8 * self.sh) / 10)

        self.widgets = [self.table]
        self.create_back_button(self.main_menu)
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
            self.database.increment("leaderboard", self.profile_name)
            self.course_selection()


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