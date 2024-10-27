import pymongo
from flask import Flask, request, render_template, jsonify
import numpy as np
import tensorflow as tf

# 连接到 MongoDB
client = pymongo.MongoClient("mongodb+srv://root:root123@testparking.3yyne.mongodb.net/")
db = client['testparking']  # 替換為你的資料庫名稱
parking_collection = db['parking_data']  # 替換為你的集合名稱
print("MongoDB 连接成功!")

# 创建 Flask 应用
app = Flask(__name__)

# 初始化模型
interpreter = tf.lite.Interpreter(model_path="static/ml/CNN_101052.tflite")
interpreter.allocate_tensors()

# 模型预测函数
def predict(input_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # 输入数据
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    # 获取模型输出
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/parking")
def parking():
    return render_template("parking.html")

@app.route("/find")
def find():
    return render_template("find.html")

@app.route("/enter", methods=["POST"])  # 确保这里的路由以斜杠开头
def enter():
    plate_number = request.form["plate_number"]
    collection = db.parking_data  # 确保 collection 被正确定义

    # 将车牌号码插入到 MongoDB
    collection.insert_one({
        "plate_number": plate_number
    })
    return render_template("parking.html")

# 接收前端數據並傳入模型
@app.route('/submit_data', methods=['POST'])
def submit_data():
    # 獲取前端傳來的數據
    data = request.json  # 包含 x, y, z, sum, signal1 和車牌號碼
    plate_number = data.get('plate_number')
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    sum_value = data.get('sum')
    signal1 = data.get('signal1')
    
    # 準備模型輸入數據
    input_data = np.array([[x, y, z, sum_value, signal1]], dtype=np.float32)
    
    # 獲取模型預測
    prediction = predict(input_data)

    # 將數據及預測結果存入資料庫
    parking_collection.insert_one({
        'plate_number': plate_number,
        'x': x,
        'y': y,
        'z': z,
        'sum': sum_value,
        'signal1': signal1,
        'prediction': prediction.tolist()  # 將預測結果轉為列表
    })
    
    return jsonify({'message': '數據已成功提交', 'prediction': prediction.tolist()}), 201

@app.route('/find_vehicle', methods=['POST'])
def find_vehicle():
    plate_number = request.json.get('plate_number')
    
    # 根據車牌號碼查詢資料庫
    vehicle_data = parking_collection.find_one({'plate_number': plate_number})
    
    if vehicle_data:
        return jsonify({
            'x': vehicle_data['x'],
            'y': vehicle_data['y'],
            'plate_number': vehicle_data['plate_number']
        })
    else:
        return jsonify({'message': '未找到車輛'}), 404
    
# 启动应用程序
if __name__ == "__main__":
    app.run(port=3000, debug=True)
