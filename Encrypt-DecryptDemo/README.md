# Encrypt/Decrypt Demo

## Assignment Overview

For this assignment, I built a small Python program that demonstrates how symmetric and asymmetric encryption work in real life. The goal was to compare two different encryption methods using the same message and show how each one handles keys, ciphertext, and decryption. This project was a good way for me to practice using Python libraries and better understand the difference between Fernet and RSA. The beginning part of this was the hardest part since I had not used Fernet and RSA in the past, but once I saw a youtube tutorial on what they do, it helped me see how they work and how they apply to the real world.

## What the Application Does

This program asks the user to enter a message, then it encrypts that message using:

- Fernet (symmetric encryption)
- RSA (asymmetric encryption)

After encrypting the message, the script decrypts it to confirm the data can be recovered correctly. It also measures how long each encryption takes and saves a full report to `demo_output.txt`.

## Project Files

- `encrypt_demo.py` - the main script that runs both encryption examples
- `demo_output.txt` - the generated report showing the keys, ciphertext, decrypted output, and timing
- `requirements.txt` - the dependency file for the project

## How It Works

The program uses `cryptography` to generate a new Fernet key for the symmetric demo and a public/private RSA key pair for the asymmetric demo. It then:

1. Encrypts the user input
2. Decrypts the encrypted version
3. Prints the output to the console
4. Saves the results to `demo_output.txt`

This makes it easy to compare how both methods behave with the same message.

## How to Run

```bash
python -m pip install -r requirements.txt
python encrypt_demo.py
```

When you run the program, it will prompt you to enter a message. After that, it will display the encrypted and decrypted results in the terminal and save the report to the project folder.

## Why I Chose This Project

I picked this project because I wanted to learn more about encryption in a hands-on way instead of just reading about it. It helped me understand that symmetric encryption uses one shared key, while asymmetric encryption uses a public key and a private key. Seeing both methods side by side made the concept much easier to understand. Using the already available packages python had and the imports like time and cryptography help cut down on redundant code I had, and shows how long it takes to encrypt and decrypt the code. You are able to put a message as an input and see how long the process takes and each have a different amount of times it takes to process which is neat!

## Reflection

This assignment was useful because it combined Python programming with cybersecurity concepts. I was able to practice working with real encryption libraries, handling keys, and checking whether encrypted data could be successfully decrypted. Overall, this project helped me understand the basics of encryption and how different methods are used in security applications.
