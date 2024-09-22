# oscar14_carga_archivos.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QScrollArea, QFileDialog, QFrame, QSlider, QProgressBar
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from pdf2image import convert_from_path
import fitz  # PyMuPDF
import PyPDF2
from PIL import ImageQt, Image
import pytesseract
import cv2
import numpy as np
import os

class VentanaCargaArchivos(QWidget):
    """
    Clase para la ventana de carga de archivos.
    Permite cargar y visualizar archivos PDF o imágenes, extraer datos de ellos y rellenar el formulario.
    """

    def __init__(self, db):
        """
        Inicializa la ventana de carga de archivos.

        :param db: Instancia de la base de datos para almacenar datos de facturas.
        """
        super().__init__()
        self.db = db  # Guardar la referencia de la base de datos
        self.init_ui()
        self.imagen_actual = None
        self.zoom_factor = 1.0

    def init_ui(self):
        """
        Configura la interfaz gráfica de la ventana.
        """
        # Configuración de la interfaz
        self.setWindowTitle('Carga de Archivos')
        self.setGeometry(100, 100, 1200, 800)  # Ajustar tamaño inicial de la ventana

        # Layout principal
        main_layout = QHBoxLayout(self)
        self.frame_previsualizacion = QFrame(self)
        self.frame_formulario = QFrame(self)

        # Añadir los frames al layout principal
        main_layout.addWidget(self.frame_previsualizacion, 2)  # 2/3 para la previsualización
        main_layout.addWidget(self.frame_formulario, 1)  # 1/3 para el formulario

        # Layout para la previsualización de archivos
        self.layout_previsualizacion = QVBoxLayout(self.frame_previsualizacion)
        self.label_previsualizacion = QLabel('Vista Previa del Archivo', self)
        self.label_previsualizacion.setAlignment(Qt.AlignCenter)
        self.scroll_area_previsualizacion = QScrollArea(self)
        self.scroll_area_previsualizacion.setWidgetResizable(True)
        self.scroll_area_previsualizacion.setWidget(self.label_previsualizacion)
        self.layout_previsualizacion.addWidget(self.scroll_area_previsualizacion)

        # Botón para cargar archivos
        self.btn_cargar_archivo = QPushButton('Cargar Archivo', self)
        self.btn_cargar_archivo.clicked.connect(self.cargar_archivo)
        self.layout_previsualizacion.addWidget(self.btn_cargar_archivo)

        # Botones para rotar, hacer zoom y ajustar imagen
        self.btn_rotar = QPushButton('Rotar', self)
        self.btn_rotar.clicked.connect(self.rotar_imagen)
        self.layout_previsualizacion.addWidget(self.btn_rotar)

        # Slider para el zoom
        self.slider_zoom = QSlider(Qt.Horizontal)
        self.slider_zoom.setMinimum(10)
        self.slider_zoom.setMaximum(200)
        self.slider_zoom.setValue(100)  # Zoom inicial al 100%
        self.slider_zoom.valueChanged.connect(self.cambiar_zoom)
        self.layout_previsualizacion.addWidget(self.slider_zoom)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        self.layout_previsualizacion.addWidget(self.progress_bar)

        # Layout para el formulario
        self.layout_formulario = QVBoxLayout(self.frame_formulario)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Campos del formulario
        self.campos_formulario = [
            "RUC Emisor", "Tipo Comprobante", "Serie", "Numeración", 
            "Monto Total", "Fecha Emisión", "Monto IGV", "RUC Adquiriente", 
            "Razón Social Emisor", "Razón Social Adquiriente", 
            "Valor Venta Gravada", "Valor Venta Inafecta", 
            "Valor Venta Exonerada", "Código Hash"
        ]
        self.campos = {}

        for nombre_campo in self.campos_formulario:
            label = QLabel(nombre_campo)
            campo = QLineEdit()
            self.scroll_layout.addWidget(label)
            self.scroll_layout.addWidget(campo)
            self.campos[nombre_campo] = campo

        # Añadir el layout scroll al formulario
        self.scroll_area.setWidget(self.scroll_content)
        self.layout_formulario.addWidget(self.scroll_area)

        # Botón para guardar datos en el formulario
        self.btn_guardar_datos = QPushButton('Guardar Datos', self)
        self.btn_guardar_datos.clicked.connect(self.guardar_datos)
        self.layout_formulario.addWidget(self.btn_guardar_datos)

        # Botón para copiar datos manualmente al formulario
        self.btn_copiar_datos = QPushButton('Copiar Datos al Formulario', self)
        self.btn_copiar_datos.clicked.connect(self.copiar_datos_al_formulario)
        self.layout_previsualizacion.addWidget(self.btn_copiar_datos)

    def cargar_archivo(self):
        """
        Función para cargar un archivo PDF o imagen.
        """
        opciones = QFileDialog.Options()
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Archivos PDF (*.pdf);;Archivos Imagen (*.jpg *.jpeg *.png)", options=opciones)
        
        if archivo:
            extension = os.path.splitext(archivo)[1].lower()
            if extension == '.pdf':
                self.procesar_pdf(archivo)
            elif extension in ['.jpg', '.jpeg', '.png']:
                self.procesar_imagen(archivo)

    def procesar_pdf(self, archivo_pdf):
        """
        Procesa un archivo PDF y muestra la primera página en la interfaz.

        :param archivo_pdf: Ruta al archivo PDF.
        """
        # Implementar sistema redundante para manejar PDFs
        try:
            # Usar pdf2image
            paginas = convert_from_path(archivo_pdf, dpi=200)  # Llamar a convert_from_path correctamente
            if paginas:
                self.mostrar_imagen(paginas[0])
                return
        except Exception as e:
            print(f"Error al procesar el PDF con pdf2image: {e}")

        try:
            # Usar PyMuPDF (fitz)
            documento = fitz.open(archivo_pdf)
            pagina = documento.load_page(0)  # Primera página
            pix = pagina.get_pixmap()
            self.mostrar_imagen(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
            return
        except Exception as e:
            print(f"Error al procesar el PDF con PyMuPDF: {e}")

        try:
            # Usar PyPDF2
            with open(archivo_pdf, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                if len(reader.pages) > 0:
                    page = reader.pages[0]
                    contenido = page.extract_text()
                    print(f"Contenido de la primera página: {contenido}")
        except Exception as e:
            print(f"Error al procesar el PDF con PyPDF2: {e}")

    def procesar_imagen(self, archivo_imagen):
        """
        Procesa un archivo de imagen y muestra la imagen en la interfaz.

        :param archivo_imagen: Ruta al archivo de imagen.
        """
        try:
            imagen = Image.open(archivo_imagen)
            self.mostrar_imagen(imagen)
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")

    def mostrar_imagen(self, imagen):
        """
        Muestra una imagen en el label de previsualización.

        :param imagen: Imagen a mostrar.
        """
        self.imagen_actual = imagen
        imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)  # Convertir usando OpenCV
        height, width, channel = imagen_cv.shape
        bytesPerLine = 3 * width
        qt_image = QImage(imagen_cv.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_previsualizacion.setPixmap(QPixmap.fromImage(qt_image))

    def cambiar_zoom(self):
        """
        Cambia el zoom de la imagen previsualizada.
        """
        self.zoom_factor = self.slider_zoom.value() / 100
        self.aplicar_zoom()

    def aplicar_zoom(self):
        """
        Aplica el zoom a la imagen previsualizada.
        """
        if self.imagen_actual:
            ancho = int(self.imagen_actual.width * self.zoom_factor)
            alto = int(self.imagen_actual.height * self.zoom_factor)
            imagen_zoom = self.imagen_actual.resize((ancho, alto), Image.LANCZOS)
            self.mostrar_imagen(imagen_zoom)

    def rotar_imagen(self):
        """
        Rota la imagen previsualizada 90 grados.
        """
        if self.imagen_actual:
            self.imagen_actual = self.imagen_actual.rotate(90, expand=True)
            self.mostrar_imagen(self.imagen_actual)

    def copiar_datos_al_formulario(self):
        """
        Copia los datos extraídos de la imagen al formulario manualmente.
        """
        # Lógica para extraer texto con pytesseract si es una imagen
        if self.imagen_actual:
            texto_extraido = pytesseract.image_to_string(self.imagen_actual)
            print(f"Texto extraído: {texto_extraido}")

    def guardar_datos(self):
        """
        Guarda los datos del formulario en la base de datos.
        """
        datos_a_guardar = {nombre: self.campos[nombre].text() for nombre in self.campos_formulario}
        self.db.guardar_factura(datos_a_guardar)
