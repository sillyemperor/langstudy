def pn(n):
    NS = [2,3,5,7]
    if n < 1:
        return False
    if n in NS:
        return True
    if any([ not n % x for x in NS]):
        return False
    return True


for i in range(100):
    if(pn(i)):
        print(i)


