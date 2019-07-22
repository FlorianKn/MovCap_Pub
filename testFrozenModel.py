import tensorflow as tf
from tensorflow.python.platform import gfile
import os
import pandas as pd
from scipy import stats
import numpy as np
from sklearn.model_selection import train_test_split

GRAPH_PB_PATH = './frozen_har.pb'
# Just disables the warning, doesn't enable AVX/FMA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

DATA_PATH = 'data/alt_data.csv'
COLUMN_NAMES = [
    'Time',
    'ElbowFlexion',
    'ElbowSupination',
    'ShoulderFlexion',
    'ShoulderAbduction',
    'ShoulderRotation',
    'User',
    'Label'
]
SEGMENT_TIME_SIZE = 150
TIME_STEP = 30
RANDOM_SEED = 13
N_EPOCHS = 10
BATCH_SIZE = 150
N_FEATURES = 5
N_CLASSES = 4
N_HIDDEN_NEURONS = 100
L2_LOSS = 0.0015
LEARNING_RATE = 0.0025

def createLSTM(X):

        W = {
            'hidden': tf.Variable(tf.random_normal([N_FEATURES, N_HIDDEN_NEURONS])),
            'output': tf.Variable(tf.random_normal([N_HIDDEN_NEURONS, N_CLASSES]))
        }

        b = {
            'hidden': tf.Variable(tf.random_normal([N_HIDDEN_NEURONS], mean=1.0)),
            'output': tf.Variable(tf.Variable(tf.random_normal([N_CLASSES])))
        }

        # Transpose and then reshape to 2D of size (BATCH_SIZE * SEGMENT_TIME_SIZE, N_FEATURES)
        X = tf.transpose(X, [1, 0, 2])
        X = tf.reshape(X, [-1, N_FEATURES])

        hidden = tf.nn.relu(tf.matmul(X, W['hidden']) + b['hidden'])
        hidden = tf.split(hidden, SEGMENT_TIME_SIZE, 0)

        # Stack two LSTM cells on top of each other
        lstm_cell_1 = tf.contrib.rnn.BasicLSTMCell(N_HIDDEN_NEURONS, forget_bias=1.0)
        lstm_cell_2 = tf.contrib.rnn.BasicLSTMCell(N_HIDDEN_NEURONS, forget_bias=1.0)
        lstm_layers = tf.contrib.rnn.MultiRNNCell([lstm_cell_1, lstm_cell_2])

        outputs, _ = tf.contrib.rnn.static_rnn(lstm_layers, hidden, dtype=tf.float32)

        # Get output for the last time step from a "many to one" architecture
        last_output = outputs[-1]

        return tf.matmul(last_output, W['output'] + b['output'])


with tf.Session() as sess:
   print("load graph")
   with gfile.FastGFile(GRAPH_PB_PATH,'rb') as f:
       graph_def = tf.GraphDef()
   graph_def.ParseFromString(f.read())
   sess.graph.as_default()
   input, predictions = tf.import_graph_def(graph_def, return_elements=['X:0','y_pred_softmax:0'])

   # LOAD DATA
   data = pd.read_csv(DATA_PATH, header=None, names=COLUMN_NAMES)
   data = data.dropna()
   data = data.iloc[1:]
   # DATA PREPROCESSING
   data_convoluted = []
   labels = []
   
   # Slide a "SEGMENT_TIME_SIZE" wide window with a step size of "TIME_STEP"
   for i in range(0, len(data) - SEGMENT_TIME_SIZE, TIME_STEP):
        eF = data['ElbowFlexion'].values[i: i + SEGMENT_TIME_SIZE]
        eS = data['ElbowSupination'].values[i: i + SEGMENT_TIME_SIZE]
        sF = data['ShoulderFlexion'].values[i: i + SEGMENT_TIME_SIZE]
        sA = data['ShoulderAbduction'].values[i: i + SEGMENT_TIME_SIZE]
        sR = data['ShoulderRotation'].values[i: i + SEGMENT_TIME_SIZE]
        data_convoluted.append([eF, eS, sF, sA, sR])

        # Label for a data window is the label that appears most commonly
        label = stats.mode(data['Label'][i: i + SEGMENT_TIME_SIZE])[0][0]

        labels.append(label)

   data_convoluted = np.asarray(data_convoluted, dtype=np.float32).transpose(0, 2, 1)
   labels = np.asarray(pd.get_dummies(labels), dtype=np.float32)

   X = tf.placeholder(tf.float32, [None, SEGMENT_TIME_SIZE, N_FEATURES], name="X")
   y = tf.placeholder(tf.float32, [None, N_CLASSES], name="y")
   y_pred = createLSTM(X)
   y_pred_softmax = tf.nn.softmax(y_pred, name="y_pred_softmax")

   # LOSS
   l2 = L2_LOSS * sum(tf.nn.l2_loss(i) for i in tf.trainable_variables())
   loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=y_pred, labels=y)) + l2
    
   # OPTIMIZER
   optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE).minimize(loss)
   correct_pred = tf.equal(tf.argmax(y_pred_softmax, 1), tf.argmax(y, 1))
   accuracy = tf.reduce_mean(tf.cast(correct_pred, dtype=tf.float32))

   X_train, X_test, y_train, y_test = train_test_split(data_convoluted, labels, test_size=0.3,    random_state=RANDOM_SEED)

   train_count = len(X_train)
   
   acc = tf.global_variables_initializer()
   acc_op = tf.local_variables_initializer()
   # Make predictions
   p_val = predictions.eval(feed_dict={input: X_test})

   
   acc, acc_op = tf.metrics.accuracy(labels=tf.argmax(y_test, 1), predictions=tf.argmax(p_val,1))
   sess.run(tf.local_variables_initializer())
   sess.run(tf.global_variables_initializer())

   stream_vars = [i for i in tf.local_variables()]
   print(stream_vars)
   print(sess.run([acc, acc_op]))
   print(sess.run([acc]))
#print len(y_test)
   #sess.run(optimizer, feed_dict={X: X_train[start:end], y: y_train[start:end]})
   #_, acc_test, loss_test = sess.run([predictions], feed_dict={X: X_test, y: y_test})
   #print acc_test
   #for i in range(1, N_EPOCHS + 1):
        #for start, end in zip(range(0, train_count, BATCH_SIZE), range(BATCH_SIZE, train_count + 1, BATCH_SIZE)):
            #sess.run(optimizer, feed_dict={X: X_train[start:end], y: y_train[start:end]})

        #_, acc_test, loss_test = sess.run([y_pred_softmax, accuracy, loss], feed_dict={X: X_test, y: y_test})
        #print acc_test

