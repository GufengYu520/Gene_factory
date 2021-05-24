#该文件实现第二个功能——差异分析
#把患病的人作为群体对待，然后找患病群体和正常群体表达值差异比较大的miRNA或者mRNA。
#导入包
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

#t-test函数，返回p-value
def t_test(a,b):
    a=np.array(a)
    b=np.array(b)
    t1, p1=stats.levene(a,b)
    if p1>0.05:
        t2, p2=stats.ttest_ind(a, b, equal_var=False)
    else:
        t2, p2=stats.ttest_ind(a,b)
    return p2

def RDA(data):
    # 每个基因（行）BH样本（正常人员）的表达平均值和方差
    bh = data.loc[:, 'BH11399-2_NBZX27_(HG-U133_Plus_2)' : 'BH11399-2_NZMY24_(HG-U133_Plus_2)']
    bh_mean = data.loc[:, 'BH11399-2_NBZX27_(HG-U133_Plus_2)' : 'BH11399-2_NZMY24_(HG-U133_Plus_2)'].mean(axis=1)
    bh_var = data.loc[:, 'BH11399-2_NBZX27_(HG-U133_Plus_2)' : 'BH11399-2_NZMY24_(HG-U133_Plus_2)'].var(axis=1)

    # 每个基因（行）US样本（病人）的表达平均值和方差
    us = data.loc[:, 'US-1047659':'US-1137753']
    us_mean = data.loc[:, 'US-1047659':'US-1137753'].mean(axis=1)
    us_var = data.loc[:, 'US-1047659':'US-1137753'].var(axis=1)

    cout = []  # 得到的差异表达值fold change

    RNA_list = []  # 筛选出的miRNA或mRNA序号
    RNA_list_up = []  # 筛选出的miRNA_up或mRNA_up组序号
    RNA_list_down = []  # 筛选出的miRNA_down或mRNA_down组序号
    RNA_cout = []  # 筛选出的miRNA或mRNA对应的差异表达值
    RNA_cout_up = []  # 筛选出的miRNA_up或mRNA_up对应的差异表达值
    RNA_cout_down = []  # 筛选出的miRNA_down或mRNA_down对应的差异表达值

    # 设置阈值进行筛选（同时也进行了统计检验）
    for i in range(data.shape[0]):
        if bh_mean[i] != 0:
            x = us_mean[i] / bh_mean[i]
        else:
            x = 0
        cout.append(x)

    for i in range(data.shape[0]):
        p = t_test(us.iloc[i, :], bh.iloc[i, :])
        if cout[i] > 2 and p<0.05:
            RNA_list_up.append(i)
            RNA_cout_up.append(cout[i])
            RNA_list.append(i)
            RNA_cout.append(cout[i])
        if cout[i] < 0.5 and cout[i] > 0 and p<0.05:
            RNA_list_down.append(i)
            RNA_cout_down.append(-1 / cout[i])
            RNA_list.append(i)
            RNA_cout.append(-1 / cout[i])

    RNA_names = []  # 筛选出来的miRNA或mRNA名称
    RNA_names_up = []
    RNA_names_down = []

    for i in range(len(RNA_list)):
        RNA_names.append(data.index[RNA_list[i]])
    for i in range(len(RNA_list_up)):
        RNA_names_up.append(data.index[RNA_list_up[i]])
    for i in range(len(RNA_list_down)):
        RNA_names_down.append(data.index[RNA_list_down[i]])

    # 将得到的分数值进行绘图
    plt.figure()
    plt.bar(RNA_names, RNA_cout)
    plt.xticks(rotation=60)

    plt.savefig('bar.png', dpi=1600)

    return RNA_names