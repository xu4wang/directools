# directools
A set of tools for using directus in real world projects.   Managing roles, permissions, flows and operations as code.


## 1. Features

- Save roles and permissions into files in JSON format
- Load roles and permissions from JSON files into a directus instance.
- Save flows and operations into files in JSON format
- Load flows and operations from JSON files into a directus intance.

The idea is to keep the settings in the Directus admin APP into human readable JSON files, so it can be version controlled and re-deployed.

## 2. How to use

### 2.1. Setup Dev Environment 

#### Set up Directus

For testing purpose, we start directus locally using docker.

```
cd test
docker compose up
```

1. Open browser and visit http://localhost:8055/  , with user name `admin@example.com` and password `d1r3ctu5`.

2. Set a static token for admin user. 
In my case, the token is `GNuG2xodzTMY19AaYh0r7yYNWSqWF-AE`

#### Create Collections

### 2.2. Load Roles

### 2.3. Save Roles

### 2.4. Save Flows

change current directory to src and run `python save_flows.py`

the script will try to save all the flows into a directory configured in the config.ini file.
Please make sure you set the correct url and token for dirctus, in the config.ini file.
You can take config.ini.sample as an example.

![image](https://github.com/kinnovent/directools/assets/311397/87f14b3f-6d69-4b8f-a10d-ef4f844eadb0)


### 2.5. Load Flows

change current directory to src and run `python load_flows.py`

the script will try to load all the flows from a directory configured in the config.ini file.
