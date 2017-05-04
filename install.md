# Installation 

Installing the "fanekart" tracking application is straightforward. 

The tracker itself is an app running on your smart phone (LINK) 

For server backend, I've choosen [pythonanywhere](https://www.pythonanywhere.com), a cloud hosting provider for with a strong love for web applications written in python *(and a great starting point for anyone who wants to learn python, but can't or won't install anything at their local machine)*. Their free account is plenty for this application (but you won't regret shilling out for their paid services, starting at $5/mo). 

If you have your own server, installing your own flask web app with this application should also be easy. 

## Pythonanywhere

### 1. Your pythonanywhere account 

Sign up for a free account at [pythonanywhere](https://www.pythonanywhere.com). 

### 2. Flask web app 

Get your web app up and running at your pythonanywhere installation. Click the "Web" tab, then the "add a new web app" button. 

![pythonanywhere web tab -> add a new web app](https://github.com/LtGlahn/fanekart/blob/master/images/pythonanywhere-startwebapp.png) 

Click at the **Flask** option at the choice **"Select a python web framework"**. Otherwise just use the default options. 

You then have to tell your web app where to put non-dynamic content (html, javascript etc). Scroll down to the **"Static files:** section. 

Your settings should be 
```
URL: /static/
Directory: /home/<yourPytonanywereUsername>/mysite/static/ 
```

In the example below, my pythonanywhere username is *JanFreeBeer* (note: Case sensitive!)

![Pythonanywhere add folder for static files](https://github.com/LtGlahn/fanekart/blob/master/images/pythanywhere-staticfiles.png)  







