
oFiles=$(shell ls -1 src/*.cpp | sed s/.cpp/.o/ | sed s/src/build/)

all: main

clean:
	rm -r build

build:
	mkdir build

build/%.o: src/%.cpp build
	g++ -c -o $@ $< -I. -std=gnu++14

main : ${oFiles}
	g++ -o main ${oFiles} -I. -std=gnu++14
