import json
import pandas as pd

def save_to_json(data, filename):
    """
    保存数据为 JSON 文件。
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_to_excel(data, filename):
    """
    保存数据为 Excel 文件。
    """
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
