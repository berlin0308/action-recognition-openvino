from openvino.runtime import Core, serialize
from openvino.tools.ovc import convert_model
# import openvino.runtime as ov
import tensorflow as tf
import openvino as ov


saved_model_dir = 'results/a2_b8_lr0.000545_g2.5_d0.6_sd0.2_86/savedmodel'
output_model_path = 'openvino/movinet_a2_model_test.xml'

savedmodel = tf.saved_model.load(saved_model_dir)

core = Core()
ov_model = ov.convert_model(input_model=savedmodel, verbose=True)

ov.save_model(ov_model, output_model_path)
# ov.save_model(ov_model, 'movinet_a2_fp16_model.xml',compress_to_fp16=True)