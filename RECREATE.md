# Steps to recreate the step of project -> Blog post

## Python backend

Create app.py file :)

## Vue app

Create the project

```
vue create kubezico
```

There are only 3 dependencies : Vuetify JS, axios, vue json pretty

```
vue add vuetify
yarn add axios
yarn add vue-json-pretty@1.7.1
```

Important to fix the vue json pretty version

Install the plugin
```
vue add electron-builder
```
electron version 9

Fix the icons and procedure

Building:

```
yarn electron:build
```

The app worked using electron serve but not using electron build and running it as a mac app.
I changed something in vue.config.js

Add the logger
```
yarn add electron-log
```

I have a problem of cors. 
I hardcoded the path of the app to run and the backend is launched.
When commenting the execFile and using the raw flask app (flask run) evrything works
But when flask is app/dist it does not.

Usefull tip.
To access the console.log of the packaged app just run the build in application directory

When deleting the process on close
https://stackoverflow.com/questions/36031465/electron-kill-child-process-exec
https://www.ericluwj.com/2015/11/25/nodejs-spawn-vs-execfile.html

It was difficult to reach the path of the exec python as it keeps saying he runs as top process
To get rid of this and keep data, I spawn the python process with the path of the data