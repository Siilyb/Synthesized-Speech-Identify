import tensorflow._api.v2.compat.v1 as tf
tf.compat.v1.disable_v2_behavior()
import argparse as aps

from heapq import nlargest
import os

BATCH_SIZE =  1
IMAGE_SIZE = 32
N_CLASSES = 12

parser = aps.ArgumentParser(description="manual to this script")
parser.add_argument("--model",type=str,default="model/mod.ckpt-0")
args = parser.parse_args()

def fileName(filename):
    for _, dirs, files in os.walk(filename):
        return files

test = fileName("data/testdata/")
# 模型地址
MODEL_PATH = "model/mod.ckpt-15000"
# 读取图像
def read_image_tensor(image_dir):
    image = tf.gfile.FastGFile(image_dir, 'rb').read()
    image = tf.image.decode_jpeg(image) #图像解码
    image = tf.image.convert_image_dtype(image, dtype=tf.uint8) #改变图像数据的类型
    image = tf.image.resize_images(image, [IMAGE_SIZE, IMAGE_SIZE], method=0)
    image = tf.image.per_image_standardization(image)
    image = tf.reshape(image,[1,IMAGE_SIZE,IMAGE_SIZE,3])
    return image

def useModel():


    labels = ["DF", "PA"]
    model = tf.train.import_meta_graph(MODEL_PATH+".meta")
    graph = tf.get_default_graph()
    inputs = graph.get_operation_by_name('x-input').outputs[0]
    is_train = graph.get_operation_by_name('is_train').outputs[0]
    pred = tf.get_collection('pred_network')[0]
    test_list = {}
    with tf.Session(graph=graph) as sess:
        model.restore(sess, MODEL_PATH)
        for path in test:
            image = read_image_tensor("data/testdata/"+path)
            image = sess.run(image)
            pred_y = sess.run(tf.nn.softmax(pred,1), feed_dict={inputs:image,is_train:[False]})
            max_index = list(map(list(pred_y[0]).index,nlargest(2,pred_y[0])))
            max_num = nlargest(2,pred_y[0])
            print("预测类别 " + path)
            test_list[path] = labels[max_index[0]]
            print("\t",labels[max_index[0]],":",max_num[0]*100,"%")
            print("\t",labels[max_index[1]],":",max_num[1]*100,"%")
            # print("\t",labels[max_index[2]],":",max_num[2]*100,"%")


#传入模型
if __name__ == '__main__':
    with tf.device("/cpu:0"):
        useModel()


def useModel2(filepath):


    labels = ["合成语音", "真实语音"]
    model = tf.train.import_meta_graph(MODEL_PATH+".meta")
    graph = tf.get_default_graph()
    inputs = graph.get_operation_by_name('x-input').outputs[0]
    is_train = graph.get_operation_by_name('is_train').outputs[0]
    pred = tf.get_collection('pred_network')[0]

    with tf.Session(graph=graph) as sess:
        model.restore(sess, MODEL_PATH)

        image = read_image_tensor(filepath)
        image = sess.run(image)
        pred_y = sess.run(tf.nn.softmax(pred,1), feed_dict={inputs:image,is_train:[False]})
        max_index = list(map(list(pred_y[0]).index,nlargest(2,pred_y[0])))
        max_num = nlargest(2,pred_y[0])
        # print("预测类别 ")
        #
        # print("\t",labels[max_index[0]],":",max_num[0]*100,"%")
        # print("\t",labels[max_index[1]],":",max_num[1]*100,"%")
        # print("\t",labels[max_index[2]],":",max_num[2]*100,"%")
        return labels[max_index[0]],max_num[0]*100,labels[max_index[1]],max_num[1]*100
