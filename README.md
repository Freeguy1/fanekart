# fanekart
Python + flask oppsett tilpasset pythonanywhere.com for live tracking av GPS. Vedlikeholder geoJSON-fil med posisjon, samt kartoppsett for visning. 

flask.py setter opp et REST api på <dinkonto>.pythonanywhere.com/gps/mypos/<gps ID>/
Din GPS-app bruker lon,lat nøkkelord for å tracke sine bevegelser. 
Eksempel:  <dinkonto>.pythonanywhere.com/gps/mypos/<gps ID>/?lat=50.4&lon


