/*
 * The problem here was that the original code tried to add 1 to the largest possible int value.
 * Once an int reaches int.MaxValue, it cannot keep growing, so the value overflows and becomes unpredictable.
 *
 * I fixed it by checking whether the number is already at the maximum before incrementing it.
 * If it is, the program stops and prints a safe message instead of trying to overflow.
 * That keeps the program stable and avoids bad values.
 */
using System;

class Program
{
    static void Main(string[] args)
    {
        int number = int.MaxValue;

        if (number == int.MaxValue)
        {
            Console.WriteLine("The value is already at the maximum int value.");
            return;
        }

        number += 1;
        Console.WriteLine("The incremented value is: " + number);
    }
}
