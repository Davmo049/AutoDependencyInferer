#include <iostream>

#include "apple.hpp"
#include "folder/banana.hpp"

#include <utility>

const char * helloMessage = "HELLO!!!";

int main(int argc, char ** argv)
{
    Banana ban(10);
    std::cout << apple() << std::endl;
    ban.eat();
}
