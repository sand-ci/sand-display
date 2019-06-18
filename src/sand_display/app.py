"""
Application File
"""
import flask
import flask.logging
from flask import Flask, Response, make_response, request, render_template
import logging
import os
import re
import sys
import traceback
import urllib.parse

import sand_display.datamodel as datamodel
import sand_display.default_config as default_config

app = Flask(__name__)
app.config.from_object(default_config)
app.config.from_pyfile("config.py", silent=True)
if "SAND_DISPLY_CONFIG" in os.environ:
    app.config.from_envvar("SAND_DISPLAY_CONFIG", silent=False)

if "LOGLEVEL" in app.config:
    app.logger.setLevel(app.config["LOGLEVEL"])


@app.route('/map/iframe')
def map():
    sources = datamodel.CachedData(app.config).GetSources()

    return render_template('iframe.html.j2', sources=sources.values())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, use_reloader=True)
else:
    root = logging.getLogger()
    root.addHandler(flask.logging.default_handler)
