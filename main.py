import pyautogui
import time
import keyboard
import threading
import pytesseract
from PIL import ImageGrab, ImageOps

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

stop_macro = False

screen_width, screen_height = pyautogui.size()
BOOK_AREA_FIRST = (1190, 580, 1450, 630)
BOOK_AREA_SECOND = (1190, 620, 1450, 670)

ENCANTAMIENTO_OBJETIVO = "Infinity"

def check_for_stop():
    global stop_macro 
    keyboard.wait('enter')
    stop_macro = True
    print("Macro detenido por el usuario.")

def colocar_atril():
    if stop_macro: return
    pyautogui.keyDown('shift')
    for _ in range(4):
        if stop_macro: return
        time.sleep(0.1)
    pyautogui.click(button='right')
    pyautogui.keyUp('shift')
    for _ in range(20):
        if stop_macro: return
        time.sleep(0.1)
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')
    if stop_macro: return
    time.sleep(0.1)
    if stop_macro: return
    pyautogui.click(button='right')
    if stop_macro: return

def capturar_libro(bbox):
    img = ImageGrab.grab(bbox)
    return img

def preprocesar_img(img):
    img = img.convert('L')
    img = ImageOps.invert(img)
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    return img

def leer_encantamiento(img):
    texto = pytesseract.image_to_string(img, lang='eng')
    return texto

def revisar_encantamiento():
    global stop_macro
    if stop_macro: return
    offset_x, offset_y = -110, -110
    screen_width, screen_height = pyautogui.size()
    base_x, base_y = screen_width // 2 + offset_x, screen_height // 2 + offset_y
    pyautogui.moveTo(base_x, base_y)
    img1 = capturar_libro(BOOK_AREA_FIRST)
    img1.save("tradeo1.png")
    img1_proc = preprocesar_img(img1)
    img1_proc.save("tradeo1_proc.png")
    texto1 = leer_encantamiento(img1_proc)
    print(texto1)
    if ENCANTAMIENTO_OBJETIVO.lower() in texto1.lower():
        stop_macro = True
        pyautogui.press('esc')
        return
    pyautogui.moveTo(base_x, base_y + 40)
    img2 = capturar_libro(BOOK_AREA_SECOND)
    img2.save("tradeo2.png")
    img2_proc = preprocesar_img(img2)
    img2_proc.save("tradeo2_proc.png")
    texto2 = leer_encantamiento(img2_proc)
    print(texto2)
    if ENCANTAMIENTO_OBJETIVO.lower() in texto2.lower():
        stop_macro = True
    pyautogui.press('esc')

def romper_atril():
    if stop_macro: return
    pyautogui.keyDown('3')
    pyautogui.mouseDown(button='left')
    for _ in range(10):
        if stop_macro:
            pyautogui.mouseUp(button='left')
            return
        time.sleep(0.1)
    pyautogui.mouseUp(button='left')
    for _ in range(5):
        if stop_macro: return
        time.sleep(0.1)
    pyautogui.keyDown('2')

def main():
    global stop_macro
    for _ in range(50):
        if stop_macro: return
        time.sleep(0.1)
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
