
libFiles=$(shell ls -1 src/*.cpp | grep -v main | sed s/.cpp/.o/ | sed s/src/build/)

all: main

clean:
	rm -r build

build:
	mkdir build

build/%.o: src/%.cpp build
	g++ -c -o $@ $< -I. -std=gnu++14

main : ${libFiles} build/main.o
	g++ -o main ${libFiles} build/main.o -I. -std=gnu++14

main2 : ${libFiles} build/main2.o
	g++ -o main2 ${libFiles} build/main2.o -I. -std=gnu++14
