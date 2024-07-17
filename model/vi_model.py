import joblib

# 加载模型
clf = joblib.load('./model/decision_tree_model.pkl')

# 打印模型
print(clf)

from pprint import pprint
pprint(vars(clf))

from sklearn.tree import export_text

tree_rules = export_text(clf)
print(tree_rules)

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(20,10))
plot_tree(clf, filled=True, feature_names=['feature1', 'feature2', 'feature3', 'feature4'], class_names=['class1', 'class2'])
plt.show()