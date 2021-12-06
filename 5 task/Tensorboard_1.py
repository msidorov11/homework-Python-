### Сделал отдельную программу для себя, чтобы разобраться, как работает Tensorboard ###

import tensorflow as tf
from tensorflow import keras
from time import time
from tensorflow.python.keras.callbacks import TensorBoard

(train_img, train_lab), (test_img, test_lab) = keras.datasets.fashion_mnist.load_data()

train_img = train_img/255.0
test_img = test_img/255.0

model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(hparams[HP_NUM_UNITS], activation=tf.nn.relu),
        tf.keras.layers.Dropout(hparams[HP_DROPOUT]),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax),
        ])

tb = TensorBoard(log_dir = "logs/{}".format(time()))

model.compile(optimizer = tf.optimizers.Adam(), loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
model.fit(train_img, train_lab, epochs = 10, callbacks = [tb])

test_loss, test_acc = model.evaluate(test_img, test_lab)

print('accuracy', test_acc)