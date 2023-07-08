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

### 2.4. Load Flows

### 2.5. Save Flows

