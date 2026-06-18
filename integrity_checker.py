import hashlib

filename = input("Enter file name: ")

try:
    with open(filename, "rb") as file:
        file_data = file.read()

    sha256_hash = hashlib.sha256(file_data).hexdigest()

    print("\nSHA-256 Hash:")
    print(sha256_hash)

except FileNotFoundError:
    print("File not found!")
