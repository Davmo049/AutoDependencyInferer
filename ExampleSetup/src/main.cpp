#include <iostream>

#include "circ1.hpp"
#include "hippo.hpp"
#include "folder/banana.hpp"

#include <utility>

const char * helloMessage = "HELLO!!!";

int main(int argc, char ** argv)
{
    std::cout << helloMessage << std::endl;
    circ1(11);
    Fruit fruit=Fruit();
    hippoEat(fruit);
    Banana ban(9999);
    ban.eat();
}
