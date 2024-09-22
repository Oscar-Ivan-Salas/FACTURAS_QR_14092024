# oscar14_main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from oscar14_backend import FacturaDatabase
from oscar14_escaneo import VentanaEscaneoQR
from oscar14_carga_archivos import VentanaCargaArchivos
from oscar14_visualizacion_bd import VentanaVisualizacionDB
from oscar14_estadistica import VentanaEstadisticas
from oscar14_configuracion import VentanaConfiguracion  # Asegúrate de que esta clase esté definida

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Facturas QR")
        self.setGeometry(100, 100, 1200, 800)

        # Inicializar la base de datos
        self.db = FacturaDatabase()

        # Crear las pestañas
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Añadir pestañas
        self.ventana_escaneo_qr = VentanaEscaneoQR(self.db)
        self.tab_widget.addTab(self.ventana_escaneo_qr, "Escaneo QR")

        self.ventana_carga_archivos = VentanaCargaArchivos(self.db)
        self.tab_widget.addTab(self.ventana_carga_archivos, "Carga de Archivos")

        self.ventana_visualizacion_bd = VentanaVisualizacionDB(self.db)
        self.tab_widget.addTab(self.ventana_visualizacion_bd, "Visualización BD")

        self.ventana_estadisticas = VentanaEstadisticas(self.db)
        self.tab_widget.addTab(self.ventana_estadisticas, "Estadísticas")

        self.ventana_configuracion = VentanaConfiguracion(self)
        self.tab_widget.addTab(self.ventana_configuracion, "Configuración")

def main():
    app = QApplication(sys.argv)
    ventana_principal = MainApp()
    ventana_principal.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
