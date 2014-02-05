all:
	gcc -v `pkg-config GoIO --cflags` -c GoIO_DeviceCheck.cpp
	gcc -v -o mytemp GoIO_DeviceCheck.o `pkg-config GoIO --libs`

clean:
	rm mytemp
	rm GoIO_DeviceCheck.o
