/*
 * The issue here was pretty simple: the program tried to use z before it was actually created.
 * Java does not let you use a variable unless it has been declared and given a value first.
 *
 * I fixed it by adding the missing line: int z = 24;
 * That gives the variable a real value before the program prints it.
 * Now the code runs normally and shows the correct output.
 */
public class Exercise1 {
    public static void main(String[] args) {
        int z = 24;
        System.out.println("The value of z is: " + z);
    }
}
