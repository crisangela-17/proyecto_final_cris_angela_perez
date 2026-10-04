# CineMax - Sistema de Reservas de Cine

Proyecto final: aplicación de consola en Python para gestionar las reservas de un cine ficticio (**CineMax**) con 5 salas y una cartelera de una semana (Lunes a Domingo). Cada día se proyectan las mismas 5 películas, pero en distinta sala, horario y formato (`Normal`, `3D`, `4DX`, `CXC`).

## Cómo ejecutarlo

```
python main.py
```

Requiere Python 3.6 o superior. No usa librerías externas.

## Menú

1. **Ver cartelera de un día**: muestra película, sala, horario y formato de las 5 funciones.
2. **Mostrar asientos de una función**: imprime la matriz de 5 filas x 6 columnas (`.` libre, `X` ocupado) con encabezados de fila y columna (A1 ... E6).
3. **Reservar asiento**: valida el día, la sala y el horario, que el asiento exista y que esté libre; guarda el nombre de quien reserva.
4. **Cancelar reserva**: valida que el asiento esté ocupado antes de liberarlo.
5. **Ver disponibilidad**: muestra asientos libres, ocupados, total y porcentaje de ocupación de cada función del día.
6. **Salir**

## Estructuras de datos

- `cartelera`: diccionario `{día: [funciones]}`; cada función es un diccionario con `pelicula`, `sala`, `horario` y `formato`.
- `estado_funciones`: diccionario `{(día, sala, horario): {"asientos": matriz, "reservas": dict}}`. Cada función tiene su propia matriz de asientos (lista de listas) y un diccionario `{"C3": "nombre"}` con quién reservó cada asiento.

## Validaciones

- El día se acepta por nombre (sin importar mayúsculas ni tildes) o por número del 1 al 7.
- El horario se acepta como `2:00 pm`, `2:00pm` o `2pm`.
- Se rechazan salas fuera del rango 1-5, funciones que no existen, asientos fuera de rango (filas A-E, columnas 1-6), asientos ya ocupados y cancelaciones de asientos que están libres.
- Si un dato no es válido, se muestra un mensaje y se vuelve al menú.