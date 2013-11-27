/* hello-ftdi.c: flash LED connected between CTS and GND.
   This example uses the libftdi API.
   Minimal error checking; written for brevity, not durability. */

#include <stdio.h>
#include <ftdi.h>

#define PIN_TX  0x01  /* Orange wire on FTDI cable */
#define PIX_RX  0x02  /* Yellow */
#define PIN_RTS 0x04  /* Green */
#define PIN_CTS 0x08  /* Brown */
#define PIN_DTR 0x10
#define PIN_DSR 0x20
#define PIN_DCD 0x40
#define PIN_RI  0x80

#define LED 0x10  /* PN_CTS */

int main ( int argc, char *argv[] )
{
    unsigned char c = 0;
    char check = '2';
    const char serial[] = "AD02655T";
    const char *descriptor = NULL;
    struct ftdi_context ftdic;

    /* Initialize context for subsequent function calls */
    ftdi_init(&ftdic);

    /* Open FTDI device based on FT232R vendor & product IDs */
    if(ftdi_usb_open_desc(&ftdic, 0x0403, 0x6001, descriptor, serial) < 0) {
        puts("Can't open device mash stirrer USB");
        return 1;
    }

    if ( argc == 1 )
    {
        printf( "Mash stirrer USB device found, all OK\n");
        return 0;
    }

    if ( argc != 2 ) /* argc should be 2 for correct execution */
    {
        /* We print argv[0] assuming it is the program name */
        printf( "usage: %s [0|1]\n", argv[0] );
        return 1;
    }
    else 
    {
        check = argv[1][0];
        /*printf("Argument: %s  C:%c\n",argv[1],check);*/
        if (check == '0')
        {
            c ^= LED;
            /*printf("On\n");*/
        }

        /* Enable bitbang mode with a single output line */
        ftdi_set_bitmode(&ftdic, LED, BITMODE_BITBANG);

        ftdi_write_data(&ftdic, &c, 1);

        return 0;
    }
}
