# ComfyUI-LoRAMerge

![ComfyUI-LoRAMerge 典型工作流](https://raw.githubusercontent.com/LBS1111/ComfyUI-LoRAMerge/refs/heads/main/6b2ce1166e64f087814f2fbd77cd08cf.png)
一个专为 ComfyUI 设计的自定义节点集，用于**零输入**加载、精确**融合**和**自动保存** LoRA 模型权重。完美解决了多个 LoRA 模型效果叠加和文件管理的需求。

---

## ✨ 核心特性 (Key Features)

* **🚀 多模式融合核心：** 提供 **Linear (线性)**、**Additive (相加)** 和 **Multiplicative (乘法)** 三种融合模式，通过 `ratio` 参数对 LoRA 权重进行精确控制。
* **💾 自动命名保存：** `LoRA模型保存器` 自动添加时间戳后缀，确保每次保存都生成一个唯一的文件名，彻底避免文件覆盖问题。
* **🧩 零输入 LoRA 选择：** `LoRA数据发射器` 独立工作，无需连接 Base Model 输入，即可选择和提取 LoRA 权重。
* **🧪 LoRA 数据流分离：** 专为 LoRA 数据流设计，实现 LoRA 融合与图像生成主工作流的分离。

## 🔬 融合模式详解 (Fusion Mode Details)

`LoRA数据融合器` 提供了三种不同的权重叠加方式，以应对不同的融合需求：

| 模式 (Mode) | 描述 | 适用场景 |
| :--- | :--- | :--- |
| **Linear (线性)** | **默认模式。** 使用加权平均公式：$W_{merged} = (1 - \alpha) \cdot W_A + \alpha \cdot W_B$ | 适用于平衡两种风格，使输出介于两者之间。 |
| **Additive (相加)** | **叠加模式。** 使用 $W_{merged} = W_A + \alpha \cdot W_B$ (其中 $\alpha=ratio$)。 | 适用于将 LoRA B 的效果以一定强度（$\alpha$）**叠加**到 LoRA A 上。 |
| **Multiplicative (乘法)** | **叠加模式。** 使用 $W_{merged} = W_A + \alpha \cdot W_B$ (其中 $\alpha=ratio$)。 | 在 LoRA 语境中，提供与 Additive 相似的叠加效果，常用于强调某种特征的缩放和融合。 |

## 📦 节点列表 (Node List)

所有节点位于 ComfyUI 菜单 **`LoRAMerge/Tools`** 下。

| 节点名称 | 作用 | 输入类型 | 输出类型 |
| :--- | :--- | :--- | :--- |
| **LoRA数据发射器 (Dict输出)** | 独立加载选定的 LoRA 文件。 | **(零输入)** | `LORA_DATA` (自定义 LoRA 字典) |
| **LoRA数据融合器 (Merge)** | **核心节点。** 根据 `ratio` 和 `mode`，融合两个 LoRA 权重。 | `LORA_DATA A`, `LORA_DATA B`, `FLOAT (ratio)`, **`STRING (mode)`** | `LORA_DATA` (融合后的字典) |
| **LoRA模型保存器 (Save)** | 将输入的 `LORA_DATA` 字典保存为 `.safetensors` 模型文件。 | `LORA_DATA`, `STRING (filename_prefix)` | `STRING` (保存状态，用于触发工作流) |

## 🚀 安装步骤

1.  **关闭 ComfyUI：** 确保您的 ComfyUI 后台服务已完全停止。
2.  **克隆仓库：** 打开命令行或 Git Bash，进入 ComfyUI 的 `custom_nodes` 文件夹：
    ```bash
    cd [您的ComfyUI路径]/ComfyUI/custom_nodes/
    ```
    执行克隆命令：
    ```bash
    git clone https://github.com/LBS1111/ComfyUI-LoRAMerge.git
    ```
3.  **重启 ComfyUI：** 启动 ComfyUI，节点将出现在 **`LoRAMerge/Tools`** 菜单下。

## 💡 典型工作流：融合与保存

1.  **加载数据：** 创建两个 `LoRA数据发射器`，分别选择 LoRA A 和 LoRA B。
2.  **设置融合：**
    * 添加 `LoRA数据融合器 (Merge)`。
    * 连接 LoRA A 和 B 的输出。
    * 选择您需要的 **`mode`** (Linear, Additive, Multiplicative)。
    * 调整 **`ratio`** (例如 0.54)。
3.  **保存文件：**
    * 添加 `LoRA模型保存器 (Save)`。
    * 连接融合器的输出到 `lora_data`。
    * 设置 `filename_prefix` (例如 `my_merged_lora/style_char_v1`)。
4.  **触发执行 (重要)：** 将 **保存器** 的 **`SAVE_STATUS`** 输出连接到您的图像生成主流程中的一个节点（例如 `Print Text` 或 `Preview Image` 的隐藏输入），以确保点击 `Queue Prompt` 时，保存操作被执行。

**保存位置：**

融合后的 `.safetensors` 文件将保存到您的 ComfyUI **`output`** 文件夹中，例如：
`ComfyUI/output/my_merged_lora/style_char_v1_20251121_195500.safetensors`

## 许可证

本项目遵循 [MIT License / Apache License 2.0  ] 许可。
