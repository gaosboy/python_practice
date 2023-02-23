'''题目
在命令行窗口运行；
程序运行时，会提示输入水印的文字，以及水印文字大小，透明度和位置，文字大小默认值为20，透明度默认为50%，位置默认为右下角。使用数字1-9分别代表左上、中上、右上、中左、正中、中右、下左、下中、下右；
程序会给当前目录下的images目录中所有png文件增加水印，并保存到watermark目录中。
'''

import os, sys, getopt
from PIL import Image, ImageDraw, ImageFont

##################### Function List #####################
# 获取字符串长度，汉字算2个长度，英文或数字算1个
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

# 转换绝对位置。根据底图大小，水印大小，九宫格位置计算出水印绝对位置
# bg_size 和 wm_size 是数组，表示w和h，pos_id从1-9
def watermark_position(bg_size, wm_rect, pos_id):
    # 留边 10px
    margin = 10
    # x y默认值 -1，表示异常
    x = -1
    y = -1

    # 取出size
    wm_size = (wm_rect[2], wm_rect[3])

    # 水印要在margin范围内
    if bg_size[0] > margin * 2 + wm_size[0] or bg_size[1] > margin * 2 + wm_size[1]:
        # 先算x
        if pos_id in [1, 4, 7]:
            x = margin
        elif pos_id in [2, 5, 8]:
            x = (bg_size[0] - wm_size[0]) / 2
        elif pos_id in [3, 6, 9]:
            x = bg_size[0] - margin - wm_size[0]
            pass

        # 再算y
        if pos_id in [1, 2, 3]:
            y = margin
        elif pos_id in [4, 5, 6]:
            y = (bg_size[1] - wm_size[0]) / 2
        elif pos_id in [7, 8, 9]:
            y = bg_size[1] - margin - wm_size[1]

    return (x, y)

# 构造水印
def watermark(bg_size, wm_text, wm_size, wm_alpha, pos_id):
    result = None

    try:
        # 透明画布
        wm = Image.new('RGBA', bg_size, (255, 255, 255, 0))
        # 字体 Verdana.ttf 字体在当前目录
        fnt = ImageFont.truetype('for_watermark.otf', wm_size)
        # 准备绘制文字
        draw = ImageDraw.Draw(wm)
        # 水印位置
        wm_pos = watermark_position(bg_size, draw.textbbox((0,0), wm_text, font=fnt), pos_id)
        # 如果水印位置出错（水印大于背景），就返回空
        if 0 < wm_pos[0] and 0 < wm_pos[1]:
            draw.text(wm_pos, wm_text, font=fnt, fill=(255, 255, 255, int(256 * wm_alpha)))
            result = wm
    except ValueError:
        pass

    return result

##################### Main Program #####################
if __name__ == '__main__':
    # 程序启动 读取参数
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

    # 确认输入文件没问题，开干！
    if 0 < len(files):
    # 一. 用户输入水印相关的各种参数
        # 1. 水印文案，缺省为空
        watermark_text = ''
        while 0 >= len(watermark_text):
            print('输入水印文字（不超过5个中文字或10个英文或数字，超出部分自动截取）：', end='')
            watermark_text  = sub_str(input(), 10)
        print(f'水印文字：{watermark_text}')

        # 2. 透明度，默认透明度50%
        watermark_alpha = 0.5
        print()
        print('输入水印透明度（0.01到1.00的数字，1为完全不透明），使用默认值直接输入回车（默认50%）：', end='')
        try:
            alpha_num = float(input())
            watermark_alpha = alpha_num if 0.01<=alpha_num<=1.0 else watermark_alpha
        except ValueError:
            pass
        print(f'水印透明度：{watermark_alpha:.2f}')

        # 3. 水印位置，默认位置 9（右下）
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

        # 4. 水印字号，默认字号 20
        watermark_size  = 20
        print()
        print('输入水印字号（10-30），使用默认值直接输入回车（默认20）：', end='')
        try:
            size_num = int(input())
            watermark_size = size_num if 10<=size_num<=30 else watermark_size
        except ValueError:
            pass
        print(f'水印字号：{watermark_size}')

    # 二. 开始添加水印
        print('---------------------------------')
        # 准备输出文件夹
        output_dir = output_dir if output_dir.endswith('/') else output_dir + '/'
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            print('Create output director:', output_dir)

        # 遍历输入的文件，逐一处理
        # 成功和失败的计数器
        succ_num = 0
        fail_num = 0
        for file in files:
            file_name = os.path.basename(file)
            print(f'开始处理 {file_name} ...', end='')
            try:
                with Image.open(file).convert('RGBA') as bg:
                    wm = watermark(bg.size, watermark_text, watermark_size, watermark_alpha, watermark_pos)
                    if None != wm:
                        output = Image.alpha_composite(bg, wm)
                        output.save(output_dir + file_name, 'PNG')
            except ValueError:
                pass

            if os.path.isfile(output_dir + file_name):
                succ_num += 1
                print(f' [√]')
            else:
                fail_num += 1
                print(f' [×]')

        print()
        print(f'共处理文件{succ_num + fail_num}个，成功处理{succ_num}个，失败{fail_num}个')
        print(f'全部文件已存入目录：{output_dir}')
    else:
        print('未找到输入文件')

