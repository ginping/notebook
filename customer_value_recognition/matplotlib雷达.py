import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

data = pd.read_excel('./result/zscoreddata.xls')  # 数据读取
k = 5  # 聚类类别数目

# 调用K-Means算法
model = KMeans(n_clusters=k, n_jobs=1)  # 输入聚类类别数目, n_jobs为并行数
model.fit(data)  # 训练

clu = model.cluster_centers_
x = [1,2,3,4,5]
colors = ['red','green','yellow','blue','black']
for i in range(5):
    plt.plot(x, clu[i], label='clustre' + str(i), linewidth=6-i, color=colors[i], marker='o')
plt.xlabel('L R F M C')
plt.ylabel('value')
plt.show()

labels = np.array(['L','R','F','M','C'])
datalength = 5
fig = plt.figure()
ax = fig.add_subplot(111,polar=True )
for i in range(5):
    data = model.cluster_centers_[i]
    angles = np.linspace(0, 2*np.pi, datalength, endpoint=False)
    data = np.concatenate((data, [data[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    ax.plot(angles, data, linewidth=2)

ax.set_thetagrids(angles * 180/np.pi, labels, fontproperties="SimHei")
ax.set_title('matplotlib雷达图', va='bottom', fontproperties='SimHei')
ax.set_rlim(-1,3)
ax.grid(True)
plt.show()
