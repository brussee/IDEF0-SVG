import subprocess as p

from flask import Flask, Response, abort

from plantuml_decoder import plantuml_decode
from parser import grammar, IdefVisitor

app = Flask(__name__)


@app.route('/svg/<base64_data>')
def render(base64_data):
    decoded = plantuml_decode(base64_data)
    tree = grammar.parse(decoded.lstrip())
    iv = IdefVisitor()
    parsed = iv.visit(tree)

    process = p.Popen('./bin/schematic', stdin=p.PIPE, stdout=p.PIPE)
    svg_data = process.communicate(parsed.encode('utf-8'))[0]

    return Response(svg_data, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
