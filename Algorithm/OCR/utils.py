import sys

import cv2
import numpy as np
import torch

from configuration import *

sys.path.append(".")


def fillAndResize(image):
    """
    将输入图像填充为正方形且变换为（28，28）
    :param image:
    :return:
    """
    h, w = image.shape
    l = max(w, h)
    ret = np.zeros((l, l), np.uint8)
    leftTop = np.array([l/2-w/2, l/2-h/2], np.uint8)
    ret[leftTop[1]:leftTop[1]+h, leftTop[0]:leftTop[0]+w] = image
    ret = cv2.resize(ret, (28, 28), interpolation=cv2.INTER_CUBIC)
    return ret


class newNet(object):
    def __init__(self):
        """
        初始化LeNet模型
        :return:
        """
        sys.path.append("newNet")
        from Algorithm.OCR.digits.LeNet import myNet, rgbNet

        self.bitNet = myNet()
        self.bitNet.eval()
        self.bitNet.load_state_dict(torch.load("Algorithm/OCR/digits/model/net.pkl"))
        self.rgbNet = rgbNet('rgb')
        self.rgbNet.eval()
        self.rgbNet.load_state_dict(torch.load("Algorithm/OCR/digits/model/rgb_myNet_net.pkl"))

        

    def recognizeNet(self, image, type):
        """
        LeNet识别图像中的数字
        :param image: 输入图像
        :return: 识别的数字值
        """
        if type == 'bit':
            image = fillAndResize(image)
            tensor = torch.Tensor(image).view((1, 1, 28, 28))/255
            tensor = tensor.to("cpu")
            result = self.bitNet.forward(tensor)
        if type == 'rgb':
            img = cv2.resize(image, (28, 28), interpolation=cv2.INTER_CUBIC)
            if len(img.shape) == 2:
                img = np.array(img, img, img)
            tensor = torch.Tensor(img).view((1, 3, 28, 28))
            tensor = tensor.to("cpu")
            result = self.rgbNet.forward(tensor)

        _, predicted = torch.max(result.data, 1)
        num = int(np.array(predicted[0]).astype(np.uint32))

        if ifShow:
            print("this number is: ", num)
            cv2.imshow("single", image)
            cv2.waitKey(0)

        return str(num) if num != 10 else "?"
