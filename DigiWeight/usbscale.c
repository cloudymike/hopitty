
#include <stdlib.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <asm/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/hiddev.h>

#define EV_NUM 5


int main (int argc, char **argv) {

  int fd = -1;
  int i,k;
  
  /*
  int val;
  struct hiddev_devinfo desc;
  */
  
  struct hiddev_event ev[EV_NUM];
  char name[100];

  char hiddev[100];
  char buf[256];
  
  for (k = 0; k < 9; k++) {
    snprintf(hiddev, sizeof hiddev, "%s%d", "/dev/usb/hiddev", k);
    if ((fd = open(hiddev, O_RDONLY)) >= 0) {
       
      ioctl(fd, HIDIOCGNAME(100), name);
      if ( strcmp(name,"DYMO 5 Pound USB Postal Scale") == 0) {
        read(fd, ev, sizeof(struct hiddev_event) * EV_NUM);
        printf("%d\n", ev[1].value);
        
        /*
        ioctl(fd, HIDIOCGVERSION, val);
        printf("Version %d\n",val);
        ioctl(fd, HIDIOCGDEVINFO, desc);
        printf("Info %d\t%d\n",desc.version, desc.num_applications);
        */

        close(fd);
        exit(0);
      }
    }
    close(fd);
  }
  printf("Scale not found\n");
  exit(1);
}
