from time import sleep
import rsa
import os
import sys
import argparse
from cryptography.fernet import Fernet


def _dir_encrypter(dirpath):
    try:
        publicdir_key , privatedir_key = rsa.newkeys(1024)
        with open("dirpriv.pem","wb") as f:
            f.write(rsa.PrivateKey.save_pkcs1(privatedir_key))
        with open("dirpub.pem","wb") as f:
            f.write(rsa.PublicKey.save_pkcs1(publicdir_key))

            dirkey = Fernet.generate_key()
            with open("dirname.key", "wb") as f:
                f.write(dirkey)

        for root,dirname,files, in os.walk(f"{dirpath}"):
            for file in files:
                filepath = root + "/" + file
                filesize = os.path.getsize(filepath)
                int(filesize)
                if filesize < 177:
                    with open(filepath,"rb") as original:
                        data = original.read()
                        encrypteddir_data = rsa.encrypt(data,publicdir_key)
                        with open(filepath,"wb") as encrypted:
                            encrypted.write(encrypteddir_data)
                            filename = os.path.basename(filepath)
                            _texter(f"[+] [{filename}] has been successfully encrypted rsa encryption\n")
                else:
                    with open("dirname.key","rb") as f:
                        key = f.read()
                        encrypt = Fernet(key)
                        with open(filepath,"rb") as f:
                            data = f.read()
                            encrypted_data = encrypt.encrypt(data)
                            with open(filepath,"wb") as f:
                                f.write(encrypted_data)
                                filename = os.path.basename(filepath)
                                _texter(f"[+] [{filename}] has been successfully encrypted using cryptography\n")
    except:
        sys.exit("error encyrpting the directory.need root permissions")


def _texter(payload):
    for letter in payload:
        sys.stdout.write(letter)
        sys.stdout.flush()
        sleep(.001)


def _file_encrypter(path):
    try:
        public_key , private_key = rsa.newkeys(1024)
        with open("private.pem","wb") as private:
            private.write(rsa.PrivateKey.save_pkcs1(private_key))
        with open("public.pem","wb") as public:
            public.write(rsa.PublicKey.save_pkcs1(public_key))

        filename = os.path.basename(path)
        filesize = os.path.getsize(filename)

        with open(path,"rb") as f:
            data = f.read()
            encrypted_data = rsa.encrypt(data,pub_key=public_key)
            with open(path,"wb") as f:
                f.write(encrypted_data)
        _texter(f"[+] {filename} has been sucecsfully encrypted\n")
        _texter(f"[+] {filesize} is the filesize of file\n")
    except:
        sys.exit("[-] Check whether you have rsa library idiot")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="encrypts the file content.")
    parser.add_argument('--filepath',dest="filepath",action='store',type=str,required=False)
    parser.add_argument('--dirpath', dest="dirpath", action="store", type=str,required=False)
    arguments = parser.parse_args()
    if arguments.filepath != None:
        _file_encrypter(path=arguments.filepath)
    else:
        _dir_encrypter(dirpath=arguments.dirpath)

