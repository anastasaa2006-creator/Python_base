# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 17:36:37 2026

@author: Анастасия
"""
class Fibo:
   
    def __init__(self, max_count=None):
        self.max_count = max_count
        self.count = 0
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.max_count is not None and self.count >= self.max_count:
            raise StopIteration
        
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result


def integers():
    n = 0
    while True:
        yield n
        n += 1

def primes():
    n = 2
    while True:
        is_prime = True
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                is_prime = False
                break
        if is_prime:
            yield n
        n += 1


if __name__ == "__main__":
    
    print("\n1. Fibo (первые 10 чисел):")
    fib = Fibo(10)
    print("  ", list(fib))
    
    print("\n2. integers (первые 10 чисел):")
    gen = integers()
    print("  ", [next(gen) for _ in range(10)])
    
    print("\n3. primes (первые 10 простых чисел):")
    gen = primes()
    print("  ", [next(gen) for _ in range(10)])