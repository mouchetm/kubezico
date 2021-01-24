# kubezico

## Running locally

### Install the flask dependencies

Create python virtualenv
```
python3 -m venv ./venv
```

Activate it
```
source venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

To run the dev server
```
flask run
```

### Install Vue dependencies

There are only 3 dependencies : Vuetify JS, axios, vue json pretty

```
vue add vuetify
yarn add axios
yarn add vue-json-pretty@1.7.1
```

Run the local server

```
yarn serve
```

Run as an eletron app

Install the plugin
```
vue add electron-builder
```

```
yarn electron:serve
```

TODO Fix icons

### Packaging

## Packaging the flask app

Here the idea is to create a single executable file that contain our code + venv 
We are using pyinstaller
```
pip install pyinstaller
```

Create the executable
```
pyinstaller --onefile app.py
```

To make sure it works 
```
dist/app
```

## Packaging the flask inside of the electron

Install the required stuff
```
yarn add path and childprocess but I did not have to it the second time
```

```
yarn add electron-builder --dev
```

Update the value of background.js to
```
./src/background.js
```