# oscar14_configuracion.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class VentanaConfiguracion(QWidget):
    """
    Clase para la ventana de configuración.

    Esta ventana permite al usuario ajustar configuraciones generales de la aplicación, como el logo y otros ajustes.
    """
    
    def __init__(self, main_app):
        """
        Inicializa la ventana de configuración.

        Args:
            main_app: Referencia a la aplicación principal.
        """
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        """
        Configura la interfaz gráfica de la ventana de configuración.
        """
        self.setWindowTitle("Configuración")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        layout = QVBoxLayout()
        
        # Añadir un ejemplo de configuración
        label = QLabel("Esta es la ventana de configuración.")
        layout.addWidget(label)

        # Botón de ejemplo
        boton_guardar = QPushButton("Guardar Configuración")
        boton_guardar.clicked.connect(self.guardar_configuracion)
        layout.addWidget(boton_guardar)

        self.setLayout(layout)

    def guardar_configuracion(self):
        """
        Guarda las configuraciones realizadas en la ventana.
        """
        # Lógica para guardar configuraciones
        pass

