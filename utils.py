import io
import urllib.request as url_request
from PIL import Image
import numpy as np

def log(info):
    print("Log : " + str( info))

#提示信息
def prompt(info):
    print(" ---" + info + "--- ")

def error_msg(info):
    print("Error : " + str( info))

def warn_msg(info):
    print("Warning : " + str( info))

'''
传入参数为headers，运行指定的Uri，返回结果可能为json或者html
'''
def run_uri(uri, headers):
    request = url_request.Request(uri, headers = headers)
    try:
        response = url_request.urlopen(request)
    except Exception as error:
        error_msg("please check the uri: " + uri)
        return None

    response_text = response.read().decode().replace('false', 'False').replace('true', 'True')
    # HTML格式文件
    if '<!Doctype html>' in response_text:
        return response_text
    else:
        # json格式文件
        log(response_text)
        data = eval(response_text)
        return data

'''
给定一个文件转换为(nx, 1)的矩阵，按照RGB排列，返回该矩阵
是否需要处理一下？除以255
'''
def image2matrix(file_name):
    image = Image.open(file_name)
    width, height = image.size
    image = image.convert("RGB")
    data = np.matrix(image.getdata(), dtype="float")
    data = np.reshape(data, (width*height*3, 1))
    return data

'''
给定一个图片的uri，返回该图片转换后的矩阵
'''
def uri2matrix(image_uri):
    request = url_request.Request(image_uri)
    response = url_request.urlopen(request).read()
    return image2matrix(io.BytesIO(response))