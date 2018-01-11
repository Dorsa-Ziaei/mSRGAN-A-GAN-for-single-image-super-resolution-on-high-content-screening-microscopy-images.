import tensorflow as tf

import sys
sys.path.append('../utils')
from layer import *

class VGG19:
    def __init__(self, trainable):
        self.n_class = 13
        self.img_dim = 96
        self.trainable = trainable
        self.x = tf.placeholder(tf.float32, [None, self.img_dim, self.img_dim, 3])
        self.t = tf.placeholder(tf.int32, [None])     
        self.is_training = tf.placeholder(tf.bool, [])
        self.out, self.phi = self.build_model(self.x, self.is_training)
        self.loss = self.inference_loss(self.out, self.t)

    def build_model(self, x, is_training, reuse=False):
        with tf.variable_scope('vgg19', reuse=reuse):
            phi = []
            with tf.variable_scope('conv1a'):
                x = conv_layer(x, [3, 3, 3, 64], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv1b'):
                x = conv_layer(x, [3, 3, 64, 64], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            phi.append(x)

            x = max_pooling_layer(x, 2, 2)
            with tf.variable_scope('conv2a'):
                x = conv_layer(x, [3, 3, 64, 128], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv2b'):
                x = conv_layer(x, [3, 3, 128, 128], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            phi.append(x)

            x = max_pooling_layer(x, 2, 2)
            with tf.variable_scope('conv3a'):
                x = conv_layer(x, [3, 3, 128, 256], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv3b'):
                x = conv_layer(x, [3, 3, 256, 256], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv3c'):
                x = conv_layer(x, [3, 3, 256, 256], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv3d'):
                x = conv_layer(x, [3, 3, 256, 256], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            phi.append(x)

            x = max_pooling_layer(x, 2, 2)
            with tf.variable_scope('conv4a'):
                x = conv_layer(x, [3, 3, 256, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv4b'):
                x = conv_layer(x, [3, 3, 512, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv4c'):
                x = conv_layer(x, [3, 3, 512, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv4d'):
                x = conv_layer(x, [3, 3, 512, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            phi.append(x)

            x = max_pooling_layer(x, 2, 2)
            with tf.variable_scope('conv5a'):
                x = conv_layer(x, [3, 3, 512, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv5b'):
                x = conv_layer(x, [3, 3, 512, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv5c'):
                x = conv_layer(x, [3, 3, 512, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            with tf.variable_scope('conv5d'):
                x = conv_layer(x, [3, 3, 512, 512], 1, self.trainable)
                x = batch_normalize(x, is_training)
                x = lrelu(x)
            phi.append(x)

            x = max_pooling_layer(x, 2, 2)
            x = flatten_layer(x)
            with tf.variable_scope('fc1'):
                x = full_connection_layer(x, 4096, self.trainable)
                x = lrelu(x)
            with tf.variable_scope('fc2'):
                x = full_connection_layer(x, 4096, self.trainable)
                x = lrelu(x)
            with tf.variable_scope('softmax'):
                x = full_connection_layer(x, self.n_class, self.trainable)

            return x, phi


    def inference_loss(self, out, t):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = out,labels =  tf.one_hot(t, self.n_class)))
        return loss

