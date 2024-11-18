# 推特数据分析工具

**中文** | [English](./README.md)

## 📚 **概述**
本项目提供了一套完整的推特（X）数据分析管道。包括基于关键词和日期的推文爬取、评论和用户信息检索，随后进行关键词提取、情感分析和统计描述。

---

## 🛠️ **功能特点**

### **1. 推特数据爬取**
- 基于指定的关键词和日期爬取推文、用户信息和评论。
- 提取结构化数据，包括：
  - 推文元数据（内容、点赞、转发、回复数和发布时间）。
  - 用户信息（粉丝数、位置等）。
  - 与推文相关的评论。

### **2. 数据清洗与预处理**
- **JSON 转 Excel**：
  - 合并并处理包含推文、用户信息和评论的原始 JSON 文件。
  - 将数据转换为结构化的 Excel 文件（`.xlsx`），包含三个工作表：
    - **Main Data**：推文详细信息。
    - **Comments**：关联评论信息。
    - **Users**：用户信息。

- **预处理方法**：
  - 删除重复和无关记录。
  - 清理特殊字符（例如移除 `@` 提及）。
  - 统一日期格式并处理缺失值。

### **3. 情感分析**
- 使用高级模型将推文和评论分类为预定义的情感类别。
- **分类系统 prompt**：
  ```plaintext
  You are an advanced language model trained to analyze the sentiment of a given text. Your task is to classify the text into one of the following categories:

  1. Positive
  2. Negative
  3. Objective
  4. Sarcastic
  5. Neutral
  6. Disappointment
  7. Disgust
  8. Contempt
  9. Hate

  For the input text, determine the most appropriate category based on its emotional tone, intent, and context. Return only the category name as the output, with no additional explanation or commentary.
  ```
- 支持的情感类别包括：
  - **积极（Positive）**、**消极（Negative）**、**中立（Neutral）**、**讽刺（Sarcastic）**、**仇恨（Hate）**、**失望（Disappointment）**、**蔑视（Contempt）**、**厌恶（Disgust）**。
- 可视化情感随时间变化的趋势。

### **4. 语言与文化背景分析**
- 分析推文和评论的语言分布。
- 生成：
  - 语言分布饼图。
  - 语言概况以展示文化趋势。

### **5. 关键词和主题分析**
- 使用以下方法提取关键词和主题：
  - **TF-IDF**：识别频繁讨论的主题。
  - **TextRank**：使用基于图的排序方法高亮关键短语。
- 创建词云和条形图直观展示关键词信息。

### **6. 统计与互动分析**
- 测量推文互动情况：
  - 分析点赞、转发和评论的分布。
  - 使用柱状图展示互动总量和平均值。
- 研究情感分布和互动随时间的趋势。

### **7. 网络与共现分析**
- 构建以下网络：
  - **关键词共现**：突出频繁提及术语之间的关系。
  - **推文传播**：分析推文的转发或评论关系。
- 导出 `.gexf` 格式的网络文件，可在 Gephi 等可视化工具中使用。

### **8. 自动化报告生成**
- 将分析结果汇总为 `.docx` 报告，包括：
  - 数据洞察。
  - 情感和语言趋势。
  - 关键词亮点和互动统计。

---

## 📋 **快速开始**

### **1. 克隆仓库**
```bash
git clone https://github.com/AquariniqueMu/TwitterCrawl4Analysis.git
cd TwitterCrawl4Analysis
```

### **2. 安装依赖**
- Python 版本要求：`>=3.8`（**推荐使用 Python 3.12.5**）
- 安装所需库：
  ```bash
  pip install -r requirements.txt
  ```

### **3. 运行代码**

本项目使用 **Jupyter Notebook** 文件（`.ipynb`）完成各步骤分析。按照以下步骤运行：

#### (1) **数据爬取**
- 打开 `twitter_crawl.ipynb`。
- 配置关键词、日期和推特账号信息，逐个运行每个代码单元，完成推文、评论和用户信息的爬取。

#### (2) **数据预处理**
- 打开 `json_process.ipynb`。
- 运行所有代码单元，将原始 JSON 文件转换为结构化的 Excel 文件（`.xlsx`）。

#### (3) **数据分析**
- 针对具体分析目标：
  - **情感分析**：打开并运行 `analysis_emotion.ipynb`。
  - **关键词和趋势分析**：打开并运行 `analysis_keyword_and_trend.ipynb`。
  - **语言分布分析**：打开并运行 `analysis_language.ipynb`。
  - **用户分析**：打开并运行 `analysis_user.ipynb`。


---

## 📊 **输出结果**

### **处理后数据**
- **Excel 文件**：
  - 包含三个工作表：`Main Data`、`Comments` 和 `Users`。

### **可视化**
- **图表**：
  - 情感分布柱状图。
  - 关键词趋势和词云图。
  - 语言分布饼图。
  - 互动与情感随时间的趋势。

---

## 🛠️ **关键工具与库**
- **数据爬取**：`Selenium`、`requests`、`webdriver-manager`
- **数据处理**：`Pandas`、`JSON`、`OpenPyXL`
- **情感分析**：`Transformers`、`OpenAI API`
- **关键词提取**：`SpaCy`、`TF-IDF`、`TextRank`
- **统计分析**：`Matplotlib`、`Seaborn`、`WordCloud`
- **网络分析**：`NetworkX`、`Gephi`

---

## 💡 **自定义**
- **关键词**：在 notebook 文件中直接修改关键词以爬取特定主题。
- **情感分析**：在 `analysis_emotion.ipynb` 中调整情感分析的 prompt 以适配定制需求。
- **可视化**：在各分析 notebook 中修改图表样式和布局。

---

## 📜 **许可证**
本项目基于 MIT 许可证开源。详情请查看 `LICENSE` 文件。

---

## 🙏 **致谢**
- 感谢 [hanxinkong](https://github.com/hanxinkong) 和 [CX330Blake](https://github.com/CX330Blake) 提供的推特爬取工具，以及[Stopwords ISO](https://github.com/stopwords-iso/stopwords-iso)，它们构成了本项目的基础。
