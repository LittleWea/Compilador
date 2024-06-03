from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QTextEdit, QTabWidget, QHBoxLayout, QPushButton, QFileDialog, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QIcon, QWheelEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtMultimedia, QtCore, QtGui

import os, re

from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QUrl

from analLexico import lexer, tipoToken


file_path_save = os.path.join(os.getcwd(), 'default.cps')

labels = {'lexico', 'semantico', 'sintactico', 'hash', 'codigo'}
colorsp1 = ['#995FA3','#93509F','#8D419B','#873297','#802392']
colorsp2 = ['#CE7B91','#B47182']

class NoScrollTextEdit(QTextEdit):
    def wheelEvent(self, event: QWheelEvent):
        pass  # Ignore wheel events

# Funcion para manejar el cambio de la seleccion de opciones
def handle_selection_change(index):
    selected_item = combo_box.currentText()
    if selected_item == 'Abrir...':
        open_file()
    elif selected_item == 'Guardar como...':
        save_file()
    elif selected_item == 'Guardar...':
        save()
    else:
        print("Selected item:", selected_item)
    combo_box.setCurrentIndex(0)

# Funcion para abrir archivos y escribir sobre el TextEdit
def open_file():
    file_path, _ = QFileDialog.getOpenFileName(window, 'Abrir Archivo', '', 'CalebPerezScript(*.cps)')
    if file_path:
        global file_path_save
        file_path_save = file_path
        print(file_path_save)
        with open(file_path, 'r') as file:
            text = file.read()
            text_box.setPlainText(text)
            update_line_numbers()
            
def apply_syntax_highlighting():
    cursor = text_box.textCursor()
    cursor.movePosition(QtGui.QTextCursor.Start)

    # Obtener el texto actual
    texto = text_box.toPlainText()

    # Limpiar el formato previo
    formato_default = QtGui.QTextCharFormat()
    formato_default.setForeground(QtGui.QColor("#FFFFFF"))  # Color de texto predeterminado
    cursor.select(QtGui.QTextCursor.Document)
    cursor.mergeCharFormat(formato_default)

    # Aplicar resaltado de sintaxis
    tokens = lexer(texto)
    for token, linea, columna in tokens:
        formato = QtGui.QTextCharFormat()
        tipo = tipoToken(token)
        color = get_color(tipo)
        formato.setForeground(QtGui.QColor(color))
        cursor.setPosition(text_box.document().findBlockByLineNumber(linea - 1).position() + columna - 1)
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, len(token))
        cursor.mergeCharFormat(formato)


# Function to get color for a token type
def get_color(token_type):
    if token_type == 'error':
        return '#00FF0D'  # Default text color
    elif token_type == 'palabra reservada':
        return '#0000FF'  # Blue
    elif token_type == 'identificador':
        return '#000000'  # Black
    elif token_type == 'comentario':
        return '#00FF00'  # Green
    elif token_type == 'simbolo aritmetico':
        return '#FFFF00'  # Yellow
    elif token_type in 'numero real':
        return '#FF0000'  # Red
    elif token_type in 'numero entero':
        return '#808080'  # Gray
    elif token_type == 'sibolo logico':
        return '#800080'  # Purple
    elif token_type in ('simbolo parentesis'):
        return '#FF00FF'  # Magenta
    elif token_type in ('simbolo corchete'):
        return '#FFA500'  # Orange
    elif token_type in ('simbolo llave'):
        return '#A52A2A'  # Brown
    elif token_type == 'simbolo puntuacion':
        return '#FFC0CB'  # Pink
    elif token_type == 'operador logico':
        return '#000080'  # Navy
    
# Funcion para actualizar la posicion del cursor
def update_cursor_position():
    cursor = text_box.textCursor()
    cursor_position = cursor.position()
    block = text_box.document().findBlock(cursor_position)
    cursor_position_in_block = cursor_position - block.position()
    line_number = block.blockNumber() + 1
    column_number = cursor_position_in_block + 1
    cursor_position_label.setText(f'Linea: {line_number}, Columna: {column_number}')
    
# Funcion para abrir un archivo y mantener su ruta por si es necesario guardarlo despues
def save_file():
    file_path, _ = QFileDialog.getSaveFileName(window, 'Guardar Archivo como', '', 'CalebPerezScript(*.cps)')
    if file_path:
        global file_path_save
        file_path_save = file_path
        text = text_box.toPlainText()
        with open(file_path, 'w') as file:
            file.write(text)

# Funcion para guardar el contenido sobre una ruta ya especificada antes
def save():
    global file_path_save
    file_path = file_path_save

    if file_path:
        text = text_box.toPlainText()
        with open(file_path, 'w') as file:
            file.write(text)

# Funcion para limpiar el editor de texto y la ruta de algun archivo
def clear():
    global file_path_save
    file_path_save = os.path.join(os.getcwd(), 'default.cps')
    text_box.clear()
    
#Función para guardar los tokens en un archivo llamado tokens.cps
def save_tokens(tokens):
    with open('tokens.cps', 'w') as file:
        for token in tokens:
            file.write(f"'{token[0]}': {tipoToken(token[0])}\n")

# Función para guardar los errores en un archivo llamado errores.cps
def save_errors(tokens):
    with open('errores.cps', 'w') as file:
        for token in tokens:
            if tipoToken(token[0]) == 'error':
                file.write(f"'{token[0]}': error en columna {token[2]}, fila {token[1]}\n")


def lexic_anal():
    text = text_box.toPlainText()
    tokens = lexer(text)
    save_tokens(tokens)
    save_errors(tokens)
    text = ''
    textError = ''
    for token in tokens:
        aux = tipoToken( token[0] )
        if aux != 'error':
            text += "'" + token[0] + ': ' + str(aux) + "\n"
        else:
            textError += "'" + token[0] + "': " + str(aux) + " en columna: " + str(token[2]) + ", fila: " + str(token[1]) + "\n"


    tab_widget_1.widget(0).layout.itemAt(0).widget().setText(text)
    tab_widget_2.widget(0).layout.itemAt(0).widget().setText(textError)


# Funcion para actualizar los numeros de linea
def update_line_numbers():
    text = text_box.toPlainText()
    lines = text.split('\n')
    line_count = len(lines)
    num_box.setPlainText('\n'.join(str(i + 1) for i in range(line_count)))
    num_box.verticalScrollBar().setValue(text_box.verticalScrollBar().value())

# Funcion para manejar el evento de cambio de texto en el QTextEdit
def text_changed():
    text_box.textChanged.disconnect()

    # Realizar la actualización del texto
    update_line_numbers()
    apply_syntax_highlighting()
    # Volver a conectar el evento textChanged
    text_box.textChanged.connect(text_changed)

# Funcion para manejar el evento de scroll
def scroll_event():
    update_line_numbers()

# Creacion de una instancia de Application
app = QApplication([])

# Crear un Widget, que sera la ventana principal
window = QWidget()
window.setWindowIcon(QIcon('window_icon.JPG'))
window.setWindowTitle("CalebPerezScript")
window.setGeometry(100, 100, 600, 400)  # Posicion y tamaño de la ventana

# Crear un HBoxLayout para poner los objetos de forma horizontal
layout = QHBoxLayout(window)

# Crear un VBoxLayout los cuales organizaran sus contenidos de forma vertical
left_layout = QVBoxLayout()
right_layout = QVBoxLayout()

# Crear un HBoxLayout para poner los objetos de forma horizontal
menu_layout = QHBoxLayout()

# Crear un ComboBox para seleccionar las opciones de archivos
combo_box = QComboBox(window)
combo_box.addItem('Opciones de Archivo')
combo_box.addItem('Abrir...')
combo_box.addItem('Guardar como...')
combo_box.addItem('Guardar...')

# Connect the currentIndexChanged signal to the handle_selection_change function
combo_box.currentIndexChanged.connect(handle_selection_change)

# Añadir el ComboBox en el layout del menu
menu_layout.addWidget(combo_box)

# Crear un PushButton para guardar el texto en un archivo ya abierto
open_button = QPushButton('', window)
open_button.setIcon(QIcon('save_icon.jpg'))  # Set the icon
open_button.setIconSize(open_button.sizeHint())
open_button.setToolTip('Save')
open_button.clicked.connect(save)

# Agregar el boton anterior en el layout de menu
menu_layout.addWidget(open_button)

# Crear un PushButton para limpiar el texto y la ruta del archivo abierto
close_button = QPushButton('', window)
close_button.setIcon(QIcon('delete_icon.jpg'))  # Set the icon
close_button.setIconSize(close_button.sizeHint())
close_button.setToolTip('Clear')
close_button.clicked.connect(clear)

# Agregar el boton anterior en el layout de menu
menu_layout.addWidget(close_button)

# Crear un PushButton para realizar el analisis lexico del texto
lexic_button = QPushButton('', window)
lexic_button.setIcon(QIcon('lex_icon.jpg'))  # Set the icon
lexic_button.setIconSize(close_button.sizeHint())
lexic_button.setToolTip('Lexic')
lexic_button.clicked.connect(lexic_anal)

# Agregar el boton anterior en el layout de menu
menu_layout.addWidget(lexic_button)

# Agregar el layout del menu al layout de la izquierda
left_layout.addLayout(menu_layout)

# Crear un HBoxLayout para manejar los EditText de num de filas y el editor de texto
text_layout = QHBoxLayout()

# Crear un TextEdit para mostrar el numero de filas en el editor de texto
num_box = NoScrollTextEdit(window)
num_box.setPlaceholderText("")
num_box.setFixedWidth(45)
num_box.setReadOnly(True)
Font_num_box = QFont()
Font_num_box.setFamily("Cascadia Code SemiLight")
Font_num_box.setPointSize(11)
num_box.setFont(Font_num_box)
num_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Disable vertical scrollbar

# Añadir el TextEdit anterior
text_layout.addWidget(num_box)

# Crear el EditText para manejar el editor de texto
text_box = QTextEdit(window)
Font = QFont()
fontf = QFontDatabase()
#print(fontf.families())
Font.setFamily("Cascadia Code SemiLight")
Font.setPointSize(11)
text_box.toPlainText()
text_box.setFont(Font)
text_box.setPlaceholderText("Enter text here...")
text_box.verticalScrollBar().valueChanged.connect(scroll_event)
text_box.textChanged.connect(text_changed)

text_box.setLineWrapMode(QTextEdit.NoWrap)

# Agregar el editor de texto
text_layout.addWidget(text_box)

# Agregar el Layout de editor de texto y num de columnas en el Layout izquierdo principal
left_layout.addLayout(text_layout)

# Crear dos instancias de TabWidget
tab_widget_1 = QTabWidget()
tab_widget_2 = QTabWidget()

# Colores para los tabs y el editor de texto
text_box.setStyleSheet("background-color: #9A7CAC; color: #FFFFFF")
# Añadir los TabWidget anteriores al layout derecho
right_layout.addWidget(tab_widget_1)
right_layout.addWidget(tab_widget_2)

# Añadir los layouts izquierdo y derecho al layout principal
layout.addLayout(left_layout)
layout.addLayout(right_layout)

# Crear los elementos para cada uno de los TabWidgets
for i in range(5):
    # Crear un Label para cada uno de los Tabs
    label = QLabel(f'Initial Text for Tab {i+1}')
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(label)
    tab_widget_1.addTab(scroll_area, f'Tab {i+1}')
    tab_widget_1.widget(i).layout = QVBoxLayout()
    tab_widget_1.widget(i).layout.addWidget(label)  # Add label to the scroll area's layout
    tab_widget_1.widget(i).setLayout(tab_widget_1.widget(i).layout)
    style = "background-color:"+colorsp1[i] + ";QTabBar::tab { background-color: " + colorsp1[i] + " color: black; }"
    tab_widget_1.setStyleSheet(style)  # Set stylesheet for the tab widget

# Acceder a cada uno de los tabs para cambiar sus titulos
tab_widget_1.setTabText(0, "Lexico")
tab_widget_1.setTabText(1, "Semantico")
tab_widget_1.setTabText(2, "Sintactico")
tab_widget_1.setTabText(3, "Hash Table")
tab_widget_1.setTabText(4, "Codigo Intermedio")

# Crear los elementos para cada uno de los TabWidgets
for i in range(2):
    # Crear un Label para cada uno de los Tabs
    label = QLabel(f'Initial Text for Tab {i+1}')
    tab_widget_2.addTab(QWidget(), f'Tab {i+1}')
    tab_widget_2.widget(i).layout = QVBoxLayout()
    tab_widget_2.widget(i).layout.addWidget(label)
    tab_widget_2.widget(i).setLayout(tab_widget_2.widget(i).layout)
    style = "background-color:"+colorsp2[i] + ";QTabBar::tab { color: black; }"
    tab_widget_2.widget(i).setStyleSheet(style)

# Acceder a cada uno de los tabs para cambiar sus titulos
tab_widget_2.setTabText(0, "Errores")
tab_widget_2.setTabText(1, "Resultados")

#Cambiar el texto interno de cada uno de los Labels de los Tabs
for i in range(5):
    tab_widget_1.widget(i).layout.itemAt(0).widget().setText(f'New Text for Tab {i+1}')

# Crear un QLabel para mostrar la posicion del cursor
cursor_position_label = QLabel('Linea: 1, Columna: 1')
left_layout.addWidget(cursor_position_label)

# Conectar el evento cursorPositionChanged al QTextEdit
text_box.cursorPositionChanged.connect(update_cursor_position)

# Mostrar la ventana principal
window.show()

# Comenzar la aplicacion en loop
app.exec_()