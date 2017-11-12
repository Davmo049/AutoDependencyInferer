#include "banana.hpp"
#include "../fruit.hpp"

#include <iostream>

Banana::Banana() :
    Fruit::Fruit(5), calories(1)
{
}
Banana::Banana(int calories) :
    Fruit::Fruit(5), calories(calories)
{
}

void Banana::eat()
{
    std::cout << "ate banana with " << calories << "calories" << std::endl;
}

