import requests

# URL del archivo .txt en línea
url_txt = 'https://elcano-kappa.vercel.app/PelisAcestream.txt'  # <-- Cambia esto por tu URL real

# Nombre del archivo de salida
archivo_salida = 'acramses.m3u'

# Prefijos para reemplazo
antiguo_prefijo = 'acestream://'
nuevo_prefijo = 'http://127.0.0.1:6878/ace/getstream?id='

try:
    # Descargar contenido del archivo
    response = requests.get(url_txt)
    response.raise_for_status()  # Lanza error si hay un problema

    # Procesar líneas y hacer reemplazos
    lineas_convertidas = []
    for linea in response.text.splitlines():
        if antiguo_prefijo in linea:
            linea = linea.replace(antiguo_prefijo, nuevo_prefijo)
        lineas_convertidas.append(linea)

    # Escribir en archivo .m3u
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for linea in lineas_convertidas:
            f.write(linea + '\n')

    print(f'Archivo guardado como: {archivo_salida}')

except requests.RequestException as e:
    print(f'Error al descargar el archivo: {e}')
except Exception as e:
    print(f'Error general: {e}')
