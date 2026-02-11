#include <cstdio>
#include <cstdint>

#define RC4BITS 256

void rc4Algorithm(const uint8_t *key, size_t keylen, uint8_t *data, size_t datalen)
{
	uint8_t outputmsg[9] = {0};
	uint8_t keyschedule[RC4BITS];
	for (int i = 0; i < RC4BITS; i++) { keyschedule[i] = i; }
	
	int i = 0;
	int j = 0;
	uint8_t tmp = 0;
	
	// Key Scheduling Algorithm
	while (i < RC4BITS)
	{
		j = (j + keyschedule[i] + key[i % keylen]) % RC4BITS;
		tmp = keyschedule[j];
		keyschedule[j] = keyschedule[i];
		keyschedule[i] = tmp;
		i++;
	}
	
	// Pseudo-random generation algorithm (PRGA)
	i = 0;
	j = 0;
	size_t n = 0;
	
	while (n < datalen)
	{
		i = (i + 1) % RC4BITS;
		j = (j + keyschedule[i]) % RC4BITS;
		tmp = keyschedule[j];
		keyschedule[j] = keyschedule[i]; 
		keyschedule[i] = tmp;
		outputmsg[n] = data[n] ^ keyschedule[(keyschedule[i] + keyschedule[j]) % RC4BITS];
		n++;
	}
	
	for (int i = 0; i < datalen; i++)
	{
		printf("%02X ", outputmsg[i]);
	}
	puts("");
}