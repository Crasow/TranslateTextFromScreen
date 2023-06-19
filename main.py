import keyboard
from PIL import Image
import pytesseract
import pyautogui
from PIL import ImageGrab
from pynput.mouse import Listener

pytesseract.pytesseract.tesseract_cmd = r'E:\Progs\PyTesseract\tesseract.exe'
target_key = 'o'
xy_coord = []
stop_waiting = False

def get_cursor_position():
    x, y = pyautogui.position()
    print(x, y)
    return x, y


def capture_screen_region():
    # Capture the screen region
    screenshot = ImageGrab.grab(bbox=(xy_coord[0][0], xy_coord[0][1], xy_coord[1][0], xy_coord[1][1]))

    # Save the captured image to a file
    screenshot.save("screenshot.png")


def recognize_txt(path_to_img):
    image = Image.open(path_to_img)
    return pytesseract.image_to_string(image)


def on_click(x, y, button, pressed):
    print(f"I get your lmb click on {x} and {y} coords")
    if button == button.left and pressed:
        xy_coord.append([x, y])
        if len(xy_coord) >= 2:
            print(f"You pressed lmb {len(xy_coord)} times already and i`ll try to stop listener")
            # Stop the listener once xy_coord has more than two elements
            return False


def on_key_press(event):
    print("You pressed the button and i will check what is it")
    if event.name == 'o':
        with Listener(on_click=on_click) as listener:
            print(f"Listener status before is {listener.is_alive()}")
            listener.join()
            print(f"Listener status after is {listener.is_alive()}")
        print("Out of Listener func")


def wait_for_key_press():
    # Register the key press event handler
    keyboard.on_press(on_key_press)

    keyboard.wait('o')
    print('you pressed O and prog go further')

    # Unregister the key press event handler
    keyboard.unhook_all()


if __name__ == '__main__':
    # keyboard.wait(target_key)
    while True:
        print('loop step')
        wait_for_key_press()
        if len(xy_coord) == 2:
            capture_screen_region()
            print(recognize_txt('screenshot.png'))
