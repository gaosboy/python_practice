'''题目
在命令行窗口运行
当程序运行时，会要求我们输入中文或者英文单词或者句子，然后程序会自动翻译成对应的英语或者中文
当输入q字母，程序不再询问并结束
'''
import requests
import json

# 接口URL
url = 'https://fanyi.baidu.com/sug'

if __name__ == '__main__':
    print('输入要翻译的词语（q或Q退出）：', end='')
    orig = input()

    # q或Q 表示退出
    if orig in ['q', 'Q']:
        exit()

    response = requests.post(url, {'kw':orig})
    # 标记位
    hasResult = False
    result = ''
    if 200 == response.status_code:
        try:
            respJson = json.loads(response.text)

            # 结果
            result = ''
            if 'errno' in respJson and 0 == respJson['errno']:
                respData = respJson['data']
                if 0 < len(respData) and orig == respData[0]['k']:
                    result = respData[0]['v']
                    hasResult = True
        except ValueError:
            pass

    if hasResult:
        print(result)
    else:
        print('查询失败')

