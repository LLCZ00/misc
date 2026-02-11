/*
* Executing Shellcode (Windows)
*/

#include <Windows.h>
#include <cstdio>

// "C:\\Windows\\System32\\calc.exe"
//using execProto = UINT (WINAPI *) (LPCSTR cmdline, UINT cmdshow);

unsigned char shellcode[14] = { 0x55, 0x89, 0xe5, 0x31, 0xc0, 0xb8, 0x5, 0x0, 0x0, 0x0, 0x89, 0xec, 0x5d, 0xc3 };

int main()
{
	LPVOID shellcodeAddr = VirtualAlloc(NULL, sizeof(shellcode), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	if (shellcodeAddr == NULL)
	{
		puts("[!!] Failed to allocate memory");
		return 1;
	}
	CopyMemory(shellcodeAddr, &shellcode, sizeof(shellcode));
	
	int val = ((int(*)())shellcodeAddr)();
	
	printf("Shellcode return value: %d\n", val);
	
	return 0;
}

