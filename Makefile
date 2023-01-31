.PHONY: clean pptests

BIN = binary_name
SOURCES = $(wildcard src/*.cpp)
HEADERS = $(wildcard src/*.hpp)
OBJ = $(SOURCES:.cpp=.o)
CC = g++

$(BIN): $(OBJ)
	$(CC) -o $@ $^

%.o: %.cpp $(HEADERS)
	$(CC) -o $@ -c $<

pptests: testscpp.cpp
	$(CC) -o $@ $<

clean:
	rm -f pptests $(BIN) $(OBJ)
