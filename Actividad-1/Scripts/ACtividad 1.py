import mysql.connector
from mysql.connector import Error

def conectar_y_consultar():
    conexion = None
    cursor = None
    try:
        # 1. Conexión a la base de datos Guia_8
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",          # Usuario de MariaDB
            password="",          # Coloca tu contraseña si aplica
            database="Guia_8"
        )

        if conexion.is_connected():
            print(f"[OK] Conexión establecida con el servidor (Versión: {conexion.server_info})")
            print("=" * 80)

            # 2. Ejecutar consulta SELECT cruzando Estudiante y sus matrículas
            cursor = conexion.cursor()
            query = """
                SELECT 
                    e.IdEstudiante,
                    CONCAT(e.PrimerNombre, ' ', e.PrimerApellido) AS Estudiante,
                    e.CorreoEstudiante,
                    COUNT(m.IdMatricula) AS MateriasInscritas
                FROM Estudiante e
                LEFT JOIN Matricula m ON e.IdEstudiante = m.IdEstudiante
                GROUP BY e.IdEstudiante, e.PrimerNombre, e.PrimerApellido, e.CorreoEstudiante
                ORDER BY e.PrimerApellido;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            # 3. Mostrar resultados en consola
            print(f"{'ID ESTUDIANTE':<15} | {'NOMBRE COMPLETO':<22} | {'CORREO':<30} | {'MATRÍCULAS'}")
            print("-" * 80)
            for id_est, nombre, correo, total_mat in resultados:
                print(f"{id_est:<15} | {nombre:<22} | {correo:<30} | {total_mat}")

            print("=" * 80)
            print(f"Total de registros recuperados: {len(resultados)}")

    except Error as err:
        # 4. Manejo de errores (credenciales incorrectas, servicio detenido, tabla inexistente)
        print(f"[ERROR SQL/CONEXIÓN] Fallo al interactuar con la base de datos: {err}")

    finally:
        # Cierre controlado de cursor y conexión
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("[INFO] Conexión cerrada de forma segura.")

if __name__ == "__main__":
    conectar_y_consultar()