from flask import Flask, make_response, request
from urllib.parse import urlparse
import base64
import requests
app = Flask(__name__)


@app.route('/vuln')
def follow_url():
    address = request.args.get('proxy')
    #are they asking for metadata service
    if "169.254.169.254" in address:
        print(address)
        #Mock Metadata doesn't support userdata so this is a hack.
        if "169.254.169.254/latest" in address:
            if "169.254.169.254/latest/user-data" in address:
                resp = make_response(base64.b64encode(b"flag"))
                resp.mimetype = "text/plain"
                return(resp, 200)

            resp = make_response("dynamic\nmeta-data\nuser-data")
            resp.mimetype = "text/plain"
            return(resp, 200)
        #This is what happens when someone doesn't choose user-data
        q = urlparse(address).path
        resp = make_response(requests.get("http://127.0.0.1:1338/"+q).text)
        resp.mimetype = "text/plain"
        return(resp, 200)
    return(make_response("not quite"), 403)

@app.route('/')
def home():
    resp = '''<h1>EC2 Proxy Helper</h1>
                <br>
                usage:
                    <br><code>http://127.0.0.1:80/vuln?url=http://example.com</code><br>
                
    '''
    return(resp,200)

if __name__ == '__main__': 
    app.debug = True 
    app.run(host='0.0.0.0',port=8000)
