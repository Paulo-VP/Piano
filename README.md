# Practicador de Piano - Prototipo

Este proyecto es un prototipo en desarrollo diseñado para interactuar con dispositivos MIDI y ofrecer diversas herramientas de práctica musical. Actualmente, la única funcionalidad habilitada es la práctica de acordes. El proyecto utiliza `Tkinter` para la interfaz gráfica, `mido` para la interacción con dispositivos MIDI, y otras bibliotecas para el manejo de acordes y escalas.

## Funcionalidades Implementadas

### 1. Práctica de Acordes
Permite al usuario:

- Seleccionar notas fundamentales y tipos de acordes.
- Generar acordes aleatorios para practicar.
- Validar si las notas tocadas en el piano MIDI coinciden con el acorde esperado.

### 2. Interfaz Gráfica del Piano
- Representa las teclas de un piano estándar de 88 teclas.
- Las teclas cambian de color al ser presionadas o liberadas, según la señal MIDI.

### 3. Detección de Entradas MIDI
- Detecta notas tocadas y las valida en tiempo real para la funcionalidad de práctica de acordes.

## Advertencias Importantes

### Estado del Proyecto
Este software está en una etapa inicial de desarrollo. Las funcionalidades adicionales (práctica de escalas, partituras y modo libre) aún no están implementadas.

### Finalización del Thread MIDI
**Muy importante:** El hilo que escucha las señales MIDI (`escucharPiano`) no se detiene automáticamente al cerrar la ventana principal. Para finalizar el programa completamente, debes cerrar el hilo manualmente:

- **En Windows:** Usa el Administrador de Tareas para finalizar el proceso.
- **En Linux:** Ejecuta el comando `kill` seguido del PID del proceso (puedes usar `ps` para encontrarlo).

## Requisitos

- **Python** 3.8 o superior.
- Bibliotecas necesarias: 
  - `tkinter`
  - `mido`
  - `threading`
  - `random`
  - `pychord`
  - `Pillow`

Para instalar las dependencias, ejecuta:

```bash
pip install -r requirements.txt
```

## Cómo Usar

1. **Conectar un dispositivo MIDI**
   - Conecta tu dispositivo MIDI al computador.
   - El programa detectará automáticamente los dispositivos MIDI disponibles. Selecciona uno al inicio para comenzar a interactuar con el piano virtual.

2. **Iniciar la práctica de acordes**
   - Usa los botones en la interfaz gráfica para elegir una nota fundamental y un tipo de acorde (mayor, menor, etc.).
   - El programa generará un acorde aleatorio para que practiques.
   - Toca las notas correspondientes en el piano MIDI y el sistema validará si las notas coinciden con el acorde esperado.

3. **Cerrar el programa**
   - Para cerrar el programa, simplemente cierra la ventana principal.
   - **Importante:** Asegúrate de finalizar manualmente el proceso del hilo MIDI para evitar que el programa siga corriendo en segundo plano.
     - **En Windows:** Usa el Administrador de Tareas para finalizar el proceso relacionado con el programa.
     - **En Linux:** Ejecuta el comando `kill` seguido del PID del proceso. Puedes usar `ps` para encontrar el PID.

