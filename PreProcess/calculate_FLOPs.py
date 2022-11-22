import tensorflow as tf
from tensorflow.python.framework import graph_util

def load_pb(pb):
    with tf.gfile.GFile(pb, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')
        return graph

# ***** (1) Create Graph *****
g = tf.Graph()
sess = tf.Session(graph=g)
with g.as_default():
    A = tf.Variable(initial_value=tf.random_normal([25, 16]))
    B = tf.Variable(initial_value=tf.random_normal([16, 9]))
    C = tf.matmul(A, B, name='output')
    sess.run(tf.global_variables_initializer())
    flops = tf.profiler.profile(g, options = tf.profiler.ProfileOptionBuilder.float_operation())
    print('FLOP before freezing', flops.total_float_ops)
# *****************************

# ***** (2) freeze graph *****
output_graph_def = graph_util.convert_variables_to_constants(sess, g.as_graph_def(), ['output'])

with tf.gfile.GFile('graph.pb', "wb") as f:
    f.write(output_graph_def.SerializeToString())
# *****************************


# ***** (3) Load frozen graph *****
g2 = load_pb('./pb/frozen_inference_graph.pb')
with g2.as_default():
    flops = tf.profiler.profile(g2, options = tf.profiler.ProfileOptionBuilder.float_operation())
    print('FLOPs: ', flops.total_float_ops)
