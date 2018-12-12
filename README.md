# CPSC_471_Term_Project

Team Members:
John Lee


## How to run:
As our project was written using python3, please make sure that the correct version of python is running 
on your machine before executing our code. 
Open two command line/terminal tabs, and simply enter 


### Server:

```bash
python3 sendfileserver.py <port number>
```

### Client:
```bash
python3 sendfileclient.py <hostname> <port number>
```

## Commands:

### Put:
To put a file to a server, enter
```bash
Put <filename>
```


### Get:
To get a file from the server, enter
```bash
Get <filename>
```
Keep in mind, that the file must first be put to the server before getting it.


### LS:
To get a listing of files from the server, enter
```bash
ls
```

### Quit:
To quit execution, enter
```bash
quit
```
