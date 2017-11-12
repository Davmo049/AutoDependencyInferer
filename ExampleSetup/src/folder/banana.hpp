#pragma once

#include "../fruit.hpp"

class Banana : public Fruit
{
public:
    Banana();
    Banana(int calories);
    Banana(const Banana& o) = default;

    virtual void eat() override;
    
private:
    int calories;
};
