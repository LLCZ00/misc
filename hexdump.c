/* Hexdump
*
* Takes a buffer and prints the bytes/ascii in
* a 'hexdump'-like fashion
*/

#include <stdio.h>
#include <stdint.h>
#include <string.h>

void hexdump(const uint8_t *buffer, uint32_t buffersize);

void hexdump(const uint8_t *buffer, uint32_t buffersize)
{
	int8_t rowlength = 16; // Bytes per line
	int8_t columnsize = 8; // Where to put space between output in each line
	uint16_t linenumber = 0;
	uint8_t ascii_chars[rowlength]; // Characters for ascii output after each line

	memset(ascii_chars, '.', rowlength);

	printf("%04X: ", linenumber);

	for (uint32_t offset = 0; offset < buffersize; offset++)
	{
		printf("%02X ", buffer[offset]);

		if ( buffer[offset] > 0x20 && buffer[offset] <= 0x7e )
		{
			ascii_chars[offset % rowlength] = buffer[offset];
		}

		if ( (((offset + 1) % rowlength) == 0) || (offset + 1 == buffersize) ) 
		{
			// Align ascii columns
			for (int cursor = (((offset) % rowlength) + 1) * 3; cursor < rowlength*3; cursor++)
			{
				printf(" ");
			}

			printf("\t| ");

			// Print ascii representation
			for (int i = 0; i < rowlength; i++)
			{
				printf("%c ", ascii_chars[i]);
			}
			printf("|\n");

			// Print new linenumber and refill ascii_chars with periods
			if (offset + 1 != buffersize)
			{
				printf("%04X: ", linenumber + (offset + 1));
				memset(ascii_chars, '.', rowlength);
			}			
		}
	}
	puts("");
}
