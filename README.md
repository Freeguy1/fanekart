# fanekart
A web application for showing live tracking data from an app at your smart phone, or any device capable of sending coordinates to a web server on the form: 
```
https://yourserver.com/gpsId/secretKey?lon=61.5555&lat=7.4444 
```

For server backend, I've choosen [pythonanywhere](https://www.pythonanywhere.com), a cloud hosting provider for with a strong love for web applications written in python *(and a great starting point for anyone who wants to learn python, but can't or won't install anything at their local machine)*. Their free account is plenty for this application (but you won't regret shilling out for their paid services, starting at $5/mo). 

Getting this up and running at your own flask web server should also be easy. Just look at the installation script to see where to change links, folder names. 

## [Installation](https://github.com/LtGlahn/fanekart/blob/master/install.md). 