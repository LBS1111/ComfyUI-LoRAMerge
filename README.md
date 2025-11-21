# ComfyUI-LoRAMerge

![LoRA Merge Logo/Banner (Optional: You can add an image here)](https://placehold.co/600x150/2E8B57/white/png?text=ComfyUI-LoRAMerge)

A specialized set of custom nodes for ComfyUI designed for **zero-input** loading, precise **merging**, and **automatic saving** of LoRA model weights. This plugin is essential for seamlessly managing and combining the effects of multiple LoRA models.

## ✨ Key Features

* **Zero-Input LoRA Selection:** The dedicated `LoRADataEmitter` node allows you to select and extract LoRA weights independently, without needing to connect a base model input.
* **Linear Merge Core:** The `LoRAMerger` node provides fine-grained control over the mixing ratio using the `ratio` parameter, determining the contribution of LoRA A and LoRA B (from 0.0 to 1.0).
* **Automatic Unique Saving:** The `LoRASaver` automatically appends a timestamp to the filename of the merged model, guaranteeing a unique file name for every save operation and preventing accidental file overwrites.
* **Workflow Separation:** Designed to handle the LoRA data stream separately from the main image generation workflow.

## 📦 Node List

All nodes can be found in the menu under **`LoRAMerge/Tools`**.

| Node Name | Function | Input Type | Output Type |
| :--- | :--- | :--- | :--- |
| **LoRA数据发射器 (Dict输出)** | Independently loads the selected LoRA file and extracts the raw weights. | **(Zero Inputs)** | `LORA_DATA` (Custom LoRA Dictionary) |
| **LoRA数据融合器 (Merge)** | Blends two `LORA_DATA` inputs based on the defined `ratio`. | `LORA_DATA A`, `LORA_DATA B`, `FLOAT (ratio)` | `LORA_DATA` (Merged Dictionary) |
| **LoRA模型保存器 (Save)** | Saves the input `LORA_DATA` dictionary as a new `.safetensors` model file with a unique, timestamped name. | `LORA_DATA` | `STRING` (Save Status, used to trigger the workflow) |

## 🚀 Installation

1.  **Stop ComfyUI:** Ensure your ComfyUI backend server is completely shut down.
2.  **Clone the Repository:** Open your command line or Git Bash and navigate to the `custom_nodes` folder:
    ```bash
    cd [Your ComfyUI Path]/ComfyUI/custom_nodes/
    ```
    Execute the clone command (using your actual URL):
    ```bash
    git clone [Your GitHub Repository URL] ComfyUI-LoRAMerge
    ```
3.  **Restart ComfyUI:** Start ComfyUI. The new nodes will appear under the **`LoRAMerge/Tools`** menu.

## 💡 Example Workflow: Merge and Save

This workflow demonstrates how to successfully merge two LoRAs and save the result:

1.  **Create Emitters A & B:**
    * Add two `LoRA数据发射器 (Dict输出)` nodes.
    * Select LoRA A and LoRA B files respectively.
2.  **Create Merger:**
    * Add the `LoRA数据融合器 (Merge)` node.
    * Connect the `LORA_WEIGHTS_DICT` outputs from the Emitters to the Merger's `lora_data_a` and `lora_data_b` inputs.
    * Adjust the `ratio` (e.g., 0.50 for a 50/50 mix).
3.  **Create Saver:**
    * Add the `LoRA模型保存器 (Save)` node.
    * Connect the Merger's `LORA_WEIGHTS_MERGED` output to the Saver's `lora_data` input.
    * Change the `filename_prefix` (e.g., `my_merged_lora/style_char_v1`).
4.  **Connect to Main Flow (Crucial for Execution):**
    * Add a **`Print Text`** or **`Primitive`** node.
    * Connect the **Saver's `SAVE_STATUS`** output to the input of the `Print Text` node.
    * The `Print Text` node (or any element in this chain) **must** be connected somewhere to your main image generation flow (e.g., to an unused input of a `Preview Image` node) to force ComfyUI to execute the save chain when you click `Queue Prompt`.

**Save Location:**

The final `.safetensors` file will be saved in your ComfyUI **`output`** folder, with an automatic timestamp appended. Example file path:

`ComfyUI/output/my_merged_lora/style_char_v1_20251121_195500.safetensors`

## License

This project is licensed under the [Specify your preferred license, e.g., MIT License].
