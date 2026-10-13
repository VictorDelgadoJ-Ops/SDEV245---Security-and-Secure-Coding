/*
 * The problem here was that y was being used before it had a value.
 * Java needs a variable to be declared and initialized before you print it or use it in code.
 *
 * I fixed it by adding: int y = 10;
 * That gives the variable a proper starting value, so the program prints correctly.
 * This is a small fix, but it resolves the error and makes the program work.
 */
public class Exercise2 {
    public static void main(String[] args) {
        int y = 10;
        System.out.println("The value of y is: " + y);
    }
}
