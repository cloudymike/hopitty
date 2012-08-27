all:
	gcc -v `pkg-config GoIO --cflags` -c GoIO_DeviceCheck.cpp
	gcc -v -o GoIO_DeviceCheck GoIO_DeviceCheck.o `pkg-config GoIO --libs`

