# @Time   : 2024/6/11
# @Author : Hang
# @Email  : hangkids3699@163.com

import random
from llm import *

class Clicker:
    def __init__(self, model_path):
        """
        初始化Clicker类，加载语言模型
        
        参数:
        model_path (str): 语言模型的路径
        """
        self.llm = LLM(model_path)
        self.prompt = None  # 根据历史记录和候选集构造提示词

    def isLike(self, like_historys, dislike_historys, target_item):
        """
        根据用户的历史喜欢和不喜欢的视频内容，判断用户是否会喜欢目标视频描述，并解释背后的三个原因。
        
        参数:
        like_historys (list): 用户历史喜欢的视频类型列表
        dislike_historys (list): 用户历史不喜欢的视频类型列表
        target_item (str): 目标视频的描述
        
        返回:
        response (str): 模型的响应，包含是否喜欢的判断和原因
        """
        prompt = f"""Given the user's historical likes and dislikes in the video content, determine whether the current user will like the target video description, and explain the three reasons behind the suggestion in concise language.
Based on the previous reasons, please respond whether you think the user would like the target video or not. Your response must include either "like" or "dislike".

Historical records of liked video types: {', '.join(like_historys)}.
Historical records of disliked video types: {', '.join(dislike_historys)}.

Target video description:
{target_item}

Please respond in the following format:
Reasons:  <analysis of whether the video is related to User preference>
Response: <"like" or "dislike">[/INST]
"""
        print("当前prompt：\n", prompt)

        # 向语言模型发送请求，判断用户是否会喜欢目标视频
        response = self.llm.requestLLM_isLike(prompt)
        print("llm输出处理后结果：", response)
        return response

    def chat(self, prompt):
        """
        与语言模型进行聊天，返回响应
        
        参数:
        prompt (str): 发送给语言模型的提示
        
        返回:
        response (str): 模型的响应
        """
        response = self.llm.requestLLM_chat(prompt)
        return response

    def isLike_woHistory(self, user_profile, target_item):
        """
        根据用户的偏好，判断用户是否会喜欢目标视频描述，并解释背后的三个原因。
        
        参数:
        user_profile (str): 用户偏好描述
        target_item (str): 目标视频的描述
        
        返回:
        response (str): 模型的响应，包含是否喜欢的判断和原因
        """
        prompt = f"""Given the user's preference in the video content, determine whether the current user will like the target video description, and explain the three reasons behind the suggestion in concise language.
Based on the previous reasons, please respond whether you think the user would like the target video or not. Your response must include either "like" or "dislike".

User preference:
{user_profile}

Target video description:
{target_item}

Please analyse whether this video is related to your interest，
Output your analysis. Then based on your analysis, output reason and response in the following format:

Reasons: <analysis of whether the video is related to User preference>
Response: <"like" or "dislike">[/INST]
"""
        # Analysis: <analysis of whether the video is related to User preference>
        print("当前prompt：\n", prompt)

        # 向语言模型发送请求，判断用户是否会喜欢目标视频
        response = self.llm.requestLLM_isLike(prompt)
        print("llm输出处理后结果：", response)
        return response
    
    def isLike_2(self, like_historys, dislike_historys, target_item):
        """
        分析目标视频描述的重要特征，判断这些特征是否可能吸引用户。
        
        参数:
        like_historys (list): 用户历史喜欢的视频类型列表
        dislike_historys (list): 用户历史不喜欢的视频类型列表
        target_item (str): 目标视频的描述
        
        返回:
        dict: 包含是否喜欢的判断和分析原因
        """
        prompt = f"""You are a user watching short videos. This is your interest video types: "{', '.join(like_historys)} and this is your less interest video types: "{', '.join(dislike_historys)}".
Analyze what are the important features of the target video description, determine whether some of the features may attract you.
Target video description:
{target_item}

Please respond in the following format:
Analysis:  <analysis of whether the video attracts you>[/INST]
"""        
        print("==="*30)
        print("当前prompt：\n", prompt)
        print("==="*30)

        # 向语言模型发送请求，获取对目标视频描述的分析
        thoughts = self.llm.requestLLM_chat(prompt)
        print("==="*30)
        print("llm输出处理后结果：", thoughts)
        print("==="*30)
        prompt = f"""Based on the following reasons, please respond whether you think the user would like the target video or not. Your response must include either "like" or "dislike".

Thoughts：{thoughts}
        
Please respond in the following format:
Response: <"like" or "dislike">[/INST]
"""
        response = self.llm.requestLLM_chat(prompt)
        print("==="*30)
        print("llm输出处理后结果：", response)
        print("==="*30)
        if "dislike" in response.lower():
            response = "Dislike"
        else:
            response = "Like"

        return {
            "like": response,
            "reason": thoughts
        }

    def isLike_woHistory_2(self, user_profile, target_item):
        """
        分析目标视频描述的重要特征，判断这些特征是否可能吸引用户（无历史记录）。
        
        参数:
        user_profile (str): 用户偏好描述
        target_item (str): 目标视频的描述
        
        返回:
        dict: 包含是否喜欢的判断和分析原因
        """
        prompt = f"""You are a user watching short videos. This is your profile: "{user_profile}".
Here is a short video for you:"{target_item}".
Analyze what are the important features of the target video description, determine whether some of the features may attract you.

Please respond in the following format:
Analysis:  <analysis of whether the video attracts you>[/INST]
"""
        print("==="*30)
        print("当前prompt：\n", prompt)
        print("==="*30)

        # 向语言模型发送请求，获取对目标视频描述的分析
        thoughts = self.llm.requestLLM_chat(prompt)
        print("==="*30)
        print("llm输出处理后结果：", thoughts)
        print("==="*30)

        prompt = f"""Based on the following reasons, please respond whether you think the user would like the target video or not. Your response must include either "like" or "dislike".

Thoughts：{thoughts}
        
Please respond in the following format:
Response: <"like" or "dislike">[/INST]
"""
        response = self.llm.requestLLM_chat(prompt)
        print("==="*30)        
        print("llm输出处理后结果：", response)
        print("==="*30)
        if "dislike" in response.lower():
            response = "Dislike"
        else:
            response = "Like"

        return {
            "like": response,
            "reason": thoughts
        }

# if __name__ == "__main__":
#     model_path = "../LlamaRec/7b-chat-hf-ml100k/"

#     clicker = Clicker(model_path)
#     user_history = ["Broken Arrow (1996)", "The Birdcage (1996)", "Twister (1996)", "Willy Wonka & the Chocolate Factory (1971)", "James and the Giant Peach (1996)"]
#     target_item = "The Hunchback of Notre Dame (1996)"  

#     print(clicker.clickOrNot(user_history, target_item))
