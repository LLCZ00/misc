/*
* C Tests - Linked List Example (For my future reference)
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>


typedef struct Person {
	char name[25];
	struct Person *previous; // Person ahead of them
	struct Person *next; // Person behind them 
}Person;


Person *first_person = NULL;
Person *last_person = NULL; // Current

void freePerson(Person *person)
{
	if (person != NULL)
	{
		//printf("[*] Freeing %s (%p)\n", person->name, person);
		free(person);
		person = NULL;
	}
}

void freeQueue() // Free all people in list
{
	Person *person_ptr = first_person;
	Person *nextperson_ptr = NULL;
	while (person_ptr)
	{
		nextperson_ptr = person_ptr->next;
		freePerson(person_ptr);
		person_ptr = nextperson_ptr;
	}
}

int getQueueLength() // Return total number of people in line
{
	int count = 0;
	Person *person_ptr = first_person;
	while(person_ptr)
	{		
		person_ptr = person_ptr->next;
		count++;
	}
	return count;
}

int placeFromPerson(Person *person) // Return place in line of given person (index + 1)
{
	int place = 1;
	Person *person_ptr = first_person;
	while(person_ptr)
	{
		if (person == person_ptr)
		{
			return place;
		}
		person_ptr = person_ptr->next;
		place++;
	}
	puts("Person not found.");
	return -1;
}

Person *personFromPlace(int place) // Return person at given place in line
{
	if (place < 1 || place > getQueueLength())
	{
		printf("[!] Invalid queue position: %d\n", place);
		return NULL;
	}
	int count = 1;
	Person *person_ptr = first_person;
	while(count != place)
	{
		person_ptr = person_ptr->next;
		count++;
	}
	return person_ptr;
}

Person *newPerson(char *name)
{
	Person *person = malloc(sizeof(Person));
	if (person == NULL)
	{
		puts("[!] Error allocating Person");
		return NULL;
	}
	strncpy(person->name, name, sizeof(person->name)-1);
	person->previous = NULL;
	person->next = NULL;
	return person;
}

void addPerson(Person *person) // Add person to end of line
{
	if (first_person == NULL)
	{
		person->previous = NULL;
		first_person = person;
	}
	else
	{
		person->previous = last_person;
		last_person->next = person;
	}
	last_person = person;
}

void insertByPlace(Person *person, int place) // Insert person into place in line (index - 1)
{
	if (place < 1 || place > getQueueLength())
	{
		puts("[!] Invalid queue position");
		return;
	}
	Person *old_person = personFromPlace(place);
	if (old_person == NULL) { return; }

	if (old_person == first_person) { first_person = person; }
	else 
	{
		if (old_person == last_person) { last_person = person; }
		if (old_person->previous) { old_person->previous->next = person; }
	}
	person->next = old_person;
	person->previous = old_person->previous;
	old_person->previous = person;
}

void removePerson(Person *person)
{
	if (person == first_person)
	{
		if (person->next) { person->next->previous = NULL; }
		first_person = person->next;
	}
	else if (person == last_person)
	{
		if (person->previous) { person->previous->next = NULL; }
		last_person = person->previous;
	}
	else
	{
		person->previous->next = person->next;
		person->next->previous = person->previous;
	}
	freePerson(person);
}

void removeByPlace(int place)
{
	if (place < 1 || place > getQueueLength())
	{
		puts("[!] Invalid queue position");
		return;
	}
	removePerson(personFromPlace(place));
}


void push(Person *person) // Push person to front of the line
{
	if (first_person == NULL)
	{
		addPerson(person);
	}
	else
	{
		insertByPlace(person, 1);
	}	
}

void pop() // Remove first person on list
{
	removeByPlace(1);
}

void reverseQueue()
{
	Person *person_ptr = first_person;
	Person *nextperson_ptr = NULL;
	while(person_ptr)
	{
		nextperson_ptr = person_ptr->next;
		person_ptr->next = person_ptr->previous;
		person_ptr->previous = nextperson_ptr;
		person_ptr = nextperson_ptr;
	}
	nextperson_ptr = first_person;
	first_person = last_person;
	last_person = nextperson_ptr;
}

void printPerson(Person *person)
{
	if (person == NULL)
	{
		puts("Person is NULL\n\n");
		return;
	}
	printf("#%d. %s\n", placeFromPerson(person), person->name);
	if (person->previous)
	{
		printf("Previous person: %s\n", person->previous->name);
	}
	if (person->next)
	{
		printf("Next person: %s\n", person->next->name);
	}	
}

void printQueue() // Print whole list of people in order
{
	printf("Queue length: %d people\n\n", getQueueLength());
	Person *person_ptr = first_person;
	while(person_ptr)
	{
		printPerson(person_ptr);
		person_ptr = person_ptr->next;
	}
	puts("");
}


int main(int argc, char **argv)
{
	Person *george = newPerson("George");

	push(newPerson("Gina"));
	addPerson(newPerson("Giles"));
	addPerson(newPerson("Bill"));
	addPerson(george);
	insertByPlace(newPerson("Stewart"), 2);
	addPerson(newPerson("Tina"));
	printQueue();

	reverseQueue();
	printQueue();

	removeByPlace(3);
	pop();
	removePerson(george);
	printQueue();

	freeQueue();

	puts("\n[*] Tests complete");
	return 0;
}
