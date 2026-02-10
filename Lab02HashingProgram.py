import os
import json
import hashlib

HASH_FILE = "hash_table.json"

def hash_file(filepath):
    sha256 = hashlib.sha256()
    try:
        f = open(filepath, "rb")
        while True:
            data = f.read(4096)
            if not data:
                break
            sha256.update(data)
        f.close()
        return sha256.hexdigest()
    except:
        return None

def traverse_directory(directory):
    hashes = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = hash_file(filepath)
            if file_hash is not None:
                hashes[filepath] = file_hash
    return hashes

def generate_table(directory):
    hashes = traverse_directory(directory)
    f = open(HASH_FILE, "w")
    json.dump(hashes, f, indent=4)
    f.close()
    print("Hash table generated.")

def validate_hash(directory):
    if not os.path.exists(HASH_FILE):
        print("No hash table found.")
        return

    f = open(HASH_FILE, "r")
    stored_hashes = json.load(f)
    f.close()

    current_hashes = traverse_directory(directory)

    for filepath in stored_hashes:
        if filepath in current_hashes:
            if stored_hashes[filepath] == current_hashes[filepath]:
                print(filepath + " hash is valid.")
            else:
                print(filepath + " hash is INVALID.")
        else:
            print(filepath + " was deleted.")

    for filepath in current_hashes:
        if filepath not in stored_hashes:
            print(filepath + " is a new file.")

def main():
    print("1. Generate new hash table")
    print("2. Verify hashes")

    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        directory = input("Enter directory path: ")
        generate_table(directory)
    elif choice == "2":
        directory = input("Enter directory path: ")
        validate_hash(directory)
    else:
        print("Invalid choice.")

main()
