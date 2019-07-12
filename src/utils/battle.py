import pyautogui



def in_battle():
    """Determines if a pokemon battle is occurring by checking for the fight button.

    Args:
        NONE

    Returns:
        (x, y) - The fight button x and y coordinates as a tuple. Otherwise returns None.
    """
    fight_button = pyautogui.locateOnScreen('../../assets/fight.PNG', confidence=0.85)
    
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
    run_button = pyautogui.locateOnScreen('../../assets/run.PNG', confidence=0.85)

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
    new_move = pyautogui.locateOnScreen('../../assets/new_move.PNG', confidence=0.9)

    if new_move != None:
        cancel_button = pyautogui.locateOnScreen('../../assets/cancel.PNG', confidence=0.9)

        if cancel_button != None:
            cancel_point = pyautogui.center(cancel_button)
            pyautogui.click(cancel_point.x, cancel_point.y)
            pause_input(2)
            yes_button = pyautogui.locateOnScreen('../../assets/yes.PNG', confidence=0.9)
            point = pyautogui.center(yes_button)
            pyautogui.click(point.x, point.y)
        
        return True

    return False