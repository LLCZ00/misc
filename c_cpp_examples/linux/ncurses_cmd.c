/*
* Text input using ncurses
* gcc ncurses_cmd.c -lncurses
*/

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <ncurses.h>

#define MAX_CMD_SIZE 50
#define MAX_HISTORY_SIZE 5 // Number of previous commands to save

void ncurses_loop()
{
    initscr();
    raw();
    noecho();
    keypad(stdscr, TRUE);

    int quit_gui = 0;
    int ch;
    int row, maxrow, column, maxcolumn;

    char command_string[MAX_CMD_SIZE];
    int command_length;

    char last_command[MAX_CMD_SIZE];
    memset(last_command, 0, sizeof(last_command));

    char *cmd_prefix = "> ";
    char *title = "~ PotatoCHIP8 Debugger ~";
    int prefix_length = strlen(cmd_prefix);

    getmaxyx(stdscr, maxrow, maxcolumn);
    mvprintw(0, (maxcolumn-strlen(title))/2, "%s\n", title);

    while (!quit_gui)
    {
        printw("\n%s", cmd_prefix);
        memset(command_string, 0, sizeof(command_string));
        command_length = 0;
        refresh();

        while (1) // Input loop
        {
            ch = getch();
            switch(ch)
            {
                case KEY_LEFT:
                    getyx(stdscr,row,column);
                    if ((column-prefix_length) > 0) { move(row, column - 1); } // Move cursor left, but not passed "> " thing
                    break;
                case KEY_RIGHT:
                    getyx(stdscr,row,column);
                    if ((column-prefix_length) < (command_length)) { move(row, column + 1); } // Move cursor right, but not more than 1 passed currently typed characters
                    break;
                case KEY_UP:
                    if (strlen(last_command))
                    {
                        getyx(stdscr,row,column);
                        move(row, prefix_length);
                        clrtoeol();
                        command_length = strlen(last_command);
                        printw("%s", last_command);
                    }
                    break;
                case KEY_DOWN:
                    break;
                case 3: // Ctrl-C
                    quit_gui = 1;
                    break;
                case 0x107: // backspace
                    getyx(stdscr,row,column);
                    if ((column-2) > 0)
                    {
                        move(row, column - 1);
                        delch();
                        command_length -= 1;
                    }
                    break;
                case 0xA: // Enter key/newline
                    getyx(stdscr,row,column);
                    move(row, command_length + prefix_length);
                    if (command_length)
                    {
                        for (int pos = 0; pos <= command_length && pos < MAX_CMD_SIZE; pos++)
                        {
                            command_string[pos] = mvinch(row, pos+prefix_length) & A_CHARTEXT;
                        }
                        command_string[command_length] = '\0';

                        strncpy(last_command, command_string, MAX_CMD_SIZE);
                    }
                    else if (strlen(last_command)) // Run last command if available and no command given
                    {
                        command_length = strlen(last_command);
                        strncpy(command_string, last_command, MAX_CMD_SIZE); 
                    }
                    break;
                default:
                    getyx(stdscr,row,column);
                    insch(ch);
                    move(row, column + 1);
                    command_length += 1;
            }
            refresh();
            if (ch == 3) { break; }
            if (ch == 0xA) { break; }
        }

        printw("\nCommand: %s\n", command_string);
    }

    endwin();
}


int main(int argc, char **argv) 
{

    ncurses_loop();

    puts("\nCtests complete.");
    return 0;
}

