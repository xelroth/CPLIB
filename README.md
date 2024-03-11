### Instalization ♨️
First You Have To Clone This Responsitory Using The Following Command

```
git clone https://github.com/xelroth/CPLIB/
```
If You Are Using Windows You Have To Download Files Or Download The Archived File
Then Use The Following Command For Installing The Library And Required Libraris
```
Python3 setup.py install
```

## CPLIB Documentation 📚

### CPanel Class:
Constructor
- cpanel = Cpanel(domain, user, password, port='2083') -> Initializes a Cpanel object with the specified domain, user, password, and port.

Methods
- cron_jobs(data={}): Add a cron job with the specified data.
- delete_cron(data={}): Delete a cron job based on the provided data.
- account_ftp(data={}): Add an FTP account with the given data.
- del_account_ftp(data={}): Delete an FTP account based on the provided username.
- create_database(name): Create a database with the specified name.
- delete_database(name): Delete a database with the specified name.

### FileManager Class:
Constructor
- file_manager = FileManager(domain, user, password) -> Initializes a FileManager object with the specified domain, user, and password.

Methods
- create_folder(data={}): Create a new folder with the provided data.
- delete_folder(data={}): Delete a folder based on the provided data.
- create_file(data={}): Create a new file with the specified data.
- delete_file(data={}): Delete a file based on the provided data.
- rename(data={}): Rename a file or folder to a new name.
- upload(data={}): Upload a file from a URL to the specified location.
- info_file(data={}): Get information about a file including its size and name.
- list_content(data={}): List the contents of a folder.
- copy_file(data={}): Copy a file from one location to another.
- file_put(data={}): Put data into a file at the specified location.


==============================
### cron_jobs(data={})

- This method allows you to add a new cron job to the cPanel server. It takes a dictionary data as an argument, which should contain the following keys: command, minute, day, hour, month, and weekday. The method
returns true if the cron job is added successfully, otherwise it returns an error message.

```
data = {
    'command': 'python script.py',
    'minute': '0',
    'hour': '1',
    'day': '*',
    'month': '*',
    'weekday': '*'
}
result = cpanel.cron_jobs(data)
print(result)
```
==============================
### delete_cron(data={})

- This method allows you to delete a cron job from the cPanel server. It takes a dictionary data as an argument, which should contain the line key specifying the line number of the cron job to be deleted. The method returns true if the cron job is deleted successfully, otherwise it returns an error message.

```
data = {
    'line': '1'
}
result = cpanel.delete_cron(data)
print(result)
```
==============================
### account_ftp(data={})

- This method allows you to create a new FTP account on the cPanel server. It takes a dictionary data as an argument, which should contain the following keys: username, password, quota, and addressdir. The method returns true if the FTP account is created successfully, otherwise it returns an error message.

```
data = {
    'username': 'ftpuser',
    'password': 'ftppassword',
    'quota': '100',
    'addressdir': '/public_html'
}
result = cpanel.account_ftp(data)
print(result)
```
==============================
### del_account_ftp(data={})

- This method allows you to delete an FTP account from the cPanel server. It takes a dictionary data as an argument, which should contain the username key specifying the username of the FTP account to be deleted. The method returns true if the FTP account is deleted successfully, otherwise it returns an error message.

```
data = {
    'username': 'ftpuser'
}
result = cpanel.del_account_ftp(data)
print(result)
```
==============================
### create_database(name)

- This method allows you to create a new database on the cPanel server. It takes the name of the database as an argument. The method returns true if the database is created successfully, otherwise it returns an error message.

```
result = cpanel.create_database('mydatabase')
print(result)
```
==============================
# delete_database(name)
- This method allows you to delete a database from the cPanel server. It takes the name of the database as an argument. The method returns true if the database is deleted successfully, otherwise it returns an error message.

```
result = cpanel.delete_database('mydatabase')
print(result)
```
==============================


### FileManager Class ###


- The FileManager class provides methods for interacting with FTP servers. To use this class, you need to instantiate an object by providing the domain, username, and password. 

```
file_manager = FileManager(domain, user, password)
```



# -> connect_to_server()

- This method allows you to connect to the FTP server. It returns true if the connection is successful, otherwise it returns false.

```
result = file_manager.connect_to_server()
print(result)
```

# -> create_folder(data={})

- This method allows you to create a new folder on the FTP server. It takes a dictionary data as an argument, which should contain the address key specifying the address of the folder to be created. The method returns Created if the folder is created successfully, otherwise it returns Error.

```
data = {
    'address': '/folder/subfolder'
}
result = file_manager.create_folder(data)
print(result)
```

# -> delete_folder(data={})

- This method allows you to delete a folder from the FTP server. It takes a dictionary data as an argument, which should contain the address key specifying the address of the folder to be deleted. The method returns Deleted if the folder is deleted successfully, otherwise it returns Error.

```
data = {
    'address': '/folder/subfolder'
}
result = file_manager.delete_folder(data)
print(result)
```

# -> create_file(data={})

This method allows you to create a new file on the FTP server. It takes a dictionary data as an argument, which should contain the address key specifying the address of the file to be created. The method returns Created if the file is created successfully, otherwise it returns Error.

```
data = {
    'address': '/folder/file.txt'
}
result = file_manager.create_file(data)
print(result)
```

# -> delete_file(data={})

- This method allows you to delete a file from the FTP server. It takes a dictionary data as an argument, which should contain the address key specifying the address of the file to be deleted. The method returns Deleted if the file is deleted successfully, otherwise it returns Error.

```
data = {
    'address': '/folder/file.txt'
}
result = file_manager.delete_file(data)
print(result)
```

# -> rename(data={})

- This method allows you to rename a file or folder on the FTP server. It takes a dictionary data as an argument, which should contain the address key specifying the address of the file or folder to be renamed, and  the Newaddress key specifying the new address. The method returns true if the file or folder is renamed successfully, otherwise it returns Error.

```
data = {
    'address': '/folder/file.txt',
    'Newaddress': '/folder/newfile.txt'
}
result = file_manager.rename(data)
print(result)
```

# -> pload(data={})

- This method allows you to upload a file to the FTP server from a URL. It takes a dictionary data as an argument, which should contain the url key specifying the URL of the file to be uploaded, the address key specifying the address on the FTP server where the file should be uploaded, and the namefile key specifying the name of the file. The method returns Uploaded if the file is uploaded successfully, otherwise it returns Error.


# -> upload(data={})

- This method allows you to upload a file to the FTP server from a URL. It takes a dictionary data as an argument, which should contain the url key specifying the URL of the file to be uploaded, the address key specifying the address on the FTP server where the file should be uploaded, and the namefile key specifying the name of the file. The method returns Uploaded if the file is uploaded successfully, otherwise it returns Error.

```
data = {
    'url': 'https://example.com/file.txt',
    'address': '/folder',
    'namefile': 'file.txt'
}
result = file_manager.upload(data)
print(result)
```

# -> info_file(data={})

- This method allows you to get information about a file on the FTP server. It takes a dictionary data as an argument, which should contain the address key specifying the address of the file. The method returns a dictionary with the following keys: status (True if the file exists, False otherwise), size (the size of the file), and namefile (the name of the file).


```
data = {
    'address': '/folder/file.txt'
}
result = file_manager.info_file(data)
print(result)
```

# -> list_content(data={})

- This method allows you to list the contents of a folder on the FTP server. It takes a dictionary data as an argument, which should contain the address key specifying the address of the folder. The method returns a string containing the names of the files and folders in the specified folder.

```
data = {
    'address': '/folder'
}
result = file_manager.list_content(data)
print(result)
```

# -> copy_file(data={})

- This method allows you to copy a file on the FTP server. It takes a dictionary data as an argument, which should contain the localaddress key specifying the local address of the file to be copied, and the Newaddress key specifying the new address on the FTP server. The method returns true if the file is copied successfully, otherwise it returns Error.

```
data = {
    'localaddress': 'local/file.txt',
    'Newaddress': '/folder/file.txt'
}
result = file_manager.copy_file(data)
print(result)
```

# -> file_put(data={})

- This method allows you to create a new file on the FTP server and write data to it. It takes a dictionary data as an argument, which should contain the address key specifying the address of the file to be created, and the data key specifying the data to be written to the file. The method returns true if the file is created and data is written successfully, otherwise it returns Error.

```
data = {
    'address': '/folder/file.txt',
    'data': 'Hello, World!'
}
result = file_manager.file_put(data)
print(result)
```

### Conclusion

- This documentation provides an overview of the provided Python library for interacting with cPanel and FTP servers. It explains the usage of each function and provides examples to help you understand how to use the library effectively. Feel free to explore the library further and customize it according to your specific needs.



🚀 Feel free to explore and use this library for your projects! 🚀

Feel free to add more descriptive details, examples, or usage instructions to make the documentation more comprehensive and user-friendly. Happy coding! 📝
If You Enjoy Using This Library, Then Dont Forget TO Give A Star To It! 🌟

⚠️ THIS PROJECT IS UNDER MIT LICENSE! FOLLOW THE LICENSE FILE TO GET MORE INFORMATION ⚠️
