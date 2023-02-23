'''题目
在命令行窗口运行；
程序运行时，会提示输入水印的文字，以及水印文字大小，透明度和位置，文字大小默认值为20，透明度默认为50%，位置默认为右下角。使用数字1-9分别代表左上、中上、右上、中左、正中、中右、下左、下中、下右；
程序会给当前目录下的images目录中所有png文件增加水印，并保存到watermark目录中。
'''

import os, sys, getopt
from PIL import Image, ImageDraw, ImageFont

# 汉字算2个长度，英文或数字算1个
def str_len(txt):
    length = 0
    for ch in txt:
        length += 2 if len(ch.encode('utf-8')) > 2 else 1

    return length

# 截取不大于某长度（汉字算2个，英文或数字算1个）的字符串
def sub_str(txt, max_len):
    result = ''
    length = 0
    for ch in txt:
        length += 2 if len(ch.encode('utf-8')) > 2 else 1
        if 10 >= length:
            result += ch
        else:
            break
    return result


# 判断文件是否为图片（可以加水印操作）
def isImage(file_name):
    if os.path.isfile(file_name):
        name, ext = os.path.splitext(file_name)
        # 根据后缀名判断
        if ext.lower() in ['.jpg', '.jpeg', '.png']:
            return True

    return False

# 获取参数
def get_args():
    argv = sys.argv[1:]
    args, others = getopt.getopt(argv, 'f:d:o:h', ['file=', 'directory=', 'output=', 'help'])

    is_help     = False
    input_file  = ''
    input_dir   = ''
    output_dir  = 'watermark' # 默认当前目录下的watermark

    for opt, arg in args:
        if opt in ('-h', '--help'):
            is_help = True
        elif opt in ('-f', '--file'):
            input_file = arg
        elif opt in ('-d', '--directory'):
            input_dir = arg
        elif opt in ('-o', '--output'):
            output_dir = arg if 0 < len(arg) else output_dir

    return is_help, input_file, input_dir, output_dir

# 加水印
def add_watermark(file, txt, size, alpha, pos):


# 主程序
if __name__ == '__main__':
    is_help, input_file, input_dir, output_dir = get_args()

    # 如果有help参数就只打印说明
    if is_help:
        print('给图片添加水印。')
        print('通过[-f|--file]指定文件，或者[-d|--directory]指定文件夹下的所有图片文件')
        print('通过[-o|--output]指定输出目录')
        exit()

    # 把制定文件和文件夹全部load进来，使用set避免重复
    files = set()

    if isImage(input_file):
        files.add(os.path.abspath(input_file))

    if os.path.isdir(input_dir):
        for file in os.listdir(input_dir):
            file = input_dir + '/' + file
            if isImage(file):
                files.add(os.path.abspath(file))

    try:
        if 0 < len(files):
            # 缺省为空
            watermark_text = ''
            while 0 >= len(watermark_text):
                print('输入水印文字（不超过5个中文字或10个英文或数字，超出部分自动截取）：', end='')
                watermark_text  = sub_str(input(), 10)
            print(f'水印文字：{watermark_text}')

            # 默认透明度50%
            watermark_alpha = 0.5
            print()
            print('输入水印透明度（0.01到1.00的数字，1为完全不透明），使用默认值直接输入回车（默认50%）：', end='')
            try:
                alpha_num = float(input())
                watermark_alpha = alpha_num if 0.01<=alpha_num<=1.0 else watermark_alpha
            except ValueError:
                pass
            print(f'水印透明度：{watermark_alpha:.2f}')

            # 默认位置 9（右下）
            watermark_pos   = 9
            print()
            print('''水印位置如图：
    |---|---|---|
    | 1 | 2 | 3 |
    |---|---|---|
    | 4 | 5 | 6 |
    |---|---|---|
    | 7 | 8 | 9 |
    |---|---|---|''')
            print('输入水印位置（1-9），使用默认值直接输入回车（默认9，右下）：', end='')
            try:
                pos_num = int(input())
                watermark_pos = pos_num if 1<=pos_num<=9 else watermark_pos
            except ValueError:
                pass
            print(f'水印位置：{watermark_pos}')

            # 默认字号 20
            watermark_size  = 20
            print()
            print('输入水印字号（10-30），使用默认值直接输入回车（默认20）：', end='')
            try:
                size_num = int(input())
                watermark_size = size_num if 10<=size_num<=30 else watermark_size
            except ValueError:
                pass
            print(f'水印字号：{watermark_size}')

            # 如果没有output文件夹，就创建一个
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
                print('Create output director:', output_dir)

            for file in files:
                print(file)
                with Image.open(file).convert('RGBA') as base:
                    pass
        else:
            print('未找到文件')

    except ValueError:
        pass

