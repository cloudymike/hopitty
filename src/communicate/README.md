# Communication routines

This is a collecion of communication routines that
allows the program to be split up into smaller services

The general idea is that each service will be a simple
standalone service that can be tested individually

The main hardware controlling routine should be a single
thread to avoid surprises with timing. This limit the
type of communication and in particular a full restful
server is not going to work.

This will also include a simple mock hardware server and a
simple mock web controller that will allow testing of the
communication routing

## Web socket
As a simplest level, a websocket communication will
be created. It should allow some basic error handling
allowing to reconnect as a socket dies.

## Commands

### run
return OK or ERROR
Start current loaded recipe

### stop
return OK or ERROR
Stop current recipe

### pause
return OK or ERROR
Hold current step on the recipe

### skip
return OK or ERROR
Skip one step of the recipe

### terminate
return OK or ERROR
Terminate program

## load{recipe json}
return  OK or ERROR
stop current recipe
load recipe provided

## status
return status of all in controllers
status also includes state (run,pause,stop etc)
