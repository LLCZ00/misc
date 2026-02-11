#pragma once
/*
* NESEmu - Mapper Header
*/

#include <cstdint>
#include <vector>


class Mapper
{
public:
	Mapper(std::vector<uint8_t> &code, std::vector<uint8_t> &chrdata, int mirroring) : code(code), chrdata(chrdata), mirroring(mirroring) {}
	virtual ~Mapper(){}

	virtual uint8_t read(uint16_t address) = 0;
    virtual void write(uint16_t address, uint8_t data) = 0;

    virtual uint8_t ppuread(uint16_t address);
    virtual void ppuwrite(uint16_t address, uint8_t data);

    int get_mirroring(void) { return mirroring; }

protected:
    std::vector<uint8_t> code;
    std::vector<uint8_t> chrdata;
    int mirroring;
};


class NROM : public Mapper 
{
public:
    NROM(std::vector<uint8_t> &code, std::vector<uint8_t> &chrdata, int mirroring) : Mapper(code, chrdata, mirroring) {}
    ~NROM() override = default;
    uint8_t read(uint16_t address) override;
    void write(uint16_t address, uint8_t data) override;
};
