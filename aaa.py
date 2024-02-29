from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QTextEdit, QTabWidget, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QIcon, QWheelEvent

file_path_save = ''

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
    if file_path_save != '':
        file_path = file_path_save
        if file_path:
            text = text_box.toPlainText()
            with open(file_path, 'w') as file:
                file.write(text)

# Funcion para limpiar el editor de texto y la ruta de algun archivo
def clear():
    global file_path_save
    file_path_save = ''
    text_box.clear()

# Funcion para actualizar los numeros de linea
def update_line_numbers():
    text = text_box.toPlainText()
    lines = text.split('\n')
    line_count = len(lines)
    num_box.setPlainText('\n'.join(str(i + 1) for i in range(line_count)))
    num_box.verticalScrollBar().setValue(text_box.verticalScrollBar().value())

# Funcion para manejar el evento de cambio de texto en el QTextEdit
def text_changed():
    update_line_numbers()

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
open_button.clicked.connect(save)

# Agregar el boton anterior en el layout de menu
menu_layout.addWidget(open_button)

# Crear un PushButton para limpiar el texto y la ruta del archivo abierto
close_button = QPushButton('', window)
close_button.setIcon(QIcon('delete_icon.jpg'))  # Set the icon
close_button.setIconSize(close_button.sizeHint())
close_button.clicked.connect(clear)

# Agregar el boton anterior en el layout de menu
menu_layout.addWidget(close_button)

# Agregar el layout del menu al layout de la izquierda
left_layout.addLayout(menu_layout)

# Crear un HBoxLayout para manejar los EditText de num de filas y el editor de texto
text_layout = QHBoxLayout()

# Crear un TextEdit para mostrar el numero de filas en el editor de texto
num_box = NoScrollTextEdit(window)
num_box.setPlaceholderText("")
num_box.setFixedWidth(45)
num_box.setReadOnly(True)
num_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Disable vertical scrollbar

# Añadir el TextEdit anterior
text_layout.addWidget(num_box)

# Crear el EditText para manejar el editor de texto
text_box = QTextEdit(window)
Font = QFont()
Font.setFamily("Algerian")
Font.setPointSize(15)
text_box.setFont(Font)
text_box.setPlaceholderText("Enter text here...")
text_box.verticalScrollBar().valueChanged.connect(scroll_event)
text_box.textChanged.connect(text_changed)

# Agregar el editor de texto
text_layout.addWidget(text_box)

# Agregar el Layout de editor de texto y num de columnas en el Layout izquierdo principal
left_layout.addLayout(text_layout)

# Crear dos instancias de TabWidget
tab_widget_1 = QTabWidget()
tab_widget_2 = QTabWidget()

# Colores para los tabs y el editor de texto
#tab_widget_1.setStyleSheet("background-color: #4A4063; color: #BFACC8")
#tab_widget_2.setStyleSheet("background-color: #4F1271; color: #BFACC8")
text_box.setStyleSheet("background-color: #9A7CAC; color: #CFB8D7")

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
    tab_widget_1.addTab(QWidget(), f'Tab {i+1}')
    tab_widget_1.widget(i).layout = QVBoxLayout()
    tab_widget_1.widget(i).layout.addWidget(label)
    tab_widget_1.widget(i).setLayout(tab_widget_1.widget(i).layout)
    style = "background-color:"+colorsp1[i] + ";QTabBar::tab { background-color: " + colorsp1[i] + " color: black; }"
    tab_widget_1.widget(i).setStyleSheet(style)

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
