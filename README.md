Audio Project Sanitizer (APS) v2.0:

English:

This program is used to sort the audio files in a mixing project before importing the files into the DAW.
It includes 3 main functions:
1) If your project files contain temporary Pro Tools files (those that start with a period), you can delete them.
2) Scans all files to see if they are mono or stereo and renames them to identify them as such.
It also recognises when a stereo file is actually a fake stereo (same information on both channels) and classifies them as 'mono' and not 'stereo'.
3) You can reorder the files by listing them according to the position we choose, and you can catalog them within different categories:
"01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"

- The executable works only on Windows, you could compile the main.py file to work on your operating system.
- This program does not need to be installed, the executable works portably.
- It may be that some antiviruses detect the executable of this program as Malware. This is a false positive, don't worry, you can review the code or compile it on your own if you don't trust it.
- IMPORTANT: you need to place the "ffmpeg" folder in the C:/ root directory of your computer so that the program can detect the mono and stereo files. If the program does not find this folder, this functionality will not work (the rest of the functions will continue to work).
- Files must be in WAV format.
- In the file reorder box, it is important that the folders maintain the preset order.
- It is not necessary or mandatory to categorize the files, if they are above the categories they will be listed anyway but will not be moved to a folder.
- If the project doesn't have temporary files (the kind that start with a period), the option to delete them doesn't appear.
- If the files are already identified as (mono) or (stereo), the option to scan the files does not appear.
- If the selected folder does not have WAV files (only folders appear), the option to reorder the files does not appear.
- If you have a project that is already categorized, you can indicate that the program enters a category (its folder) and reorder the files as well (without having to categorize them).

----------------------------------------------------------------------------------------------------------

Español:

Este programa sirve para ordenar los archivos de audio de un proyecto de mezcla antes de importar los archivos al DAW.
Incluye 3 funciones principales:
1) Si los archivos del proyecto contienen archivos temporales de Pro Tools (los que empiezan con un punto) los puede borrar.
2) Analiza todos los archivos para ver si son mono o si son estéreo y los renombra para identificarlos como tal.
Reconoce también cuando un archivo estéreo es en realidad un falso estéreo (misma información en ambos canales) y los cataloga como 'mono' y no como 'stereo'.
3) Puede reordenar los archivos enumerándolos según la posición que elijamos, y puede catalogarlos dentro de diferentes categorías:
"01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"

- El ejecutable funciona únicamente en Windows, podrías compilar el archivo main.py para que te funcione en tu sistema operativo.
- Este programa no necesita instalarse, el ejecutable funciona de forma portable.
- Puede ser que algunos antivirus detecten el ejecutable de este programa como Malware. Ésto es un falso positivo, no te preocupes, puedes revisar el código o compilarlo por tu cuenta si no te fías.
- IMPORTANTE: necesitas colocar la carpeta "ffmpeg" en el directorio raiz C:/ de tu ordenador para que el programa pueda detectar los archivos mono y stereo. Si el programa no encuentra esta carpeta esta funcionalidad no funcionará (el resto de funcionalidades seguirán funcionando).
- Los archivos deben estar en formato WAV.
- En el cuadro de reordenación de los archivos es importante que las carpetas mantengan el orden preestablecido.
- No es necesario u obligatorio categorizar los archivos, si quedan por encima de las categorías se enumerarán igualmente pero no se moverán a una carpeta.
- Si el proyecto no tiene archivos temporales (de los que comienzan con un punto) la opción de eliminarlos no aparece.
- Si los archivos ya están identificados como (mono) o (stereo) la opción de analizar los archivos no aparece.
- Si la carpeta seleccionada no tiene archivos WAV (solo aparecen carpetas) la opción de reordenar los archivos no aparece.
- Si tienes un proyecto que ya está categorizado, puedes indicar para que el programa entre en alguna categoría (a su carpeta) y reordenar igualmente los archivos (sin necesidad de categorizarlos).  
