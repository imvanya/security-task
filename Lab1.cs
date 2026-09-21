using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("N = 18, K = 12, a = 0, b = 2, c = 3\n");

        while (true)
        {
            Console.WriteLine("=== МЕНЮ ВИТОКУ ===");
            Console.WriteLine("1. Завдання 1: Визначення виду трикутника");
            Console.WriteLine("2. Завдання 2: Обробка послiдовностi цифр");
            Console.WriteLine("3. Завдання 4: НСД (Перебор проти Евклiда)");
            Console.WriteLine("0. Вихiд");
            Console.Write("Оберiть пункт (0-3): ");

            if (!int.TryParse(Console.ReadLine(), out int choice))
            {
                Console.WriteLine("Помилка! Введiть цiле число.\n");
                continue;
            }

            switch (choice)
            {
                case 1:
                    Task1();
                    break;
                case 2:
                    Task2();
                    break;
                case 3:
                    Task4();
                    break;
                case 0:
                    return; 
                default:
                    Console.WriteLine("Некоректний вибiр! Спробуйте ще раз.\n");
                    break;
            }
            Console.WriteLine("\n-----------------------------------\n");
        }
    }

    static void Task1()
    {
        Console.WriteLine("\n--- Завдання 1 ---");
        int sideA = ReadInt("Введiть першу сторону (a): ");
        int sideB = ReadInt("Введiть другу сторону (b): ");
        int sideC = ReadInt("Введiть третю сторону (c): ");

        if (sideA <= 0 || sideB <= 0 || sideC <= 0 ||
            sideA + sideB <= sideC || sideA + sideC <= sideB || sideB + sideC <= sideA)
        {
            Console.WriteLine("Трикутник не iнує.");
            return;
        }

        if (sideA == sideB && sideB == sideC)
        {
            Console.WriteLine("Трикутник: Рiностороннiй.");
        }
        else if (sideA == sideB || sideA == sideC || sideB == sideC)
        {
            Console.WriteLine("Трикутник: Рiвнобедрений.");
        }
        else if ((long)sideA * sideA + (long)sideB * sideB == (long)sideC * sideC ||
                 (long)sideA * sideA + (long)sideC * sideC == (long)sideB * sideB ||
                 (long)sideB * sideB + (long)sideC * sideC == (long)sideA * sideA)
        {
            Console.WriteLine("Трикутник: Прямокутний.");
        }
        else
        {
            Console.WriteLine("Трикутник: Рiзностороннiй.");
        }
    }

    static void Task2()
    {
        Console.WriteLine("\n--- Завдання 2 ---");
        int number = ReadInt("Введiть натуральне число: ");

        if (number <= 0)
        {
            Console.WriteLine("Число має бути натуральним (більшим за 0).");
            return;
        }

        int temp = number;
        int digitCount = 0;
        int divisor = 1;

        while (temp > 0)
        {
            digitCount++;
            temp /= 10;
            if (temp > 0) divisor *= 10;
        }

        int sum = 0;
        int zeroCount = 0;
        int targetIndex = -1;
        int currentIndex = 1;

        temp = number;
        while (divisor > 0)
        {
            int digit = temp / divisor;
            temp %= divisor;
            divisor /= 10;

            sum += digit;
            if (digit == 0) zeroCount++;

            if (digit > 12 && targetIndex == -1)
            {
                targetIndex = currentIndex;
            }

            currentIndex++;
        }

        Console.WriteLine($"Спiлтьна частина -> Сума цифр: {sum}, Кiлькiсть нулiв: {zeroCount}");
        Console.WriteLine($"Результат (номер першого елеВента > 12): {targetIndex}");
    }

    static void Task4()
    {
        Console.WriteLine("\n--- Завдання 4 ---");
        int a = 1000018;
        int b = 999981;

        int minVal = a < b ? a : b;
        int gcdBrute = 1;
        long bruteIterations = 0;

        for (int i = minVal; i >= 1; i--)
        {
            bruteIterations++;
            if (a % i == 0 && b % i == 0)
            {
                gcdBrute = i;
                break; 
            }
        }

        int tempA = a;
        int tempB = b;
        long euclidIterations = 0;

        while (tempB != 0)
        {
            euclidIterations++;
            int remainder = tempA % tempB;
            tempA = tempB;
            tempB = remainder;
        }
        int gcdEuclid = tempA;

        Console.WriteLine($"1. Перебор: НСД = {gcdBrute}, iтерацiй = {bruteIterations}");
        Console.WriteLine($"2. Алгоритм Евклiда: НСД = {gcdEuclid}, iтерацiй = {euclidIterations}");
    }

    static int ReadInt(string prompt)
    {
        int result;
        while (true)
        {
            Console.Write(prompt);
            if (int.TryParse(Console.ReadLine(), out result))
            {
                return result;
            }
            Console.WriteLine("Помилка! Введено некоректне значення. Спробуйте ще раз.");
        }
    }
}