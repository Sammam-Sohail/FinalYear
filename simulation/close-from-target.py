import numpy as np
import math

target1 = 110
target2 = 2550
# 240,2300
val = [95,93,105,70,83]
val2 = [2200,2330,2000,2334,2400]

#


closest2 = min(val2, key=lambda x:abs(x-target2))
closest = min(val, key=lambda x:abs(x-target1))

# dis = math.dist([target1],[closest])
# dis2 = math.dist([target2],[closest2])
dis = (closest/target1 ) * 100
dis2 = (closest2/target2 ) * 100
print(dis,dis2)
print(target1-closest,target2-closest2)
# print((target-closest)/(target))

# print(dis)


#targets not ahieved in timeframe