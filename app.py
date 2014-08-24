#!/usr/bin/env python

import hashlib
import hmac
import os
import subprocess
from flask import Flask, request, abort
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('application.cfg')


class ChecksumCalcStream(object):

    def __init__(self, stream, key):
        self._stream = stream
        self._hash = hmac.new(key, digestmod=hashlib.sha1)

    def read(self, bytes):
        rv = self._stream.read(bytes)
        self._hash.update(rv)
        return rv

    def readline(self, size_hint):
        rv = self._stream.readline(size_hint)
        self._hash.update(rv)
        return rv


def generate_checksum(request, key=None):
    env = request.environ
    stream = ChecksumCalcStream(env['wsgi.input'], key=key)
    env['wsgi.input'] = stream
    return stream._hash


def run_command():
    path = '/usr/lib/myawesomeapp'
    python_path =  '/'.join([path, 'bin/python'])
    ext_path = '/'.join([path, 'src/myawesomeapp'])
    git_pull = 'git pull origin master'
    install = '{0} setup.py develop'.format(python_path)
    restart = 'sudo service apache2 reload'

    os.chdir(ext_path)
    subprocess.call(git_pull.split(' '))
    subprocess.call(install.split(' '))
    subprocess.call(restart.split(' '))


@app.route("/", methods=['POST'])
def deploy():
    hash = generate_checksum(request, key=app.config['GITHUB_SECRET'])
    # Accessing json just to parse the stream
    request.json
    headers = request.headers
    if 'sha1={0}'.format(hash.hexdigest()) == headers.get('X-Hub-Signature'):
        run_command()
        return 'OK'
    abort(404)


if __name__ == "__main__":
    app.run(debug=True)
