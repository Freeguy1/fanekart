# Installation 


## Pythonanywhere server backend

### 1. Your pythonanywhere account 

Sign up for a free account at [pythonanywhere](https://www.pythonanywhere.com). Note your username (case sensitive). 

### 2. Get your flask web app running. 

Get your flask web app up and running at your pythonanywhere installation. Click the "Web" tab, then the "add a new web app" button. 

![pythonanywhere web tab -> add a new web app](https://github.com/LtGlahn/fanekart/blob/master/images/pythonanywhere-startwebapp.png) 

Click at the **Flask** option at the choice **"Select a python web framework"**. Otherwise go with the defaults. 

You then have to tell your web app where to put non-dynamic content (html, javascript etc). Scroll down to the **"Static files:** section. 

Your settings should be 
```
URL: /static/
Directory: /home/<yourPytonanywereUsername>/mysite/static/ 
```

In the example below, my pythonanywhere username is *JanFreeBeer* (note: Case sensitive!)

![Pythonanywhere add folder for static files](https://github.com/LtGlahn/fanekart/blob/master/images/pythanywhere-staticfiles.png)  

Hit **Reload web app**. 

### 3. Download the fanekart web application. 

In your browser, open a console. Type 
```
git clone https://github.com/LtGlahn/fanekart
```

### 4. Configure fanekart. 

*To be written... basically moving files, inserting the appropriate folder names and links at the appropriate places. I'm writing a shell script that should take care of all this* 

### 5. Your tracker. 






