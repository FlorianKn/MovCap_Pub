import tensorflow as tf
import os
# Just disables the warning, doesn't enable AVX/FMA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

gf = tf.GraphDef()
FROZEN_MODEL = 'frozen_har.pb'
LITE_MODEL = 'converted_model.tflite'

m_file = open(FROZEN_MODEL,'rb')
gf.ParseFromString(m_file.read())

input_tensors = gf.node[0].name
output_tensors = gf.node[len(gf.node)-1].name

graph_def_file = FROZEN_MODEL
input_arrays = [input_tensors]
output_arrays = [output_tensors]

converter = tf.lite.TFLiteConverter.from_frozen_graph(
  graph_def_file, input_arrays, output_arrays)
tflite_model = converter.convert()
open(LITE_MODEL, "wb").write(tflite_model)

print "Success"

