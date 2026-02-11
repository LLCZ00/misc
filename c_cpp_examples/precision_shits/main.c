/*
* C Tests - Sodium library
*
* Testing encryption/hashing functions n such
* from the 'sodium' library.
*/

// -lsodium needs to be added to end of gcc command

#include "percision.h" // BigNumber (Arbitrary-percision)
#include <stdio.h>
#include <stdint.h> // data types (uint8_t)
#include <stdlib.h> // srand, rand, malloc, etc.
#include <string.h> // memset
#include <sodium.h>


static void addSubTest(BigNumber *big)
{
	int32_t values[] = {0xABCDEF, 0x1, 45, 0xFF03, 255};
	size_t vcount = sizeof(values)/sizeof(int32_t);

	for (int i = 0; i < vcount; i++)
	{
		printf("Add 0x%02X: ", values[i]);
		bigAddInt(big, values[i]);
		bigPrint(big);
		printf("Sub 0x%02X: ", values[i]);
		bigSubInt(big, values[i]);
		bigPrint(big);
	}
	puts("");
}

static void shiftTest(BigNumber *big)
{
	int32_t values[] = {3, 5, 0xF, 0, 1, 0xFF};
	size_t vcount = sizeof(values)/sizeof(int32_t);

	for (int i = 0; i < vcount; i++)
	{
		printf("LShift 0x%02X: ", values[i]);
		bigLShift(big, values[i]);
		bigPrint(big);
		printf("RShift 0x%02X: ", values[i]);
		bigRShift(big, values[i]);
		bigPrint(big);
	}
	puts("");
}

int main(void)
{
	if (sodium_init() == -1)
	{
		puts("[!] Libsodium failed to initialize");
		return -1;
	}

	uint8_t bytearray[] = {0xFF, 0x12}; 
	//uint8_t bytearray[] = {0xFF, 0xAA, 0x00, 0x12}; 

	printf("Big number: ");
	BigNumber *big = bigByteArray(bytearray, sizeof(bytearray));
	bigPrint(big);
	puts("");

	// addSubTest(big);
	shiftTest(big);


	bigFree(big);
	puts("\n[*] C test exited gracefully");
	return 0;
}



