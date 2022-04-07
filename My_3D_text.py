from colorama import init, AnsiToWin32 #https://pypi.org/project/colorama/
from contextlib import closing
from pynput import keyboard
from os import system
from time import sleep, time
import sys
import math
from random import randint
import codecs

#Округление до ближайшего целого
def my_round(num):
    if math.modf(num)[0] > 0.5:
        return math.ceil(num)
    else:
        return math.floor(num)

#Вводит на экран первой строкой информацию о текущих координатах
def print_info(X, Y, A):
    print('\033['+'0' +';'+'5' +'H'  + '\033[' + str(40) + 'm' + '    ')
    print('\033['+'0' +';'+'5' +'H'  + '\033[' + str(40) + 'm' + str(X)[:4])
    print('\033['+'0' +';'+'15' +'H'  + '\033[' + str(40) + 'm' + '    ')
    print('\033['+'0' +';'+'15' +'H'  + '\033[' + str(40) + 'm' + str(Y)[:4])
    print('\033['+'0' +';'+'25' +'H'  + '\033[' + str(40) + 'm' + '    ')
    print('\033['+'0' +';'+'25' +'H'  + '\033[' + str(40) + 'm' + str(A)[:4])


def ray_casting(da_map): #чтобы карты можно было разные проверять 
    global player_x 
    global player_y
    global player_a
    
    global X_max
    global Y_max
    global angle
    global depth
    
    for x in range (X_max):
        RayAngle = (player_a - angle/2) + (x /X_max) * angle
        
        DistanceToWall = 0
        HitWall = False
        
        eye_X = math.sin(RayAngle) #единичные вектора
        eye_Y = math.cos(RayAngle)

        while (not HitWall and DistanceToWall < depth):
            DistanceToWall += 0.1
            
            TestX = player_x + eye_X * DistanceToWall
            TestY = player_y + eye_Y * DistanceToWall

            if TestX < 0 or TestX >= len(da_map) or TestY < 0 or TestY >= len(da_map):
                HitWall = True
                DistanceToWall = depth

            else:
                if da_map[int(TestY)][int(TestX)] == '#':
                    HitWall = True
    #Ищем расстояние до потолка и пола
        Celling = int( Y_max / 2  - Y_max / DistanceToWall +3 )
        Floor = int(Y_max - Celling)

        

        if DistanceToWall <= depth/7:
            Shade = 9608 #█
        elif DistanceToWall <= depth/4:
            Shade = 9619 #▓
        elif DistanceToWall <= depth/3:
            Shade = 9618 #▒
        elif DistanceToWall <= depth:
            Shade = 9617 #░
        else:
            Shade = 32 # ' ' 
            
        for y in range(2, Y_max):
            if y > 17 or X_max -x > 16:
                
                if y < Celling:
                    if randint(0,100)==0:
                        
                        S = "'"
                    else:
                        S = ' '
                    print('\033['+str(y) +';'+str(X_max -x) +'H' + '\033[' + str(randint(31, 39)) + 'm' + '\033[' + str(44) + 'm' + S)
                    
                elif(y > Celling and y <= Floor) :
                    
                    n = 45
                    if Shade == 32:
                        n = 44
                    print('\033['+str(y) +';'+str(X_max -x) +'H' + '\033[' + str(36) + 'm' + '\033[' + str(n) + 'm'  + chr(Shade))
                else:
                    
                    depth_floor =  0.1   - (y- Y_max)/(Y_max/2)
                    if depth_floor< 0.25:
                        Shade = ord('#')
                    elif depth_floor < 0.5:
                        Shade = ord('x')
                    elif depth_floor < 0.75:
                        Shade = ord('.')
                    elif depth_floor < 0.9:
                        Shade = 160
                    bel = 42
                    el = 34
                    if Shade == 32:
                        bel = 44
                        Shade = 9617
                        el = 43
                    print('\033['+str(y) +';'+str(X_max -x) +'H'  + '\033[' + str(el) + 'm'+ '\033[' + str(bel) + 'm' + chr(Shade))
                    
                    
                    
#установка размера экрана в символах
global X_max
global Y_max
X_max = 120
Y_max = 30
system('mode con:cols='+ str(X_max)+' lines=' + str(Y_max))

#создаем карту по-дибильному из-за очень сейчас мешающейся оптимизации
map_ = []

map_ = map_ + [['#']*16]
#for i in range (14):
#    map_ = map_ + [['#'] + [' ']*14 + ['#']]
map_ = map_ + ['#              #']
map_ = map_ + ['########       #']
map_ = map_ + ['#              #']
map_ = map_ + ['#              #']
map_ = map_ + ['#           ####']
map_ = map_ + ['#          #   #']
map_ = map_ + ['#          #   #']
map_ = map_ + ['#          #   #']
map_ = map_ + ['#              #']
map_ = map_ + ['#     ##       #']
map_ = map_ + ['#     ##       #']
map_ = map_ + ['#              #']
map_ = map_ + ['#              #']
map_ = map_ + ['###            #']
map_ = map_ + [['#']*16]

#Ваще не помню, зачем это
init(wrap=False)
#Немного костылей от библиотеки 
stream = AnsiToWin32(sys.stderr).stream


#ставим персонажа
global player_x 
global player_y
global player_a
global angle
global depth
global player_sign
global of_sign
global index_sign
index_sign = 0
of_sign = [chr(709), 'L', chr(706), 'Г', chr(708), chr(741), chr(707), chr(745) ]


player_sign = chr(709)
angle = 3.14159/2 # угол обзора
depth = 7 #макс. дистанция обзора 

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
    global player_sign
    global of_sign
    global index_sign
    if key == keyboard.Key.up :
        if player_x+ math.sin(player_a) >= 0 and player_x+ math.sin(player_a) < len(map_) and  player_y+ math.cos(player_a) >= 0 and player_x+ math.cos(player_a)< len(map_):
            if map_[ my_round(player_y+ math.cos(player_a)) ][ my_round(player_x+ math.sin(player_a)) ] != '#':
                print('\033['+str(my_round(player_y)+2) +';'+str(my_round(player_x)+1) +'H'  + '\033[' + str(40) + 'm' + ' ')
                player_x += math.sin(player_a)
                player_y += math.cos(player_a)
                print('\033['+str(my_round(player_y)+2) +';'+str(my_round(player_x)+1) +'H'   + '\033[' + str(40) + 'm'  + '\033[' + str(33) + 'm' + player_sign)
        
                #Вывод на экран доп инфы
                print_info(player_x, player_y, player_a)
                
    if key == keyboard.Key.down :
        if player_x-math.sin(player_a) >= 0 and player_x- math.sin(player_a)< len(map_) and  player_y- math.cos(player_a) >= 0 and player_x- math.cos(player_a)< len(map_):
            if map_[my_round(player_y- math.cos(player_a))][my_round( player_x- math.sin(player_a))] != '#':
                print('\033['+str(my_round(player_y)+2) +';'+str(my_round(player_x)+1) +'H'  + '\033[' + str(40) + 'm' + ' ')
                player_x -= math.sin(player_a)
                player_y -= math.cos(player_a)
                print('\033['+str(my_round(player_y)+2) +';'+str(my_round(player_x)+1) +'H'  + '\033[' + str(40) + 'm'   + '\033[' + str(33) + 'm' + player_sign)
                
                #Вывод на экран доп инфы
                print_info(player_x, player_y, player_a)
        
    if key == keyboard.Key.left :
        player_a -= (45*math.pi)/180
        
        index_sign+= 1
        if index_sign >= len(of_sign):
            index_sign = 0
        player_sign = of_sign[index_sign]
        
        print('\033['+str(my_round(player_y)+2) +';'+str(my_round(player_x)+1) +'H'  + '\033[' + str(40) + 'm'   + '\033[' + str(33) + 'm' + player_sign)
        #Вывод на экран доп инфы
        print_info(player_x, player_y, player_a)

    if key == keyboard.Key.right :
        player_a += (45*math.pi)/180

        index_sign-= 1
        if index_sign < 0:
            index_sign = len(of_sign ) - 1 
        player_sign = of_sign[index_sign]

        print('\033['+str(my_round(player_y)+2) +';'+str(my_round(player_x)+1) +'H'  + '\033[' + str(40) + 'm'   + '\033[' + str(33) + 'm' + player_sign)
        #Вывод на экран доп инфы
        print_info(player_x, player_y, player_a)


            
def on_release(key):
    
    if key == keyboard.Key.esc:
        # Stop listener
        return False

last_time = time()

listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()
while True:
    
    ray_casting(map_)
    fps = 1/(time() - last_time)
    last_time = time()
    print('\033['+'0' +';'+'40' +'H' + '\033[' + str(randint(31, 39)) + 'm'  + '\033[' + str(40) + 'm' + '#FPS    ' + str(fps)[:5])
    

    
