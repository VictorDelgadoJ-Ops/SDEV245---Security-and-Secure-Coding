//A02: Cryptographic Failures.

//Original problem: MD5 and SHA-1 are fast, obsolete password hashes without
//salts, making stolen password databases easier to crack.
//Change made: I replaced MD5 with BCrypt to make the password hash harder to
//crack. BCrypt also adds a salt and uses a work factor.


import org.mindrot.jbcrypt.BCrypt;

public String hashPassword(String password) {
    return BCrypt.hashpw(password, BCrypt.gensalt(12));
}
