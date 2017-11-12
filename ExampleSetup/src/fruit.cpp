#include "fruit.hpp"

Fruit::Fruit() : number(123)
{
}

void Fruit::eat()
{
    std::cout << "YUMMY" << number << std::endl;
}

