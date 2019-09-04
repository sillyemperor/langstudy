import time

# 计数器，超过10秒计算并打印平均值
def counter():
    count = 0
    tt = time.time()
    while True:
        n = yield
        count += 1
        dlt = time.time() - tt
        if dlt > 10:
            ratio = count/dlt
            print(ratio)
            count = 0
            tt = time.time()