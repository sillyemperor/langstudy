from decimal import Decimal, getcontext
getcontext().prec=50000

pi = 0
for k in range(10000):
    pi += 1/Decimal(16)**k *\
          (Decimal(4)/(8*k+1) -
           Decimal(2)/(8*k+4) -
           Decimal(1)/(8*k+5) -
           Decimal(1)/(8*k+6))
    if k % 100 == 99:
        print(k, pi)
