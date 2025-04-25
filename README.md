DuLLahan - BotFirmFramework
============================

(WIP) 


# Usage

(WIP)

install to local environment with `-e` option

```
pip install -e
```

and import this library


##  sample : jupyter notebook

(WIP)


## sample : python code

(WIP)







# To run examples

You need to install python environment. recommend to use venv and activate.

```
python -m venv .venv
.venv\scripts\activate
```


# To test

We use pytest testing framework. and, need to add PYTHON_PATH environemnt variable.

```powershell
# for example windows / powershell
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)";
pytest .\test\
```

