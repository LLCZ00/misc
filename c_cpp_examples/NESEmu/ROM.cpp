/*
* NESEmu - ROM
* - Class representing an NES ROM
* - Handles parsing ROM, detecting format, retrieving mappers, etc.
*/

#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include "ROM.hpp"


bool ROM::load(const char *filepath)
{
	FILE *ROMfp = fopen(filepath, "r");
	if (ROMfp == NULL) { puts("Failed to open file."); return false; }
	fread((uint8_t *)&header, 1, sizeof(header), ROMfp);
	
	trainer.reserve(512);
	program_code.resize(header.program_size * 16384);
	chardata.resize(header.chardata_size * 8192);

	mirroring = header.flags6 & 1;

	if ((header.flags6 >> 2) & 1) // If trainer flag set
	{
		fread((uint8_t *)trainer.data(), 1, 512, ROMfp);
	}

	fread((uint8_t *)program_code.data(), 1, header.program_size * 16384, ROMfp);

	if (header.chardata_size > 0)
	{
		fread((uint8_t *)chardata.data(), 1, header.chardata_size * 8192, ROMfp);
	}
	else
	{
		chardata = std::vector<uint8_t>(8192, 0);
	}

	mapper_num = ((header.flags6 & 0xF0) >> 4) | (header.flags7 & 0xF0);

	fclose(ROMfp);
	if (strncmp(header.nes, "NES", 3) != 0) { puts("Incorrect header detected."); return false; }
	return true;
}

int ROM::get_mirroring(void) { return mirroring; }

Mapper *ROM::get_mapper(void)
{
	switch(mapper_num)
	{
		case 0:
			return new NROM(program_code, chardata, mirroring);
			break;
		// case 1:
		// 	puts("MMC1");
		// 	break;
		// case 2:
		// 	puts("UnROM");
		// 	break;
		// case 3:
		// 	puts("CNROM");
		// 	break;
		default:
			puts("Unsupported mapper.");
			return NULL;
	}
}

void ROM::printheader(void)
{
	printf("Signature: %.*s\n", 3, header.nes);
	printf("Program code size: %d bytes\n", (int)header.program_size * 16384);
	printf("Graphical data size: %d bytes\n", (int)header.chardata_size * 8192);
	printf("Mirroring: %d\n", mirroring);
	printf("Mapper number: %d\n", mapper_num);
}

