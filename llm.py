# @Time   : 2024/6/11
# @Author : Hang
# @Email  : hangkids3699@163.com

import os
import re
import torch
import random
os.environ['CUDA_VISIBLE_DEVICES'] = '2'  # 指定使用的CUDA设备编号

from transformers import AutoTokenizer, AutoModelForCausalLM

class LLM:
    def __init__(self, model_path):
        """
        初始化LLM类，加载指定路径的模型。
        :param model_path: 模型的路径或者是模型的名称（如果是Hugging Face Model Hub中的模型）
        """
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.load_model()  # 调用加载模型的方法

    def load_model(self):
        """
        加载模型和tokenizer。
        """
        try:
            # 使用AutoModelForCausalLM从预设路径加载因果语言模型，并指定返回字典格式、数据类型和设备映射
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                return_dict=True,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            # 自动从预设路径加载tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            # 如果加载模型失败，打印错误信息
            print(f"Failed to load model: {e}")

    def is_model_loaded(self):
        """
        检查模型是否已经被加载。
        :return: 布尔值，如果模型已加载则返回True，否则返回False。
        """
        return self.model is not None and self.tokenizer is not None

    def requestLLM_chat(self, prompt):
        """
        发送prompt到模型并获取响应。
        :param prompt: 输入的prompt文本。
        :return: 模型生成的文本响应。
        """
        # 将prompt文本转换为模型可接受的输入格式，并将其发送到GPU
        input_ids = self.tokenizer(prompt, return_tensors="pt", truncation=True).input_ids.to("cuda")
        # 设置生成文本的参数
        generate_input = {
            "input_ids": input_ids,
            "max_new_tokens": 512,  # 最大新生成词数
            "do_sample": True,      # 是否采样生成
            "top_k": 50,            # 采样的词汇范围
            "top_p": 0.95,          # 累积概率阈值
            "temperature": 0.1,     # 温度参数，控制随机性
            "repetition_penalty": 1.3,  # 重复惩罚因子
            # 以下为特殊标记的ID
            "eos_token_id": self.tokenizer.eos_token_id,  # 结束标记
            "bos_token_id": self.tokenizer.bos_token_id,  # 开始标记
            "pad_token_id": self.tokenizer.pad_token_id   # 长度不够补的padding标记
        }
        # 使用模型生成响应
        generate_ids = self.model.generate(**generate_input)
        text = self.tokenizer.decode(generate_ids[0])

        # 清理生成的文本，移除prompt部分和结束标记
        text = text.replace("<s> " + prompt, "").strip()[:-4]
        return text

    def requestLLM_isLike(self, prompt):
        """
        发送prompt到模型并获取响应，用于判断用户是否喜欢某个内容。
        :param prompt: 输入的prompt文本。
        :return: 包含用户是否喜欢及其原因的字典。
        """
        # 将prompt文本转换为模型可接受的输入格式，并将其发送到GPU
        input_ids = self.tokenizer(prompt, return_tensors="pt", truncation=True).input_ids.to("cuda")
        # 设置生成文本的参数
        generate_input = {
            "input_ids": input_ids,
            "max_new_tokens": 512,  # 最大新生成词数
            "do_sample":True,
            "top_k":50,
            "top_p":0.95,
            "temperature":0.,
            "repetition_penalty":1.3,
            "eos_token_id":self.tokenizer.eos_token_id, # 结束标记
            "bos_token_id":self.tokenizer.bos_token_id, # 开始标记
            "pad_token_id":self.tokenizer.pad_token_id  # 长度不够补的padding标记
        }
        generate_ids = self.model.generate(**generate_input)
        text = self.tokenizer.decode(generate_ids[0])
        print("llm原始输出：\n",text) # llama输出的所有信息。

        text = text.replace("<s> "+prompt, "").strip()

        # result = text.replace("<s> "+prompt, "").strip()[:-4]
        reasons_pattern = re.compile(r'Reasons:\s*(.*?)\s*Response:', re.DOTALL)
        response_pattern = re.compile(r'Response:\s*(.*)', re.DOTALL)
        # like = re.findall(r"Response:\s*(.*?)$", text, re.MULTILINE)
        # reason = re.findall(r"Reasons:\s*(.*?)$", text, re.MULTILINE)
        reasons_match = reasons_pattern.search(text)
        if reasons_match:
            reasons_content = reasons_match.group(1).strip()

        response_match = response_pattern.search(text)
        if response_match:
            response_content = response_match.group(1).strip()
        result = {
            "like": response_content.replace("</s>", "").strip(),
            "reason": reasons_content
        }
        return result