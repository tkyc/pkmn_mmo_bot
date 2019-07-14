from src.utils.battle import in_battle
import pyautogui
import time

#TESTING
def is_character_stacked(direction):
    battle_chatbox = pyautogui.locateOnScreen('../../assets/battle_chatbox.PNG', confidence=0.85)

    if not is_character_visible():
        if not bool(in_battle()) and battle_chatbox == None:
            print('Character sprite is stacked...')
            run_to(direction=direction, steps=2)
            return True
    return False



def is_character_visible():
    """Determines if your character is currently visible on screen.

    Args:
        NONE

    Returns:
        boolean - True if visible, otherwise false.
    """
    character_f = pyautogui.locateOnScreen('../../assets/character.PNG', confidence=0.65)
    character_b = pyautogui.locateOnScreen('../../assets/character_b.PNG', confidence=0.65)
    character_l = pyautogui.locateOnScreen('../../assets/character_l.PNG', confidence=0.65)
    character_r = pyautogui.locateOnScreen('../../assets/character_r.PNG', confidence=0.65)

    print('Checking if character is visible...')
    if character_f == None and character_b == None and character_l == None and character_r == None:
        print('Character is not visible.')
        return False

    print('Character is visible.')
    return True



#TESTING
def bike_to(direction, steps, face=None):
    """Bike in the specified cardinal direction.

    Args:
        face - The direction the character is currently facing.
        direction - The direction the character should bike in.
        steps - The number of steps to bike.

    Returns:
        NONE
    """    
    def take_step(direction_):
        p_time = time.time()

        while time.time() - p_time < 0.014:
            pyautogui.keyDown(direction_)
        pyautogui.keyUp(direction_)

    if face != direction:
        pyautogui.keyDown(direction)
        pyautogui.keyUp(direction)

    for i in range(steps):
        take_step(direction)



def run_to(direction, steps, face=None):
    """Run in the specified cardinal direction.

    Args:
        face - The direction the character is currently facing.
        direction - The direction the character should run in.
        steps - The number of steps to run.
    
    Returns:
        NONE
    """
    pyautogui.keyDown('x')
    walk_to(direction, steps, face)
    pyautogui.keyUp('x')



def walk_to(direction, steps, face=None):
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