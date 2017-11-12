#pragma once

#include <iostream>

class Fruit
{
public:
    Fruit();
    Fruit(int num) : number(num) {}
    virtual void eat();
private:
    int number;
};
