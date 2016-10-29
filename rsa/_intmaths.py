"""This module contains some integer maths functions. They are:
   gcd
   modpower
   modinverse
   rooflog
"""


def gcd(x, y, *z) :
    """
    Returns the GCD of the arguments.
    Solves by using Euclid's division lemma. """
    # Input validation
    def entrycheck(x, y) :
        return x < 1 or y < 1 or x != int(x) or y != int(y)
    
    # Compute if two entries given
    if len(z) == 0 :
        if entrycheck(x, y) : return "Error"
        
        x, y = max(x, y), min(x, y)
        while y > 0 :
            x, y = y, x%y
        return x
    
    # Else recurse
    else :
        ans=gcd(x,y)
        i=0
        while i < len(z) and ans > 1:
            ans = gcd(ans, z[i])
            i=i+1
        return ans

def modpower (base,power,mod) :
    """ Returns base**power(mod mod)"""
    if power == 0:
        return 1
    c=1
    while power>1 :
        if power%2 :
            c *= base
            c %= mod
        base *= base
        base %= mod
        power /= 2
    return (c*base)%mod

def modinverse(a,m):
    """ 
    Returns the multiplicative inverse of a in Z/Z[m]
    Uses extended euclidean algorithm.
    """
    # Code is very cryptic. I didn't completely understand it while making it also.
    r1=a
    r2=m
    x_2=1
    y_2=0
    x_1=0
    y_1=1
    while (x_1*r1+y_1*r2)>1:
        q=(x_2*r1+y_2*r2)/(x_1*r1+y_1*r2)
        x_2,x_1=x_1,x_2-q*x_1
        y_2,y_1=y_1,y_2-q*y_1
    return x_1%m

def rooflog(n,base=2):
    """
    Return roof(logbase(n)). Which is basically the number of (base)its required to store n.
    Works only with integers."""
    n-=1
    i=0
    while n!=0:
        n/=base
        i+=1
    return i
