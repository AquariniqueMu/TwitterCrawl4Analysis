Here’s the updated English README based on the changes made to the Chinese version:

---

# Twitter Data Analysis Tool

[中文](./README_zh.md) | **English**

## 📚 **Overview**
This project provides a comprehensive pipeline for analyzing Twitter (X) data, including crawling tweets, retrieving comments and user information based on keywords and date ranges, and further performing keyword extraction, sentiment analysis, and statistical descriptions.

---

## 🛠️ **Features**

### **1. Twitter Data Crawling**
- Crawl tweets, user information, and comments based on specified keywords and date ranges.
- Extract structured data, including:
  - Tweet metadata (content, likes, retweets, replies, and timestamps).
  - User information (followers, location, etc.).
  - Comments related to the tweets.

### **2. Data Cleaning and Preprocessing**
- **Convert JSON to Excel**:
  - Merge and process raw JSON files containing tweets, user information, and comments.
  - Convert data into structured Excel files (`.xlsx`) with three sheets:
    - **Main Data**: Detailed tweet information.
    - **Comments**: Associated comment data.
    - **Users**: User profile data.

- **Preprocessing Methods**:
  - Remove duplicate and irrelevant records.
  - Clean special characters (e.g., removing `@` mentions).
  - Standardize date formats and handle missing values.

### **3. Sentiment Analysis**
- Classify tweets and comments into predefined sentiment categories using advanced models.
- **Classification System Prompt**:
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
- Supported sentiment categories include:
  - **Positive**, **Negative**, **Neutral**, **Sarcastic**, **Hate**, **Disappointment**, **Contempt**, **Disgust**.
- Visualize sentiment trends over time.

### **4. Language and Cultural Background Analysis**
- Analyze language distribution in tweets and comments.
- Generate:
  - Language distribution pie charts.
  - Language profiles to showcase cultural trends.

### **5. Keyword and Topic Analysis**
- Extract keywords and topics using:
  - **TF-IDF**: Identify frequently discussed topics.
  - **TextRank**: Highlight key phrases using graph-based ranking methods.
- Create word clouds and bar charts for intuitive visualization of keyword information.

### **6. Statistical and Engagement Analysis**
- Measure tweet engagement:
  - Analyze distributions of likes, retweets, and comments.
  - Use bar charts to display total and average engagement.
- Explore sentiment distributions and engagement trends over time.

### **7. Network and Co-occurrence Analysis**
- Build networks:
  - **Keyword Co-occurrence**: Highlight relationships between frequently mentioned terms.
  - **Tweet Propagation**: Analyze retweet or comment relationships in tweets.
- Export networks in `.gexf` format for visualization in tools like Gephi.

### **8. Automated Report Generation**
- Summarize analysis results into a `.docx` report, including:
  - Data insights.
  - Sentiment and language trends.
  - Keyword highlights and engagement statistics.

---

## 📋 **Quick Start**

### **1. Clone the Repository**
```bash
git clone https://github.com/AquariniqueMu/TwitterCrawl4Analysis.git
cd TwitterCrawl4Analysis
```

### **2. Install Dependencies**
- Python version: `>=3.8` (**Recommended: Python 3.12.5**)
- Install required libraries:
  ```bash
  pip install -r requirements.txt
  ```

### **3. Running the Pipeline**

This project uses **Jupyter Notebook** files (`.ipynb`) for all steps of the analysis. Follow the steps below:

#### (1) **Data Crawling**
- Open `twitter_crawl.ipynb`.
- Configure the keywords, date range, and Twitter account information. Execute each cell to crawl tweets, comments, and user information.

#### (2) **Data Preprocessing**
- Open `json_process.ipynb`.
- Execute all cells to convert raw JSON files into structured Excel files (`.xlsx`).

#### (3) **Data Analysis**
- For specific analysis tasks:
  - **Sentiment Analysis**: Open and run `analysis_emotion.ipynb`.
  - **Keyword and Trend Analysis**: Open and run `analysis_keyword_and_trend.ipynb`.
  - **Language Distribution Analysis**: Open and run `analysis_language.ipynb`.
  - **User Analysis**: Open and run `analysis_user.ipynb`.

---

## 📊 **Outputs**

### **Processed Data**
- **Excel Files**:
  - Three sheets: `Main Data`, `Comments`, and `Users`.

### **Visualizations**
- **Charts**:
  - Sentiment distribution bar charts.
  - Keyword trends and word clouds.
  - Language distribution pie charts.
  - Engagement and sentiment trends over time.

---

## 🛠️ **Key Tools and Libraries**
- **Data Crawling**: `Selenium`, `requests`, `webdriver-manager`
- **Data Processing**: `Pandas`, `JSON`, `OpenPyXL`
- **Sentiment Analysis**: `Transformers`, `OpenAI API`
- **Keyword Extraction**: `SpaCy`, `TF-IDF`, `TextRank`
- **Statistical Analysis**: `Matplotlib`, `Seaborn`, `WordCloud`
- **Network Analysis**: `NetworkX`, `Gephi`

---

## 💡 **Customization**
- **Keywords**: Modify keywords directly in the notebook files to crawl specific topics.
- **Sentiment Analysis**: Adjust the sentiment analysis prompt in `analysis_emotion.ipynb` for tailored analysis.
- **Visualizations**: Modify chart styles and layouts in the analysis notebooks.

---

## 📜 **License**
This project is open-sourced under the MIT License. See the `LICENSE` file for details.

---

## 🙏 **Acknowledgments**
- Thanks to [hanxinkong](https://github.com/hanxinkong) and [CX330Blake](https://github.com/CX330Blake) for their Twitter crawling tools, as well as [Stopwords ISO](https://github.com/stopwords-iso/stopwords-iso), which formed the foundation of this project.

--- 