from utils.general import *

PP_USED = 1

# #Route one
# def goto_pokemon_centre():
#     move_character_to(face='', direction='up', steps=2)
#     move_character_to(face='up', direction='left', steps=11)
#     move_character_to(face='left', direction='up', steps=17)
#     move_character_to(face='up', direction='right', steps=4)
#     move_character_to(face='right', direction='up', steps=1)
#     pause_input(2)
#     move_character_to(face='up', direction='up', steps=4)
#     hold_key('z', 5)

# def exit_pokemon_centre():
#     move_character_to(face='up', direction='down', steps=5)
#     pause_input(2)
#     move_character_to(face='down', direction='down', steps=3)
#     pause_input(1)
#     move_character_to(face='down', direction='down', steps=2)
#     move_character_to(face='down', direction='left', steps=2)
#     move_character_to(face='left', direction='down', steps=11)
#     move_character_to(face='down', direction='right', steps=4)
#     move_character_to(face='right', direction='down', steps=2)

def goto_pokemon_centre():
    move_character_to(face='', direction='down', steps=2)
    move_character_to(face='', direction='right', steps=6)
    move_character_to(face='', direction='up', steps=6)
    move_character_to(face='', direction='right', steps=24)
    move_character_to(face='', direction='up', steps=2)
    move_character_to(face='', direction='right', steps=9)
    move_character_to(face='', direction='down', steps=1)
    move_character_to(face='', direction='right', steps=4)
    move_character_to(face='', direction='up', steps=1)
    pause_input(2)
    move_character_to(face='', direction='up', steps=4)
    hold_key('z', 5)

def exit_pokemon_centre():
    move_character_to(face='up', direction='down', steps=5)
    pause_input(2)
    move_character_to(face='', direction='down', steps=1)
    move_character_to(face='', direction='left', steps=4)
    move_character_to(face='', direction='up', steps=1)
    move_character_to(face='', direction='left', steps=9)
    move_character_to(face='', direction='down', steps=2)
    move_character_to(face='', direction='left', steps=24)
    move_character_to(face='', direction='down', steps=6)
    move_character_to(face='', direction='left', steps=6)
    move_character_to(face='', direction='up', steps=2)


pause_input(2)
focus_window()

walk_to(face='left', direction='left', steps=1)
# while True:

#     while is_character_visible():
#         move_character_to(face='', direction='left', steps=5)
#         move_character_to(face='right', direction='right', steps=5)

#     while not is_character_visible():
#         if bool(in_battle()):
#             pyautogui.click(in_battle().x, in_battle().y)
#             select_move(0)
#             PP_USED = PP_USED + 1
#             print('Used ' + str(PP_USED) + ' pp so far...')
#         else:
#             break

#     steps = 0
#     while PP_USED % 11 == 0:
#         move_character_to('', direction='right', steps=5)
        
#         if not is_character_visible():
#             pyautogui.press('x')
#             run()

#         steps = steps + 1
#         if steps % 7 == 0:
#             goto_pokemon_centre()
#             exit_pokemon_centre()
#             PP_USED = 1
#             break
