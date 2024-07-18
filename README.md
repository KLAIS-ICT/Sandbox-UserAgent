# Click 项目摘要

基本信息：Click是一个Web应用，主要功能是：根据用户历史或用户特征，判断该用户是否喜欢某个项目。

基本功能概述：
1. 基于用户历史序列，判断该用户是否喜欢某个项目。
2. 基于用户特征，判断该用户是否喜欢某个项目。
3. 提供接口，可直接和大模型进行交互。

项⽬特⾊：
1. 轻量级，使用轻量级的Web应用框架Flask，封装开源大模型，提供接口，可直接和大模型进行交互。
2. 可以根据需要，自由开发特定的和大模型交互的接口。

# 项目配置说明

硬件环境：

操作系统：内核版本为 3.10.0-1160.95.1.el7.x86_64的CentOS 7
CPU: Intel(R) Xeon(R) Silver 4310 CPU @ 2.10GHz
GPU：NVIDIA Tesla V100 GPU

软件环境配置：
```bash
conda create -n click_env python==3.10.14
conda activate click_env
pip install -r requirements.txt
```

设置LLM模型路径：
修改 app.py 文件中的对应位置，设置您的模型路径。仅支持Llama系列。
```python
clicker = Clicker('/LLM/Path/')
```
> 这里指定的是下载到本地的Llama模型路径。
> 下载地址：https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
> 国内镜像：https://www.modelscope.cn/models/shakechen/Llama-2-7b-chat-hf
> 也可以从其他服务器上copy到本地，/data22/public/llama_model/7b-chat-hf

# 运行说明
启动应用服务：
```python
python app.py
```
默认端口为8989，可发送GET请求到 `对应服务器IP:8989/hello` 确认服务器是否正常启动。

一共提供了5个接口：
1. GET `IP:8989/hello` 测试Web服务是否正常启动；
2. POST `IP:8989/chat` 访问次接口，可和大模型对话；
3. POST `IP:8989/islike` 根据用户历史序列，判断该用户是否喜欢某个项目；
4. POST `IP:8989/islike2` 根据用户历史序列，两段式的判断该用户是否喜欢某个项目；
5. POST `IP:8989/islike_woHistory` 根据用户特征描述，判断该用户是否喜欢某个项目；
6. POST `IP:8989/islike_woHistory2` 根据用户特征描述，两段式的判断该用户是否喜欢某个项目；
> 非两段式：Reason和是否喜欢，同时输出，仅访问LLM一次；两段式，先访问LLM输出Reason，然后带着Reason再访问一次LLM输出是否喜欢。共访问LLM两次。

下面是对应接口的请求和响应格式的详细信息。
## POST `IP:8989/chat` 
发送请求：
```python
data = {
    'prompt': "你好，请问今天天气怎么样 ？[/INST]"
}
headers = {'Content-Type': 'application/json'}
response = requests.post('http://Your Server IP:8989/chat', json=data, headers=headers)
```
响应格式:
```python
response.json()
# {'Prompt': "你好，请问今天天气怎么样 ？[/INST]", 'Answer': "今天天气很不错，适合外出郊游。"}
```

## `IP:8989/islike`
发送请求：
```python
data = {
    'like_historys': ["science and technology,consumption", "Hot girl,music", "military,history", "Health,medical care", "military,Hot girl"],
    'dislike_historys': ["Car,scenery", "Sports,Travel", "Politics,Gaming", "cooking,lifestyle", "scenery,lifestyle"],
    'target_item': "A young content creator stands before a white wall, adorned with cat ears and dressed in a colorful outfit. She flashes a cheerful smile while making peace or victory signs."
}
headers = {'Content-Type': 'application/json'}
response = requests.post('http://Your Server IP:8989/islike', json=data, headers=headers)
```
- `like_historys`: 用户喜欢的视频类型的历史序列；
- `dislike_historys`: 用户不喜欢的视频类型的历史序列：
- `target_item`: 需要判断的目标短视频描述。

响应格式:
```python
response.json()
# {
#   "isLiker": {
#     "like": Like or DisLike,
#     "reason": LLM响应的对应Reasons,
#   }
# }
```
- `like`: "Like"表示喜欢；"Dislike"表示不喜欢；
- `reason`: LLM响应的对应Reasons。

## POST `IP:8989/islike2`
islike2的接口的请求和响应格式与islike接口完全相同。

## POST`IP:8989/islike_woHistory`
发送请求：
```python
data = {
    'user_profile': "I am only interested in anything related to basketball. I'm less interested in other topics such as cars, movies, etc.",
    'target_item': "this is a screenshot of a short video about basketball."
}
headers = {'Content-Type': 'application/json'}
response = requests.post('http://Your Server IP:8989/islike_woHistory', json=data, headers=headers)
```
- `user_profile`: 用户特征描述；
- `target_item`: 需要判断的目标短视频描述。

响应格式:
```python
response.json()
# {
#   "isLiker": {
#     "like": Like or DisLike,
#     "reason": LLM响应的对应Reasons,
#   }
# }
```
- `like`: "Like"表示喜欢；"Dislike"表示不喜欢；
- `reason`: LLM响应的对应Reasons。

## POST `IP:8989/islike_woHistory2`
islike_woHistory2的接口的请求和响应格式与islike_woHistory接口完全相同。

# 工程结构说明

Web应用的主体，和程序的入口都是 `app.py`。
- `app.py` 中定义路由，全局模式加载LLM到显存中待命，并对客户端参数进行解析后，交由各个路由对应的Service层（click_item_proj1.py）进行处理。
- `click_item_proj1.py` 调用LLM（LLM.py）用于处理用户请求，并返回相应的响应。

