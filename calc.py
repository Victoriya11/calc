import sys
from typing import Union, Optional
from operator import add, sub, mul, truediv, pow
from decimal import *
from math import sqrt

from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import *

from design import Ui_MainWindow

operations = {
    '+': add,
    '-': sub,
    '×': mul,
    '÷': truediv,
    '^': pow,    
}

error_zero_div = 'Деление на ноль невозможно'
error_undefined = 'Результат не определен'
error_big_num = 'Слишком большое число'

default_font_size = 16
default_entry_font_size = 25

class Calculator(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Calculator, self).__init__(*args, **kwargs)
        self.setupUi(self)      
        self.entry_max_len = self.entry.maxLength() 

        # кнопки цифр
        self.btn_0.clicked.connect(self.add_digit)
        self.btn_1.clicked.connect(self.add_digit)
        self.btn_2.clicked.connect(self.add_digit)
        self.btn_3.clicked.connect(self.add_digit)
        self.btn_4.clicked.connect(self.add_digit)
        self.btn_5.clicked.connect(self.add_digit)
        self.btn_6.clicked.connect(self.add_digit)
        self.btn_7.clicked.connect(self.add_digit)
        self.btn_8.clicked.connect(self.add_digit)
        self.btn_9.clicked.connect(self.add_digit)

        # кнопки функций
        self.btn_del.clicked.connect(self.clear_all)
        self.btn_per.clicked.connect(self.percent)
        self.btn_point.clicked.connect(self.add_point)
        self.btn_neg.clicked.connect(self.negate)
        self.btn_backspace.clicked.connect(self.backspace)
        self.btn_ms.clicked.connect(self.memory_save)
        self.btn_mr.pressed.connect(self.memory_recall)
        self.btn_sqrt.clicked.connect(self.sqrt)
        self.btn_1x.clicked.connect(self.obrat)
        self.btn_equal.clicked.connect(self.equals)

        # кнопки арифметических операций
        self.btn_add.clicked.connect(self.math_operation)
        self.btn_sub.clicked.connect(self.math_operation)
        self.btn_mul.clicked.connect(self.math_operation)
        self.btn_div.clicked.connect(self.math_operation)
        self.btn_pow.clicked.connect(self.math_operation)      
        
        # кнопка решить квадратное уравнение
        self.btn_result.clicked.connect(self.quadratic_equation) 

    def add_digit(self) -> None: # добавление цифры при нажатии на кнопку
        self.remove_error()
        self.clear_temp_if_equality()
        btn = self.sender() 

        digit_buttons = ('btn_0', 'btn_1', 'btn_2', 'btn_3', 'btn_4',
                         'btn_5', 'btn_6', 'btn_7', 'btn_8', 'btn_9') 
        
        if btn.objectName() in digit_buttons:
            if self.entry.text() == '0':
                self.entry.setText(btn.text()) 
            else:
                self.entry.setText(self.entry.text() + btn.text()) 
        self.adjust_entry_font_size()
        
    def percent(self): # функция вычисления процента   
        self.remove_error()
        entry = self.entry.text()
        temp = self.temp.text()
        if temp:
            try:
                per = self.get_entry_num() * self.get_temp_num() / 100
                result = self.remove_trailing_zeros(
                str(round(operations[self.get_math_sign()](self.get_temp_num(), per), 6)))
                
                self.temp.setText(temp + self.remove_trailing_zeros(entry) + ' %')
                self.adjust_temp_font_size()
                self.entry.setText(result)
                self.adjust_entry_font_size()
                
            except KeyError: 
                pass                                     
             
    def memory_save(self): # функция запомнить число в поле
        global save
        if self.is_number():
            save = self.entry.text()
            
    def is_number(self): # функция проверки строки на число
        try:
            float(self.entry.text())
            return True
        except ValueError:
            return False
        
    def memory_recall(self): # функция добавить в поле ввода число из памяти
        try:
            self.entry.setText(save)
            self.adjust_entry_font_size()
        except NameError: 
            pass     
        
    def sqrt(self): # функция извлечения из квадратного корня
        entry = self.entry.text()
        temp = self.temp.text()
        self.remove_error()
        try:
            result = self.remove_trailing_zeros(
            str(round(sqrt(self.get_entry_num()), 6)))
            
            self.temp.setText('√ ' + self.remove_trailing_zeros(entry))
            self.adjust_temp_font_size()
            self.entry.setText(result)
            self.adjust_entry_font_size()
            
        except KeyError: 
            pass   
        except TypeError: 
            pass  
        except ValueError: 
            pass        
                    
    def obrat(self): # функция нахождение обратного числа
        entry = self.entry.text()
        temp = self.temp.text()       
        self.remove_error()
        
        try:
            result = self.remove_trailing_zeros(
            str(round(1 / self.get_entry_num()), 6))
            
            self.temp.setText('1 / ' + self.remove_trailing_zeros(entry))
            self.adjust_temp_font_size()
            self.entry.setText(result)
            self.adjust_entry_font_size()
                
        except KeyError: 
            pass         
        except ZeroDivisionError:
            if self.get_temp_num() == 0:
                self.show_error(error_undefined)
            else:
                self.show_error(error_zero_div)   
                
    def add_point(self) -> None: # добавление точки для вещественных чисел
        self.clear_temp_if_equality()
        if '.' not in self.entry.text():
            self.entry.setText(self.entry.text() + '.')
            self.adjust_entry_font_size()

    def negate(self) -> None: # функция смены знака
        self.remove_error()
        self.clear_temp_if_equality()
        entry = self.entry.text()

        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]

        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.entry.setMaxLength(self.entry_max_len + 1) 
        else:
            self.entry.setMaxLength(self.entry_max_len)

        self.entry.setText(entry)
        self.adjust_entry_font_size()

    def backspace(self) -> None: # удаляет последний символ
        self.remove_error()
        self.clear_temp_if_equality()
        entry = self.entry.text()

        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.entry.setText('0')
            else:
                self.entry.setText(entry[:-1])  
        else:
            self.entry.setText('0')

        self.adjust_entry_font_size()

    def clear_all(self) -> None: # очищаем поле ввода и временное выражение
        self.remove_error()
        self.entry.setText('0')
        self.adjust_entry_font_size()
        self.temp.clear()
        self.adjust_temp_font_size()

    def clear_temp_if_equality(self) -> None: # функция очищения временного выражения, если в нем есть знак равно        
        if self.get_math_sign() == '=':
            self.temp.clear()
            self.adjust_temp_font_size()
              
    @staticmethod
    def remove_trailing_zeros(num: str) -> str: # удаляем незначащие конечные нули
        try:
            n = str(float(num))
            return n.replace('.0', '') if n.endswith('.0') else n        
        except ValueError:
            pass

    def add_temp(self) -> None:  # добавляем временное выражение
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.entry.text()) 
        try:
            if self.get_entry_num() > 99999999:
                self.show_error(error_big_num) 
            else:  
                if not self.temp.text() or self.get_math_sign() == '=':
                    self.temp.setText(entry + f' {btn.text()} ') 
                    self.adjust_temp_font_size()
                    self.entry.setText('0') 
                    self.adjust_entry_font_size()               
        except TypeError:
            pass

    def get_entry_num(self) -> int | str: # возвращаем число из поля ввода
        try:
            entry = self.entry.text().strip('.')
            return Decimal(str(entry)) if '.' in entry else int(entry)
        except ValueError:
            pass

    def get_temp_num(self) -> int | str | None: # возвращаем число из временного выражения
        if self.temp.text(): 
            temp = self.temp.text().strip('.√').split()[0]
            return Decimal(str(temp)) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:  # получаем знак операции
        if self.temp.text():
            return self.temp.text().strip('.').split()[-1]

    def equals(self) -> Optional[str]: # функция вычисления
        entry = self.entry.text()
        temp = self.temp.text()
        self.clear_temp_if_equality()
        self.remove_error()
        if temp:
            try:
                if '%' in temp: 
                    if '=' not in temp:
                        self.temp.setText(temp + ' =')
                        self.adjust_temp_font_size()
                    elif self.get_math_sign() == btn.text():
                        self.temp.setText(entry + f' {btn.text()} ') 
                        self.adjust_temp_font_size()
                        self.entry.setText('0') 
                        self.adjust_entry_font_size()                           
                elif '/' in temp and '=' not in temp:
                    self.temp.setText(temp + ' =')
                    self.adjust_temp_font_size()
                elif '√' in temp and '=' not in temp:
                    self.temp.setText(temp + ' =')
                    self.adjust_temp_font_size()                      
                     
                else:    
                    result = self.remove_trailing_zeros(
                    str(round(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()), 6))
                )
                    self.temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
                    self.adjust_temp_font_size()
                    if len(result) > self.entry_max_len:
                        self.show_error(error_undefined)
                    else:
                        self.entry.setText(result)
                        self.adjust_entry_font_size()
                        return result

            except KeyError: 
                pass

            except ZeroDivisionError:
                if self.get_temp_num() == 0:
                    self.show_error(error_undefined)
                else:
                    self.show_error(error_zero_div)    
            except InvalidOperation:
                self.show_error(error_undefined)

    def math_operation(self) -> None: # функция математической операции
        temp = self.temp.text()
        btn = self.sender()
        self.remove_error()
        
        if not temp:
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == '=':
                    self.add_temp()
                else:   
                    if '%' not in temp and '√' not in temp and '/' not in temp:
                        self.temp.setText(temp[:-2] + f'{btn.text()} ')  
                    else:
                        self.temp.setText(self.remove_trailing_zeros(self.entry.text()) + f' {btn.text()} ')
                        self.entry.setText('0')
            else:
                try:                                       
                    self.temp.setText(self.equals() + f' {btn.text()} ')
                    self.entry.setText('0')
                except TypeError:
                    pass

        self.adjust_temp_font_size()

    def show_error(self, text: str) -> None: # функция показа ошибки
        self.entry.setMaxLength(len(text))
        self.entry.setText(text)
        self.adjust_entry_font_size()

    def remove_error(self) -> None: # если текст поля равен ошибке, возвращаем дефолтное состояние
        if self.entry.text() in (error_undefined, error_zero_div, error_big_num):
            self.entry.setMaxLength(self.entry_max_len)
            self.entry.setText('0')
            self.adjust_entry_font_size()

    def get_entry_text_width(self) -> int: # получаем ширину текста ввода в пикселях
        return self.entry.fontMetrics().boundingRect(self.entry.text()).width()

    def get_temp_text_width(self) -> int: # получаем ширину текста временного выражения в пикселях
        return self.temp.fontMetrics().boundingRect(self.temp.text()).width()
    
    def adjust_entry_font_size(self) -> None: # регулирование размера шрифта в поле ввода
        font_size = default_entry_font_size
        while self.get_entry_text_width() > self.entry.width() - 15:
            font_size -= 1 
            self.entry.setStyleSheet('font-size: ' + str(font_size) + 'pt; border: none;')

        font_size = 1
        while self.get_entry_text_width() < self.entry.width() - 60:
            font_size += 1 

            if font_size > default_entry_font_size:
                break

            self.entry.setStyleSheet('font-size: ' + str(font_size) + 'pt; border: none;')

    def adjust_temp_font_size(self) -> None: # регулирование размера шрифта в поле временного выражения
        font_size = default_font_size
        while self.get_temp_text_width() > self.temp.width() - 10:
            font_size -= 1
            self.temp.setStyleSheet('font-size: ' + str(font_size) + 'pt; color: #666666;')

        font_size = 1
        while self.get_temp_text_width() < self.temp.width() - 60:
            font_size += 1

            if font_size > default_font_size:
                break

            self.temp.setStyleSheet('font-size: ' + str(font_size) + 'pt; color: #666666;')

    def resizeEvent(self, event) -> None: # регулируем размер шрифта при изменении ширины окна
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()

    def quadratic_equation(self): # функция вычисления дискриминанта и корней квадратного уравнения
        try: 
            a = int(self.a.text())
            b = int(self.b.text())
            c = int(self.c.text())
            d = b**2 - 4 * a * c
            if d > 0:
                x1 = (- b + sqrt(d))/(2*a)
                x2 = (- b - sqrt(d))/(2*a)
            elif d == 0:
                x1 = -b/(2*a)
                x2 = 'нет корня'        
            elif d < 0:
                x1 = 'нет корня'
                x2 = 'нет корня'
            self.Discriminant.setText('D = ' + str(d))
            self.x1.setText('x1 = ' + str(x1))
            self.x2.setText('x2 = ' + str(x2))
        except ValueError:
            pass    
        except ZeroDivisionError:
            self.Discriminant.setText('a ≠ 0')
            self.x1.setText('')
            self.x2.setText('') 
            
if __name__ == "__main__":
    app = QApplication(sys.argv) 

    window = Calculator() 
    window.show() 

    sys.exit(app.exec()) 
