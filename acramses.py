import requests
import sys

# URL del archivo .txt en línea
# ¡IMPORTANTE! Cambia esto por tu URL real si es diferente.
url_txt = 'https://elcano-kappa.vercel.app/PelisAcestream.txt' 

# Nombre del archivo de salida
archivo_salida = 'acramses'

# Prefijos para reemplazo
antiguo_prefijo = 'acestream://'
nuevo_prefijo = 'http://127.0.0.1:6878/ace/getstream?id='

print(f"Iniciando la descarga desde: {url_txt}")
print(f"El archivo de salida será: {archivo_salida}")

try:
    # 1. Descargar contenido del archivo
    response = requests.get(url_txt, timeout=15) # Añadido timeout por seguridad
    response.raise_for_status()  # Lanza error si hay un problema HTTP

    # 2. Procesar líneas y hacer reemplazos
    lineas_convertidas = ['#EXTM3U'] # <-- AÑADIDO: Encabezado estándar M3U
    
    # Obtener el contenido del archivo de texto
    content_lines = response.text.splitlines()
    
    print(f"Líneas totales leídas: {len(content_lines)}")

    for linea in content_lines:
        linea_limpia = linea.strip() # Limpia espacios en blanco
        
        # Solo procesar líneas que no estén vacías y que no sean comentarios (opcional)
        if not linea_limpia or linea_limpia.startswith('#'):
            lineas_convertidas.append(linea)
            continue
            
        if antiguo_prefijo in linea_limpia:
            # Realizar el reemplazo solo en la línea que contiene el prefijo
            linea_reemplazada = linea_limpia.replace(antiguo_prefijo, nuevo_prefijo)
            lineas_convertidas.append(linea_reemplazada)
        else:
            # Si no contiene el prefijo, se mantiene la línea original (ej. títulos EXTINF)
            lineas_convertidas.append(linea_limpia)

    # 3. Escribir en archivo .m3u
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        # Aseguramos que todas las líneas se escriban
        f.write('\n'.join(lineas_convertidas) + '\n') 

    print(f'✅ Proceso completado. Archivo guardado como: {archivo_salida}')

except requests.exceptions.Timeout:
    print(f'❌ Error de tiempo de espera (Timeout) al conectar con {url_txt}', file=sys.stderr)
    sys.exit(1)
except requests.RequestException as e:
    print(f'❌ Error al descargar el archivo o error HTTP: {e}', file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f'❌ Error general en la ejecución: {e}', file=sys.stderr)
    sys.exit(1)
