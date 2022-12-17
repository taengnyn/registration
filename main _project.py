import sqlite3
from PyQt5 import QtWidgets
import part
import helper
import re

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    password TEXT
)''')
db.commit()

db1 = sqlite3.connect('database1.db')
cursor2 = db.cursor()

cursor2.execute('''CREATE TABLE IF NOT EXISTS user(
    user_name TEXT,
    user_secondn TEXT
)''')
db1.commit()

for i in cursor.execute('SELECT * FROM users'):
    print(i)

for e in cursor2.execute('SELECT * FROM users'):
    print(e)

class Help(QtWidgets.QMainWindow, helper.Ui_MainWindow):
    def __init__(self):
        super(Help, self).__init__()
        self.setupUi(self)
        self.plainTextEdit.setPlainText('Вітаю вас у програмі реєстрації клієнтів!\n В цьому додатку ви можете створити свій обліковий запис(1) або видалити його, якщо вже зареєстровані(2)\n 1.    Створення облікового запису\n Після натискання «Реєстрація» вам надається два текстові поля для введення свого імені, прізвища. Ці данні мають складатися з букв українського або англійського алфавіту, перша з них – велика літера. Після введення даних в кожне поле ви повинні підтвердити введення, а в самому кінці натиснути «далі», щоб перейти до наступного етапу реєстрації. \n Наступний крок вашої реєстрації – це введення логіну та паролю. В разі, якщо введені вами дані не підходять під вимоги програми, вам буде про це повідомлення у строці повідомлень. Після підтвердження вами введених даних, програма відображає ваш акаунт, як зареєстрований. В разі, якщо ви вже маєте обліковий запис, вам достатньо ввести логін та пароль від свого акаунту, після чого натиснути «вхід» та потрапити до нього.\n 2.    Видалення облікового запису\n" Якщо ви бажаєте видалити свій обліковий запис, потрібно натиснути «Х». Після цього потрібно ввести свій логін та пароль. В разі, якщо вони вірні, програма повідомить, що ваш обліковий запис видалено, після чого ви потрапите на головне меню.\n 3.    Вхід\nЯкщо ви вже маєте обліковий запис, та бажаєте увійти до нього, потрібно натиснути «Увійти» та вам буде представлено сторінку для вводу ваших особистих даних. Достатньо ввести логін та пароль, які були створені під час реєстрації.')
        self.pushButtonn.setText('Назад')
        self.setWindowTitle('Допомога')
        
        self.pushButtonn.pressed.connect(self.login6)
        
    def login6(self):
        self.login = Login()
        self.login.show()
        self.hide()

class Delet(QtWidgets.QMainWindow, part.Ui_MainWindow):
    def __init__(self):
        super(Delet, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Видалити')
        self.lineEdit.setPlaceholderText('Введіть логін')
        self.lineEdit_2.setPlaceholderText('Введіть пароль')
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setText('')
        self.pushButton.setText('Реєстрація')
        self.pushButton_2.setText('Назад')
        self.pushButton_4.setText('Видалити')
        self.setWindowTitle('Видалення')
        
        self.pushButton.pressed.connect(self.regestr)
        self.pushButton_2.pressed.connect(self.regg)
        self.pushButton_4.pressed.connect(self.deleter)

    def regestr(self):
        self.reg = Registration()
        self.reg.show()
        self.hide()


    def regg(self):
        self.helper = Login()
        self.helper.show()
        self.hide()

    def deleter(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0:
            return

        if len(user_password) == 0:
            return

        #потрібно прописати функцію видалення user_login та user_password
        check_login = cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
        check_pass = cursor.execute(f'SELECT password FROM users WHERE login="{user_password}"')
        

        if check_login and check_pass is not None:
            #яку тут написати умову щоб видалявся аккаунт, якщо він є
            #чи правильно тут?
            check_login = cursor.execute(f'DELETE FROM users WHERE login="{user_login}"')
            check_pass = cursor.execute(f'DELETE FROM users WHERE login="{user_password}"')
            self.label.setText('Користувача видалено!')
        else:
            self.label.setText('Такого користувача не знайдено!')
        

class Login(QtWidgets.QMainWindow, part.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Увійти')
        self.lineEdit.setPlaceholderText('Введіть логін')
        self.lineEdit_2.setPlaceholderText('Введіть пароль')
        self.pushButton.setText('Вхід')
        self.pushButton_2.setText('Реєстрація')
        self.pushButton_3.setText('X')
        self.pushButton_4.setText('Допомога')
        self.setWindowTitle('Вхід')
        

        self.pushButton.pressed.connect(self.login)
        self.pushButton_2.pressed.connect(self.reg)
        self.pushButton_3.pressed.connect(self.deleter)
        self.pushButton_4.pressed.connect(self.helper)

    def deleter(self):
        self.helper = Delet()
        self.helper.show()
        self.hide()

    def helper(self):
        self.helper = Help()
        self.helper.show()
        self.hide()

    def reg(self):
        self.reg = Registration()
        self.reg.show()
        self.hide()

    def login(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0:
            return

        if len(user_password) == 0:
            return

        cursor.execute(f'SELECT password FROM users WHERE login="{user_login}"')
        check_pass = cursor.fetchall()

        cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
        check_login = cursor.fetchall()

        if check_pass[0][0] == user_password and check_login[0][0] == user_login:
            self.label.setText('Авторизація пройшла успішно!')
        else:
            self.label.setText('Йой! Ви ще не зареєстровані')
    

    
        

class Registration(QtWidgets.QMainWindow, part.Ui_MainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Реєстрація')
        self.lineEdit.setPlaceholderText("Введіть ім'я")
        self.lineEdit_2.setPlaceholderText('Введіть прізвище')
        self.pushButton.setText('Далі')
        self.pushButton_2.setText('Назад')
        self.pushButton_3.setText('')
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setText('Підтвердити')
        self.setWindowTitle('Реєстрація')
        

        self.pushButton.pressed.connect(self.login1)
        self.pushButton_2.pressed.connect(self.login2)
        self.pushButton_4.pressed.connect(self.reg1)


    def login2(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def login1(self):
        self.login = Registration1()
        self.login.show()
        self.hide()

    def reg1(self):
        user_name = self.lineEdit.text()
        user_secondn = self.lineEdit_2.text()

        if len(user_secondn) == 0 or len(user_name) == 0:
            self.label.setText("Заповніть, будь ласка, всі поля")

        if cursor2.fetchone() is None:
            if user_name.isalpha() == False or user_secondn.isalpha() == False:
                self.label.setText("Фамілія, ім'я повинні містити тільки літери!") 
            else:
                self.label.setText("Збережено!") 
                cursor2.execute(f'INSERT INTO user VALUES ("{user_name}", "{user_secondn}")')
                db1.commit()    


class Registration1(QtWidgets.QMainWindow, part.Ui_MainWindow):
    def __init__(self):
        super(Registration1, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Реєстрація')
        self.lineEdit.setPlaceholderText("Введіть логін")
        self.lineEdit_2.setPlaceholderText('Введіть пароль')
        self.pushButton.setText('Далі')
        self.pushButton_2.setText('Назад')
        self.pushButton_3.setText('')
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setText('Підтвердити')
        self.setWindowTitle('Реєстрація')
        

        self.pushButton.pressed.connect(self.login4)
        self.pushButton_2.pressed.connect(self.login3)
        self.pushButton_4.pressed.connect(self.reg3)

    def login3(self):
        self.login = Registration()
        self.login.show()
        self.hide()

    def login4(self):
        self.login = Login()
        self.login.show()
        self.hide() 
    
    def reg3(self):
            user_login = self.lineEdit.text()
            user_password = self.lineEdit_2.text()

            if len(user_login) == 0:
                return

            if len(user_password) == 0:
                return

            cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
            if cursor.fetchone() is None:
                if re.match(r'\w*', user_login) and re.match(r'\w*', user_password):
                    cursor.execute(f'INSERT INTO users VALUES ("{user_login}", "{user_password}")')
                    self.label.setText(f'Вітаємо {user_login} у програмі!')
                    db.commit()
                else:
                    self.label.setText('Щось не так(')

            else:
                self.label.setText('Вас було зареєстровано раніше.')


App = QtWidgets.QApplication([])
window = Login()
window.show()
App.exec()