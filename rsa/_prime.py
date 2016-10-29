"""This module contains functons for prime numbers: isPrime and nextPrime."""


def is_prime(num):
    '''This function checks whether a number is prime.
    It takes an integer value and returns True if the number is prime otherwise returns False.
    Returns False for non natural numbers.'''
    if type(num)!=int and type(num)!=long:	#checking whether the input is an integer
        return False
    if num<=1:		#non-natural numbers and 1 are not a prime
        return False
    if num==2:		#2 is a prime
        return True
    if num%2==0:	#even numbers are not prime
        return False
    i=3
    while i*i<=num:
    #for i in range(3,int(sqrt(num))+1,2):	#all odd numbers from 3 to the squre root of the number are checked to see if they divide the candidate
        if num%i==0:
            return False
        i+=2
    return True

def next_prime(start):
    """ Returns the next prime number after start"""
    primeToCheck = start + (start+1)%2		#stores the candidate to be checked for prime
    while not is_prime(primeToCheck):
        primeToCheck+=2
    return primeToCheck

