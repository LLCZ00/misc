/*
* NESEmu - Mapper Classes
*/

#include "Mappers.hpp"


uint8_t Mapper::ppuread(uint16_t address) 
{
    return chrdata[address];
}

void Mapper::ppuwrite(uint16_t address, uint8_t data) 
{
    chrdata[address] = data;
}


uint8_t NROM::read(uint16_t address) 
{
    if (address < 0x8000) 
    {
        return 0;
    }

    address = (address - 0x8000) % code.size();
    return code[address];
}

void NROM::write(uint16_t address, uint8_t data) {} // No write in NROM
