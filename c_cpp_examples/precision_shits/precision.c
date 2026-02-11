/*
* Test - Percision
*
* Functions and structs for implimenting
* arbitrary percision integers.
*
* TODO:
*     - Support negative numbers
*     - Shift right is fucked up
*     - 
*/

#include "percision.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h> 
#include <string.h> 
#include <stddef.h>


static size_t bigLength(BigNumber *bignum)
{
	BigNumber *tmp = bignum;
	size_t count = 0;
	while(tmp)
	{
		count++;
		tmp = tmp->next;
	}
	return count;
}


/* Arbitrary length linked list from an array of unsigned bytes (little endian) */
BigNumber *bigByteArray(uint8_t *buffer, size_t size)
{
	if (size < 1) { puts("[!] Invalid size"); return NULL; }

	BigNumber *head = malloc(sizeof(BigNumber));
	head->value = buffer[size-1];
	head->next = NULL;

	BigNumber *last = head;
	BigNumber *tmp = NULL;

	for (int32_t i = size-2; i >= 0; i--)
	{
		tmp = malloc(sizeof(BigNumber));
		tmp->value = buffer[i];
		tmp->next = NULL;
		last->next = tmp;
		last = tmp;
		tmp = tmp->next;
	}
	return head;
}

void bigAddInt(BigNumber *bignum, int32_t val)
{
	if (val < 0)
	{
		bigSubInt(bignum, abs(val));
		return;
	}
	int32_t sum;
	int32_t carry = val; // Initial "carry"
	BigNumber *current_ptr = bignum;
	BigNumber *last_ptr = bignum;

	while (carry)
	{
		if (current_ptr == NULL)
		{
			current_ptr = malloc(sizeof(BigNumber));
			current_ptr->value = 0;
			current_ptr->next = NULL;
			last_ptr->next = current_ptr;
		}
		sum = carry + current_ptr->value;
		carry = sum/256;
		current_ptr->value = (uint8_t) sum & 0xFF;

		last_ptr = current_ptr;
		current_ptr = current_ptr->next;
	}
}

void bigSubInt(BigNumber *bignum, int32_t val)
{
	if (val < 0)
	{
		bigAddInt(bignum, abs(val));
		return;
	}
	BigNumber *current_ptr = bignum;
	int32_t remains = val; // Remaining amount to subtract
	int32_t diff;
	uint8_t result;

	while (remains && current_ptr)
	{
		diff = current_ptr->value - remains;
		remains = abs(diff)/256;
		result = (uint8_t) diff & 0xFF;

		if (diff < 0 && result > 0) 
		{
			if (current_ptr->next)
			{
				remains += 1; 
			}
			else
			{
				result = 0;
				remains = 0;
			}
		}
		current_ptr->value = result;
		current_ptr = current_ptr->next;
	}
}

void bigLShift(BigNumber *bignum, int32_t val)
{
	int32_t shift;
	int32_t carry = 0; // Initial "carry"
	BigNumber *current_ptr = bignum;
	BigNumber *last_ptr = bignum;

	while (carry || current_ptr)
	{
		if (current_ptr == NULL)
		{
			current_ptr = malloc(sizeof(BigNumber));
			current_ptr->value = 0;
			current_ptr->next = NULL;
			last_ptr->next = current_ptr;
		}
		shift = (current_ptr->value << (val % 16)) + carry;
		carry = shift >> 8;
		current_ptr->value = (uint8_t) shift & 0xFF;

		last_ptr = current_ptr;
		current_ptr = current_ptr->next;
	} 
}

void bigRShift(BigNumber *bignum, int32_t val)
{
	int32_t carry = 0; // Initial "carry"
	BigNumber *current_ptr = bignum;
	BigNumber *last_ptr = NULL;

	while (current_ptr)
	{
		if (last_ptr)
		{
			carry = (current_ptr->value << 8-(val % 8));
			last_ptr->value = (uint8_t) (carry | last_ptr->value);
		}
		current_ptr->value = (uint8_t) (current_ptr->value >> val) & 0xFF;
		last_ptr = current_ptr;
		current_ptr = current_ptr->next;
	}
}

void bigDivInt(BigNumber *bignum, int32_t val)
{

}

void bigMulInt(BigNumber *bignum, int32_t val)
{

}

/* Free linked list */
void bigFree(BigNumber *bignum)
{
	BigNumber *current_ptr = bignum;
	BigNumber *next_ptr = NULL;
	while (current_ptr)
	{
		next_ptr = current_ptr->next;
		free(current_ptr);
		current_ptr = next_ptr;
	}
}

/* Print big number, starting with most significant bit (big endian) */
void bigPrint(BigNumber *bignum) // Kinda trash
{
	uint8_t *bytearray = malloc(bigLength(bignum));
	BigNumber *tmp = bignum;
	int32_t index = -1;
	while(tmp)
	{
		index++;
		bytearray[index] = tmp->value;
		tmp = tmp->next;
	}

	printf("0x");
	for (index; index >= 0; index--)
	{
		printf("%02X", bytearray[index]);
	}
	puts("");

	free(bytearray);
}

/* Print big number, starting with least significant bit (lil endian) */
void bigPrintLSB(BigNumber *bignum)
{
	BigNumber *tmp = bignum;
	printf("0x");
	while(tmp)
	{
		printf("%02X", tmp->value);
		tmp = tmp->next;
	}
	puts("");
}

