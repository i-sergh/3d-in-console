from colorama import init, AnsiToWin32 #https://pypi.org/project/colorama/
from contextlib import closing
from pynput import keyboard
from os import system
from time import sleep
import sys





#установка размера экрана в символах
X_max = 140
Y_max = 30
system('mode con:cols='+ str(X_max)+' lines=' + str(Y_max))

#создаем карту по-дибильному из-за очень сейчас мешающейся оптимизации
map_ = []

map_ = map_ + [['#']*16]
for i in range (14):
    map_ = map_ + [['#'] + [' ']*14 + ['#']]
map_ = map_ + [['#']*16]


#Ваще не помню, зачем это
init(wrap=False)
#Немного костылей от библиотеки 
stream = AnsiToWin32(sys.stderr).stream


#ставим персонажа
global player_x 
global player_y
global player_a
player_x = 5
player_y = 5
player_a = 0 # Угол позиции игрока


print('x =     ; y =     ; a =     ;')
for i in range (len(map_)):
    for j in range(len(map_[i])):
        print(map_[i][j], end = '')
    print()

print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + '@')
print('\033['+'0' +';'+'5' +'H' + str(player_x))
print('\033['+'0' +';'+'15' +'H' + str(player_y))
print('\033['+'0' +';'+'25' +'H' + str(player_a))
def on_press(key):
    global player_x
    global player_y
    global player_a
    
    if key == keyboard.Key.up :
        if map_[player_y - 1][ player_x] != '#':
                print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + ' ') 
                player_y -= 1
                print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + '@')
                print('\033['+'0' +';'+'5' +'H' + '    ')
                print('\033['+'0' +';'+'5' +'H' + str(player_x))
                print('\033['+'0' +';'+'15' +'H' + '    ')
                print('\033['+'0' +';'+'15' +'H' + str(player_y))
                print('\033['+'0' +';'+'25' +'H' + '    ')
                print('\033['+'0' +';'+'25' +'H' + str(player_a))
                
    if key == keyboard.Key.down :
        if map_[player_y + 1][ player_x] != '#':
            print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + ' ') 
            player_y += 1
            print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + '@')
            print('\033['+'0' +';'+'5' +'H' + '    ')
            print('\033['+'0' +';'+'5' +'H' + str(player_x))
            print('\033['+'0' +';'+'15' +'H' + '    ')
            print('\033['+'0' +';'+'15' +'H' + str(player_y))
            print('\033['+'0' +';'+'25' +'H' + '    ')
            print('\033['+'0' +';'+'25' +'H' + str(player_a))

    if key == keyboard.Key.left :
        if map_[player_y ][ player_x-1] != '#':
            print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + ' ') 
            player_x -= 1
            print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + '@')
            print('\033['+'0' +';'+'5' +'H' + '    ')
            print('\033['+'0' +';'+'5' +'H' + str(player_x))
            print('\033['+'0' +';'+'15' +'H' + '    ')
            print('\033['+'0' +';'+'15' +'H' + str(player_y))
            print('\033['+'0' +';'+'25' +'H' + '    ')
            print('\033['+'0' +';'+'25' +'H' + str(player_a))        

    if key == keyboard.Key.right :
        if map_[player_y ][ player_x+1] != '#':
            print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + ' ') 
            player_x += 1
            print('\033['+str(player_y+2) +';'+str(player_x+1) +'H' + '@')
            print('\033['+'0' +';'+'5' +'H' + '    ')
            print('\033['+'0' +';'+'5' +'H' + str(player_x))
            print('\033['+'0' +';'+'15' +'H' + '    ')
            print('\033['+'0' +';'+'15' +'H' + str(player_y))
            print('\033['+'0' +';'+'25' +'H' + '    ')
            print('\033['+'0' +';'+'25' +'H' + str(player_a))
            
def on_release(key):
    
    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()


