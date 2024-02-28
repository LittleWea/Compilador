from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QTextEdit, QTabWidget, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

file_path_save = ''

labels = {'lexico', 'semantico', 'sintactico', 'hash', 'codigo'}

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

def clear():
    global file_path_save
    file_path_save = ''
    text_box.clear()

# Creacion de una instancia de Application
app = QApplication([])

# Crear un Widget, que sera la ventana principal
window = QWidget()
window.setWindowIcon(QIcon('window_icon.JPG'))
window.setWindowTitle("CalebPerezScript")
window.setGeometry(100, 100, 600, 400)  # Posicion y tamaño de la ventana

# Crear un HBoxLayout para poner los objetos de forma horizontal
layout = QHBoxLayout(window)

# Crear un Label
label = QLabel('Hello, PyQt5!', parent=window)

# Agregar el Label anterior
layout.addWidget(label)

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

# Crear un PushButton para limpiar el texto
close_button = QPushButton('', window)
close_button.setIcon(QIcon('delete_icon.jpg'))  # Set the icon
close_button.setIconSize(close_button.sizeHint())
close_button.clicked.connect(clear)

# Agregar el boton anterior en el layout de menu
menu_layout.addWidget(close_button)

#Agregar el layout del menu al layout de la izquierda
left_layout.addLayout(menu_layout)

# Crear un TextEdit para escribir u obtener el codigo planteado
text_box = QTextEdit(window)
text_box.setPlaceholderText("Enter text here...")

# Agregar el TextEdit anterior en el layout izquierdo
left_layout.addWidget(text_box)

# Crear dos instancias de TabWidget
tab_widget_1 = QTabWidget()
tab_widget_2 = QTabWidget()

# Añadir los TabWidget anteriores al layout derecho
right_layout.addWidget(tab_widget_1)
right_layout.addWidget(tab_widget_2)

# Añadir los layouts izquierdo y derecho al layout principal
layout.addLayout(left_layout)
layout.addLayout(right_layout)

# Crear los elementos para cada uno de los TabWidgets
for i in range(5):
    # Create a label for the tab
    label = QLabel(f'Initial Text for Tab {i+1}')
    # Add the label to the tab's widget
    tab_widget_1.addTab(QWidget(), f'Tab {i+1}')
    tab_widget_1.widget(i).layout = QVBoxLayout()
    tab_widget_1.widget(i).layout.addWidget(label)
    tab_widget_1.widget(i).setLayout(tab_widget_1.widget(i).layout)

# Access the widget associated with each tab in tab_widget_1 and change the text of its label
    
tab_widget_1.setTabText(0, "Lexico")
tab_widget_1.setTabText(1, "Semantico")
tab_widget_1.setTabText(2, "Sintactico")
tab_widget_1.setTabText(3, "Hash Table")
tab_widget_1.setTabText(4, "Codigo Intermedio")

for i in range(4):
    # Create a label for the tab
    label = QLabel(f'Initial Text for Tab {i+1}')
    tab_widget_2.addTab(QWidget(), f'Tab {i+1}')
    tab_widget_2.widget(i).layout = QVBoxLayout()
    tab_widget_2.widget(i).layout.addWidget(label)
    tab_widget_2.widget(i).setLayout(tab_widget_2.widget(i).layout)

tab_widget_2.setTabText(0, "Errores Lexicos")
tab_widget_2.setTabText(1, "Errores Sintacticos")
tab_widget_2.setTabText(2, "Errores Semanticos")
tab_widget_2.setTabText(3, "Resultados")

for i in range(5):
    tab_widget_1.widget(i).layout.itemAt(0).widget().setText(f'New Text for Tab {i+1}')

# Show the main window
window.show()

# Start the application's event loop
app.exec_()
