# Module 3 Security Demo

For this project, I wanted to build something that felt like a small security lab inside Python. The goal was to create an interactive demo that shows how different protections work in real systems and how they are used for different purposes. I liked that this assignment let me connect the ideas from class to actual code, instead of only reading about them. I used some of the code from the linked video on module 3 assignment from pixegami to build my program and made it my own with smaller implementations.

This application uses a Tkinter GUI to demonstrate the main security concepts I learned:

- **Authentication and RBAC:** users log in with a password and receive either
  the `admin` or `student` role. Only `admin` can create and verify signatures.
- **Caesar cipher:** option 1 shifts letters to encrypt or decrypt a message.
- **SHA-256:** options 2 and 3 hash text or a file. File hashing reads in
  chunks, so it also works for larger files.
- **Digital signatures:** option 4 generates a temporary RSA key pair, signs a
  message with the private key, and verifies it with the public key. It also
  verifies that a changed message fails.

## How I designed this project

I wanted this project to be easy to understand while still showing real security concepts in action. Instead of just displaying lines of code, I built it as a simple demo where the user can actually log in, test different methods, and see what each one does. That made it easier for me to explain how hashing is different from encryption and how signatures help prove authenticity.

## Run

From this directory:

```bash
python -m pip install -r requirements.txt
python Hashing-Encryption-Demo.py
```

The normal command opens the GUI login window. To use the original text-based
menu instead, run:

```bash
python Hashing-Encryption-Demo.py --console
```

Tkinter is included with most Python installations. On Linux, install the
system package for Tkinter if the GUI module is unavailable.

Demo credentials are `admin` / `Admin123!` and `student` / `Student123!`.
Passwords are salted and hashed with PBKDF2-HMAC-SHA256 before comparison;
the application does not store plaintext passwords. The credentials and RSA
keys are intentionally recreated each time for demonstration purposes.

## How this is similar to the Encrypt/Decrypt Demo

This project is very similar to my Encrypt/Decrypt demo because both are hands-on examples that helped me understand how cryptography works in real life. In both projects, I used Python to apply security techniques to input data and then checked the results to see what happened. The biggest difference is the purpose: one project focuses on making data unreadable and recoverable, while this one focuses on proving integrity and protecting stored credentials.

I think the two projects complement each other well. The Encrypt/Decrypt demo helped me see how encryption uses keys to protect confidentiality, and this project helped me understand how hashing is used for verification and security checks. Together they showed me that cybersecurity is not just one single tool; it uses different methods depending on whether the goal is confidentiality, integrity, or authentication. I used the Encrypt Demo to build off of and I think it worked well where it gives someone a easily navigable GUI rather than the terminal (I am a very big advocate of not needing to rely on the terminal and having a UI for my programs if possible)

## Security notes

One of the biggest things I learned from this assignment is that randomness matters a lot in security. Unpredictable salts prevent identical passwords from producing identical stored values, and random RSA key generation creates a fresh key pair. It also taught me why it is important to have long passwords/ passphrases so someone is not able to enter the correct password easily. Weak or predictable randomness makes cryptographic systems easier to guess or reuse. A Caesar cipher is educational only and provides no modern confidentiality. SHA-256 verifies integrity but does not encrypt data, and a signature provides authenticity only when the public key is trusted. My favorite part of this project was trying to make the caesar cipher work on the GUI where you can select how many shifts you want to take, so I used a counter to be able to determine how much you want the shift to move which made it seem more realistic than just having it shift left or right one spot.

