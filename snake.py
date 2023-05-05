import cv2
import numpy
from random import randint

#################### function list #####################
def renderSnake(frame, snake) :
    for i, dot in enumerate(snake) :
        if i == 0 :
            cv2.circle(frame, dot, snakeSize - 5, 255, 5)
        else :
            cv2.circle(frame, dot, snakeSize - 1, 255, 1)

def renderApple(frame, apple) :
    appleSize = snakeSize
    cv2.circle(frame, apple, 1, (255,0,0), appleSize)

def growup(snake) :
    snake.append(snake[-1])
    return snake

# 初始化
title       = 'Snake'       # 标题
length      = 1000          # 场地边长

gameOver = False

snake       = [(100, 100)]  # 蛇的队列
snakeSize   = 10
speedLvl    = 0             # 0-9

apple       = (500, 500)    # 初始的苹果位置
hungry      = False         # 苹果被吃掉了

velocity    = snakeSize     # 一次爬一节
dx, dy      = 0, 0          # 方向，上：0, -1；下：0, 1；左：-1, 0；右：1, 0
vx, vy      = 0, 0          # x和y两个方向的速度，初始0，速度 * 方向 = 两个方向的速度

cv2.namedWindow(title)

# 再长大两节
growup(snake)
growup(snake)

# 初始化第一帧
frame = numpy.zeros((length, length), dtype = numpy.uint8) # 刷新场地

renderSnake(frame, snake)
renderApple(frame, apple)

cv2.imshow(title, frame)

while True :
    # 转向
    key = cv2.waitKey(100 - 10 * speedLvl) # 监听输入
    if key == 0 and abs(dy) == 0 : # 上
        ldx, ldy = dx, dy # 缓存上一次的方向
        dx, dy = 0, -1
    elif key == 1 and abs(dy) == 0 : # 下
        dx, dy = 0, 1
    elif key == 2 and abs(dx) == 0 : # 左 
        dx, dy = -1, 0
    elif key == 3 and abs(dx) == 0: # 右 
        dx, dy = 1, 0 
    elif key == ord('q') : # q 结束
        print('Quit')
        break

    # 计算爬行向量
    vx, vy = velocity * dx, velocity * dy
    if abs(vx) + abs(vy) <= 0 :
        continue

    # 下一帧
    for i in range(-1, -len(snake)-1, -1) :
        ii = len(snake) + i
        if ii > 0 :
            snake[ii] = snake[ii - 1] # 往前爬一节
        elif ii == 0 : # 头
            (x, y) = snake[ii]
            snake[ii] = (x + vx, y + vy)

    if x < 0 or x > length or y < 0 or y > length : # 撞墙了
        gameOver = True
    elif snake[ii] in snake[1:] : # 撞自己
        gameOver = True
    elif snake[ii] == apple : # 吃果了
        hungry = True
        growup(snake)

    # 渲染
    frame = numpy.zeros((length, length), dtype = numpy.uint8) # 刷新场地

    renderSnake(frame, snake)
    renderApple(frame, apple)
    cv2.putText(frame, f'>> Length: {len(snake)} | Speed Level: {speedLvl + 1}/10 <<', (10, 990), cv2.FONT_HERSHEY_DUPLEX, 1, 155)

    cv2.imshow(title, frame)

    # 处理状态
    if gameOver :
        break
    elif hungry :
        apple = (randint(1, 90) * 10, randint(1, 90) * 10)
        hungry = False
        speedLvl = len(snake) // 10
        if speedLvl > 9 :
            speedLvl = 9 

cv2.destroyAllWindows()

