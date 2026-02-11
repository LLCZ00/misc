/*
* C Tests - Random bytes
*
* Several different methods for filling an
* array with random bytes.
*/

#include <stdio.h>
#include <stdint.h> // data types (uint8_t)
#include <stdlib.h> // srand, rand
#include <string.h> // memset
#include <time.h>
#include <sys/random.h> // getentropy

#define COOKIESIZE 16

/*
printf("%s\n", );
*/

static void rand_method(uint8_t *buffer, size_t size);
static void entropy_method(uint8_t *buffer, size_t size);

static void printbytes(const uint8_t *buffer, size_t size, const char *title)
{
	if (title) { printf("%s: ", title); }

	for (size_t i = 0; i < size; i++)
	{
		printf("%02X ", buffer[i]);
	}
	puts("");
}


int main(void)
{
	uint8_t cookie[COOKIESIZE];

	// rand_method(cookie, COOKIESIZE);
	// printbytes(cookie, COOKIESIZE, "Cookie (rand)");

	rand_method(cookie, COOKIESIZE);
	printbytes(cookie, COOKIESIZE, "Cookie (entropy)");
	

	puts("\n[*] C test exited gracefully");
	return 0;
}

/* Fill buffer using the srand and rand functions
* - Requires "seeding" of random number
* - Probably best when you need multiple random things, after seeding
*/
static void rand_method(uint8_t *buffer, size_t size)
{
	memset(buffer, 0, size);
	srand(time(NULL)); // Seed random with current epoch time (only needs to be called once)

	for (size_t i = 0; i < size; i++)
	{
		buffer[i] = rand();
	}	
}

/* Fill buffer using the getentropy function 
* - Max length of buffer is 256
* - Appears to be a wrapper around getrandom(), 
*   which also appears to use the current epoch 
*   value as the seed
* - Probably best for when you only need a random thing once
*/
static void entropy_method(uint8_t *buffer, size_t size)
{
	memset(buffer, 0, size);
	getentropy(buffer, size);
}

