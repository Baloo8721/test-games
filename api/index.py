from flask import Flask, Response
app = Flask(__name__)

@app.route('/')
def chess():
    return Response('''
        <html>
        <body style="background:#000;color:#fff">
            <h1>Political Chess Online</h1>
            <div id="board" style="font-family:monospace;font-size:24px">
            ''' + 
            '\n'.join(['♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜<br/>'] + 
                     ['♟'*8 + '<br/>']*2 +
                     ['&nbsp;'*15 + '<br/>']*4 +
                     ['♙'*8 + '<br/>']*2 +
                     ['♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖']) + '''
            </div>
        </body>
        </html>
    ''', mimetype='text/html')

def main():
    app.run(host='0.0.0.0')