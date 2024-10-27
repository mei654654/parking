import numpy as np
import tensorflow as tf

# 初始化模型
interpreter = tf.lite.Interpreter(model_path="static/ml/CNN_101052.tflite")
interpreter.allocate_tensors()

# 模型预测函数
def predict(input_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 確保輸入數據形狀正確
    input_shape = input_details[0]['shape']
    input_data = np.reshape(input_data, input_shape)  # 調整數據形狀

    # 输入数据
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # 获取模型输出
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # 假設輸出是座標，你需要根據模型輸出的格式來解析
    x = output_data[0][0]  # 假設 output_data 的第一個元素是 x 座標
    y = output_data[0][1]  # 假設 output_data 的第二個元素是 y 座標
    
    return x, y  # 返回坐標
