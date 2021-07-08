#include <stdio.h>
#include <stdlib.h>

void main(int argc, char *argv[] )
{

    int i, n, p, count, flag;
    n = atoi(argv[1]);
    p = 2;
    i = 1;
    while (i <= n)
    {
        flag = 1;
        for (count = 2; count <= p - 1; count++)
        {
            if (p % count == 0) //Will be true if p is not prime
            {
                flag = 0;
                break; //Loop will terminate if p is not prime
            }
        }
        if (flag == 1)
        {
            i++;
        }
        p++;
    }
}