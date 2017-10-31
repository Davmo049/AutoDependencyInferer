#include "circ1.hpp" //nm U
#include "circ2.hpp"

#include "globals.hpp"

#include <iostream>


int Numbers::largeValue = 123; //nm D
int bss=0; // nm B
void circ2(int i) //nm T
{
    std::cout << "bss" << bss << std::endl;
    circ1(i);
    std::cout << "circ2:" << i << " " << Numbers::largeValue << std::endl;
}
