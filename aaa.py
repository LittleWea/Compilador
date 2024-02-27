from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QComboBox, QTextEdit, QTabWidget, QWidget, QHBoxLayout, QPushButton, QFileDialog

# Create a custom slot function to handle the selection change
def handle_selection_change(index):
    selected_item = combo_box.currentText()
    if selected_item == 'Option 1':
        open_file()
    elif selected_item == 'Option 2':
        save_file()
    else:
        print("Selected item:", selected_item)

# Function to open a file
def open_file():
    file_path, _ = QFileDialog.getOpenFileName(window, 'Open File', '', 'All Files (*)')
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            text_box.setPlainText(text)

def save_file():
    file_path, _ = QFileDialog.getSaveFileName(window, 'Save File', '', 'All Files (*)')
    if file_path:
        text = text_box.toPlainText()
        with open(file_path, 'w') as file:
            file.write(text)

# Create a QApplication instance
app = QApplication([])

# Create a QWidget instance (main window)
window = QWidget()
window.setGeometry(100, 100, 600, 400)  # Set window size and position

# Create a QHBoxLayout to arrange widgets horizontally
layout = QHBoxLayout(window)

# Create a QLabel widget (text label)
label = QLabel('Hello, PyQt5!', parent=window)

# Add the label to the layout
layout.addWidget(label)

# Create a QVBoxLayout to arrange widgets vertically
left_layout = QVBoxLayout()
right_layout = QVBoxLayout()

# Create a QComboBox widget (dropdown menu)
combo_box = QComboBox(window)
combo_box.addItem('Option 1')
combo_box.addItem('Option 2')
combo_box.addItem('Option 3')

# Connect the currentIndexChanged signal to the handle_selection_change function
combo_box.currentIndexChanged.connect(handle_selection_change)

# Add the combo box to the left layout
left_layout.addWidget(combo_box)

# Create a QTextEdit widget (text box)
text_box = QTextEdit(window)
text_box.setPlaceholderText("Enter text here...")

# Add the text box to the left layout
left_layout.addWidget(text_box)

# Create two instances of QTabWidget
tab_widget_1 = QTabWidget()
tab_widget_2 = QTabWidget()

# Add the tab widgets to the right layout
right_layout.addWidget(tab_widget_1)
right_layout.addWidget(tab_widget_2)

# Add the layouts to the main layout
layout.addLayout(left_layout)
layout.addLayout(right_layout)

# Create five tabs for each QTabWidget
for i in range(5):
    tab_widget_1.addTab(QWidget(), f'Tab {i+1}')
    tab_widget_2.addTab(QWidget(), f'Tab {i+1}')

# Create a QPushButton to open a file
open_button = QPushButton('Open File', window)
open_button.clicked.connect(open_file)

# Add the button to the left layout
left_layout.addWidget(open_button)

# Show the main window
window.show()

# Start the application's event loop
app.exec_()
