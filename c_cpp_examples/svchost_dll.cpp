/*
* A DLL capable of being hosted by svchost.exe
* After compilation (via powershell/cmd):
* 	1. sc.exe create [serviceName] binPath= "c:\windows\System32\svchost.exe -k [groupName]" type= share start= auto
* 	2. reg add HKLM\SYSTEM\CurrentControlSet\services\[serviceName]\Parameters /v ServiceDll /t REG_EXPAND_SZ /d C:\Windows\system32\[serviceName] /f
* 	3. Add [serviceName] to the list in [groupName] at Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost
* 	4. sc.exe start [serviceName]
*/

#include "pch.h"
#define SVCNAME TEXT("Sus Service")

SERVICE_STATUS serviceStatus;
SERVICE_STATUS_HANDLE serviceStatusHandle;
HANDLE stopEvent = NULL;

VOID UpdateServiceStatus(DWORD currentState)
{
	serviceStatus.dwCurrentState = currentState;
	SetServiceStatus(serviceStatusHandle, &serviceStatus);
}

DWORD ServiceHandler(DWORD controlCode, DWORD eventType, LPVOID eventData, LPVOID context)
{
	switch (controlCode)
	{
	case SERVICE_CONTROL_STOP:
		serviceStatus.dwCurrentState = SERVICE_STOPPED;
		SetEvent(stopEvent);
		break;
	case SERVICE_CONTROL_SHUTDOWN:
		serviceStatus.dwCurrentState = SERVICE_STOPPED;
		SetEvent(stopEvent);
		break;
	case SERVICE_CONTROL_PAUSE:
		serviceStatus.dwCurrentState = SERVICE_PAUSED;
		break;
	case SERVICE_CONTROL_CONTINUE:
		serviceStatus.dwCurrentState = SERVICE_RUNNING;
		break;
	case SERVICE_CONTROL_INTERROGATE:
		break;
	default:
		break;
	}

	UpdateServiceStatus(SERVICE_RUNNING);
	return NO_ERROR;
}

VOID ExecuteServiceCode()
{
	stopEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	UpdateServiceStatus(SERVICE_RUNNING);

	/* Code here */

	while (1)
	{
		WaitForSingleObject(stopEvent, INFINITE);
		UpdateServiceStatus(SERVICE_STOPPED);
		return;
	}
}

extern "C" __declspec(dllexport) VOID WINAPI ServiceMain(DWORD argc, LPWSTR * argv)
{
	serviceStatusHandle = RegisterServiceCtrlHandler(SVCNAME, (LPHANDLER_FUNCTION)ServiceHandler);
	
	serviceStatus.dwServiceType = SERVICE_WIN32_SHARE_PROCESS;
	serviceStatus.dwServiceSpecificExitCode = 0;

	UpdateServiceStatus(SERVICE_START_PENDING);
	ExecuteServiceCode();
}