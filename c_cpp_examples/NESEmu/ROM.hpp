#pragma once
/*
* NESEmu - Cartridge Headers
* - Class representing an NES cartridge
* - Handles parsing ROM, detecting format, retrieving mappers, etc.
*/

#include <string>
#include <cstdint>
#include <vector>
#include "Mappers.hpp"


struct iNESHeader{
	char nes[4];
	uint8_t program_size;
	uint8_t chardata_size;
	uint8_t flags6;
	uint8_t flags7;
	uint8_t program_ram_size;
	uint8_t flags9;
	uint8_t flags10;
	char pad[5];
};


class ROM
{
public:
	bool load(const char *filepath);
	int get_mirroring(void);
	Mapper *get_mapper(void);
	void printheader(void);
	std::vector<uint8_t> get_program_code() { return program_code; };
	std::vector<uint8_t> get_chardata() { return chardata; };

private:
	struct iNESHeader header;
	int mirroring;
	uint8_t mapper_num;
	std::vector<uint8_t> trainer;
	std::vector<uint8_t> program_code;
	std::vector<uint8_t> chardata;

};
