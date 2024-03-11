Audio Project Sanitizer (APS) v2.5

You can download version 2.5 from this link: // Puedes descargar la versión 2.5 desde este enlace:

https://www.dropbox.com/scl/fi/8ylph8n9wm6koz1wel1za/APS_2.5.rar?rlkey=clbosgc7lyq5wd4htsfj78ieo&dl=0


----------------------------------------------------------------------------------------------------------

English:

WARNING: although this program works non-destructively (saving a copy of the files it has modified in a specific folder) it is always advisable to make a copy of your original files.

This program is used to sort the audio files in a mixing project before importing the files into the DAW.
It includes 5 main functions:
1) If your project files contain temporary Pro Tools files (those that start with a dot), it can delete them.
2) Scans all files to see if they are mono or stereo and renames them to identify them as such.
It also recognises when a stereo file is actually a fake stereo (same information on both channels) and classifies them as 'dualmono' and not 'stereo'.
3) It gives the possibility of converting "dualmono" files into mono without any quality loss. This allows you to work with smaller files.
4) Search for files that could be L and R, show in a window what it have found and ask if you want to put them together in a single stereo file.
5) You can reorder the files by listing them according to the position we choose, and you can catalog them within different categories:
"01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"

- The executable file works only on Windows. If you use another operating system, you could directly run the main.py file by installing Python on your computer or compile that file to make the program work on your operating system.
- This program does not need to be installed, the executable file works portably, so you can place this file wherever you want.
- It may be that some antiviruses detect the executable of this program as Malware. This is a false positive, don't worry, you can review the code or compile it on your own if you don't trust it.
- IMPORTANT: you need to keep the ffprobe.exe file in the same folder as the executable file so that the program can detect the mono and stereo files. If the program does not find this file, this functionality will not work (the rest of the functionalities will continue to work). The ffprobe.exe file that I provide with the download of this program was downloaded from the official site of FFmpeg (https://ffmpeg.org/download.html) and is only for Windows, if you need this file for another operating system you can download it from that page.
- Files must be in WAV format.
- In the file reorder box, it is important that the folders maintain the preset order.
- It is not necessary or mandatory to categorize the files, if they are above the categories they will be listed anyway but will not be moved to a folder.
- If the project doesn't have temporary files (the kind that start with a dot), the option to delete them doesn't appear.
- If the files are already identified as (mono) or (stereo), the option to scan the files does not appear.
- If the selected folder does not have WAV files (only folders appear), the option to reorder the files does not appear.
- If you have a project that is already categorized, you can indicate that the program enters a category (its folder) and reorder the files as well (without having to categorize them).

This program is completely free but if this program is useful to you, you could help me with a donation at:

https://ko-fi.com/docshadrach

----------------------------------------------------------------------------------------------------------

Español:

ADVERTENCIA: aunque este programa trabaja de forma no destructiva (guardando en una carpeta específica una copia de los archivos que ha modificado) es siempre recomendable hacer una copia de tus archivos originales.

Este programa sirve para ordenar los archivos de audio de un proyecto de mezcla antes de importar los archivos al DAW.
Incluye 5 funciones principales:
1) Si los archivos del proyecto contienen archivos temporales de Pro Tools (los que empiezan con un punto) los puede borrar.
2) Analiza todos los archivos para ver si son mono o si son estéreo y los renombra para identificarlos como tal.
Reconoce también cuando un archivo estéreo es en realidad un falso estéreo (misma información en ambos canales) y los cataloga como 'dualmono' y no como 'stereo'.
3) Da la posibilidad de convertir los archivos "dualmono" en mono sin ningún tipo de pérdida de calidad. Ésto permite trabajar con archivos más pequeños.
4) Busca archivos que puedan ser L y R, muestra en una ventana lo que ha encontrado y pregunta si se quieren juntar en un solo archivo estéreo.
5) Puede reordenar los archivos enumerándolos según la posición que elijamos, y puede catalogarlos dentro de diferentes categorías:
"01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"

- El ejecutable funciona únicamente en Windows. Si utilizas otro sistema operativo podrías ejecutar directamente el archivo main.py instalando Python en tu ordenador o compilar ese archivo para hacer que el programa funcione en tu sistema operativo.
- Este programa no necesita instalarse, el ejecutable funciona de forma portable, así que puedes colocar este archivo donde quieras.
- Puede ser que algunos antivirus detecten el ejecutable de este programa como Malware. Ésto es un falso positivo, no te preocupes, puedes revisar el código o compilarlo por tu cuenta si no te fías.
- IMPORTANTE: necesitas mantener el archivo ffprobe.exe en la misma carpeta que el ejecutable para que el programa pueda detectar los archivos mono y stereo. Si el programa no encuentra este archivo esta funcionalidad no funcionará (el resto de funcionalidades seguirán funcionando). El archivo ffprobe.exe que proveo con la descarga de este programa fue descargado desde el sitio oficial de FFmpeg (https://ffmpeg.org/download.html) y sirve solo para Windows, si necesitas este archivo para otro sistema operativo lo puedes descargar desde esa página.
- Los archivos deben estar en formato WAV.
- En el cuadro de reordenación de los archivos es importante que las carpetas mantengan el orden preestablecido.
- No es necesario u obligatorio categorizar los archivos, si quedan por encima de las categorías se enumerarán igualmente pero no se moverán a una carpeta.
- Si el proyecto no tiene archivos temporales (de los que comienzan con un punto) la opción de eliminarlos no aparece.
- Si los archivos ya están identificados como (mono) o (stereo) la opción de analizar los archivos no aparece.
- Si la carpeta seleccionada no tiene archivos WAV (solo aparecen carpetas) la opción de reordenar los archivos no aparece.
- Si tienes un proyecto que ya está categorizado, puedes indicar para que el programa entre en alguna categoría (a su carpeta) y reordenar igualmente los archivos (sin necesidad de categorizarlos).

Este programa es totalmente gratuito pero si este programa te resulta de utilidad podrías ayudarme con una donación en:

https://ko-fi.com/docshadrach

