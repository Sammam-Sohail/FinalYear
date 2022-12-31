import random
import time
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import numpy as np


value = 100
T1 = 101
T2 = 102
T3 = 103
t1achieved = False
t2achieved = False
t3achieved = False
# w1 = 0
# w2 = 0
# w3 = 0

def generate_random_value(mean, stddev):
  value = random.normalvariate(mean, stddev)
  return value

def check_guess(t1,t2,t3,value,t_current):
    # print("current value:", value)
    value = round(generate_random_value(value, random.uniform(3,5)),4)
    l1.append(value)
    global t1achieved
    global t2achieved
    global t3achieved
    global w1
    global w2
    global w3
    global t1achievedtime
    global t2achievedtime
    global t3achievedtime
    if t1 <= value and t1achieved == False:
        # print("T1 achieved!", value)
        t1achieved = True
        # w1 = 1
        t1achievedtime = t_current
    if t2 <= value and t2achieved == False:
        # print("T2 achieved!", value)
        t2achieved = True
        # w2 = 1
        t2achievedtime = t_current
    if t3 <= value and t3achieved == False:
        # print("T3 achieved!", value)
        t3achieved = True
        # w3 = 1
        t3achievedtime = t_current
        return -1
    # else:
        # print("incorrect. Actual value was:", value)

    return value

if __name__ == "__main__":

    eva = dict()
    for i in range(1):
        value = 100
        T1 = 101 + random.uniform(2,3)
        T2 = T1 + random.uniform(2,3)
        T3 = T2 + random.uniform(2,3)
        l1 = list()
        # l2 = list()
        # l3 = list()

        t1achieved = False
        t2achieved = False
        t3achieved = False
        # w1 = 0
        # w2 = 0
        # w3 = 0
        t1achievedtime = 0
        t2achievedtime = 0
        t3achievedtime = 0
        t_end = time.time() + 30 
        t_start = time.time()
        while time.time() < t_end:
            t_current = time.time() - t_start
            value = check_guess(T1,T2,T3,value,t_current)
            if value == -1:
                break
            time.sleep(1)

        secList = [i for i in range(30,0,-1)]
        secList = np.reshape(secList, (-1,1))
        minMaxScaler = MinMaxScaler(feature_range=(0, 1))
        minMaxScaler.fit(secList)
        scaledList = minMaxScaler.transform(secList)
        f1 = scaledList[int(round(t1achievedtime,0))][0]
        f2 = scaledList[int(round(t2achievedtime,0))][0]
        f3 = scaledList[int(round(t3achievedtime,0))][0]

        

        # sD = np.std(l1)
        # print("std:", sD)
        # m = np.mean(l1)
        # print("mean:", m)

        # meanList = list()
        # for i in range(len(l1)):
        #     meanList.append((l1[i] - m) / sD)
        # print(meanList)
        # psum = 0
        # pcount = 0
        # nsum = 0
        # ncount = 0
        # for i in range(len(l1)):
        #     if meanList[i] > 0:
        #         psum += l1[i]
        #         pcount += 1
        #     else:
        #         nsum += l1[i]
        #         ncount += 1
        
        # print("pmean",psum/pcount)
        # if ncount != 0: print("num",nsum/ncount)
        # [0,0.2,0.4,0.6,0.8,1]

        # std = 4


        # p1 = ((T1 - value) / T1)
        # p2 = ((T2 - T1) / T2)
        # p3 = ((T3 - T2) / T3)

        # x = ((p1*w1) + ((p2-p1)*w2) + ((p3-p2)*w3))
        # eva[i] = x
        # print(p1, p2, p3)
        # print(T1, T2, T3)
        # print(w1, w2, w3)
        # print("---->",x)
        # print("T1 achieved at:", t1achievedtime)
        # print("T2 achieved at:", t2achievedtime)
        # print("T3 achieved at:", t3achievedtime)

        
        
    #print sorted eva
    eva = sorted(eva.items(), key=lambda x:x[1])
    # print(eva)
    
