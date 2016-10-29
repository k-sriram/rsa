"""Contains the key generation function for rsa."""


from random import randint

import rsa._prime as prime
import rsa._intmaths as intmaths

def generate_key(primeno):
    '''Generates an rsa key with the two primes being upto the prime number just after primeno. Returns a list [n,e,d]'''
    p=prime.next_prime(randint(primeno/10,primeno))  #the two primes are p and q
    q=prime.next_prime(randint(primeno/10,primeno))
    n=p*q
    Q=(p-1)*(q-1)  #Q looks like phi. Q=totient(n)
    e=randint(1,Q-1)
    while intmaths.gcd(e,Q)!=1:
        e = randint(1,Q-1)
    d = intmaths.modinverse(e,Q)
    return [n,e,d]
