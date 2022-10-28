;----------------------------------------
;get nth fibbonacci number
;
;nasm, linux
;
;"small" first assembly program
;
;currently only goes up to the 47th 
;fibbonacci number
;
;I'm including all used functions within
;this file instead of importing, for simplicity and
;so I don't have to upload multiple files
;
;----------------------------------------

section .data
title db "~~Fibbonaci Calculator~~", 0xa, 0
prompt db "Enter number: ", 0

section .bss
n: resb 255

section .text
global _start

_start:
	mov eax, title
	call sprint

	mov eax, prompt
	call sprint

	mov eax, 3
	mov ebx, 0
	mov ecx, n
	mov edx, 255
	int 0x80

	mov esi, ecx
	mov ecx, 0
	call s_to_i ;loads input number into ecx

;----------begin fibonacci calculation----------;

	mov ebx, 0
	mov eax, 1
	dec ecx

fib_loop:
	cmp ecx, 0
	jz done
	push eax
	add eax, ebx
	pop ebx
	dec ecx
	jmp fib_loop

done:
	call iprintlf
	call exit

;----------convert input to integer----------;
s_to_i:
	mov ebx, 0
	mov bl, [esi]
	inc esi

	cmp bl, '0'
	jb invalid
	cmp bl, '9'
	ja invalid

	sub bl, '0'
	imul ecx, 10
	add ecx, ebx
	jmp s_to_i 

invalid:
	ret

;----------
;string length calculation
;----------

slen:
	push ebx
	mov  ebx, eax
	

next_char:
	cmp byte [eax], 0
	jz finished
	inc eax
	jmp next_char

finished:
	sub eax, ebx
	pop ebx
	ret

;----------
;string printing function
;----------
sprint:
	push ebx
	push ecx
	push edx
	push eax
	call slen	;string length stored in eax

	mov edx, eax
	pop eax
	mov ecx, eax
	mov eax, 4
	mov ebx, 1
	int 0x80

	pop edx
	pop ecx
	pop ebx
	ret

;----------
;Printing number
;----------

iprint:
	push eax
	push ecx
	push edx
	push esi
	mov ecx, 0

divide_loop:
	inc ecx
	mov edx, 0
	mov esi, 10
	idiv esi
	add edx, 48
	push edx
	cmp eax, 0
	jnz divide_loop

print_loop:
	dec ecx
	mov eax, esp
	call sprint
	pop eax
	cmp ecx, 0
	jnz print_loop

	pop esi
	pop edx
	pop ecx
	pop eax
	ret

;printing number w/ newline

iprintlf:
	call iprint
	
	push eax
	mov eax, 0xa
	push eax
	mov eax, esp
	call sprint
	pop eax
	pop eax
	ret

;----------
;Exit function
;---------- 
exit:
	mov eax, 1
	mov ebx, 0
	int 0x80