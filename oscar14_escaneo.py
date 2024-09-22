# oscar14_escaneo.py
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import numpy as np
import re

class VentanaEscaneoQR(QWidget):
    """
    Clase para la ventana de escaneo de códigos QR.
    Permite escanear un código QR con la webcam y extraer los datos para rellenar el formulario.
    """

    def __init__(self, db):
        """
        Inicializa la ventana de escaneo QR.

        Args:
            db: Objeto de la base de datos para guardar los datos escaneados.
        """
        super().__init__()
        self.db = db
        self.init_ui()
        self.cap = None  # Variable para la webcam

    def init_ui(self):
        """
        Configura la interfaz de usuario para la ventana de escaneo QR.
        """
        self.setWindowTitle("Escaneo de Facturas QR")
        self.setGeometry(100, 100, 1200, 800)  # Dimensiones de la ventana

        # Layout principal
        layout_principal = QHBoxLayout(self)

        # Parte izquierda: formulario de datos
        self.formulario_layout = QVBoxLayout()

        self.campos = {}
        campos_nombres = [
            "RUC Emisor", "Tipo Comprobante", "Serie", "Numeración",
            "Monto Total", "Fecha Emisión", "Monto IGV", "RUC Adquiriente",
            "Razón Social Emisor", "Razón Social Adquiriente",
            "Valor Venta Gravada", "Valor Venta Inafecta",
            "Valor Venta Exonerada", "Código Hash"
        ]

        for nombre in campos_nombres:
            label = QLabel(nombre)
            label.setStyleSheet("color: black; font-size: 14px;")
            campo = QLineEdit()
            campo.setReadOnly(True)
            self.formulario_layout.addWidget(label)
            self.formulario_layout.addWidget(campo)
            self.campos[nombre] = campo

        # Botón para guardar los datos
        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_datos)
        self.formulario_layout.addWidget(self.boton_guardar)

        # Botón para limpiar el formulario
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_formulario)
        self.formulario_layout.addWidget(self.boton_limpiar)

        # Establecer diseño y color de fondo
        self.formulario_layout.setAlignment(Qt.AlignTop)
        layout_principal.addLayout(self.formulario_layout)

        # Parte derecha: vista de la webcam
        self.webcam_frame = QFrame()
        self.webcam_layout = QVBoxLayout()
        self.label_webcam = QLabel("Vista de la Webcam")
        self.label_webcam.setAlignment(Qt.AlignCenter)
        self.webcam_layout.addWidget(self.label_webcam)

        # Botón para iniciar la webcam
        self.boton_iniciar_webcam = QPushButton("Iniciar Webcam")
        self.boton_iniciar_webcam.clicked.connect(self.iniciar_webcam)
        self.webcam_layout.addWidget(self.boton_iniciar_webcam)
        
        self.webcam_frame.setLayout(self.webcam_layout)
        layout_principal.addWidget(self.webcam_frame)

        self.timer = QTimer()
        self.timer.timeout.connect(self.mostrar_frame)

    def iniciar_webcam(self):
        """
        Inicia la cámara web para escanear códigos QR.
        """
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)

    def mostrar_frame(self):
        """
        Captura y muestra el frame de la cámara web en tiempo real.
        Intenta detectar y decodificar un código QR.
        """
        ret, frame = self.cap.read()
        if ret:
            # Detección de QR con OpenCV
            qr_detector = cv2.QRCodeDetector()
            data, points, _ = qr_detector.detectAndDecode(frame)
            
            if points is not None:
                pts = np.array(points, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                frame = cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                
                if data:
                    self.procesar_datos_qr(data)

            # Convertir frame para mostrar en QLabel
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label_webcam.setPixmap(QPixmap.fromImage(qt_image))

    def procesar_datos_qr(self, data):
        """
        Procesa y muestra los datos extraídos del código QR en el formulario.
        Utiliza una lógica más robusta para asignar los valores a los campos correctos.

        Args:
            data (str): Datos extraídos del código QR.
        """
        # Descomponer los datos según un delimitador, asumiendo que es '|'
        campos_extraidos = data.split('|')
        
        # Definir un mapeo directo según la posición en la lista (ajustar si es necesario)
        mapeo_campos = [
            "RUC Emisor", "Tipo Comprobante", "Serie", "Numeración",
            "Monto Total", "Fecha Emisión", "Monto IGV", "RUC Adquiriente",
            "Razón Social Emisor", "Razón Social Adquiriente",
            "Valor Venta Gravada", "Valor Venta Inafecta",
            "Valor Venta Exonerada", "Código Hash"
        ]
        
        # Rellenar los campos con los datos extraídos
        for i, nombre_campo in enumerate(mapeo_campos):
            if i < len(campos_extraidos) and campos_extraidos[i].strip():
                self.campos[nombre_campo].setText(campos_extraidos[i].strip())
            else:
                self.campos[nombre_campo].setText('')  # Dejar vacío si el dato no está disponible

    def limpiar_formulario(self):
        """
        Limpia los campos del formulario para permitir un nuevo escaneo.
        """
        for campo in self.campos.values():
            campo.clear()

    def guardar_datos(self):
        """
        Lógica para guardar los datos en la base de datos.
        """
        # Crear un diccionario con los datos del formulario
        datos_a_guardar = {campo: self.campos[campo].text() for campo in self.campos}
        self.db.guardar_factura(datos_a_guardar)

    def cerrar_webcam(self):
        """
        Libera los recursos de la cámara web.
        """
        if self.cap:
            self.cap.release()
            self.timer.stop()

    def closeEvent(self, event):
        """
        Evento que se ejecuta al cerrar la ventana.
        Cierra la cámara web si está activa.
        """
        self.cerrar_webcam()
        super().closeEvent(event)
