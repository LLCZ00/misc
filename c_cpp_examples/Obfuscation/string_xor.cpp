/* *
 * XOR String Encryptor
 * */


#include <cstdio>
#include <cstdlib>

unsigned char *xor_encrypt(const char *plaintxt);
char *xor_decrypt(const unsigned char *xortxt);

static size_t my_strlen(const char *string)
{
    size_t count = 0;
    while (string[count] != '\0')
    {
        count++;
    }
    return count;
}
static void print_hex(const unsigned char *string)
{
    size_t slen = my_strlen((char *)string);
    for (size_t i = 0; i <= slen; i++)
    {
        printf("%x ", string[i]);
    }
    puts("");
}

int main()
{
    char test[] = "cmd.exe";
    //unsigned char process[] = "\x8a\x84\x8d\xc7\x8c\x91\x8c";
    //char *unXOR = xor_decrypt((unsigned char *)"\x8a\x84\x8d\xc7\x8c\x91\x8c");
    printf("OG Hex:\n");
    print_hex((unsigned char *)test);

    unsigned char *XORtxt = xor_encrypt(test);
    printf("XOR Hex:\n");
    print_hex(XORtxt);

    char *unXOR = xor_decrypt(XORtxt);
    printf("\nDe-XOR'd: %s\n", unXOR);

    free(XORtxt);
    free(unXOR);
    return 0;
}
unsigned char *xor_encrypt(const char *plaintxt)
{
    unsigned char key = 0xe9;
    size_t slen = my_strlen(plaintxt);
    auto *XORtxt = (unsigned char *)malloc((slen+1) * sizeof(char));

    for (int i = 0; i < slen; i++)
    {
        XORtxt[i] = (plaintxt[i] ^ key);
    }
    XORtxt[slen] = '\0';
    return XORtxt;
}
char *xor_decrypt(const unsigned char *xortxt)
{
    unsigned char key = 0xe9;
    size_t slen = my_strlen((char *)xortxt);
    auto *unXOR = (unsigned char *)malloc((slen+1) * sizeof(char));

    for (int i = 0; i < slen; i++)
    {
        unXOR[i] = (xortxt[i] ^ key);
    }
    unXOR[slen] = '\0';
    return (char *)unXOR;
}