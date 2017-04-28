# -*- coding: utf-8 -*-

from flask import Flask, request, url_for, render_template, make_response, abort
import flask
import random
import httpLoggHistory
import mydefinitions
import getThisLink
import loggGps
import requests
import vegreferanser

# Directory where we write (and read!) our geojson-data
dataDir = '/home/jansimple/mysite/static/gps/'

app = Flask(__name__)
app.secret_key = 'This is really unique and secret'


# Proxy som henter vegreferanse i koordinat fra NVDB api og visveginfo-tjenesten
@app.route('/sjekkvegreferanser')
def sjekkvegreferanse():
    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    ost = request.args.get('ost', '')
    nord = request.args.get('nord', '')

    if is_number( lat) and is_number( lon):
        vegref = vegreferanser.sjekkvegreferanser( lon, lat)

        return flask.jsonify(**vegref)

    elif is_number( nord) and is_number( ost):

        vegref = vegreferanser.sjekkvegreferanser( ost, nord, utm=True)

        return flask.jsonify(**vegref)

    else:
        r = make_response('Wrong input parameters' + str(lat) + str(lon), 400)
        return r


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


#@app.route('/checkurl/<testType>/')
#@app.route('/checkurl/<group>/<testType>/')
#def testurl(testType='example_org',group='eksempler'):


@app.route('/')
def hello_person():
    return """
        <p>Who do you want me to say "Hi" to?</p>
        <form method="POST" action="%s"><input name="person" /><input type="submit" value="Go!" /></form>
    """ % (url_for('greet'),)

@app.route('/greet', methods=['POST'])
def greet():
    greeting = random.choice(["Hiya", "Hallo", "Hola", "Ola", "Salut", "Privet", "Konnichiwa", "Ni hao"])
    return """
        <p>%s, %s!</p>
        <p><a href="%s">Back to start</a></p>
    """ % (greeting, request.form["person"], url_for('hello_person'))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hellotemplate', name=name)

@app.route('/wmserrors/')
@app.route('/wmserrors/<int:days>day/')
@app.route('/wmserrors/<int:days>days/')
@app.route('/wmserrors/<int:days>dag/')
@app.route('/wmserrors/<int:days>dager/')
def wmserrors(days=7):
    err = httpLoggHistory.httpErrors(days=days)
    mytitle = "%d errors the last %d days" % (err.numerrors, err.days)
    errsummary = err.summary()
    return render_template('connectionerrortemplate', mytitle=mytitle, mytable=errsummary )

@app.route('/test/')
@app.route('/checklogg/')
def test():
    s0 = '<a href="/wmserrors/7days">Feilsituasjoner siste 7 dager</a>'
    s1 = '<a href="/checklogg/getMap/1days">getMap_fartsgrenser siste 24 timer</a>'
    s2 = '<a href="/checklogg/getCap/1days">getCapabilities siste 24 timer</a>'
    s3 = '<a href="/checklogg/getMap_XMLGW/1days">getMap fra XML gateway siste 24 timer</a>'
    s4 = '<a href="/checklogg/getCap_XMLGW/1days">getCap fra XML gateway siste 24 timer</a>'
    s5 = '<a href="/checklogg/getMap_UTV/1days">getMap UTV siste 24 timer</a>'
    s6 = '<a href="/checklogg/getCap_UTV/1days">getCapabilities UTV siste 24 timer</a>'
    s7 = '<a href="/checklogg/getCap_TESTPROD/1days">getCapabilities TESTPROD siste 24 timer</a>'
    s8 = '<a href="/checklogg/getMap_TESTPROD/1days">getMap TESTPROD siste 24 timer</a>'
    ll = [s0,s1,s2,s3,s4,s5,s6,s7,s8]
    return render_template('loggtemplate', mytitle='Logg over http(s) kall', mylist=ll)

@app.route('/checklogg/<testType>/')
@app.route('/checklogg/<testType>/<int:days>day/')
@app.route('/checklogg/<testType>/<int:days>days/')
@app.route('/checklogg/<testType>/<int:days>dag/')
@app.route('/checklogg/<testType>/<int:days>dager/')
def checklogg(testType='getMap_fartsgrenser', days=1):
    logg = httpLoggHistory.httpLoggHistory(testType=testType, days=days)
    summary, logglist = logg.summary()
    return render_template('loggtemplate', mylist=summary, logglist=logglist)


@app.route('/checkurl/')
@app.route('/checkurl/<group>/')
def checkurl(group=""):
    candidates = mydefinitions.testcandidates(group=group)
    return render_template( 'urltable', candidates=candidates, mytitle='Lenker vi skal teste' )


@app.route('/checkurl/<testType>/')
@app.route('/checkurl/<group>/<testType>/')
def testurl(testType='example_org',group='eksempler'):
    candidate = mydefinitions.validCandidate( testType) # Returns false if no match

    if not candidate:
        return render_template( 'generic.html',
                        mytitle='Connection test: ' + testType + ' not found',
                        text =  [ 'Please go back and check again' ]
                        )
    else: # Send http(s) request for matching candidate

        # Skip SSL verification?
        if 'verify' in candidate and candidate['verify'].lower() == "false":
            verify = False
        else:
            verify = True

        # Can we add HEADER section here... ? I think so. Adding a new keyword

        # Password protected service?
        if 'auth' in candidate:
            resp  = getThisLink.getThisLink(
                                    mylink=candidate['link'],
                                    testType=candidate['name'],
                                    auth = (candidate['auth'][0],
                                            candidate['auth'][1]),
                                    verify=verify,
                                    headers={'Origin': 'jansimple.pythonanywhere.com'}
                                            )
        else:
            resp  = getThisLink.getThisLink(
                                    mylink=candidate['link'],
                                    testType=candidate['name'],
                                    verify=verify,
                                    headers={'Origin': 'jansimple.pythonanywhere.com'}
                                    )
        if resp['headertable']:
            return render_template( 'generic.html',
                    mytitle='Connection test: ' + testType,
                    text = [
                        candidate['comment'],
                        'Http status: ' + str(resp['status_code'] ),
                        'Time elapsed: ' + str(resp['time']),
                        'File save status: ' + resp['filesavestatus'],
                        'Lenke: ' + candidate['link'],
                        'Http response header: '
                        ],
                    table = resp['headertable'],
                    link = resp['link'], embed = resp['link']
                    )

        else:
            return render_template( 'generic.html',
                        mytitle='No success with test named: "' + candidate['name'] + '"',
                        text = ['No success with test named: "' + candidate['name'] + '"',
                                candidate['link'],
                                resp['comment'],
                                'Overview with possible tests:'
                                ],
                        link = 'http://jansimple.pythonanywhere.com/checkurl/'
                        )

            'comment'

def getRoadRef_latlon( lat, lon):

    url = 'http://visveginfo-static.opentns.org/RoadInfoService/GetRoadReferenceForLocation'
    payload = {'northing': lat, 'easting': lon, 'coordinateSystem' : 'WGS84',
                'TopologyLevel' : 'Overview'}

    r = requests.get(url, params=payload)

    if r.ok:
        return r.text
    else:
        return "<RoadReference><TextualRoadReference>No roads here! " + r.url + "</TextualRoadReference></RoadReference>"




    text =    """<RoadReference>
            <County></County>
            <Municipality></Municipality>
            <ReflinkOID></ReflinkOID>
            <RoadCategory>Klarte ikke hente vegreferanse</RoadCategory>
            <RoadNumber></RoadNumber>
            <RoadNumberSegment></RoadNumberSegment>
            <RoadStatus></RoadStatus>
            <TextualRoadReference>INVALID</TextualRoadReference>
            <Measure>INVALID</Measure>
            <RoadNetPosition>
            <SRID>25833</SRID>
            <X></X>
            <Y></Y>
            </RoadNetPosition>
            <RoadNumberSegmentDistance></RoadNumberSegmentDistance>
            <RoadnetHeading></RoadnetHeading>
            </RoadReference>
            """

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False