import os
import torch
import comfy.model_management
from comfy.utils import load_torch_file, save_torch_file
import folder_paths
import numpy as np
import datetime # 用于时间戳命名


# 定义自定义输出类型。
LORA_DATA_TYPE = "LORA_DATA"

# 获取 LoRA 文件列表
LORA_FILE_LIST = folder_paths.get_filename_list("loras")


# ====================================================================
# 节点 A: LoRA 数据发射器 (LoRA Data Emitter)
# --------------------------------------------------------------------
class LoRADataEmitter:
    """
    节点 A: 只加载 LoRA 文件本身，并输出其原始权重数据（LORA_DATA）。
    """
    CATEGORY = "LoRAMerge/Tools"
    FUNCTION = "load_lora_data"
    
    RETURN_TYPES = (LORA_DATA_TYPE,)
    RETURN_NAMES = ("LORA_WEIGHTS_DICT",) 
    
    @classmethod
    def INPUT_TYPES(s):
        lora_options = LORA_FILE_LIST if LORA_FILE_LIST else ["None_Found"]
        default_lora = lora_options[0] if lora_options else "None_Found"

        return {
            "required": {
                "lora_name": (lora_options, {"default": default_lora}),
            }
        }

    def load_lora_data(self, lora_name):
        if lora_name == "None_Found":
            raise Exception("错误：未找到 LoRA 文件。")

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora_model_data = load_torch_file(lora_path)
        
        return (lora_model_data,)


# ====================================================================
# 节点 B: LoRA 数据融合器 (LoRA Merger)
# --------------------------------------------------------------------
class LoRAMerger:
    """
    节点 B: 融合两个 LORA_DATA 字典，并输出融合后的 LORA_DATA。
    """
    CATEGORY = "LoRAMerge/Tools"
    FUNCTION = "merge_loras"
    
    RETURN_TYPES = (LORA_DATA_TYPE,)
    RETURN_NAMES = ("LORA_WEIGHTS_MERGED",)
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_data_a": ("LORA_DATA",), 
                "lora_data_b": ("LORA_DATA",),
                "ratio": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                # 新增模式选择：线性、相加、乘法
                "mode": (["Linear", "Additive", "Multiplicative"], {"default": "Linear"}),
            }
        }

    def merge_loras(self, lora_data_a, lora_data_b, ratio, mode): 
        if not lora_data_a or not lora_data_b:
            raise Exception("错误：LoRA 融合需要两个有效的 LORA_DATA 输入。")

        merged_data = lora_data_a.copy()
        
        for key in merged_data:
            if key in lora_data_b:
                tensor_a = merged_data[key].float() 
                tensor_b = lora_data_b[key].float()
                
                if mode == "Linear":
                    # 模式 1: 线性插值 (Weighted Sum)
                    # 公式: (1 - ratio) * W_A + ratio * W_B
                    merged_tensor = torch.lerp(tensor_a, tensor_b, ratio)
                
                elif mode == "Additive" or mode == "Multiplicative":
                    # 模式 2 & 3: 相加或乘法叠加
                    # 公式: W_A + ratio * W_B (W_B的效果以ratio强度叠加到W_A上)
                    merged_tensor = tensor_a + ratio * tensor_b
                
                else:
                    raise Exception(f"不支持的融合模式: {mode}")

                merged_data[key] = merged_tensor
        
        return (merged_data,)


# ====================================================================
# 节点 C: LoRA 模型保存器 (LoRA Saver)
# --------------------------------------------------------------------
class LoRASaver:
    """
    节点 C: 将 LORA_DATA 字典保存为新的 LoRA 模型文件 (.safetensors)。
    """
    CATEGORY = "LoRAMerge/Tools"
    FUNCTION = "save_lora"

    # 添加 STRING 输出，用于连接到主流程
    RETURN_TYPES = ("STRING",) 
    RETURN_NAMES = ("SAVE_STATUS",) 
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_data": ("LORA_DATA",), 
                "filename_prefix": ("STRING", {"default": "merged_lora/merged"}), 
            },
            # 必须设置 hidden 来触发执行
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}, 
        }

    # 包含 prompt 和 extra_pnginfo 参数，并实现时间戳命名
    def save_lora(self, lora_data, filename_prefix, prompt=None, extra_pnginfo=None): 
        
        # 1. 获取基础保存路径 (默认 output 目录)
        save_path = folder_paths.get_output_directory()
        
        # 2. 自动生成时间戳后缀
        now = datetime.datetime.now()
        timestamp = now.strftime("_%Y%m%d_%H%M%S")
        
        # 3. 构造完整文件名 (前缀 + 时间戳 + 后缀)
        base_prefix = filename_prefix.strip().rstrip('/') 
        filename = f"{base_prefix}{timestamp}.safetensors"
        full_path = os.path.join(save_path, filename)

        # 4. 确保目标目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # 5. 保存文件
        print(f"正在保存融合后的 LoRA 文件到: {full_path}")
        save_torch_file(lora_data, full_path)
        print("LoRA 模型保存完成。")

        # 返回状态消息
        status_message = f"LoRA模型保存完成: {full_path}"
        
        return (status_message,)
        
# ====================================================================
# --- 注册节点 ---
# --------------------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "LoRADataEmitter": LoRADataEmitter,
    "LoRAMerger": LoRAMerger,
    "LoRASaver": LoRASaver, 
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoRADataEmitter": "LoRA数据发射器 (Dict输出)",
    "LoRAMerger": "LoRA数据融合器 (Merge)",
    "LoRASaver": "LoRA模型保存器 (Save)", 
}