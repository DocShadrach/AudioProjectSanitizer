# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import filedialog
import ffmpeg
from tqdm import tqdm
import soundfile as sf
import numpy as np

def detect_channel_type(file_path, correlation_threshold=0.95):
    # Cargar el archivo WAV
    data, samplerate = sf.read(file_path)

    # Verificar si el archivo tiene un solo canal
    if len(data.shape) == 1 or data.shape[1] == 1:
        return "Mono"  # El archivo es mono

    # Verificar si el archivo tiene dos canales
    if data.shape[1] == 2:
        # Extraer los canales izquierdo y derecho
        left_channel = data[:, 0]
        right_channel = data[:, 1]

        # Calcular la correlación entre los canales izquierdo y derecho
        correlation = np.corrcoef(left_channel, right_channel)[0, 1]

        # Verificar si la correlación es mayor que el umbral
        if correlation > correlation_threshold:
            return "False stereo"  # La correlación es alta, es un 'falso estéreo'

        return "True stereo"  # La correlación es baja, es un 'estéreo verdadero'

    return "Unknown"  # No se puede determinar el tipo de canal

def obtener_tipo_audio(archivo):
    try:
        # Especificar la ubicación del ejecutable de ffprobe en la llamada a probe
        info = ffmpeg.probe(archivo, cmd='C:/ffmpeg/bin/ffprobe.exe')
        num_canales = info['streams'][0]['channels']
        if num_canales == 1:
            return "mono"
        elif num_canales == 2:
            channel_type = detect_channel_type(archivo)
            if channel_type == "False stereo":
                return "mono"  # Si es falso estéreo, lo tratamos como mono
            else:
                return "stereo"
        else:
            return "unknown"
    except ffmpeg.Error as e:
        print("Error al obtener información del archivo:", e)
        return None

def renombrar_archivos(carpeta):
    for directorio_raiz, directorios, archivos in os.walk(carpeta):
        for archivo in archivos:
            # Eliminar archivos cuyo nombre comience con un punto
            if archivo.startswith("."):
                ruta_archivo = os.path.join(directorio_raiz, archivo)
                os.remove(ruta_archivo)
                print(f"Archivo eliminado: {ruta_archivo}")
    for directorio_raiz, directorios, archivos in os.walk(carpeta):
        archivos_wav = [archivo for archivo in archivos if archivo.endswith(".wav")]
        with tqdm(total=len(archivos_wav), desc=f"Procesando archivos en {directorio_raiz}") as pbar:
            for archivo in archivos_wav:
                ruta_original = os.path.join(directorio_raiz, archivo)
                tipo_audio = obtener_tipo_audio(ruta_original)
                if tipo_audio:
                    nuevo_nombre = archivo.replace(".wav", f" ({tipo_audio}).wav")
                    os.rename(ruta_original, os.path.join(directorio_raiz, nuevo_nombre))
                pbar.update(1)

def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta")
    return carpeta

if __name__ == "__main__":
    carpeta = seleccionar_carpeta()
    if carpeta:
        renombrar_archivos(carpeta)
        print("Archivos renombrados exitosamente.")
    else:
        print("No se seleccionó ninguna carpeta.")
