from src.utils.battle import *
from src.utils.environment import *
from src.utils.general import *
import time


#Total battles
BATTLES = 0

#Next pokemon to use if the current one faints
NEXT_AVAILABLE_PKMN = 1

#Primary move to use in battle
MOVE = 0


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
    
    pause_input(3)
    while(not is_character_visible()):
        pause_input(3)

    run_to(face='', direction='up', steps=4)
    hold_key('z', 5)



def exit_pokemon_centre():
    run_to(face='up', direction='down', steps=5)

    pause_input(3)
    while(not is_character_visible()):
        pause_input(3)

    run_to(face='down', direction='down', steps=3)
    run_to(face='down', direction='left', steps=4)
    run_to(face='left', direction='down', steps=6)
    run_to(face='down', direction='left', steps=11)
    run_to(face='left', direction='up', steps=8)
    run_to(face='up', direction='left', steps=22)
    run_to(face='left', direction='down', steps=6)
    run_to(face='down', direction='left', steps=6)
    run_to(face='left', direction='up', steps=2)



#START
pause_input(2)
focus_window()

#Start in Cerulean pokemon centre with character at desk facing nurse
#Screen size should be about 1280 x 960, disable overworld
exit_pokemon_centre()

while True:
    while is_character_visible():
        run_to(direction='left', steps=5)
        run_to(face='left', direction='right', steps=5)

    while not is_character_visible():
        is_character_stacked('right')
        if bool(in_battle()):
            BATTLES = BATTLES + 1

            while not is_character_visible():
                is_character_stacked('right')
                fight_button = in_battle()

                if is_pokemon_fainted():
                    switch_fainted_pokemon_out(NEXT_AVAILABLE_PKMN)
                    NEXT_AVAILABLE_PKMN = NEXT_AVAILABLE_PKMN + 1

                if bool(fight_button):
                    pyautogui.click(in_battle().x, in_battle().y)
                    select_move(MOVE)
                    pause_input(1)
                    check_pp(MOVE + 1)
    
    print('Fought ' + str(BATTLES) + ' battles so far...')

    while BATTLES % 10 == 0 and BATTLES > 0:
        p_time = time.time()
        return_delay = 10

        while time.time() - p_time < return_delay:
            run_to(direction='right', steps=5)
            if not is_character_visible():
                is_character_stacked('right')
                return_delay = return_delay + 3
                pyautogui.press('x')
                run()

        goto_pokemon_centre()
        NEXT_AVAILABLE_PKMN = 1
        exit_pokemon_centre()
        break
#END