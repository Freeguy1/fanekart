
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, url_for, render_template, make_response, abort
import loggGps

# Directory where we write (and read!) our geojson-data
dataDir = '/home/<YOUR PATH>/mysite/static/gps/'


app = Flask(__name__)
app.secret_key = 'This is really unique and secret'

@app.route('/getfile/<filename>')
def getFile(filename):
    filename = dataDir + filename

    try:
        with open( filename) as file:
            blob = file.read()
    except:
        abort(404)
        pass

    r = make_response(blob)
    r.mimetype='application/json'
    r.headers['Access-Control-Allow-Origin'] = '*'

    return r


@app.route('/gps/mypos/<gpsId>/')
def getpos(gpsId=''):
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')

    ok = loggGps.loggGps( str(lat), str(lon), str(gpsId))

    return( ok + "<br>gps ID" + str(gpsId) + "<br>\n" +
            'lat' + str(lat) + "<br>\n" +
            "lon" + str(lon) )


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

