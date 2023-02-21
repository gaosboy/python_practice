''' 题目
直接在控制台使用命令行运行
程序运行之后倒计时1分钟之后结束
随机出100以内的2个整数加减乘除运算题目（除法确保能够除尽，但除数不能为0）
每出一道题目，由玩家给出答案，然后程序判断对错，接着出下一题，并且显示剩余时间
1分钟时间结束，显示总题数和正确率（正确率精确到小数点后2位），并将之前的题目和答案显示出来
'''
import time
import random

def get_rand_int(operator='+'):
    '''
    生成随机数，加法和减法可以生成100以内
    乘法和除法 要保证乘积（被除数）小于100
    '''
    a = random.randint(1, 99)
    b = random.randint(1, 99)
    if operator == '+':
        return a, b, a+b
    elif operator == '-':
        if a<b:
            a, b = b, a
        return a, b, a-b
    elif operator == '*':
        divisor = random.randint(1, 10)
        quotient = random.randint(1, 10)
        dividend = divisor * quotient
        return divisor, quotient, dividend
    elif operator == '/':
        divisor = random.randint(1, 10)
        quotient = random.randint(1, 10)
        dividend = divisor * quotient
        return dividend, divisor, quotient
    return 0, 0

if __name__ == '__main__':
    # 一局时间60秒
    maxtime = 10
    # 启动时间
    starttime = int(time.time())
    # 倒计时器
    countdown = 0
    # 总题目
    total = 0
    # 正确题目
    correct = 0
    # 题目列表
    questions = []

    while countdown < maxtime:
        print()
        print(f'本局剩余时间{maxtime - countdown}秒')

        # 出题
        op = random.choice(['+', '-', '*', '/'])
        a, b, r = get_rand_int(op)
        question = f'{a} {op} {b} = {r}'
        print(f'{a} {op} {b} = ', end='')

        total += 1 # 题目+1

        # 作答
        inputstr = input()
        if inputstr.isnumeric():
            result = int(inputstr)
        else:
            result  -1

        # 判断
        if result == r:
            # 正确
            correct += 1
            question += ' √'
            print('回答正确！')
        else:
            # 错误
            question += ' ×'
            print(f'答错了，正确答案是：{r}')

        questions.append(question)

        # 剩余时间
        countdown = int(time.time()) - starttime

    # 结束输出结果
    print()
    print(f'本局结束>> 整体耗时{countdown}秒')
    print(f'完成题目总数：{total}，答对：{correct}，准确率：{correct/total*100:.2f}%')
    print()
    for question in questions:
        print(question)

