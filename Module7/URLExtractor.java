/*
 * The issue with the original regex was that it was too loose and not strict enough for a real URL.
 * That means it could match bad or weird input instead of only valid website addresses.
 *
 * I fixed it by using a simpler pattern that only accepts a normal http or https URL with a valid domain.
 * It checks for the structure we expect and ignores anything that does not look like a real web address.
 */
import java.util.regex.*;

public class URLExtractor {
    public static void main(String[] args) {
        String text = "Visit my website at http://www.url.example.com";
        String regex = "https?://[A-Za-z0-9.-]+\\.[A-Za-z]{2,}(:[0-9]+)?(/[A-Za-z0-9._~:/?#[\\]@!$&'()*+,;=%-]*)?";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(text);

        while (matcher.find()) {
            System.out.println("URL: " + matcher.group());
        }
    }
}
