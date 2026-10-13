/*
 * The original ZIP code pattern was too broad and did not clearly match the format the user was expected to enter.
 * That means some invalid values could slip through if the pattern was not strict enough.
 *
 * I fixed it by using a pattern that only allows either a 5-digit ZIP code or a ZIP+4 code.
 * That matches the real format most people use and rejects entries that are not valid.
 */
import java.util.regex.*;
import java.util.Scanner;

public class ZipCodeValidator {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            String zipPattern = "^\\d{5}(-\\d{4})?$";
            System.out.print("Enter a zipcode: ");
            String zipCode = scanner.nextLine();

            if (zipCode.matches(zipPattern)) {
                System.out.println("Correct zip code");
            } else {
                System.out.println("Incorrect zip code");
            }
        }
    }
}
