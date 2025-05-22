import pyautogui
import time
import keyboard
import threading
import pytesseract
from PIL import ImageGrab, ImageOps

# Configura la ruta a tesseract.exe si es necesario
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Bandera global para detener el macro
stop_macro = False

# Coordenadas de la zona donde aparece el libro de encantamientos (ajusta a tu pantalla)
screen_width, screen_height = pyautogui.size()
BOOK_AREA = (1150, 580, 1400, 680)

# Nombre del encantamiento a buscar (ajusta según idioma y nombre exacto)
ENCANTAMIENTO_OBJETIVO = "Infinity"

def check_for_stop():
    global stop_macro 
    keyboard.wait('enter')
    stop_macro = True
    print("Macro detenido por el usuario.")

def colocar_atril():
    if stop_macro: return
    # Mantener Shift
    pyautogui.keyDown('shift')
    time.sleep(0.4)
    # Click derecho (colocar atril)
    pyautogui.click(button='right')
    # Soltar Shift
    pyautogui.keyUp('shift')
    time.sleep(2)
    # Saltar
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')
    # Esperar unas milésimas
    time.sleep(0.1)
    # Click derecho (abrir aldeano)
    pyautogui.click(button='right')
    # Esperar a que se abra el menú

def capturar_libro():
    img = ImageGrab.grab(bbox=BOOK_AREA)
    return img

def preprocesar_img(img):
    img = img.convert('L')  # Escala de grises
    img = ImageOps.invert(img)  # Invertir colores si el texto es claro sobre fondo oscuro
    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Binarización
    return img

def leer_encantamiento(img):
    texto = pytesseract.image_to_string(img, lang='eng')  # Usa 'spa' si tu juego está en español
    return texto

def revisar_encantamiento():
    global stop_macro
    if stop_macro: return
    # Definir el desplazamiento desde el centro
    offset_x, offset_y = -110, -110
    screen_width, screen_height = pyautogui.size()
    base_x, base_y = screen_width // 2 + offset_x, screen_height // 2 + offset_y
    pyautogui.moveTo(base_x, base_y)
    for _ in range(20):  # 2 segundos en pasos de 0.1s
        if stop_macro: return
        time.sleep(0.1)
    # Captura y OCR del primer tradeo
    img1 = capturar_libro()
    img1.save("tradeo1.png")  # Siempre sobrescribe el archivo anterior
    img1_proc = preprocesar_img(img1)
    img1_proc.save("tradeo1_proc.png")  # Guarda la imagen procesada para depuración
    texto1 = leer_encantamiento(img1_proc)
    print("Texto tradeo 1:", texto1)
    if ENCANTAMIENTO_OBJETIVO.lower() in texto1.lower():
        print(f"¡Encantamiento '{ENCANTAMIENTO_OBJETIVO}' encontrado en el primer tradeo! Deteniendo macro.")
        stop_macro = True
        pyautogui.press('esc')
        return
    # Mover el mouse 40 píxeles hacia abajo desde la posición anterior
    pyautogui.moveTo(base_x, base_y + 40)
    for _ in range(20):
        if stop_macro: return
        time.sleep(0.1)
    # Captura y OCR del segundo tradeo
    img2 = capturar_libro()
    img2.save("tradeo2.png")
    img2_proc = preprocesar_img(img2)
    img2_proc.save("tradeo2_proc.png")
    texto2 = leer_encantamiento(img2_proc)
    print("Texto tradeo 2:", texto2)
    if ENCANTAMIENTO_OBJETIVO.lower() in texto2.lower():
        print(f"¡Encantamiento '{ENCANTAMIENTO_OBJETIVO}' encontrado en el segundo tradeo! Deteniendo macro.")
        stop_macro = True
    pyautogui.press('esc')
2
def romper_atril():
    if stop_macro: return
    # Mantener click izquierdo (romper atril)
    pyautogui.keyDown('3')
    pyautogui.mouseDown(button='left')
    for _ in range(10):  # 1 segundo en pasos de 0.1s
        if stop_macro:
            pyautogui.mouseUp(button='left')
            return
        time.sleep(0.1)
    pyautogui.mouseUp(button='left')
    for _ in range(5):  # 0.5 segundos en pasos de 0.1s
        if stop_macro: return
        time.sleep(0.1)
    pyautogui.keyDown('2')

def main():
    global stop_macro
    time.sleep(5)  # Tiempo para que te dé tiempo de cambiar a Minecraft
    print("Macro iniciado. Presiona ENTER para detenerlo.")
    # Iniciar el hilo que escucha la tecla Enter
    threading.Thread(target=check_for_stop, daemon=True).start()
    while not stop_macro:
        colocar_atril()
        if stop_macro: break
        revisar_encantamiento()
        if stop_macro: break
        romper_atril()
        if stop_macro: break

if __name__ == "__main__":
    main()
