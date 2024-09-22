# oscar14_visualizacion_bd.py
import os
import openpyxl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class VentanaVisualizacionDB(QWidget):

    def __init__(self, db):
        super().__init__()
        self.db = db

        # Configuración de la ventana
        self.setWindowTitle("Visualización de la Base de Datos")
        self.resize(800, 600)

        # Layout principal
        self.layout = QVBoxLayout(self)

        # Tabla para visualizar los datos
        self.tabla_facturas = QTableWidget()
        self.tabla_facturas.setColumnCount(18)  # Número de columnas en la base de datos
        self.tabla_facturas.setHorizontalHeaderLabels([
            "RUC Emisor", "Tipo Comprobante", "Serie", "Numeración", "Monto Total", 
            "Fecha Emisión", "Monto IGV", "RUC Adquiriente", "Razón Social Emisor",
            "Razón Social Adquiriente", "Valor Venta Gravada", "Valor Venta Inafecta",
            "Valor Venta Exonerada", "Código Hash", "Domicilio Emisor", "Domicilio Adquiriente", 
            "Fecha Registro", "Estado Validación"
        ])
        self.tabla_facturas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.tabla_facturas)

        # Botones para cargar y exportar datos
        self.btn_cargar_datos = QPushButton("Cargar Datos")
        self.btn_cargar_datos.clicked.connect(self.cargar_datos)
        self.layout.addWidget(self.btn_cargar_datos)

        self.btn_exportar_txt = QPushButton("Exportar a TXT")
        self.btn_exportar_txt.clicked.connect(self.exportar_a_txt)
        self.layout.addWidget(self.btn_exportar_txt)

        self.btn_exportar_excel = QPushButton("Exportar a Excel")
        self.btn_exportar_excel.clicked.connect(self.exportar_a_excel)
        self.layout.addWidget(self.btn_exportar_excel)

        # Estilos
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: white;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 14px;
                padding: 5px;
            }
            QTableWidget {
                background-color: #FFFFFF;
                color: black;
            }
        """)

    def cargar_datos(self):
        try:
            # Obtener datos de la base de datos
            facturas = self.db.obtener_facturas()

            # Limpiar la tabla
            self.tabla_facturas.setRowCount(0)

            # Rellenar la tabla con los datos
            for factura in facturas:
                fila_actual = self.tabla_facturas.rowCount()
                self.tabla_facturas.insertRow(fila_actual)
                for columna, (key, value) in enumerate(factura.items()):
                    self.tabla_facturas.setItem(fila_actual, columna, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar los datos: {e}")

    def exportar_a_txt(self):
        try:
            # Obtener datos de la tabla
            facturas = self.obtener_datos_tabla()

            # Seleccionar ruta para guardar el archivo
            opciones = QFileDialog.Options()
            archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo TXT", "", "Archivos de Texto (*.txt)", options=opciones)
            if archivo:
                with open(archivo, 'w') as f:
                    for factura in facturas:
                        f.write(", ".join(f"{key}: {value}" for key, value in factura.items()) + "\n")
                QMessageBox.information(self, "Éxito", f"Datos exportados a {archivo}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al exportar a TXT: {e}")

    def exportar_a_excel(self):
        try:
            # Obtener datos de la tabla
            facturas = self.obtener_datos_tabla()

            # Seleccionar ruta para guardar el archivo
            opciones = QFileDialog.Options()
            archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo Excel", "", "Archivos Excel (*.xlsx)", options=opciones)
            if archivo:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Facturas"

                # Escribir encabezados
                encabezados = facturas[0].keys()
                ws.append(list(encabezados))

                # Escribir datos
                for factura in facturas:
                    ws.append(list(factura.values()))

                wb.save(archivo)
                QMessageBox.information(self, "Éxito", f"Datos exportados a {archivo}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al exportar a Excel: {e}")

    def obtener_datos_tabla(self):
        # Recopilar datos de la tabla en una lista de diccionarios
        facturas = []
        for fila in range(self.tabla_facturas.rowCount()):
            factura = {}
            for columna in range(self.tabla_facturas.columnCount()):
                encabezado = self.tabla_facturas.horizontalHeaderItem(columna).text()
                item = self.tabla_facturas.item(fila, columna)
                factura[encabezado] = item.text() if item else ""
            facturas.append(factura)
        return facturas
