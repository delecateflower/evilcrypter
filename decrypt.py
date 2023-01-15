import argparse
import os
import sys
import rsa
from crypt import _texter
from cryptography.fernet import Fernet


def _dir_encrypter(dirpath,rsadirkey,cryptdirkey):
        with open(rsadirkey,"rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        with open(cryptdirkey, "rb") as f:
            key = f.read()

        for root,dirname,files, in os.walk(f"{dirpath}"):
            for file in files:
                filepath = root + "/" + file
                filesize = os.path.getsize(filepath)
                int(filesize)
                if filesize < 177:
                    with open(filepath,"rb") as original:
                        data = original.read()
                        decrypted_data = rsa.decrypt(data, private_key)
                        with open(filepath,"wb") as encrypted:
                            print(decrypted_data)
                            encrypted.write(decrypted_data)
                            filename = os.path.basename(filepath)
                            _texter(f"[+] [{filename}] has been successfully decrypted\n")
                else:
                    decrypt = Fernet(key)
                    with open(filepath,"rb") as f:
                        data = f.read()
                        decrypted_data = decrypt.decrypt(data)
                        with open(filepath,"wb") as f:
                            f.write(decrypted_data)
                            filename = os.path.basename(filepath)
                            _texter(f"[+] [{filename}] has been successfully decrypted\n")


def _decrypt(file_path,key_file):
    try:
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(filename)

        with open(key_file,"rb") as key:
            private_key = rsa.PrivateKey.load_pkcs1(key.read())

            with open(file_path,"rb") as encrypted:
                data = encrypted.read()

                decrypted_data = rsa.decrypt(data,private_key)
                with open(file_path,"wb") as decrypted:
                    decrypted.write(decrypted_data)

        _texter(f"[+] {filename} has been successfully decrypted.\n")
        _texter(f"[-] {filesize} is the full size of the file\n")
    except:
        sys.exit("[-] Oops error decrypting data.You are not permitted.The devil does not know you!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypts encrypted file with key")
    parser.add_argument('--filepath', dest="filepath", action="store", type=str, required=False)
    parser.add_argument('--keyfile', dest="keyfile", action="store", type=str, required=False)
    parser.add_argument('--dirpath', dest="dirpath", action="store", type=str,required=False)
    parser.add_argument('--dirkeyfile', dest="dirkeyfile", action="store", type=str,required=False)
    parser.add_argument('--cryptdirkey', dest="cryptdirkey", action="store", type=str, required=False)
    arguments = parser.parse_args()
    if arguments.filepath != None:
        _decrypt(arguments.filepath,arguments.keyfile)
    else:
        _dir_encrypter(arguments.dirpath,arguments.dirkeyfile,arguments.cryptdirkey)
