#该文件实现第一个功能——序列全局比对

from collections import namedtuple

F = namedtuple('F', ('score', 'pointer'))

# 初始化二维矩阵， # 生成 x行，y列的二维矩阵，初始化第0行，0列的元素
def init_array(x, y):
    array = [[0] * (y) for _ in range(x)]
    array[0][0] = F(0, None)
    for j in range(1, y):
        array[0][j] = F((-5)*j, [0, j-1])
    for i in range(1, x):
        array[i][0] = F((-5)*i, [i-1, 0])
    return array

# 一行一行的计算矩阵中的每个各自中的最优结果。当前格子中的最优结果由它的三个来源推出
def compute(array, seq1, seq2):
    row, col = len(seq2), len(seq1)
    for i in range(1, row+1):
        for j in range(1, col+1):
            if seq1[j-1] == seq2[i-1]:  # 这里简化了得分矩阵，完全匹配得10分，不完全得5分，有gap减5分
                s = 10
            else:
                s = 5
            lu = [array[i-1][j-1].score+s, [i-1, j-1]] # idx 0：最大得分，idx 1：来源坐标
            left = [array[i-1][j].score-5, [i-1, j]]
            up = [array[i][j-1].score-5, [i, j-1]]
            max_choice = max([lu,left, up], key=lambda x: x[0])
            score= max_choice[0]
            pointer = max_choice[1]
            array[i][j] = F(score, pointer)  # 在当前保存最大得分，和来源坐标，方便回溯。
    return array

# 回溯。从（m,n）一直回溯到（0，0）
def backtrack(array, seq1, seq2):
    s1 = []
    s2 = []
    row, col = len(seq2), len(seq1)
    while array[row][col].score != 0:
        i, j = array[row][col].pointer # pointer 指向来源方的坐标
        if i+1 == row and j+1 == col: # 左上方
            s1.append(seq1[col-1])
            s2.append(seq2[row-1])
            row, col = i, j
        elif row == i+1 and col == j: # 来源：上方
            s1.append("-")
            s2.append(seq2[i])
            row, col = i, j
        elif row == i and col == j+1: # 左方
            s1.append(seq1[j])
            s2.append("-")
            row, col = i, j
    s1 = ''.join(s1[::-1])  #因为是从最后往前回溯的，需要将逆转一下list
    s2 = ''.join(s2[::-1])
    return s1, s2

def main(seq1, seq2):
    x, y = len(seq2)+1 , len(seq1)+1 # x是矩阵行数，y是矩阵列数

    array = init_array(x, y)
    array = compute(array, seq1, seq2)
    s1, s2 = backtrack(array, seq1, seq2)
    max_score = array[x-1][y-1].score

    return max_score,s1,s2

