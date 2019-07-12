from src.utils.battle import *
from src.utils.environment import *
from src.utils.general import *
import time



BATTLES = 0



def goto_pokemon_centre():
    run_to(direction='down', steps=2)
    run_to(face='down', direction='right', steps=6)
    run_to(face='right', direction='up', steps=6)
    run_to(face='up', direction='right', steps=22)
    run_to(face='right', direction='down', steps=8)
    run_to(face='down', direction='right', steps=11)
    run_to(face='right', direction='up', steps=6)
    run_to(face='down', direction='right', steps=4)
    run_to(face='right', direction='up', steps=4)
    
    while(not is_character_visible()):
        pause_input(1)

    run_to(face='', direction='up', steps=4)
    hold_key('z', 5)



def exit_pokemon_centre():
    run_to(face='up', direction='down', steps=5)

    while(not is_character_visible()):
        pause_input(1)

    run_to(face='down', direction='down', steps=3)
    run_to(face='down', direction='left', steps=4)
    run_to(face='left', direction='down', steps=6)
    run_to(face='down', direction='left', steps=11)
    run_to(face='left', direction='up', steps=8)
    run_to(face='up', direction='left', steps=22)
    run_to(face='left', direction='down', steps=6)
    run_to(face='down', direction='left', steps=6)
    run_to(face='left', direction='up', steps=2)



pause_input(2)
focus_window()

#Start in Cerulean pokemon centre with character at desk facing nurse
exit_pokemon_centre()

while True:
    while is_character_visible():
        run_to(direction='left', steps=5)
        run_to(face='left', direction='right', steps=5)

    while not is_character_visible():
        if bool(in_battle()):
            BATTLES = BATTLES + 1

            while not is_character_visible():
                fight_button = in_battle()

                if bool(fight_button):
                    pyautogui.click(in_battle().x, in_battle().y)
                    select_move(0)
    
    print('Fought ' + str(BATTLES) + ' so far...')

    while BATTLES % 5 == 0 and BATTLES > 0:
        p_time = time.time()

        while time.time() - p_time < 10:
            run_to(direction='right', steps=5)
            if not is_character_visible():
                pyautogui.press('x')
                run()

        goto_pokemon_centre()
        exit_pokemon_centre()
        break

    # steps = 0
    # while PP_USED % 11 == 0:
    #     run_to(direction='right', steps=5)
        
    #     if not is_character_visible():
    #         pyautogui.press('x')
    #         run()

    #     steps = steps + 1
    #     if steps % 7 == 0:
    #         goto_pokemon_centre()
    #         exit_pokemon_centre()
    #         PP_USED = 1
    #         break