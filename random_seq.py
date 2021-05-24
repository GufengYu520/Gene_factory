#该文件实现第三个功能——产生随机序列

import random

def Tranverse(a):
    """将数字序列转化为ATGC"""
    seq=''
    for i in range(len(a)):
        if a[i]==0:
            seq+='A'
        elif a[i]==1:
            seq+='T'
        elif a[i]==2:
            seq+='G'
        else:
            seq+='C'
    return seq

def Random_seqs(n,m):
    """产生随机数字序列，n为序列个数，m为序列的大小长度"""
    seqs=[]
    for i in range(n):
        nums=[]
        for j in range(m):
            nums.append(random.randrange(4))
        seq=Tranverse(nums)
        seqs.append(seq)
    return seqs
