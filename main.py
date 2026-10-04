"""
CineMax - Sistema de Reservas de Cine (Proyecto Final)

Aplicación de consola para:
  1. Ver la cartelera de un día
  2. Mostrar los asientos de una función
  3. Reservar un asiento
  4. Cancelar una reserva
  5. Ver la disponibilidad de las funciones de un día

Estructuras de datos principales:
  - cartelera: diccionario {día: [funciones]}; cada función es un diccionario.
  - estado_funciones: diccionario {(día, sala, horario): {"asientos": matriz, "reservas": dict}}.
    La matriz de asientos es una lista de listas (5 filas x 6 columnas):
    "." = libre y "X" = ocupado.

Para ejecutarlo:  python main.py
"""

import unicodedata

# ======================================================================
# DATOS
# ======================================================================
cartelera = {
    "Lunes": [
        {"pelicula": "Resident Evil: Noche Cero", "sala": 1, "horario": "2:00 pm", "formato": "Normal"},
        {"pelicula": "Avengers: Endgame (reestreno)", "sala": 2, "horario": "4:30 pm", "formato": "3D"},
        {"pelicula": "Los Juegos del Hambre: Sinsajo Pt. 2", "sala": 3, "horario": "6:00 pm", "formato": "4DX"},
        {"pelicula": "Rápido y Furioso (reestreno)", "sala": 4, "horario": "5:30 pm", "formato": "Normal"},
        {"pelicula": "El Final", "sala": 5, "horario": "8:00 pm", "formato": "CXC"},
    ],
    "Martes": [
        {"pelicula": "Resident Evil: Noche Cero", "sala": 3, "horario": "5:00 pm", "formato": "4DX"},
        {"pelicula": "Avengers: Endgame (reestreno)", "sala": 1, "horario": "7:00 pm", "formato": "Normal"},
        {"pelicula": "Los Juegos del Hambre: Sinsajo Pt. 2", "sala": 2, "horario": "3:00 pm", "formato": "Normal"},
        {"pelicula": "Rápido y Furioso (reestreno)", "sala": 5, "horario": "6:30 pm", "formato": "3D"},
        {"pelicula": "El Final", "sala": 4, "horario": "9:00 pm", "formato": "Normal"},
    ],
    "Miércoles": [
        {"pelicula": "Resident Evil: Noche Cero", "sala": 4, "horario": "4:00 pm", "formato": "Normal"},
        {"pelicula": "Avengers: Endgame (reestreno)", "sala": 5, "horario": "2:30 pm", "formato": "CXC"},
        {"pelicula": "Los Juegos del Hambre: Sinsajo Pt. 2", "sala": 1, "horario": "7:30 pm", "formato": "3D"},
        {"pelicula": "Rápido y Furioso (reestreno)", "sala": 2, "horario": "5:00 pm", "formato": "Normal"},
        {"pelicula": "El Final", "sala": 3, "horario": "8:30 pm", "formato": "4DX"},
    ],
    "Jueves": [
        {"pelicula": "Resident Evil: Noche Cero", "sala": 2, "horario": "6:30 pm", "formato": "3D"},
        {"pelicula": "Avengers: Endgame (reestreno)", "sala": 3, "horario": "3:30 pm", "formato": "Normal"},
        {"pelicula": "Los Juegos del Hambre: Sinsajo Pt. 2", "sala": 4, "horario": "8:00 pm", "formato": "Normal"},
        {"pelicula": "Rápido y Furioso (reestreno)", "sala": 1, "horario": "2:00 pm", "formato": "4DX"},
        {"pelicula": "El Final", "sala": 5, "horario": "5:30 pm", "formato": "CXC"},
    ],
    "Viernes": [
        {"pelicula": "Resident Evil: Noche Cero", "sala": 5, "horario": "4:00 pm", "formato": "Normal"},
        {"pelicula": "Avengers: Endgame (reestreno)", "sala": 4, "horario": "7:00 pm", "formato": "3D"},
        {"pelicula": "Los Juegos del Hambre: Sinsajo Pt. 2", "sala": 1, "horario": "5:30 pm", "formato": "CXC"},
        {"pelicula": "Rápido y Furioso (reestreno)", "sala": 3, "horario": "9:00 pm", "formato": "Normal"},
        {"pelicula": "El Final", "sala": 2, "horario": "2:30 pm", "formato": "4DX"},
    ],
    "Sábado": [
        {"pelicula": "Resident Evil: Noche Cero", "sala": 1, "horario": "3:00 pm", "formato": "Normal"},
        {"pelicula": "Avengers: Endgame (reestreno)", "sala": 2, "horario": "6:00 pm", "formato": "4DX"},
        {"pelicula": "Los Juegos del Hambre: Sinsajo Pt. 2", "sala": 5, "horario": "8:30 pm", "formato": "3D"},
        {"pelicula": "Rápido y Furioso (reestreno)", "sala": 4, "horario": "4:30 pm", "formato": "Normal"},
        {"pelicula": "El Final", "sala": 3, "horario": "7:30 pm", "formato": "CXC"},
    ],
    "Domingo": [
        {"pelicula": "Resident Evil: Noche Cero", "sala": 3, "horario": "2:30 pm", "formato": "3D"},
        {"pelicula": "Avengers: Endgame (reestreno)", "sala": 5, "horario": "5:00 pm", "formato": "Normal"},
        {"pelicula": "Los Juegos del Hambre: Sinsajo Pt. 2", "sala": 2, "horario": "7:00 pm", "formato": "CXC"},
        {"pelicula": "Rápido y Furioso (reestreno)", "sala": 1, "horario": "8:30 pm", "formato": "4DX"},
        {"pelicula": "El Final", "sala": 4, "horario": "4:00 pm", "formato": "Normal"},
    ],
}

DIAS = list(cartelera.keys())  # ["Lunes", "Martes", ..., "Domingo"]
NUM_SALAS = 5
FILAS = 5
COLUMNAS = 6
LETRAS_FILAS = "ABCDE"  # una letra por fila (A1, A2, ... E6)
LIBRE = "."
OCUPADO = "X"


# ======================================================================
# ESTADO DE LAS SALAS
# ======================================================================
def crear_sala():
    """Devuelve una matriz FILAS x COLUMNAS con todos los asientos libres."""
    return [[LIBRE for _ in range(COLUMNAS)] for _ in range(FILAS)]


def crear_estado_inicial():
    """Crea la matriz de asientos y el registro de reservas de cada función de la semana."""
    estado = {}
    for dia, funciones in cartelera.items():
        for funcion in funciones:
            clave = (dia, funcion["sala"], funcion["horario"])
            estado[clave] = {
                "asientos": crear_sala(),
                "reservas": {},  # {"C3": "Nombre de quien reservó"}
            }
    return estado


estado_funciones = crear_estado_inicial()


def obtener_estado(dia, funcion):
    """Devuelve el estado (asientos y reservas) de una función."""
    return estado_funciones[(dia, funcion["sala"], funcion["horario"])]


# ======================================================================
# FUNCIONES AUXILIARES (validación y conversión de datos)
# ======================================================================
def quitar_acentos(texto):
    """Pasa a minúsculas y quita tildes: 'Miércoles' y 'miercoles' quedan iguales."""
    descompuesto = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")
    return sin_tildes.strip().lower()


def normalizar_horario(texto):
    """Deja el horario en un formato comparable: '2:00 PM', '2pm' y '2:00pm' -> '2:00pm'."""
    texto = texto.lower().replace(" ", "").replace(".", "")
    if ":" not in texto and texto[-2:] in ("am", "pm"):
        texto = texto[:-2] + ":00" + texto[-2:]
    return texto


def buscar_funcion(dia, sala, horario):
    """Busca la función de ese día, sala y horario. Devuelve None si no existe."""
    horario = normalizar_horario(horario)
    for funcion in cartelera[dia]:
        if funcion["sala"] == sala and normalizar_horario(funcion["horario"]) == horario:
            return funcion
    return None


def convertir_asiento(texto):
    """Convierte un asiento como 'C3' en (fila, columna) con índices desde 0.
    Devuelve None si el formato no es válido o el asiento no existe en la sala."""
    texto = texto.replace(" ", "").upper()
    if len(texto) < 2:
        return None
    letra, numero = texto[0], texto[1:]
    if letra not in LETRAS_FILAS or not numero.isdecimal():
        return None
    fila = LETRAS_FILAS.index(letra)
    columna = int(numero) - 1
    if columna < 0 or columna >= COLUMNAS:
        return None
    return fila, columna


def nombre_asiento(fila, columna):
    """Convierte (fila, columna) con índices desde 0 en un nombre como 'C3'."""
    return f"{LETRAS_FILAS[fila]}{columna + 1}"


def contar_asientos(matriz):
    """Devuelve (libres, ocupados, total) de una matriz de asientos."""
    ocupados = sum(fila.count(OCUPADO) for fila in matriz)
    total = FILAS * COLUMNAS
    return total - ocupados, ocupados, total


# ======================================================================
# PANTALLAS (lo que se imprime)
# ======================================================================
def imprimir_cartelera(dia):
    """Imprime las funciones de un día: película, sala, horario y formato."""
    print(f"\n--- Cartelera del {dia} ---")
    print(f"{'Película':<38}{'Sala':<6}{'Horario':<10}Formato")
    print("-" * 62)
    for funcion in cartelera[dia]:
        print(f"{funcion['pelicula']:<38}{funcion['sala']:<6}{funcion['horario']:<10}{funcion['formato']}")
    print()


def imprimir_asientos(dia, funcion):
    """Imprime la matriz de asientos de una función con encabezados de fila y columna."""
    matriz = obtener_estado(dia, funcion)["asientos"]
    libres, ocupados, total = contar_asientos(matriz)

    print(f"\n{funcion['pelicula']} - Formato {funcion['formato']}")
    print(f"{dia} {funcion['horario']} - Sala {funcion['sala']}\n")
    print(" " * 6 + "PANTALLA".center(3 * COLUMNAS - 2, "="))
    print(" " * 6 + "  ".join(str(n) for n in range(1, COLUMNAS + 1)))
    for i, fila in enumerate(matriz):
        print(f"  {LETRAS_FILAS[i]}   " + "  ".join(fila))
    print(f"\n{LIBRE} = Libre   {OCUPADO} = Ocupado")
    print(f"Libres: {libres}   Ocupados: {ocupados}   Total: {total}\n")


# ======================================================================
# ENTRADA DE DATOS DEL USUARIO (cada función valida lo que se escribe)
# ======================================================================
def pedir_dia():
    """Pide un día (por nombre o por número). Devuelve el día o None si no es válido."""
    print("Días: " + ", ".join(f"{n}. {dia}" for n, dia in enumerate(DIAS, start=1)))
    entrada = quitar_acentos(input("Elija un día (nombre o número): "))
    if entrada.isdecimal() and 1 <= int(entrada) <= len(DIAS):
        return DIAS[int(entrada) - 1]
    for dia in DIAS:
        if quitar_acentos(dia) == entrada:
            return dia
    print(f"[!] Día no válido. Escriba un día de {DIAS[0]} a {DIAS[-1]} (o un número del 1 al {len(DIAS)}).")
    return None


def pedir_sala():
    """Pide el número de sala. Devuelve el número o None si no es válido."""
    entrada = input(f"Número de sala (1-{NUM_SALAS}): ").strip()
    if entrada.isdecimal() and 1 <= int(entrada) <= NUM_SALAS:
        return int(entrada)
    print(f"[!] Sala no válida. Debe ser un número del 1 al {NUM_SALAS}.")
    return None


def pedir_funcion():
    """Pide día, sala y horario, y valida que esa función exista.
    Devuelve (dia, funcion) o None si algún dato no es válido."""
    dia = pedir_dia()
    if dia is None:
        return None
    imprimir_cartelera(dia)  # así el usuario ve qué sala y horario le interesan

    sala = pedir_sala()
    if sala is None:
        return None

    horario = input("Horario de la función (ej. 2:00 pm): ").strip()
    funcion = buscar_funcion(dia, sala, horario)
    if funcion is None:
        print(f"[!] El {dia.lower()} no hay función en la sala {sala} a las {horario}.")
        print("    Revise la cartelera del día e inténtelo de nuevo.")
        return None
    return dia, funcion


def pedir_asiento():
    """Pide un asiento (ej. C3). Devuelve (fila, columna) o None si no existe."""
    ultima_fila = LETRAS_FILAS[-1]
    entrada = input(f"Asiento (ej. C3; filas A-{ultima_fila}, columnas 1-{COLUMNAS}): ")
    posicion = convertir_asiento(entrada)
    if posicion is None:
        print(f"[!] Ese asiento no existe. Use una letra de la A a la {ultima_fila} "
              f"seguida de un número del 1 al {COLUMNAS} (ej. C3).")
    return posicion


def pedir_nombre():
    """Pide el nombre de quien reserva (no puede quedar vacío)."""
    while True:
        nombre = input("Nombre de quien reserva: ").strip()
        if nombre:
            return nombre
        print("[!] El nombre no puede estar vacío.")


# ======================================================================
# OPCIONES DEL MENÚ
# ======================================================================
def ver_cartelera():
    """Opción 1: muestra las 5 funciones de un día."""
    print("\n=== 1. Ver cartelera de un día ===")
    dia = pedir_dia()
    if dia is not None:
        imprimir_cartelera(dia)


def mostrar_asientos():
    """Opción 2: muestra la matriz de asientos de una función."""
    print("\n=== 2. Mostrar asientos de una función ===")
    resultado = pedir_funcion()
    if resultado is not None:
        dia, funcion = resultado
        imprimir_asientos(dia, funcion)


def reservar_asiento():
    """Opción 3: reserva un asiento libre de una función."""
    print("\n=== 3. Reservar asiento ===")
    resultado = pedir_funcion()
    if resultado is None:
        return
    dia, funcion = resultado
    estado = obtener_estado(dia, funcion)

    imprimir_asientos(dia, funcion)
    posicion = pedir_asiento()
    if posicion is None:
        return
    fila, columna = posicion
    asiento = nombre_asiento(fila, columna)

    if estado["asientos"][fila][columna] == OCUPADO:
        print(f"[!] El asiento {asiento} ya está ocupado. Elija otro asiento.")
        return

    nombre = pedir_nombre()
    estado["asientos"][fila][columna] = OCUPADO
    estado["reservas"][asiento] = nombre
    print(f"\n[OK] Reserva confirmada a nombre de {nombre}.")
    print(f"     Película: {funcion['pelicula']} ({funcion['formato']})")
    print(f"     {dia} a las {funcion['horario']} - Sala {funcion['sala']} - Asiento {asiento}")


def cancelar_reserva():
    """Opción 4: libera un asiento que estaba ocupado."""
    print("\n=== 4. Cancelar reserva ===")
    resultado = pedir_funcion()
    if resultado is None:
        return
    dia, funcion = resultado
    estado = obtener_estado(dia, funcion)

    libres, ocupados, total = contar_asientos(estado["asientos"])
    if ocupados == 0:
        print("[!] Esa función no tiene asientos reservados.")
        return

    imprimir_asientos(dia, funcion)
    posicion = pedir_asiento()
    if posicion is None:
        return
    fila, columna = posicion
    asiento = nombre_asiento(fila, columna)

    if estado["asientos"][fila][columna] != OCUPADO:
        print(f"[!] El asiento {asiento} no está ocupado, no hay reserva que cancelar.")
        return

    nombre = estado["reservas"].pop(asiento, "(sin nombre)")
    estado["asientos"][fila][columna] = LIBRE
    print(f"\n[OK] Reserva cancelada: asiento {asiento} de {nombre}.")
    print(f"     {funcion['pelicula']} - {dia} a las {funcion['horario']} - Sala {funcion['sala']}")


def ver_disponibilidad():
    """Opción 5: muestra cuántos asientos libres y ocupados tiene cada función de un día."""
    print("\n=== 5. Ver disponibilidad ===")
    dia = pedir_dia()
    if dia is None:
        return

    print(f"\n--- Disponibilidad del {dia} ---")
    suma_libres = 0
    suma_ocupados = 0
    for funcion in cartelera[dia]:
        libres, ocupados, total = contar_asientos(obtener_estado(dia, funcion)["asientos"])
        suma_libres += libres
        suma_ocupados += ocupados
        porcentaje = ocupados / total * 100
        print(f"Sala {funcion['sala']} | {funcion['horario']} | {funcion['formato']} | {funcion['pelicula']}")
        print(f"    Libres: {libres}   Ocupados: {ocupados}   Total: {total}   Ocupación: {porcentaje:.1f}%")

    suma_total = suma_libres + suma_ocupados
    porcentaje_dia = suma_ocupados / suma_total * 100
    print(f"\nTotal del día: {suma_libres} libres y {suma_ocupados} ocupados de {suma_total} asientos "
          f"({porcentaje_dia:.1f}% de ocupación)")


# ======================================================================
# PROGRAMA PRINCIPAL
# ======================================================================
def mostrar_menu():
    print("\n===== CineMax - Sistema de Reservas =====")
    print("1. Ver cartelera de un día")
    print("2. Mostrar asientos de una función")
    print("3. Reservar asiento")
    print("4. Cancelar reserva")
    print("5. Ver disponibilidad")
    print("6. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ver_cartelera()
        elif opcion == "2":
            mostrar_asientos()
        elif opcion == "3":
            reservar_asiento()
        elif opcion == "4":
            cancelar_reserva()
        elif opcion == "5":
            ver_disponibilidad()
        elif opcion == "6":
            print("\nGracias por usar CineMax. ¡Hasta pronto!")
            break
        else:
            print("[!] Opción no válida. Elija un número del 1 al 6.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma finalizado. ¡Hasta pronto!")