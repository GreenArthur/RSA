import random
"""
sources
https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
https://simple.wikipedia.org/wiki/RSA_algorithm

"""

#using Sieve of Eratosthenes to generate all prime numbers up to input n
def ListAllPrimeNum(n):
    allPosiblePrime = []
    prime = [True for i in range(n + 1)]
    p = 2
    while (p * p <= n):
         
        
        if (prime[p] == True):
             
            
            for i in range(p ** 2, n + 1, p):
                prime[i] = False
        p += 1
    prime[0]= False
    prime[1]= False
    
    for p in range(n + 1):
        if prime[p]:
            allPosiblePrime.append(p)
    
    return allPosiblePrime


def checkForPrime(n):
    if n % 2 != 0:
        return True
    else:
        return False

    
def gcd(p,q):
    while q != 0:
        p, q = q, p%q
    return p

#find the multiplicative inverse of e and phi
def modInverse(e, phi):
    m0 = phi
    y = 0
    x = 1
 
    if (phi == 1):
        return 0
 
    while (e > 1):
 

        q = e // phi
 
        t = phi
 

        phi = e % phi
        e = t
        t = y
 

        y = x - q * y
        x = t
 

    if (x < 0):
        x = x + m0
 
    return x
 





def GenerateKeys(p,q):
    #error checking
    if not (checkForPrime(q) or checkForPrime(q)):
        raise ValueError("Both numbers must be prime")
    elif q == p:
        raise ValueError("p and q must not be equall")
    # calculate for mod
    mod = p * q
    #calculate for the totient
    phi = (p - 1)*(q - 1)
    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1,phi)
    
    #check of e and phi are co prime
    g = gcd(e, phi)
    #if not we generate a new e
    #and check it again
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    #using euclidean extended algorithm to find the private key
    d = modInverse(e,phi)

    return ((e, mod), (d, mod))



def encrypt(pk,plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    aux = [str(pow(char, key, n)) for char in ciphertext]
    # Return the array of bytes as a string
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)



    


if __name__ == '__main__':
    n = int(input("list all possible prime numbers up to your input n: "))
    print(ListAllPrimeNum(n))
    p = int(input("input a prime number frome the listing: "))
    q = int(input("input another prime number different from above: "))

    public, private = GenerateKeys(p, q)
    print(" - Your public key is ", public, " and your private key is ", private)
    message = input(" - Enter a message to encrypt with your public key: ")
    encrypted_msg = encrypt(public, message)
    print(" - Your encrypted message is: ", ''.join(map(lambda x: str(x), encrypted_msg)))
    print(" - Your message is: ", decrypt(private, encrypted_msg))
