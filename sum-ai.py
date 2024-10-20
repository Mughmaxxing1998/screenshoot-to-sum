import os
import tkinter as tk
from PIL import ImageGrab, Image
import keyboard
import time
import google.generativeai as gemini
import pytesseract as pts
from colorama import Fore

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

gemini.configure(api_key="Your API key")
model = gemini.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config, safety_settings=safety_settings)

def take_region_screenshot(x1, y1, x2, y2):
    global FileName
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    if not os.path.exists('pic'):
        os.makedirs('pic')
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    FileName = f"pic/screenshot_{timestamp}.png"
    try:
        screenshot.save(FileName)
        print(f"Screenshot saved as {FileName}")
        generate()
    except Exception as e:
        print(f"Failed to save screenshot: {e}")

def select_region():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes('-alpha', 0.3)
    root.config(cursor="cross")

    start_x, start_y = 0, 0
    rect = None

    def on_click(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    def on_drag(event):
        nonlocal rect
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline='red', width=2)

    def on_release(event):
        root.destroy()
        take_region_screenshot(start_x, start_y, event.x, event.y)

    def on_esc(event):
        print("Screenshot canceled.")
        root.destroy()

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.bind("<Escape>", on_esc)
    root.focus_force()
    root.mainloop()

def generate():
    try:
        img = Image.open(FileName)
        Ai_Input = pts.image_to_string(img)
        if Ai_Input.strip() == "":
            print("No text detected in the image.")
            return
        response = model.generate_content(f"summarize this text (use bullet points if you can and dont use bold or any font effects): {Ai_Input}")
        print(Fore.YELLOW+f"\n\n\n{response.text}"+Fore.WHITE)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Press 'Ctrl + Alt + R' to select a region for screenshot.")
    while True:
        try:
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('alt') and keyboard.is_pressed('r'):
                print("Selecting region...")
                select_region()
                time.sleep(0.5)
        except:
            pass


main()
