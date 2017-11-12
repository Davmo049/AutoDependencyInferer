#include "circ1.hpp"
#include "circ2.hpp"
#include "hippo.hpp" //nm W
#include "fruit.hpp"
#include "folder/banana.hpp"
#include "globals.hpp" //nm U

#include <iostream>
#include <utility>

void circ1(int i) //nm T
{
    if ((i % 2) == 1)
    {
        circ2(i+1);
    }
    std::cout << "circ1:" << i << " " << Numbers::largeValue << std::endl;
    Banana ban = Banana();
    hippoEat(ban);
}
