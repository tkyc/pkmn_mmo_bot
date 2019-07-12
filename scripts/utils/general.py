import pyautogui
import time

#Seconds for walking one step
WALKING_STEP_MULTIPLIER = 0.200

#Seconds for running one step
RUNNING_STEP_MULTIPLIER = 6 / 1000


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



def is_character_visible():
    """Determines if your character is currently visible on screen.

    Args:
        NONE

    Returns:
        boolean - True if visible, otherwise false.
    """
    character_f = pyautogui.locateOnScreen('../assets/character.PNG', confidence=0.65)
    character_b = pyautogui.locateOnScreen('../assets/character_b.PNG', confidence=0.65)
    character_l = pyautogui.locateOnScreen('../assets/character_l.PNG', confidence=0.65)
    character_r = pyautogui.locateOnScreen('../assets/character_r.PNG', confidence=0.65)

    print('Checking if character is visible...')
    if character_f == None and character_b == None and character_l == None and character_r == None:
        print('Character is not visible.')
        return False

    print('Character is visible.')
    return True



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



def run_to(face, direction, steps):
    """Run in the specified cardinal direction.

    Args:
        face - The direction the character is currently facing.
        direction - The direction the character should run in.
        steps - The number of steps to run.
    
    Returns:
        NONE
    """
    p_time = time.time()
    pyautogui.keyDown('x')

    def take_step(direction_):
        pyautogui.keyDown(direction)
        pyautogui.keyUp(direction)
    
    #If not facing the intended direction, make a correction.
    if face != direction:
        pyautogui.keyDown(direction)
        pyautogui.keyUp(direction)

    for i in range(steps):
        take_step(direction)
    pyautogui.keyUp('x')



def walk_to(face, direction, steps):
    """Moves character in the specified cardinal direction.
       The expected number of steps work only for walking.

    Args:
        face - The direction the character is currently facing.
        direction - The direction the character should move in. One of the following: up, down, left, right.
        steps - The number of steps to take in the specified direction.
    
    Returns:
        NONE
    """
    def take_step(direction_):
        pyautogui.keyDown(direction_)
        pyautogui.keyUp(direction_)
    
    #If not facing the intended direction, make a correction.
    if face != direction:
        pyautogui.keyDown(direction)
        pyautogui.keyUp(direction)

    for i in range(steps):
        take_step(direction)



def in_battle():
    """Determines if a pokemon battle is occurring by checking for the fight button.

    Args:
        NONE

    Returns:
        (x, y) - The fight button x and y coordinates as a tuple. Otherwise returns None.
    """
    fight_button = pyautogui.locateOnScreen('../assets/fight.PNG', confidence=0.85)
    
    if fight_button == None:
        return None

    return pyautogui.center(fight_button)



def run():
    """Run away from a wild pokemon encounter.

    Args:
        NONE
    
    Returns:
        (x, y) - The run button x and y coordinates as a tuple. Otherwise returns None.
    """
    run_button = pyautogui.locateOnScreen('../assets/run.PNG', confidence=0.85)

    if run_button != None:
        point = pyautogui.center(run_button)
        pyautogui.click(point.x, point.y)
        print('Ran away from battle!')



def select_move(move):
    """Select the pokemon's battle move.

    Args:
        move - One of the following: 0, 1, 2, 3.
    
    Returns:
        NONE
    """
    if move == 0:
        pyautogui.press('left')
        pyautogui.press('up')
    
    if move == 1:
        pyautogui.press('right')
        pyautogui.press('up')

    if move == 2:
        pyautogui.press('left')
        pyautogui.press('down')
    
    if move == 3:
        pyautogui.press('right')
        pyautogui.press('down')
    
    pyautogui.press('z')
    print("Your pokemon used move: " + str(move) + '.')



def cancel_learning_move():
    """Give up on learning new move on level up.

    Args:
        NONE

    Return:
        boolean - True on successful cancellation, otherwise false.
    """
    new_move = pyautogui.locateOnScreen('../assets/new_move.PNG', confidence=0.9)

    if new_move != None:
        cancel_button = pyautogui.locateOnScreen('../assets/cancel.PNG', confidence=0.9)

        if cancel_button != None:
            cancel_point = pyautogui.center(cancel_button)
            pyautogui.click(cancel_point.x, cancel_point.y)
            pause_input(2)
            yes_button = pyautogui.locateOnScreen('../assets/yes.PNG', confidence=0.9)
            point = pyautogui.center(yes_button)
            pyautogui.click(point.x, point.y)
        
        return True

    return False