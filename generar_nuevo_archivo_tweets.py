import csv

def leer_csv(nombre_archivo):
    datos = []
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo)
        for linea in lector_csv:
            datos.append(linea)
    return datos

def escribir_csv(datos, nombre_archivo):
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        escritor_csv = csv.writer(archivo)
        for i in range(2000000):
            escritor_csv.writerow(datos[i])
