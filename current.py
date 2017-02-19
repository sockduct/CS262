import time

def wrapper(s):
    start = time.clock()
    result = eval(s)
    runtime = time.clock()-start
    return result,runtime

def fibo(n):
  if n<=2:
    return 1
  else:
    return fibo(n-1)+fibo(n-2)

def cacheproc(chart,f,n):
    # Best approach since must return chart[n] in either case
    if n not in chart:
        chart[n] = f(n,chart)
    return chart[n]

def memofibo(n,chart=None):
    if chart == None:
        chart = {}
    if n < 0:
        print "Error!  Fibonacci values are only defined for values >= 0."
        return None
    elif n <= 2:
        return 1
    else:
        return (cacheproc(chart,memofibo,n-1) + cacheproc(chart,memofibo,n-2))

