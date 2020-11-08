# Ing_Soft_1-KND

## Back installation to python 3.6.X and python 3.8.X / 3.7.X

### Check your python3 version

```bash
$ python3 --version
```

### Check if venv is installed.

```bash
$ whereis pyvenv-3
```

If something like the following appears

```
pyvenv-3: path/pyvenv-3.X
```

the venv of your python3 is installed.

If nothing appears, execute

```bash
$ sudo apt-get install python3-venv
```

### Create your virtual enviroment with name 'namevenv' (or other name that you like)

```bash
$ python3 -m venv namevenv
```

### Download repository, activate your virtual enviroment

```bash
$ git clone https://github.com/Diegoolei/Ing_Soft_1-KND_Back.git
$ source namevenv/bin/activate
$ cd Ing_Soft_1-KND_Back
```

### Install resources in your virtual enviroment

**If your version is 3.6.X** 

```bash
$ pip install -r requirements0.txt
```

**If your version is 3.7.X / 3.8.X**

```bash
$ pip install -r requirements1.txt
```

### Run your unicorn server 

```bash
$ uvicorn main:app --reload
```

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13331] using statreload
INFO:     Started server process [13334]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Deactivate your virtual enviroment

```bash
$ deactivate
```
