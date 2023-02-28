''' 描述
一个简单的OpenAI图片Demo程序
可以根据描述生成图片，根据输入修改图片，或是自动调整图片
'''

import sys, openai, webbrowser, os, getopt
from PIL import Image

def get_args():
    operation   = ''
    input_img   = ''
    mask_img    = ''
    prompt      = ''

    if 1 < len(sys.argv):
        argv = sys.argv[1:]
        args, others = getopt.getopt(argv, 'hcevi:m:p:', ['help', 'create', 'edit', 'variation', 'input=', 'mask=', 'prompt='])

        for opt, arg in args:
            if opt in ['-h', '--help']:
                operation += 'help' # 用 += 一直追加，如果输入了多个op参数就会被识别出错误
            elif opt in ['-c', '--create']:
                operation += 'create'
            elif opt in ['-e', '--edit']:
                operation += 'edit'
            elif opt in ['-v', '--variation']:
                operation += 'variation'
            elif opt in ['-i', '--input']:
                input_img = arg
            elif opt in ['-m', '--mask']:
                mask_img = arg
            elif opt in ['-p', '--prompt']:
                prompt = arg

    return operation, input_img, mask_img, prompt

# 判断文件是否为图片
def is_image(file_name):
    if os.path.isfile(file_name):
        name, ext = os.path.splitext(file_name)
        # 根据后缀名判断
        if ext.lower() in ['.jpg', '.jpeg', '.png']:
            return True

    return False

# 转换成RGBA
def convert_mode(input_file, to='RGBA'):
    output_file = ''
    try:
        img = Image.open(input_file)
        to_img = img.convert(to)
        output_file = input_file + '_convert_' + to + '.' + img.format 
        to_img.save(output_file)
    except ValueError:
        pass
    return output_file

# 生产图片
def create_image(prompt):
    response = None
    try:
        response = openai.Image.create(
                prompt=prompt,
                n=1,
                size='512x512')
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)


    return response

# 编辑图片
def edit_image(input_img, mask_img, prompt):
    response = None
    try:
        response = openai.Image.create_edit(
                image=open(input_img, 'rb'),
                mask=open(mask_img, 'rb'),
                prompt=prompt,
                n=1,
                size='512x512')
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)

    return response

# 自动调整
def variation_image(input_img):
    response = None
    try:
        response = openai.Image.create_variation(
                image=open(input_img, 'rb'),
                n=1,
                size='512x512')
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)

    return response

# 主程序
if __name__ == '__main__':
    # 处理参数
    operation, input_img, mask_img, prompt = get_args()

    # 开始执行
    resp = None
    if 'help' == operation:
        print('''
Usage: python image_gen.py [options] ... [-i image | --input=image] [-p prompt | --prompt=prompt] [-c | --create | -e | --edit | -v | --variation]

-c | --create       : 生成图片。根据给定的描述自动生成一张图片
-v | --variation    : 自动调整。自动调整给定图片
-e | --edit         : 编辑图片。根据输入的文本对给定图片进行编辑

-i | --input        : 输入的图片文件。只有操作为编辑和自动调整（-v|-e）时该参数才有意义
-p | --prompt       : 描述文字。给AI的提示，只有操作为生成和编辑（-c|-e）时才有意义
              ''')
        exit()
    elif 'create' == operation:
        if not prompt or '' == prompt:
            print('描述为空，无法正常执行')
            exit()
        else:
            print('Creating image...')
            resp = create_image(prompt)
    elif 'edit' == operation:
        if not is_image(input_img):
            print('输入图片不合法，无法正常执行')
            exit()
        elif not is_image(mask_img):
            print('输入的蒙版不合法，无法正常执行')
            exit()
        elif not prompt or '' == prompt:
            print('描述为空，无法正常执行')
            exit()
        else:
            with Image.open(input_img) as img:
                if not img.mode in ['RGBA', 'L', 'LA']:
                    print('Convert Image to RGBA')
                    input_img = convert_mode(input_img)
            with Image.open(mask_img) as img:
                if not img.mode in ['RGBA', 'L', 'LA']:
                    print('Convert Image to RGBA')
                    mask_img = convert_mode(mask_img)

            print(f'Editing Image: {input_img}')
            resp = edit_image(input_img, mask_img, prompt)
    elif 'variation' == operation:
        if not is_image(input_img):
            print('输入图片不合法，无法正常执行')
            exit()
        else:
            with Image.open(input_img) as img:
                if not img.mode in ['RGBA', 'L', 'LA']:
                    print('Convert Image to RGBA')
                    input_img = convert_mode(input_img)
            print(f'Changing Image: {input_img}')
            resp = variation_image(input_img)
    else:
        print('没有合法的操作参数。通过 -h 或 --help 了解如何使用')
        exit()

    if resp and 0 < len(resp['data']):
        output_url = resp['data'][0]['url']
        print(f'Image URL: {output_url}')
        webbrowser.open(output_url)
    else:
        print('执行失败，请重试')

