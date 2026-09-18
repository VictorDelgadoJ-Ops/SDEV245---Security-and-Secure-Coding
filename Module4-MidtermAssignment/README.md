# Module 4: Integrity Capsule

Integrity Capsule is a small desktop security lab that combines the work from the earlier assignments into one practical handoff workflow. A user can enter a message or choose a text file, then create a capsule that encrypts the content and stores a SHA-256 fingerprint inside the encrypted package. Opening the capsule decrypts the content and compares the recorded hash with a newly calculated hash. Like said earlier, this is a build off of my earlier projects so the GUI looks very similar, though now it uses a security capsule application which I saw on youtube and thought was very intriguing. This application uses multiple packages from python but overall makes the application simpler and uses the existing packages to make it simpler.

The project carries forward the earlier lessons:

- Salted PBKDF2-HMAC-SHA256 password verification and demo roles from Module 3.
- Fernet symmetric encryption from the Encrypt/Decrypt Demo.
- SHA-256 text/file integrity checks from Module 3.
- A Tkinter interface so the workflow can be demonstrated without relying on the terminal. The interface should look similar to Module 3's interface but with some enhanced looks to make it seem more friendly.

## What makes this project different

Rather than showing encryption, hashing, and decryption as disconnected examples, the application creates a self-describing Integrity Capsule. It records the source type, source name, creation time, and original SHA-256 digest with the encrypted payload. The Open and Verify view shows the recovered content and a clear PASS or FAIL result. The tamper test flips a byte in the encrypted token and demonstrates that authenticated encryption rejects the altered capsule. This is a great project for my midterm project since it incorporates everything from module 1-4. This heavily uses a lot of the information from module 3, and some from module 4's assignment as well with the code snippets.

## Security concepts

**Confidentiality:** Fernet encrypts the capsule with a randomly generated symmetric key. The ciphertext is not readable without the key. This covers the confidentiality part to ensure not anyone is able to read the file.

**Integrity:** SHA-256 creates a fixed-length fingerprint of the original bytes. After decryption, the program hashes the recovered bytes again and compares the values with `hmac.compare_digest`. This will voer the integrity of the file so not every time someone decrypts the file, it will hash the recovered bytes again so its not the same.

**Availability:** The app supports both short messages and file input, reads files through Python's normal file APIs, and reports malformed or unreadable capsules instead of crashing silently.

**Entropy and key generation:** `Fernet.generate_key()` uses the operating system's cryptographically secure random source to create a fresh key for every capsule. The unpredictable key and Fernet's random nonce make repeated input produce different ciphertext. The demo stores the key beside the capsule so the assignment can be demonstrated easily; a production application would protect the key separately, such as with a password-derived key or a key-management service.

## Run

From this directory:

```bash
python -m pip install -r requirements.txt
python secure_capsule.py
```

Use `admin / Admin123!` or `student / Student123!` at the login screen. The passwords are only used to create fresh salted PBKDF2 digests at startup; plaintext passwords are not stored in the user records. This is the same as module 3's asignment so it should look similar to it.

Tkinter is included with most Python installations. The optional `--console` argument checks credentials from the terminal, but the capsule workflow is intentionally presented through the GUI.

## CIA triad summary

- **Confidentiality:** encryption prevents casual access to the protected content.
- **Integrity:** SHA-256 comparison detects changes to the recovered payload, while Fernet also authenticates the encrypted token.
- **Availability:** the application gives users a repeatable way to protect and recover either messages or files and reports errors clearly.

To reiterate, this is meant to serve for only module 4 midterm assignment. Even though the application seems safe and sound, it still has one flaw, which is that is uses the same JSON file to save the stored data, which can be a vulnerability by itself. I also updated the tkinter interface to make it look nicer which I think is an improvement from just using the console, which in my opinion I do not enjoy. I will say that for module 4, it covers all the basis for the midterm project, but by the final project, I want to continue this application built and fix all the vulnerability issue's it has and make the interface much better as well. The work that has been done so far is just my knowledge from the module's given so far.