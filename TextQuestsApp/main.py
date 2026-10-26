import pygame
import sys
from class_play import Text, Button, TextField, Quest, Scene, Choice, Theme, Variable, Condition, Image
from random import randint, shuffle
from quests import quests

pygame.init()

S_WIDTH = 1200
S_HEIGHT = 800

green1 = (250, 250, 250)
dark_blue = (0, 5, 30)

screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Text-quests")
clock = pygame.time.Clock()

my_quest = quests[0]

game_text = Text(600, 50, 64, None, (255, 255, 250), "Захоплюючі текстові квести", True)
choose_quest_btn = Button(300, 400, 600, 200, 48, None, green1, dark_blue, "Переглянути доступні квести", True)
caption = Text(600, 20, 64, None, (255, 255, 250), my_quest.name, False)
description = TextField(100, 80, 1000, 450, 32, None, green1, (0,0,0), my_quest.description, False)
start_btn = Button(400, 600, 400, 100, 24, None, my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color, "Розпочати гру", False)
text = TextField(100, 80, 1000, 440, 28, None, my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color, my_quest.current_scene.text, False)
btn_start_again = Button(100, 600, 400, 100, 24, None, my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color, "Спробувати знову", False)
btn_return_to_menu = Button(700, 600, 400, 100, 24, None, my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color, "Повернутись до меню", False)
states = {"start":[game_text, choose_quest_btn], "review_avaiable_quests":[], "quest_details":[caption, description, start_btn], "doing_quest":[caption, text, btn_start_again, btn_return_to_menu]}
current_state = "start"
q_btn_y = 50
for q in quests:
    
    btn = Button(400, q_btn_y, 400, 100, 24, None, green1, dark_blue, q.name, True)
    states["review_avaiable_quests"].append(btn)
    q_btn_y += 150

choices = []
def a():
    choices.clear()

    choice_list = []
    for c in my_quest.current_scene.choices:
        if c.check_availability(my_quest):
            choice_list.append(c)

    shuffle(choice_list)
    positions = []
    if len(choice_list) <= 2:
        positions = [
            (100, 630),
            (700, 630),
        ]
    
    elif len(choice_list) <= 4:
            positions = [
                        (100, 550),
                        (100, 680),
                        (700, 550),
                        (700, 680),
                    ]

    elif len(choice_list) <= 6:
                positions = [
                            (50, 550),
                            (50, 680),
                            (450, 550),
                            (450, 680),
                            (850, 550),
                            (850, 680),
                        ]
    elif len(choice_list) <= 8:
                    positions = [
                                (0, 550),
                                (0, 680),
                                (300, 550),
                                (300, 680),
                                (600, 550),
                                (600, 680),
                                (900, 550),
                                (900, 680),
                            ]
    
    for choice, (x,y) in zip(choice_list, positions):
        btn = Button(x, y, 400, 100, 24, None, my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color, choice.name, False)
        choices.append((btn, choice))
                          
a()


run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if start_btn.is_clicked(e) and current_state == "quest_details":
            for v in my_quest.variables:
                v.value = v.initial_v
            start_btn.visible = False
            text.visible = True
            description.visible = True
            caption.visible = True
            caption.fcolor = my_quest.current_scene.theme.fill_color
            btn_start_again.visible = False
            btn_return_to_menu.visible = False
            current_state = "doing_quest" 
            
            
            for btn, c in choices:
                btn.visible = True
            break
        if choose_quest_btn.is_clicked(e) and current_state == "start":
            current_state="review_avaiable_quests"
            for i in states[current_state]:
                i.visible = True
            break
        

        elif btn_start_again.is_clicked(e) and current_state == "doing_quest":
            for v in my_quest.variables:
                v.value = v.initial_v
            text.visible = True
            caption.visible = True
            my_quest.current_scene = my_quest.scenes[my_quest.first_scene_index]
            caption.fcolor = my_quest.current_scene.theme.fill_color
            btn_start_again.visible = False
            btn_return_to_menu.visible = False
            text.change_text(my_quest.current_scene.text)
            a()
            for btn, c in choices:
                btn.visible = True
            text.update(my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color)
            break

        elif btn_return_to_menu.is_clicked(e) and current_state == "doing_quest":
                    text.visible = False
                    caption.visible = False
                    btn_start_again.visible = False
                    btn_return_to_menu.visible = False
                    current_state = "start"
        if current_state == "review_avaiable_quests":
            for i in states[current_state]:
                if type(i) == Button:
                    if i.is_clicked(e):
                        for q in quests:
                            if i.text == q.name:
                                my_quest = q
                                current_state = "quest_details" 
                                caption.visible = True
                                caption.text = my_quest.name
                                caption.fcolor = my_quest.current_scene.theme.fill_color
                                description.visible = True
                                start_btn.visible = True
                                start_btn.update(my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color)
                                description.change_text(my_quest.description)
                                description.update(my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color)
                                my_quest.current_scene = my_quest.scenes[my_quest.first_scene_index]
                                btn_start_again.visible = False
                                btn_return_to_menu.visible = False
                                text.change_text(my_quest.current_scene.text)
                                      
                                a()
                                for btn, c in choices:
                                    btn.visible = True
                                text.update(my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color)
        if current_state == "doing_quest":
            description.visible = False
            start_btn.visible = False
            text.visible = True
            caption.visible = True
            selected_choice = None
            for btn, c in choices:
                if btn.is_clicked(e):
                    my_quest.current_scene = c.get_scene(my_quest)
                    text.change_text(my_quest.current_scene.text)
                    my_quest.current_scene.change(my_quest)
                    caption.fcolor = my_quest.current_scene.theme.fill_color
                    
                    for i in my_quest.variables:
                        print(i)

                    selected_choice = c
                    
                    if not my_quest.current_scene.choices:
                        btn_start_again.visible = True
                        btn_start_again.update(my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color)
                        btn_return_to_menu.visible = True
                        btn_return_to_menu.update(my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color)
                    
                    text.update(my_quest.current_scene.theme.fill_color, my_quest.current_scene.theme.font_color)
                    break

            if selected_choice is not None:
                a()
                for btn, c in choices:
                    btn.visible = True
    
    keys = pygame.key.get_pressed()

    if current_state == "start" or current_state == "review_avaiable_quests":
        screen.fill((100, 0, 180))
    else:
        if my_quest.current_scene.theme.image:
            my_quest.current_scene.theme.image.draw(screen)
        else:
            screen.fill(my_quest.current_scene.theme.background_color)
    for i in states[current_state]:
        if type(i) == TextField:
            i.draw(keys, screen)
        else:
            i.draw(screen)
    if current_state == "doing_quest":
        for btn, c in choices:
            btn.draw(screen)
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()