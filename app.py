# @Time   : 2024/6/11
# @Author : Hang
# @Email  : hangkids3699@163.com

from flask import Flask, g, jsonify, request

# 导入Clicker类
from click_item_proj1 import Clicker

# 创建Flask应用实例
app = Flask(__name__)

# 定义一个简单的路由，返回一个JSON格式的问候语
@app.route('/hello')
def hello():
    return jsonify('Hello, xxxxxxxxxxxxxxx')

# 定义一个全局的Clicker对象
clicker = Clicker('/LLM/Path/')

# 定义一个路由，用于处理聊天请求
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json  # 获取请求中的JSON数据
    prompt = data.get('prompt')  # 从数据中提取prompt字段
    global clicker
    answer = clicker.chat(prompt)  # 使用Clicker对象生成回答
    return jsonify({'Prompt': prompt, 'Answer': answer})  # 返回JSON格式的回答

# 定义一个路由，用于判断是否喜欢某个项目
@app.route('/islike', methods=['POST'])
def islike():
    data = request.json  # 获取请求中的JSON数据
    like_historys = data.get('like_historys')  # 获取用户喜欢的历史记录
    dislike_historys = data.get('dislike_historys')  # 获取用户不喜欢的历史记录
    target_item = data.get('target_item')  # 获取目标项目

    global clicker
    isLiker = clicker.isLike(like_historys, dislike_historys, target_item)  # 判断是否喜欢目标项目
    return jsonify({'isLiker': isLiker})  # 返回判断结果

# 定义一个路由，用于判断是否喜欢某个项目
@app.route('/islike2', methods=['POST'])
def islike2():
    data = request.json  # 获取请求中的JSON数据
    like_historys = data.get('like_historys')  # 获取用户喜欢的历史记录
    dislike_historys = data.get('dislike_historys')  # 获取用户不喜欢的历史记录
    target_item = data.get('target_item')  # 获取目标项目

    # 删除目标项目中的特定关键词，特殊操作。
    target_item = target_item.lower()
    target_item = target_item.replace("fiba3x3", "")

    global clicker
    isLiker = clicker.isLike_2(like_historys, dislike_historys, target_item)  # 判断是否喜欢目标项目
    return jsonify({'isLiker': isLiker})  # 返回判断结果

# 定义一个路由，用于判断是否喜欢某个项目（使用用户描述）
@app.route('/islike_woHistory', methods=['POST'])
def islike_woHistory():
    data = request.json  # 获取请求中的JSON数据
    user_profile = data.get('user_profile')  # 获取用户资料
    target_item = data.get('target_item')  # 获取目标项目

    global clicker
    isLiker = clicker.isLike_woHistory(user_profile, target_item)  # 判断是否喜欢目标项目
    return jsonify({'isLiker': isLiker})  # 返回判断结果

# 定义一个路由，用于判断是否喜欢某个项目（使用用户描述）
@app.route('/islike_woHistory2', methods=['POST'])
def islike_woHistory2():
    data = request.json  # 获取请求中的JSON数据
    user_profile = data.get('user_profile')  # 获取用户资料
    target_item = data.get('target_item')  # 获取目标项目

    # 删除目标项目中的特定关键词
    target_item = target_item.lower()
    target_item = target_item.replace("fiba3x3", "")

    global clicker
    isLiker = clicker.isLike_woHistory_2(user_profile, target_item)  # 判断是否喜欢目标项目
    return jsonify({'isLiker': isLiker})  # 返回判断结果

# 启动Flask应用
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # 监听所有主机地址
        port=8989,  # 端口号
        debug=True)  # 启用调试模式

# 后台运行Flask应用，并将输出重定向到日志文件
# nohup python -u app.py > app.log &
