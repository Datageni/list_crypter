# List Crypter

## Overview

`list_crypter` is a digital agenda program designed to securely manage tasks and lists by encrypting the stored information. The application allows users to create, read, update, and delete lists, ensuring that unauthorized users cannot access the personal information contained within these lists. The program requires a password for any operation that involves reading, updating, or deleting specific tasks, while creating and deleting entire lists do not require authentication.

## Repository Structure

The repository is divided into three main scripts:

1. **main.py**
   - Stores the main menu.
   - Calls the four CRUD functions (Create, Read, Update, Delete) to manage lists.

2. **crud_functions.py**
   - Contains the four CRUD functions:
     - `create_list()`: Create new lists.
     - `read_list()`: Read and decrypt existing lists.
     - `update_list()`: Update tasks within a list.
     - `delete_list()`: Delete specific tasks from a list.

3. **functions.py**
   - Stores functions unrelated to CRUD operations.
   - Includes encryption and decryption functions to secure data.
   - Contains additional helper functions for the program's functionality.

## Functionality

### Main Menu

The main menu in `main.py` provides options for users to:
- Create a new list
- Read an existing list (requires password)
- Update an existing list (requires password)
- Delete an entire list

### Encryption

The program uses symmetric encryption to secure the data within the lists. The encryption process ensures that unauthorized users cannot view the contents of the lists without the correct password.

#### Key Derivation Function

The key derivation function (KDF) is used to generate a secure encryption key from the user's password. The `PBKDF2HMAC` algorithm is used with the following parameters:
- Algorithm: SHA256
- Key Length: 32 bytes
- Salt: Retrieved from an environment variable (`env_salt`)
- Iterations: 100,000

The derived key is then base64-encoded for use in encryption and decryption functions.

#### Mathematical Explanation

1. **Key Derivation:**
   - The `PBKDF2HMAC` function derives a key from the user's password and salt using HMAC (Hash-based Message Authentication Code) with SHA256 as the hashing algorithm.
   - Formula: 
     $\text{key} = \text{Base64Encode}(\text{PBKDF2HMAC}(\text{password}, \text{salt}, \text{iterations} = 100000, \text{algorithm} = \text{SHA256}, \text{length} = 32}))$
   - Here, the `PBKDF2HMAC` function applies the HMAC algorithm 100,000 times to the password and salt to derive a 32-byte key. The key is then encoded in base64 for use.

2. **Encryption:**
   - The `Fernet` encryption scheme from the `cryptography` library is used to encrypt messages.
   - Formula: 
     $\text{encrypted\_message} = \text{Fernet}(\text{key}).\text{encrypt}(\text{message})$
   - The encryption process involves taking the derived key and the plaintext message, and using the `Fernet` scheme to produce an encrypted message.

3. **Decryption:**
   - The `Fernet` decryption scheme is used to decrypt messages.
   - Formula: 
     $\text{message} = \text{Fernet}(\text{key}).\text{decrypt}(\text{encrypted\_message})$
   - The decryption process involves taking the derived key and the encrypted message, and using the `Fernet` scheme to produce the original plaintext message.





### Usage

To use the program, follow these steps:

1. **Set Environment Variables:**
   - `env_password`: The password used for encryption and decryption.
   - `env_salt`: The salt used in the key derivation process.
   - `BASE_DIR`: The directory where the lists will be stored.

2. **Run the Main Script:**
   - Execute `main.py` to access the main menu and perform desired operations.

