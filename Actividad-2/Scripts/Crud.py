import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    """Establece y retorna una conexión activa con la base de datos Guia_8."""
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",          # Ajusta si configuraste contraseña
        database="Guia_8"
    )


def insertar_estudiante():
    """CREATE: Inserta un nuevo estudiante usando consulta parametrizada."""
    print("\n--- REGISTRAR NUEVO ESTUDIANTE ---")
    try:
        id_est = int(input("ID Estudiante (Documento): ").strip())
        p_nombre = input("Primer Nombre: ").strip()
        s_nombre = input("Segundo Nombre (Enter si no tiene): ").strip() or None
        p_apellido = input("Primer Apellido: ").strip()
        s_apellido = input("Segundo Apellido (Enter si no tiene): ").strip() or None
        correo = input("Correo Institucional: ").strip()
        prefijo = input("Prefijo Teléfono (ej. +57): ").strip() or "+57"
        telefono = input("Teléfono: ").strip()
        fecha_nac = input("Fecha de Nacimiento (YYYY-MM-DD): ").strip()
        direccion = input("Dirección (Enter si no aplica): ").strip() or None

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO Estudiante (
                IdEstudiante, PrimerNombre, SegundoNombre,
                PrimerApellido, SegundoApellido, CorreoEstudiante,
                PrefijoTelefono, Telefono, FechaNacimiento, Direccion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            id_est, p_nombre, s_nombre,
            p_apellido, s_apellido, correo,
            prefijo, telefono, fecha_nac, direccion
        )

        cursor.execute(sql, valores)
        conexion.commit()
        print(f"[OK] Estudiante '{p_nombre} {p_apellido}' registrado correctamente.")

    except ValueError:
        print("[ERROR] El ID del estudiante debe ser un número entero.")
    except Error as err:
        print(f"[ERROR SQL] No se pudo insertar el estudiante: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()


def consultar_estudiantes():
    """READ: Lista todos los estudiantes o busca uno por ID parametrizado."""
    print("\n--- CONSULTAR ESTUDIANTES ---")
    print("1. Listar todos los estudiantes")
    print("2. Buscar estudiante por ID")
    opcion = input("Seleccione una opción: ").strip()

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        if opcion == "1":
            sql = """
                SELECT IdEstudiante,
                       CONCAT_WS(' ', PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido) AS NombreCompleto,
                       CorreoEstudiante,
                       CONCAT(PrefijoTelefono, ' ', Telefono) AS TelefonoCompleto,
                       FechaNacimiento
                FROM Estudiante
                ORDER BY PrimerApellido
            """
            cursor.execute(sql)
            filas = cursor.fetchall()

        elif opcion == "2":
            id_buscar = int(input("Ingrese el ID del estudiante a buscar: ").strip())
            sql = """
                SELECT IdEstudiante,
                       CONCAT_WS(' ', PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido) AS NombreCompleto,
                       CorreoEstudiante,
                       CONCAT(PrefijoTelefono, ' ', Telefono) AS TelefonoCompleto,
                       FechaNacimiento
                FROM Estudiante
                WHERE IdEstudiante = %s
            """
            cursor.execute(sql, (id_buscar,))
            filas = cursor.fetchall()
        else:
            print("[AVISO] Opción no válida.")
            return

        if not filas:
            print("[INFO] No se encontraron registros.")
            return

        print("\n" + "=" * 95)
        print(f"{'ID':<12} | {'NOMBRE COMPLETO':<30} | {'CORREO':<30} | {'TELÉFONO'}")
        print("-" * 95)
        for id_est, nombre, correo, tel, _ in filas:
            print(f"{id_est:<12} | {nombre:<30} | {correo:<30} | {tel}")
        print("=" * 95)

    except ValueError:
        print("[ERROR] El ID debe ser numérico.")
    except Error as err:
        print(f"[ERROR SQL] Error al consultar: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()


def actualizar_estudiante():
    """UPDATE: Actualiza correo, teléfono y dirección mediante consulta parametrizada."""
    print("\n--- ACTUALIZAR DATOS DE ESTUDIANTE ---")
    try:
        id_est = int(input("Ingrese el ID del estudiante a modificar: ").strip())
        nuevo_correo = input("Nuevo correo institucional: ").strip()
        nuevo_tel = input("Nuevo teléfono: ").strip()
        nueva_dir = input("Nueva dirección: ").strip() or None

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE Estudiante
            SET CorreoEstudiante = %s,
                Telefono = %s,
                Direccion = %s
            WHERE IdEstudiante = %s
        """
        valores = (nuevo_correo, nuevo_tel, nueva_dir, id_est)

        cursor.execute(sql, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"[OK] Registro con ID {id_est} actualizado exitosamente.")
        else:
            print(f"[AVISO] No existe ningún estudiante con el ID {id_est}.")

    except ValueError:
        print("[ERROR] El ID debe ser un número entero.")
    except Error as err:
        print(f"[ERROR SQL] No se pudo actualizar el registro: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()


def eliminar_estudiante():
    """DELETE: Elimina un estudiante por ID usando consulta parametrizada."""
    print("\n--- ELIMINAR ESTUDIANTE ---")
    try:
        id_est = int(input("Ingrese el ID del estudiante a eliminar: ").strip())
        confirmar = input(f"¿Está seguro de eliminar al estudiante {id_est}? (s/n): ").strip().lower()

        if confirmar != "s":
            print("[INFO] Operación cancelada.")
            return

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "DELETE FROM Estudiante WHERE IdEstudiante = %s"
        cursor.execute(sql, (id_est,))
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"[OK] Estudiante con ID {id_est} eliminado correctamente.")
        else:
            print(f"[AVISO] No se encontró ningún estudiante con ID {id_est}.")

    except ValueError:
        print("[ERROR] El ID debe ser un número entero.")
    except Error as err:
        # Captura si falla por restricción de llave foránea (ej. tiene matrículas activas)
        print(f"[ERROR SQL] No se pudo eliminar (verifique si tiene matrículas asociadas): {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()


def menu_principal():
    """Menú interactivo en consola para gestionar operaciones CRUD."""
    while True:
        print("\n==============================================")
        print("   SISTEMA DE GESTIÓN DE ESTUDIANTES (CRUD)   ")
        print("==============================================")
        print("1. Insertar nuevo estudiante (CREATE)")
        print("2. Consultar estudiantes (READ)")
        print("3. Actualizar datos de estudiante (UPDATE)")
        print("4. Eliminar estudiante (DELETE)")
        print("5. Salir")
        print("==============================================")

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            insertar_estudiante()
        elif opcion == "2":
            consultar_estudiantes()
        elif opcion == "3":
            actualizar_estudiante()
        elif opcion == "4":
            eliminar_estudiante()
        elif opcion == "5":
            print("[INFO] Saliendo del sistema...")
            break
        else:
            print("[AVISO] Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()