import os
import shutil
from pathlib import Path

directorio = Path(Path.home(), "Recetas", "Recetas")  #Indicar el directorio indicado
recetas = set()
categorias = set()
accion = ''
nombre = ''
categoria = ''


def menu():
    opcion = ''
    while opcion != 6:
        os.system("cls")
        contenido = os.listdir(directorio)
        opcion = input("""Bienvenido al recetario!!! 
        
[1] Ver Recetas
[2] Añadir Recetas
[3] Añadir Categoria
[4] Eliminar Recetas
[5] Eliminar Categorias
[6] Salir

Ingresa el NÚMERO de la opción a realizar: """)
        os.system("cls")
        match opcion:
            case '1':
                accion = 'visualizar'
                nivel = 1
                categoria_a_receta(directorio, nivel, accion, contenido, nombre, categoria, opcion)
                print("\n")
                os.system("pause")
            case "2":
                nivel = 1
                accion = 'agregar receta'
                categoria_a_receta(directorio, nivel, accion, contenido, nombre, categoria, opcion)
                print("\n")
                os.system("pause")
            case "3":
                agregar('categoria', categoria)
                print("\n")
                os.system("pause")
            case "4":
                nivel = 1
                accion = 'eliminar receta'
                categoria_a_receta(directorio, nivel, accion, contenido, nombre, categoria, opcion)
                print("\n")
                os.system("pause")
            case "5":
                nivel = 1
                accion = 'eliminar categoria'
                categoria_a_receta(directorio, nivel, accion, contenido, nombre, categoria, opcion)
                print("\n")
                os.system("pause")
            case "6":
                os.system("cls")
                print("PROGRAMA FINALIZADO\n\n\n\n")
                break
            case _:
                print("INGRESA UNA OPCION VALIDA")
                os.system("pause")


def mostrar_nombre_archivo_sin_extension(accion, contenido, opcion):
    indice = 1
    print(f"Ingrese la {opcion} que desea {accion}\n")
    for archivo in contenido:
        ruta_completa = os.path.join(directorio, archivo)
        if opcion == 'receta' and archivo.endswith('.txt'):
            nombre, extension = os.path.splitext(archivo)
            print(f"[{indice}] {nombre}")
            indice += 1
            recetas.add(nombre)
        elif opcion == 'categoria' and os.path.isdir(ruta_completa):
            nombre, extension = os.path.splitext(archivo)
            print(f"[{indice}] {nombre}")
            indice += 1
            categorias.add(archivo)


def verificar_existencia(nombre, lista):
    os.system("cls")
    return nombre in lista


def categoria_a_receta(directorio, nivel, accion, contenido, nombre, categoria, opcion):
    if nivel == 1:
        opcion = 'categoria'
        mostrar_nombre_archivo_sin_extension(accion, contenido, opcion)
        nombre = input(f"\nNombre EXACTO de la {opcion} a {accion}: ")
        os.system("cls")

        if not verificar_existencia(nombre, categorias):
            print(f"""LA {opcion} INGRESADA NO SE ENCUENTRA EN SISTEMA

VERIFICA SI FUE INGRESADA CORRECTAMENTE, RECUERDA TIENE QUE ESTAR ESCRITA EXACTAMENTE COMO APARECE EN PANTALLA
            """)
            return

        if accion == 'eliminar categoria':
            eliminar(opcion, categoria, nombre)

        if accion == 'visualizar' or accion == 'eliminar receta' or accion == 'agregar receta':
            nivel = 2
            categoria_a_receta(directorio, nivel, accion, contenido, nombre, categoria, opcion)

    elif nivel == 2:
        categoria = nombre
        contenido = os.listdir(visualizar_categoria_o_receta(directorio, opcion, nombre, categoria))
        opcion = 'receta'
        mostrar_nombre_archivo_sin_extension(accion, contenido, opcion)

        if accion == 'visualizar':
            nombre = input(f"\nNombre EXACTO de la {opcion} a {accion}: ")
            if not verificar_existencia(nombre, recetas):
                print(f"""LA {opcion} INGRESADA NO SE ENCUENTRA EN SISTEMA

VERIFICA SI FUE INGRESADA CORRECTAMENTE, RECUERDA TIENE QUE ESTAR ESCRITA EXACTAMENTE COMO APARECE EN PANTALLA
                """)
                return
            print("\n")
            visualizar_categoria_o_receta(directorio, opcion, nombre, categoria)

        elif accion == 'eliminar receta':
            nombre = input(f"\nNombre EXACTO de la {opcion} a {accion}: ")
            if not verificar_existencia(nombre, recetas):
                print(f"""LA {opcion} INGRESADA NO SE ENCUENTRA EN SISTEMA

VERIFICA SI FUE INGRESADA CORRECTAMENTE, RECUERDA TIENE QUE ESTAR ESCRITA EXACTAMENTE COMO APARECE EN PANTALLA
                """)
                return
            eliminar(opcion, categoria, nombre)

        elif accion == 'agregar receta':
            agregar(opcion, categoria)


def visualizar_categoria_o_receta(directorio, opcion, nombre, categoria):
    os.system("cls")
    if opcion == 'categoria':
        categoria = nombre
        directorio = Path(f'{directorio}\\{categoria}')
        return directorio

    elif opcion == 'receta':
        receta = (f'{directorio}\\{categoria}\\{nombre}.txt')
        archivo = open(receta, 'r')
        print(archivo.read())
        archivo.close()


def agregar(opcion, categoria):
    archivo = input(f"Ingresa el nombre de tu nueva {opcion}: ")
    os.system("cls")
    if opcion == 'receta':
        if verificar_existencia(archivo, recetas):
            os.system("cls")
            print(f"YA EXISTE UNA {opcion} CON ESE NOMBRE")
            return

        archivo = open(f"{directorio}\\{categoria}\\{archivo}.txt", 'w')
        print("Ingresa tu receta (presiona Ctrl + Z en una línea vacía para terminar)\n")
        texto = ''

        while True:
            try:
                linea = input("")
                texto += linea + '\n'
            except EOFError:
                break

        archivo.writelines(f"""{texto}""")
        archivo.close()
        os.system("cls")
        print("La receta se agrego correctamente!!!")

    elif opcion == 'categoria':
        if verificar_existencia(archivo, categorias):
            os.system("cls")
            print(f"YA EXISTE UNA {opcion} CON ESE NOMBRE")
            return
        os.makedirs(f'{directorio}\\{archivo}')
        print("La categoria se agrego correctamente!!!")
    else:
        pass


def eliminar(opcion, categoria, nombre):
    if opcion == 'receta':
        recetas.remove(nombre)
        nombre += '.txt'
        os.remove(f'{directorio}\\{categoria}\\{nombre}')
        os.system("cls")
        print("RECETA ELIMINADA CORRECTAMENTE")
    elif opcion == 'categoria':
        categoria = nombre
        shutil.rmtree(f"{directorio}\\{categoria}")
        categorias.remove(nombre)
        os.system("cls")
        print("CATEGORIA ELIMINADA CORRECTAMENTE")
    else:
        pass


menu()
