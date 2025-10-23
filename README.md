Audio Project Sanitizer (APS) v3.0

You can download version 3.0 from this link: // Puedes descargar la versión 3.0 desde este enlace:

https://www.dropbox.com/scl/fi/6njx4fvaakssuqueiuonz/APS_3.0.rar?rlkey=03b91otquzf611f83fzqigcwx&st=57760lvg&dl=0

(For now, only for Windows.) // (Por ahora, solo para Windows.)

Videotutorial (ver 2.6): https://youtu.be/le1fA-1PH2E

Old version (2.6): https://www.dropbox.com/scl/fi/bs2dy9n8jh35jzg8jqe8g/APS_2.6b.rar?rlkey=8jj6cj9l7fmyeiuzsuutwaxbg&dl=0

----------------------------------------------------------------------------------------------------------

English:

This application is designed for mix engineers who work with large numbers of exported audio tracks. It automates tasks such as identifying file type (mono/stereo/dualmono), precise conversion to true mono or stereo, track reordering, and organizing material by category.
It does not alter the audio content or compromise sound fidelity. Every step in the workflow has been designed to save time while maintaining full technical quality.

WARNING: although this program works non-destructively (saving a copy of the files it has modified in a specific folder) it is always advisable to make a copy of your original files.

It includes 5 main functions:
1) If your project files contain temporary MacOS files (those that start with a dot), it can delete them.
2) Scans all files to see if they are mono or stereo and renames them to identify them as such.
It also recognises when a stereo file is actually a fake stereo (same information on both channels) and classifies them as 'dualmono' and not 'stereo'.
3) It gives the possibility of converting "dualmono" files into mono without any quality loss. This allows you to work with smaller files.
4) Search for files that could be L and R, show in a window what it have found and ask if you want to put them together in a single stereo file.
5) You can reorder the files by listing them according to the position we choose, and you can catalog them within different categories:
"01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"

NEW FEATURES IN VERSION 3.0:
- Enhanced file selection interface with checkboxes for dualmono and L/R files
- Progress window with real-time status updates and detailed activity log
- Automatic detection and handling of files with silent channels
- Improved audio format preservation using soundfile library
- Better file selection control - you can now choose which specific files to process
- Enhanced L/R file matching with improved pattern recognition
- More informative dialogs with file previews
- Better error handling and user feedback

- The executable file works only on Windows. If you use another operating system, you could directly run the main.py file by installing Python on your computer or compile that file to make the program work on your operating system.
- This program does not need to be installed, the executable file works portably, so you can place this file wherever you want.
- It may be that some antiviruses detect the executable of this program as Malware. This is a false positive, don't worry, you can review the code or compile it on your own if you don't trust it.
- Files must be in WAV format.
- In the file reorder box, it is important that the folders maintain the preset order.
- It is not necessary or mandatory to categorize the files, if they are above the categories they will be listed anyway but will not be moved to a folder.
- If the project doesn't have temporary files (the kind that start with a dot), the option to delete them doesn't appear.
- If the files are already identified as (mono) or (stereo), the option to scan the files does not appear.
- If the selected folder does not have WAV files (only folders appear), the option to reorder the files does not appear.
- If you have a project that is already categorized, you can indicate that the program enters a category (its folder) and reorder the files as well (without having to categorize them).

Audio Quality Guarantee!!
This tool has been designed to ensure that all audio analysis, conversion, and organization processes fully preserve the original quality. These are the guarantees it offers:
1) Bit depth and sample rate are preserved exactly during any file conversion.
2) Dualmono files are not averaged; instead, the system analyzes both channels and retains only the active one (if the other is silent), avoiding artifacts and preserving fidelity.
3) When building stereo tracks from L/R files, both sources are verified to be true mono. If not, they are safely converted without altering their technical properties.
4) Original files are never overwritten. Any processed file is automatically moved to a backup folder (-- OBSOLETE FILES) to allow full reversibility if needed.
5) The system automatically detects mislabeled or structurally incorrect files (e.g. false stereo or silent channels) and classifies them correctly, speeding up workflow without compromising quality.

This program is completely free but if this program is useful to you, you could help me with a donation at:

https://ko-fi.com/docshadrach

----------------------------------------------------------------------------------------------------------

Español:

Esta aplicación está pensada para ingenieros de mezcla que trabajan con grandes cantidades de pistas exportadas. Automatiza tareas como la identificación de tipo de archivo (mono/estéreo/dualmono), la conversión precisa a mono o estéreo real, la reordenación de pistas, y la organización del material por categorías.
No modifica el contenido sonoro ni compromete la fidelidad del audio. Cada decisión en el flujo de trabajo ha sido tomada con el objetivo de facilitar la preparación de sesiones sin perder tiempo ni calidad.

ADVERTENCIA: aunque este programa trabaja de forma no destructiva (guardando en una carpeta específica una copia de los archivos que ha modificado) es siempre recomendable hacer una copia de tus archivos originales.

Incluye 5 funciones principales:
1) Si los archivos del proyecto contienen archivos temporales de MacOS (los que empiezan con un punto) los puede borrar.
2) Analiza todos los archivos para ver si son mono o si son estéreo y los renombra para identificarlos como tal.
Reconoce también cuando un archivo estéreo es en realidad un falso estéreo (misma información en ambos canales) y los cataloga como 'dualmono' y no como 'stereo'.
3) Da la posibilidad de convertir los archivos "dualmono" en mono sin ningún tipo de pérdida de calidad. Ésto permite trabajar con archivos más pequeños.
4) Busca archivos que puedan ser L y R, muestra en una ventana lo que ha encontrado y pregunta si se quieren juntar en un solo archivo estéreo.
5) Puede reordenar los archivos enumerándolos según la posición que elijamos, y puede catalogarlos dentro de diferentes categorías:
"01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"

NUEVAS CARACTERÍSTICAS EN VERSIÓN 3.0:
- Interfaz mejorada de selección de archivos con casillas de verificación para archivos dualmono y L/R
- Ventana de progreso con actualizaciones en tiempo real y registro detallado de actividad
- Detección automática y manejo de archivos con canales silenciosos
- Mejor preservación del formato de audio usando la librería soundfile
- Mejor control de selección de archivos - ahora puedes elegir qué archivos específicos procesar
- Mejor reconocimiento de patrones para archivos L/R
- Diálogos más informativos con previsualización de archivos
- Mejor manejo de errores y retroalimentación al usuario

- El ejecutable funciona únicamente en Windows. Si utilizas otro sistema operativo podrías ejecutar directamente el archivo main.py instalando Python en tu ordenador o compilar ese archivo para hacer que el programa funcione en tu sistema operativo.
- Este programa no necesita instalarse, el ejecutable funciona de forma portable, así que puedes colocar este archivo donde quieras.
- Puede ser que algunos antivirus detecten el ejecutable de este programa como Malware. Ésto es un falso positivo, no te preocupes, puedes revisar el código o compilarlo por tu cuenta si no te fías.
- Los archivos deben estar en formato WAV.
- En el cuadro de reordenación de los archivos es importante que las carpetas mantengan el orden preestablecido.
- No es necesario u obligatorio categorizar los archivos, si quedan por encima de las categorías se enumerarán igualmente pero no se moverán a una carpeta.
- Si el proyecto no tiene archivos temporales (de los que comienzan con un punto) la opción de eliminarlos no aparece.
- Si los archivos ya están identificados como (mono) o (stereo) la opción de analizar los archivos no aparece.
- Si la carpeta seleccionada no tiene archivos WAV (solo aparecen carpetas) la opción de reordenar los archivos no aparece.
- Si tienes un proyecto que ya está categorizado, puedes indicar para que el programa entre en alguna categoría (a su carpeta) y reordenar igualmente los archivos (sin necesidad de categorizarlos).

Garantía de calidad del audio!!
Esta herramienta ha sido diseñada para asegurar que todos los procesos de análisis, conversión y organización de archivos de audio respeten al 100% la calidad original. Estas son las garantías que ofrece:
1) El bit depth y la frecuencia de muestreo de todos los archivos se mantienen intactos durante cualquier conversión.
2) Los archivos dualmono no se convierten haciendo un promedio entre canales, sino que se analiza cuál de los dos es realmente útil (si uno está vacío) y se conserva únicamente el canal activo, evitando artefactos o degradación.
3) En la reconstrucción de pistas estéreo a partir de archivos L/R, se asegura que ambas fuentes sean mono reales. Si alguna no lo es, se convierte sin pérdida, manteniendo su integridad técnica.
4) Todos los archivos originales se conservan. Cualquier archivo que haya sido procesado se mueve automáticamente a una carpeta de respaldo (-- OBSOLETE FILES) para permitir una reversión si es necesaria.
5) El sistema detecta de forma automática archivos mal etiquetados o con estructuras erróneas (como falsos estéreo o canales silenciosos) y los clasifica correctamente, lo que agiliza el flujo de trabajo sin poner en riesgo la calidad.

Este programa es totalmente gratuito pero si este programa te resulta de utilidad podrías ayudarme con una donación en:

https://ko-fi.com/docshadrach


