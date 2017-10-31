#pragma once

#include <iostream>

class Fruit
{
public:
    Fruit() : number(123) {}
    Fruit(int num) : number(num) {}
    virtual void eat()
    {
        std::cout << "YUMMY" << number << std::endl;
    }
private:
    int number;
};
