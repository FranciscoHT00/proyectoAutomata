import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
import time


from model import AppAutomata


class ControlPanel(qtw.QWidget):

    start_signal = qtc.pyqtSignal(str)
    speed_signal = qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(qtw.QVBoxLayout())
        self.setFixedSize(150, 500)

        self.automata_pixmap = qtg.QPixmap()
        self.automata_pixmap.load('./img/kleene_label.PNG')
        self.automata_label = qtw.QLabel()
        self.automata_label.setFixedSize(140, 40)
        self.automata_label.setPixmap(self.automata_pixmap.scaled(150, 60))
        self.word_label = qtw.QLabel('PALABRA')
        self.word_label.setFixedHeight(20)
        self.word_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.word_input = qtw.QLineEdit()
        self.state_label = qtw.QLabel('ESTADO')
        self.state_label.setFixedHeight(20)
        self.state_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.state_output = qtw.QTextEdit()
        self.state_output.setReadOnly(True)

        self.start_button = qtw.QPushButton('Iniciar')
        self.start_button.clicked.connect(self.start_button_pressed)

        self.speed_label = qtw.QLabel('VELOCIDAD')
        self.speed_label.setFixedHeight(20)
        self.speed_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.speed_state = qtw.QLineEdit()
        self.speed_state.setReadOnly(True)

        self.speed_buttonGroup = qtw.QButtonGroup()
        self.slow_speed_button = qtw.QPushButton('Lenta')
        self.slow_speed_button.clicked.connect(self.slow_speed_button_pressed)
        self.normal_speed_button = qtw.QPushButton('Normal')
        self.normal_speed_button.clicked.connect(self.normal_speed_button_pressed)
        self.fast_speed_button = qtw.QPushButton('Rápida')
        self.fast_speed_button.clicked.connect(self.fast_speed_button_pressed)
        self.speed_buttonGroup.addButton(self.slow_speed_button)
        self.speed_buttonGroup.addButton(self.normal_speed_button)
        self.speed_buttonGroup.addButton(self.fast_speed_button)

        self.layout().addWidget(self.automata_label)
        self.layout().addWidget(self.word_label)
        self.layout().addWidget(self.word_input)
        self.layout().addWidget(self.state_label)
        self.layout().addWidget(self.state_output)
        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.speed_label)
        self.layout().addWidget(self.speed_state)
        self.layout().addWidget(self.slow_speed_button)
        self.layout().addWidget(self.normal_speed_button)
        self.layout().addWidget(self.fast_speed_button)

    def start_button_pressed(self):
        self.start_signal.emit(self.word_input.text())

    def cancel_button_pressed(self):
        pass

    def step_speed_button_pressed(self):
        self.speed_signal.emit('step')

    def slow_speed_button_pressed(self):
        self.speed_signal.emit('slow')

    def normal_speed_button_pressed(self):
        self.speed_signal.emit('normal')

    def fast_speed_button_pressed(self):
        self.speed_signal.emit('fast')

    def instant_speed_button_pressed(self):
        self.speed_signal.emit('instant')

    def next_button_pressed(self):
        pass


class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Proyecto Autómata')
        self.setFixedWidth(1000)
        self.setFixedHeight(600)

        self.model = AppAutomata()

        self.pixmap = qtg.QPixmap()
        self.pixmap.load('./img/graph.png')
        self.image_label = qtw.QLabel()
        self.image_label.setPixmap(self.pixmap)
        self.setCentralWidget(self.image_label)

        self.graph_automata()

        menu_bar = self.menuBar()

        self.automata_menu = menu_bar.addMenu('Automata')
        self.automata_menu.addAction('Automata a la 5', self.load_automata_a_la_5)
        self.automata_menu.addAction('Automata - Clausura de Kleene', self.load_automata_kleene)

        language_menu = menu_bar.addMenu('Idioma')
        language_menu.addAction(qtg.QIcon('./img/en_icon'), 'English')
        language_menu.addAction(qtg.QIcon('./img/es_icon'), 'Español')

        self.controlPanel_dock = qtw.QDockWidget('Panel de Control')
        self.controlPanel = ControlPanel()
        self.controlPanel_dock.setWidget(self.controlPanel)
        self.controlPanel_dock.setFeatures(qtw.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        self.controlPanel_dock.setAllowedAreas(
            qtc.Qt.DockWidgetArea.RightDockWidgetArea | qtc.Qt.DockWidgetArea.LeftDockWidgetArea)

        self.addDockWidget(qtc.Qt.DockWidgetArea.RightDockWidgetArea, self.controlPanel_dock)

        self.controlPanel.speed_state.setText(self.model.speed)
        self.controlPanel.start_signal.connect(self.validate_word)
        self.controlPanel.speed_signal.connect(self.set_speed)

        self.statusBar().showMessage('Bienvenido a nuestra app!', 4000)

        self.show()

    def load_graph_img(self):
        self.pixmap.load('./img/graph.png')
        self.image_label.setPixmap(self.pixmap)
        self.update()
        self.image_label.repaint()
        qtw.QApplication.processEvents()

    def graph_automata(self):

        self.model.reset_graph()
        self.load_graph_img()

    def load_automata_kleene(self):

        self.model.active_automata = self.model.automata_kleene
        self.model.active_graph = self.model.graph_kleene
        self.model.active_automata_tag = 'automata_kleene'
        self.graph_automata()

    def load_automata_a_la_5(self):

        self.model.active_automata = self.model.automata_a_la_5
        self.model.active_graph = self.model.graph_a_la_5
        self.model.active_automata_tag = 'automata_a_la_5'
        self.graph_automata()

    def validate_word(self, word):

        last = 'q0'
        self.controlPanel.state_output.clear()
        try:
            result = self.model.validate_word(word)
            for i in result:
                last = i
                self.controlPanel.state_output.append(last)
                self.model.update_graph(last)
                self.load_graph_img()

                if self.model.speed == 'step':
                    time.sleep(2)
                elif self.model.speed == 'slow':
                    time.sleep(2)
                elif self.model.speed == 'normal':
                    time.sleep(1)
                elif self.model.speed == 'fast':
                    time.sleep(0.5)
        except:
            self.model.update_graph_error(last)
            self.load_graph_img()
            self.controlPanel.state_output.append('La palabra fue rechazada')
        else:
            self.controlPanel.state_output.append('La palabra fue aceptada')
        finally:
            self.load_graph_img()

    def set_speed(self, speed):
        self.model.speed = speed
        self.controlPanel.speed_state.setText(self.model.speed)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())