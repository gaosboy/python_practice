import sys, getopt

''' 测试输入输出
print('Input your number', end=': ')
no = input()
print('Number is', no)
print('%d add 10 is %d'%(int(no), int(no) + 10))
print(f'Number is {no}')
'''

'''测试参数
def main(argv):
    inf = ''
    outf = ''
    args, others = getopt.getopt(argv, 'hi:o:', ['input=', 'output=', 'help'])
    print(args)
    for opt, arg in args:
        if opt in ('-h', '--help'):
            print('This is a python code for practice.')
            print('-i | --input=, -o | --output, -h | --help')
        elif opt in ('-i', '--input'):
            inf = arg
        elif opt in ('-o', '--output'):
            outf = arg

    print('Input file:', inf)
    print('Output file:', outf)

if __name__ == '__main__':
    main(sys.argv[1:])
'''

''' for
for i in range(1, 100, 2):
    print(i)
'''

''' set
s=set([1, 2, 3])
ss={1, 3, 4}
print(s, ss)
print(s & ss)
print(s - ss)
'''

''' function
def person(name, age, *, job, city):
    print(f'name: {name}, age:{age}, job:{job}, city:{city}')

person('Gaosboy', 36, city='HZ', job='engineer')
'''

''' generator
print('max: ', end=' ')
arg1 = input()
m = int(arg1)
def numbers(m=100):
    i = 0
    while i<=m:
        yield i
        i = i + 1
    return 'DONE'

no=numbers(m)
print(next(no))
print(next(no))
print(next(no))
print(next(no))
print(next(no))
print(next(no))
print(next(no))
print(next(no))
print(next(no))
'''

''' random
'''
import random
print(random.randint(1,99))
a = 1
a += 1
print(a)

