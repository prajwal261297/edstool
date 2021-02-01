#!/usr/bin/python3
import subprocess
import sys
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(passe,filename):
	chunksize =64*1024
	outputFile = "encrypted_" + filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(passe, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk +=b' ' * (16-(len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))

def decrypt(passd, filename):
	chunksize = 64*1024
	outputFile = "decrypted_" + filename[10:]

	infile = open(filename, 'rb')
	filesize = int(infile.read(16))
	IV = infile.read(16)

	decryptor = AES.new(passd, AES.MODE_CBC, IV)


	outfile =  open(outputFile, 'wb')
	while True:
		chunk = infile.read(chunksize)
		if len(chunk) == 0:
			break
		outfile.write(decryptor.decrypt(chunk))
	outfile.truncate(filesize)

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

def main():
	choice=input('Encrypt(E or e) or decrypt(D or d) or share the file(S or s):  ')
	if choice=='E' or choice=='e':
		filename=input('Enter the file name encrypt: ')
		password=input('Enter Password: ')
		encrypt(getKey(password),filename)
		share=input('Do you want to share this file(yes or no): ')
		if share=='yes' or share=='y':
			subprocess.call('./sharing.sh')
		else:
			pass

	elif choice=='S' or  choice=='s':
		subprocess.call('./sharing.sh')

	elif choice=='D' or choice=='d':
		filename=input('Enter the file name to decrypt: ')
		password=input('Enter password: ')
		decrypt(getKey(password),filename)
	else:
		print('Invalid Choice')

if __name__=='__main__':
	main()
