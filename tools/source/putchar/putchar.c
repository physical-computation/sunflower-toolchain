/*
 *	This is from @harrysarson
 */

extern long write(int, const char*, unsigned long);

void _putchar(char character)
{
    write(1, &character, 1);
}
