from flask import Flask
app = Flask(__name__)

@app.route('/')
def chess():
    return '''
    <html><body style="background:black;color:white">
    <h1>Political Chess (WORKING BASE)</h1>
    <div id="game" style="border:2px solid white;width:800px;height:800px">
    GAME LOADING...
    </div>
    </body></html>
    '''