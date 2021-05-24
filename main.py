#这是小程序的实现文件

import pandas as pd
from RDA import *
import dp_program as dp
from random_seq import *
from tkinter import *

class Smallprogram:
    def __init__(self, model):
        self.model = model
        self.state = 'off'

        self.root = Tk()
        self.root.title(self.model)
        self.lb_state = Label(self.root, text=self.state, fg='red', bg='yellow')
        self.lb_state.grid()
        self.bn_state = Button(self.root, text='On/Off', command=self.on_off)
        self.bn_state.grid()

        self.bn_fun1 = Button(self.root, text='进行序列比对', command=self.fun1)
        self.bn_fun1.grid(row=0, column=1, columnspan=2, rowspan=2)
        self.bn_fun2 = Button(self.root, text='进行差异分析', command=self.fun2)
        self.bn_fun2.grid(row=0, column=3, columnspan=2, rowspan=2)
        self.bn_fun3 = Button(self.root, text='产生随机序列', command=self.fun3)
        self.bn_fun3.grid(row=0, column=5, columnspan=2, rowspan=2)

        self.lb_seq1 = Label(self.root, text="第一条序列")
        self.lb_seq1.grid(row=3, column=1)
        self.Et_seq1 = Entry(self.root, bd=2)
        self.Et_seq1.grid(row=4, column=1)
        self.lb_seq2 = Label(self.root, text="第二条序列")
        self.lb_seq2.grid(row=5, column=1)
        self.Et_seq2 = Entry(self.root, bd=2)
        self.Et_seq2.grid(row=6, column=1)

        self.lb_file = Label(self.root, text="需要读取的文件")
        self.lb_file.grid(row=3, column=3)
        self.Et_file = Entry(self.root, bd=2)
        self.Et_file.grid(row=5, column=3)

        self.lb_n = Label(self.root, text="序列数量")
        self.lb_n.grid(row=3,column=5)
        self.Et_n = Entry(self.root, bd=2)
        self.Et_n.grid(row=4,column=5)
        self.lb_m = Label(self.root, text="序列长度")
        self.lb_m.grid(row=5,column=5)
        self.Et_m = Entry(self.root, bd=2)
        self.Et_m.grid(row=6,column=5)

        self.notion1 = Label(self.root, text="欢迎使用基因工厂小程序\n通过查看源代码和报告以获取帮助", fg='red')
        self.notion1.grid(row=0, column=7, rowspan=2)
        self.notion2 = Label(self.root, text="程序暂无响应")
        self.notion2.grid(row=2, column=7, rowspan=5)

        self.root.mainloop()

    def on_off(self):
        if self.state == 'off':
            self.state = 'on'
        else:
            self.state = 'off'
        self.lb_state['text'] = self.state

    def fun1(self):
        """实现第一个功能"""
        if self.state == 'on':
            seq1=self.Et_seq1.get()
            seq2=self.Et_seq2.get()
            (max_score,s1,s2)=dp.main(seq1,seq2)
            self.notion2['text']="最高得分为：" + str(max_score) + '\n' + "最佳匹配方式为：" + '\n' + s1 + '\n' + s2 + '\n' + "序列比对完成！"

    def fun2(self):
        """实现第二个功能"""
        if self.state == 'on':
            # 载入数据，数据已经进行了log操作（normalization），数值可以直接进行利用
            filename=self.Et_file.get()
            data = pd.read_table(filename, header=0, index_col=0)

            #进行差异分析
            features=RDA(data)

            filename="feature_names.txt"
            with open(filename, 'w') as file_object:
                for i in range(len(features)):
                    file_object.write(features[i])
                    file_object.write('\n')
                file_object.write("共筛选出"+str(len(features))+"个特征")

            self.notion2['text'] = "筛选得出的miRNA或RNA已保存在文件中\n将其对应的分值进行绘图并保存\n差异分析完成！"

    def fun3(self):
        """实现第三个功能"""
        if self.state == 'on':
            n=self.Et_n.get()
            m=self.Et_m.get()
            n=int(n)
            m=int(m)
            seqs=Random_seqs(n,m)

            filename='seqs.txt'
            with open(filename, 'w') as file_object:
                for i in range(len(seqs)):
                    file_object.write(seqs[i])
                    file_object.write('\n')

            self.notion2['text'] = "产生的第一条序列为：\n" + seqs[0] + "\n其它序列已经保存在文件中\n产生随机序列完成！"


smallprogram = Smallprogram('基因工厂小程序1.0')
