# GESTIÓN DE DATOS DE PAÍSES EN PYTHON

## Descripción del Programa

Este proyecto es un **Sistema de Gestión de Datos de Países** implementado en Python, desarrollado como Trabajo Práctico Integrador (TPI) de Programación I. Permite almacenar, consultar, modificar y analizar datos de países utilizando estructuras de datos avanzadas y persistencia en archivos CSV.

* **Estructuras clave:** El sistema gestiona los datos utilizando una **Lista** principal donde cada país es almacenado como un **Diccionario**.
* **Persistencia:** La información se guarda y se recupera desde el archivo **`datos_paises.csv`** para asegurar que los cambios no se pierdan al cerrar el programa.

## Características Principales

* **Validaciones Robustas:** Validación numérica usando `.isdigit()`, prevención de duplicados.
* **Datos de Respaldo:** Carga dataset inicial si el CSV no existe.
* **Ordenamiento:** Utiliza el algoritmo **burbuja** personalizado para 6 criterios.
* **Limpieza de Texto:** Búsqueda insensible a mayúsculas/minúsculas.
* **Persistencia de Datos:** Guardado automático en operaciones críticas con encoding UTF-8.

## Instrucciones de Uso

### Requisitos
* Python 3.x instalado en el sistema.
* Módulos estándar (`csv`, `os`).

### Ejecución
1.  Asegúrese de que los archivos `gestion_paises.py` y `datos_paises.csv` estén en el mismo directorio.
2.  Abra la terminal o Símbolo del sistema.
3.  Ejecute el programa con el siguiente comando (corregido):

    ```bash
    python gestion_paises.py
    ```

### Ejemplos de Entradas y Salidas

| Opción | Funcionalidad | Ejemplo de Interacción (Entrada) | Salida del Sistema |
| :--- | :--- | :--- | :--- |
| **1** | Agregar país | `Nombre: Colombia`, `Población: 51870000` | `Registro exitoso: El país 'Colombia' ya está agregado a la lista.` |
| **3** | Buscar país | `Escribe parte del nombre a buscar: chi` | `-> Chile, Población: 19,116,201` (Búsqueda parcial) |
| **6** | Filtrar por Rango | Filtra países con población entre 40M y 70M. | Muestra solo Argentina, España y Francia. |
| **8** | Estadísticas | `Seleccione opción: 8` | Muestra país con mayor/menor población y cantidad de países por continente. |
| **9** | Salir | `Seleccione opción: 9` | `Cerrando sistema y guardando datos. ¡Adiós!` (Guarda todos los cambios en CSV) |

## Participación de los Integrantes

Este proyecto fue desarrollado por los alumnos **Montenegro Dahyana** y **Domínguez Matías**.

| Integrante | Rol y Responsabilidades |
| :--- | :--- |
| **Dahyana Montenegro** | Desarrollo de las funciones de **Persistencia de Datos** (Carga y Guardado del CSV), implementación de la estructura de control (`match/case`), y funciones de entrada/salida. |
| **Matías Domínguez** | Desarrollo e implementación de la **Lógica Principal** del menú y las operaciones numéricas (Estadísticas, Ordenamiento por algoritmo de intercambio). |
