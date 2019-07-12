import pyautogui
import time



def print_mouse_position():
    """Prints the current mouse position.

    Args:
        NONE
    
    Returns:
        NONE
    """
    print(pyautogui.position())



def focus_window():
    """Focus on the PKMNMMO window.

    Args:
        NONE

    Returns:
        NONE
    """
    pkmn_mmo = pyautogui.locateOnScreen('../assets/pkmn_mmo.PNG', grayscale=True, confidence=0.9)

    if pkmn_mmo != None:
        point = pyautogui.center(pkmn_mmo)
        pyautogui.click(point.x, point.y)
    else:
        print('Failed to focus on game window...')



def pause_input(seconds):
    """Pauses input for the specified number of seconds.

    Args:
        seconds - The number of seconds to pause for.

    Returns:
        NONE
    """
    print('Pausing input for ' + str(seconds) + ' seconds...')
    time.sleep(seconds)
    print('Resuming input...')



def hold_key(key, seconds):
    """Hold a key down for a certain amount of seconds.

    Args:
        key - The key to hold down.
        seconds = The amount of seconds to hold the key for.
    
    Returns:
        NONE
    """
    c_time = time.time()

    print('Holding ' + key + ' down...')
    while time.time() - c_time < seconds:
        pyautogui.keyDown(key)
    print('Releasing ' + key + '...')
    pyautogui.keyUp(key)