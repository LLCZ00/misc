/*
* Test - Percision Header
*
* Functions and structs for implimenting
* arbitrary percision integers.
*/

#ifndef TEST_PERCISION
#define TEST_PERCISION

#include <stdint.h>
#include <stddef.h>


typedef struct BigNumber {
	uint8_t value;
	struct BigNumber *next;

} BigNumber;


/* Arbitrary length linked list from an array of unsigned bytes (little endian) */
BigNumber *bigByteArray(uint8_t *buffer, size_t size);


/* Arithmetic Functions */
void bigAddInt(BigNumber *bignum, int32_t val);
void bigSubInt(BigNumber *bignum, int32_t val);
void bigLShift(BigNumber *bignum, int32_t val);
void bigRShift(BigNumber *bignum, int32_t val);
void bigDivInt(BigNumber *bignum, int32_t val);
void bigMulInt(BigNumber *bignum, int32_t val);


/* Free linked list */
void bigFree(BigNumber *bignum);

/* Print big number, hex, starting with most significant bit (big endian) */
void bigPrint(BigNumber *bignum);

/* Print big number, hex, starting with least significant bit (lil endian) */
void bigPrintLSB(BigNumber *bignum);


#endif // TEST_PERCISION
