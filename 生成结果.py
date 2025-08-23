import pandas as pd
from sklearn.metrics import classification_report

# 读取数据
df = pd.read_excel('D:/优化实验/test/test_all带分类.xlsx')

# # 清洗标签：去除前后空格，统一大小写（如果需要）
# df['ground_truth'] = df['ground_truth'].astype(str).str.strip()
# df['result'] = df['result'].astype(str).str.strip()

# # 如果你想统一大小写，可以取消下面注释
# df['ground_truth'] = df['ground_truth'].str.lower()
# df['result'] = df['result'].str.lower()

# 定义类别名称，确保和数据中的标签完全一致（大小写和空格）
# target_names = ['gameTopic', 'otherTopic', 'financeTopic', 'lawTopic', 'telecomTopic', 'medicineTopic', 'insuranceTopic']

# 转换为列表
y_true = df['ground_truth'].tolist()
y_pred = df['result_fc'].tolist()

# # 打印标签唯一值，确认无误
# print("ground_truth unique labels:", set(y_true))
# print("result unique labels:", set(y_pred))

# 生成分类报告，输出为字典格式
# report_dict = classification_report(y_true, y_pred, target_names=target_names, output_dict=True)
report_dict = classification_report(y_true, y_pred, output_dict=True)

# 转换为 DataFrame，方便保存和查看
report_df = pd.DataFrame(report_dict).transpose()

# 保存到 Excel
report_df.to_excel('D:/优化实验/report/fc_nosft.xlsx')

print("分类报告已保存")

# print(df['ground_truth'].value_counts())
# print(df['result'].value_counts())