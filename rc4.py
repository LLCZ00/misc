"""
RC4 Enryption Algorithm
"""

def rc4(input, key):
    # Key-scheduling algorithm #
    ks_schedule = bytearray([byte for byte in range(256)]) # Populate array with every possible byte (0-255)
    key_length = len(key)    
    i = 0
    j = 0
    tmp = 0
    
    while i < 256:
        j = (j + ks_schedule[i] + key[i % key_length]) % 256
        
        tmp = ks_schedule[j]
        ks_schedule[j] = ks_schedule[i] # Swap i and j
        ks_schedule[i] = tmp
        
        i += 1
    
    # Pseudo-random generation algorithm (PRGA) #
    i = 0
    j = 0
    n = 0
    ciphertxt = bytearray()
    while n < len(input):
        i = (i + 1) % 256
        j = (j + ks_schedule[i]) % 256
        
        tmp = ks_schedule[j]
        ks_schedule[j] = ks_schedule[i] # Swap i and j
        ks_schedule[i] = tmp
        
        key_stream = ks_schedule[(ks_schedule[i] + ks_schedule[j]) % 256]
        ciphertxt.append(input[n] ^ key_stream)
        n += 1
        
    return ciphertxt
