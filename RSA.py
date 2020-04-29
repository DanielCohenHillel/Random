import numpy as np

def mod_inv(a, m) : 
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
  
        # q is quotient 
        q = a // m 
  
        t = m 
  
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
  
        # Update x and y 
        y = x - q * y 
        x = t 
  
  
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
  
    return x 

# Pick random prime numbers
p = 11
q = 5

n = p*q

tot = np.lcm(p-1, q-1)

e = 3

d = mod_inv(e, tot)

# Seceret messege
m = 4
# Ciphertext
c = m^e%n
# Secret messege from decription of ciphertext
m_dec = c^d%n

print(f'Super secret messege: {m}')
print(f'You cant decrypt this! {c}')
print(f'Is this the messege you were looking for? {m_dec}')

