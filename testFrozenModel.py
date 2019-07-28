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

DATA_PATH = 'data/data_ref.csv'
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
N_FEATURES = 5

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

   X_train, X_test, y_train, y_test = train_test_split(data_convoluted, labels, test_size=0.7,    random_state=RANDOM_SEED)
   print len(X_test)
   print X_test.shape

#np.savetxt('test.txt', X_test)
  
   # Make predictions
   p_val = predictions.eval(feed_dict={input: X_test})
   
   acc, acc_op = tf.metrics.accuracy(labels=tf.argmax(y_test, 1), predictions=tf.argmax(p_val,1))
   sess.run(tf.local_variables_initializer())
   sess.run(tf.global_variables_initializer())

   sess.run([acc, acc_op])
   l = sess.run([acc])
   print('Accuracy: ' + str(l[0]))
  



   


