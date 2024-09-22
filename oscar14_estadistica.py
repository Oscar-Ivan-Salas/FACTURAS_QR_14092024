# oscar14_estadisticas.py
# oscar14_estadisticas.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class VentanaEstadisticas(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db  # Almacenar la referencia de la base de datos
        self.init_ui()

    def init_ui(self):
        # Configuración de la interfaz
        self.setWindowTitle("Estadísticas")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Área de desplazamiento
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Área del gráfico
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        scroll_layout.addWidget(self.canvas)

        # Botón para actualizar estadísticas
        btn_actualizar = QPushButton("Actualizar Estadísticas")
        btn_actualizar.clicked.connect(self.mostrar_estadisticas)
        scroll_layout.addWidget(btn_actualizar)

        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        
        layout_principal.addWidget(scroll_area)
        self.setLayout(layout_principal)

    def mostrar_estadisticas(self):
        # Limpiar la figura antes de dibujar nuevas estadísticas
        self.figura.clear()

        # Crear un gráfico de ejemplo, ajustar esto según los datos reales de la base de datos
        ax = self.figura.add_subplot(111)

        # Aquí se debe obtener y procesar los datos desde self.db
        # Ejemplo simple con datos aleatorios
        data = np.random.rand(10)
        ax.bar(range(len(data)), data)

        # Dibujar el gráfico
        self.canvas.draw()





