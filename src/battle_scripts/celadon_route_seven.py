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
    bike_to(direction='down', steps=3)
    bike_to(face='down', direction='left', steps=5)
    bike_to(face='left', direction='up', steps=5)
    bike_to(face='up', direction='left', steps=18)
    bike_to(face='left', direction='up', steps=3)
    
    pause_input(3)
    while(not is_character_visible()):
        pause_input(3)

    bike_to(face='', direction='up', steps=4)
    hold_key('z', 5)



def exit_pokemon_centre():
    run_to(face='up', direction='down', steps=5)

    pause_input(3)
    while(not is_character_visible()):
        pause_input(3)

    use_key_item('f2')
    bike_to(face='down', direction='right', steps=18)
    bike_to(face='right', direction='down', steps=4)
    bike_to(face='down', direction='right', steps=4)



#START
pause_input(2)
focus_window()

exit_pokemon_centre()
goto_pokemon_centre()
exit_pokemon_centre()
goto_pokemon_centre()

#Start in Cerulean pokemon centre with character at desk facing nurse
#Screen size should be 1280 x 960, disable overworld
# exit_pokemon_centre()

# while True:
#     while is_character_visible():
#         bike_to(direction='left', steps=7)
#         bike_to(face='left', direction='right', steps=7)

#     while not is_character_visible():
#         is_character_stacked('right')
#         if bool(in_battle()):
#             BATTLES = BATTLES + 1

#             while not is_character_visible():
#                 is_character_stacked('right')
#                 fight_button = in_battle()

#                 if is_pokemon_fainted():
#                     switch_fainted_pokemon_out(NEXT_AVAILABLE_PKMN)
#                     NEXT_AVAILABLE_PKMN = NEXT_AVAILABLE_PKMN + 1

#                 if bool(fight_button):
#                     pyautogui.click(in_battle().x, in_battle().y)
#                     select_move(MOVE)
#                     pause_input(1)
#                     check_pp(MOVE + 1)
    
#     print('Fought ' + str(BATTLES) + ' battles so far...')

#     while BATTLES % 10 == 0 and BATTLES > 0:
#         p_time = time.time()
#         return_delay = 10

#         while time.time() - p_time < return_delay:
#             bike_to(direction='left', steps=5)
#             if not is_character_visible():
#                 is_character_stacked('left')
#                 return_delay = return_delay + 3
#                 pyautogui.press('x')
#                 run()

#         goto_pokemon_centre()
#         NEXT_AVAILABLE_PKMN = 1
#         exit_pokemon_centre()
#         break
#END