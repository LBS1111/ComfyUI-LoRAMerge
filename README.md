# ComfyUI-LoRAMerge

https://raw.githubusercontent.com/LBS1111/ComfyUI-LoRAMerge/refs/heads/main/2159324ef57f8dd14f26dd7b1e804d1d.png
一个专为 ComfyUI 设计的自定义节点集，用于**零输入**加载、精确**融合**和**自动保存** LoRA 模型权重。完美解决了多个 LoRA 模型效果叠加和文件管理的需求。

---

## ✨ 主要特性

* **零输入 LoRA 选择：** 提供独立的 `LoRA数据发射器` 节点，您无需连接模型输入，即可独立选择和提取 LoRA 权重。
* **线性融合核心：** `LoRA数据融合器` 允许您通过 `ratio` 参数精确控制两个 LoRA 模型 (LoRA A 和 LoRA B) 的混合比例，实现精细的风格或概念叠加。
* **自动命名保存：** `LoRA模型保存器` 自动为融合后的模型添加时间戳，确保每次保存都生成一个唯一的文件名，避免文件覆盖。
* **工作流分离：** 专为 LoRA 数据流设计，实现 LoRA 融合与图像生成工作流的分离。

## 📦 节点列表

所有节点位于菜单 **`LoRAMerge/Tools`** 下。

| 节点名称 | 作用 | 输入类型 | 输出类型 |
| :--- | :--- | :--- | :--- |
| **LoRA数据发射器 (Dict输出)** | 独立加载选定的 LoRA 文件。 | **(零输入)** | `LORA_DATA` (自定义 LoRA 字典) |
| **LoRA数据融合器 (Merge)** | 根据 `ratio` 比例，融合两个 `LORA_DATA` 输入。 | `LORA_DATA A`, `LORA_DATA B`, `FLOAT (ratio)` | `LORA_DATA` (融合后的字典) |
| **LoRA模型保存器 (Save)** | 将输入的 `LORA_DATA` 字典保存为 `.safetensors` 模型文件。 | `LORA_DATA` | `STRING` (保存状态，用于触发工作流) |

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
3.  **重新启动 ComfyUI：** 启动 ComfyUI，节点将出现在 **`LoRAMerge/Tools`** 菜单下。

## 💡 典型工作流：融合与保存

这是一个典型的 LoRA 融合和保存流程的工作流：

1.  **创建发射器 A & B：**
    * 添加两个 `LoRA数据发射器 (Dict输出)`。
    * 分别选择 LoRA A 和 LoRA B 文件。
2.  **创建融合器：**
    * 添加 `LoRA数据融合器 (Merge)` 节点。
    * 将发射器 A 和 B 的 `LORA_WEIGHTS_DICT` 输出连接到 `lora_data_a` 和 `lora_data_b`。
    * 调整 `ratio` (例如 0.54)。
3.  **创建保存器：**
    * 添加 `LoRA模型保存器 (Save)` 节点。
    * 将融合器的 `LORA_WEIGHTS_MERGED` 输出连接到保存器的 `lora_data` 输入。
    * 修改 `filename_prefix` (例如 `my_merged_lora/style_char_v1`)。
4.  **连接到主流程 (触发执行)：**
    * 添加一个 `Print Text` 或 `Primitive` 节点。
    * 将 **保存器** 的 **`SAVE_STATUS`** 输出连接到 `Print Text` 的输入。
    * 将 `Print Text` 连接到您的**图像生成主流程**中的一个节点（例如 `Preview Image` 的隐藏输入或 `VAE Decode` 的隐藏输入），以确保整个链条在 `Queue Prompt` 时被执行。

**保存位置：**

融合后的 `.safetensors` 文件将保存到您的 ComfyUI **`output`** 文件夹中，并自动带上时间戳后缀，例如：
`ComfyUI/output/my_merged_lora/style_char_v1_20251121_195500.safetensors`

## 许可证

本项目遵循 [MIT License / Apache License 2.0 / etc.] 许可。
