import torch
import numpy as np
from torchvision import models,transforms
from PIL import Image
from tensorboardX import SummaryWriter



vgg16 = models.vgg16() # 这里下载预训练好的模型
print(vgg16)           # 打印一下这个模型


transform_2 = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    # convert RGB to BGR
    # from <https://github.com/mrzhu-cool/pix2pix-pytorch/blob/master/util.py>
    transforms.Lambda(lambda x: torch.index_select(x, 0, torch.LongTensor([2, 1, 0]))),
    transforms.Lambda(lambda x: x*255),
    transforms.Normalize(mean = [103.939, 116.779, 123.68],
                          std = [ 1, 1, 1 ]),
])



cat_img = Image.open('../data/lena_std.tif')
vgg16_input=transform_2(cat_img)[np.newaxis]# 因为pytorch的是分批次进行的，所以我们这里建立一个批次为1的数据集
print(vgg16_input.shape)


# 开始前向传播，打印输出值
raw_score = vgg16(vgg16_input)
raw_score_numpy = raw_score.data.numpy()
print(raw_score_numpy.shape, np.argmax(raw_score_numpy.ravel()))


# 将结构图在tensorboard进行展示
with SummaryWriter(log_dir='./vgg16_logs', comment='vgg16') as writer:
    writer.add_graph(vgg16, (vgg16_input,))