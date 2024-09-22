# oscar14_backend.py #
import sqlite3
import os
from openpyxl import Workbook

class DataHandler:
    def __init__(self):
        self.data_dir = 'data'
        self.txt_file = os.path.join(self.data_dir, 'facturas_data.txt')
        self.xlsx_file = os.path.join(self.data_dir, 'facturas_data.xlsx')

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def guardar_en_archivo(self, datos):
        try:
            with open(self.txt_file, 'a') as f:
                f.write(", ".join(f"{key}: {value}" for key, value in datos.items()) + "\n")
        except Exception as e:
            print(f"Error al guardar en archivo: {e}")

    def exportar_a_archivos(self, facturas):
        self.exportar_a_txt(facturas)
        self.exportar_a_excel(facturas)

    def exportar_a_txt(self, facturas):
        try:
            with open(self.txt_file, 'w') as f:
                for factura in facturas:
                    f.write(", ".join(f"{key}: {value}" for key, value in factura.items()) + "\n")
        except Exception as e:
            print(f"Error al exportar a TXT: {e}")

    def exportar_a_excel(self, facturas):
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Facturas"

            encabezados = facturas[0].keys()
            ws.append(list(encabezados))

            for factura in facturas:
                ws.append(list(factura.values()))

            wb.save(self.xlsx_file)
        except Exception as e:
            print(f"Error al exportar a Excel: {e}")

class FacturaDatabase:
    def __init__(self):
        self.data_dir = 'data'
        self.db_path = os.path.join(self.data_dir, 'facturas.db')

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.conn = sqlite3.connect(self.db_path)
        self.crear_tabla_facturas()

    def crear_tabla_facturas(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS facturas (
                ruc_emisor TEXT,
                tipo_comprobante TEXT,
                serie TEXT,
                numeracion TEXT,
                monto_total TEXT,
                fecha_emision TEXT,
                monto_igv TEXT,
                ruc_adquiriente TEXT,
                razon_social_emisor TEXT,
                razon_social_adquiriente TEXT,
                valor_venta_gravada TEXT,
                valor_venta_inafecta TEXT,
                valor_venta_exonerada TEXT,
                codigo_hash TEXT,
                domicilio_emisor TEXT,
                domicilio_adquiriente TEXT,
                fecha_registro TEXT,
                estado_validacion TEXT
            )
            """
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de facturas: {e}")

    def guardar_factura(self, datos):
        try:
            query = """
            INSERT INTO facturas (ruc_emisor, tipo_comprobante, serie, numeracion, monto_total, fecha_emision, monto_igv,
                                  ruc_adquiriente, razon_social_emisor, razon_social_adquiriente, valor_venta_gravada,
                                  valor_venta_inafecta, valor_venta_exonerada, codigo_hash, domicilio_emisor,
                                  domicilio_adquiriente, fecha_registro, estado_validacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.conn.execute(query, tuple(datos.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al guardar la factura en la base de datos: {e}")

    def obtener_facturas(self):
        try:
            query = "SELECT * FROM facturas"
            cursor = self.conn.execute(query)
            columnas = [column[0] for column in cursor.description]
            return [dict(zip(columnas, row)) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al obtener facturas: {e}")
            return []

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()



