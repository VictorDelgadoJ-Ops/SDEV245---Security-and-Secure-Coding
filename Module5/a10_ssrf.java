//A07: Identification and Authentication Failures.

//Original problem: the application compared the entered password as plain text.
//Change made: I used BCrypt to compare the entered password with its stored
//hash, instead of comparing plain-text passwords.

import org.mindrot.jbcrypt.BCrypt;

if (BCrypt.checkpw(inputPassword, user.getPassword())) {
    // Login success
}


