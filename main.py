#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import env
import secrets
import requests
import json
from jinja2 import Template
from os.path import basename, join, abspath
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import tempfile
import subprocess as sp
from shutil import rmtree
from flask import Flask, jsonify, request
import codecs
import logging

logging.basicConfig(level=env.LOG_LEVEL, filename=env.LOG_FILE,
        format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y%m%d-%H:%M%p')
log = logging.getLogger('kindlestack')

with open('template.html') as f:
    template = Template(f.read())

def get_data(site, question_id):

    params = {'site': site, 'filter': '!*KelRYy2aYCTvWZj'}

    if hasattr(secrets, 'STACKEXCHANGE_API_KEY'):
        params['key'] = secrets.STACKEXCHANGE_API_KEY

    response = requests.get(
            'https://api.stackexchange.com/2.0/questions/' + question_id,
            params=params)
    response.raise_for_status()

    return json.loads(response.text)

def send_mail(send_to, subject, text, files=[], server='localhost',
        username=None, password=None):

    send_from = 'kindlestack@sharats.me'

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(f, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                'attachment; filename="%s"' % basename(f))
        msg.attach(part)

    smtp = SMTP(server)
    if username is not None:
        smtp.login(str(username), str(password))

    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def answer_sort_key(ans):
    return ans['score'] + (10 if ans['is_accepted'] else 0)

def send_to_kindle(site, question_id, email):
    data = get_data(site, question_id)['items'][0]

    data['answers'].sort(key=answer_sort_key, reverse=True)

    tloc = tempfile.mkdtemp(prefix='tmp-kindle-stack-')

    with codecs.open(join(tloc, 'rendered.html'), 'w', 'utf-8') as f:
        f.write(template.render(data))

    sp.call([abspath(env.KINDLEGEN), 'rendered.html', '-o',
        'kindle-stacked.mobi'], cwd=tloc)

    send_mail([email], 'kindle-stack: ' + data['title'], '-none-',
            files=[join(tloc, 'kindle-stacked.mobi')],
            server=secrets.SMTP_HOST,
            username=secrets.SMTP_USER, password=secrets.SMTP_PASS)

    rmtree(tloc)

def make_webapp():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return ('Hello. Welcome to kindle-stack. An app by @sharat87.<hr>')

    @app.route('/send', methods=['POST'])
    def send():
        args = request.args if request.method == 'GET' else request.form
        site, question, email = args['site'], args['question'], args['email']
        log.info('send from ' + site + '/' + question + ' to ' + email)
        send_to_kindle(site, question, email)
        return jsonify(ok=True)

    return app

if __name__ == '__main__':
    app = make_webapp()
    app.debug = True
    app.run(host='localhost', port=5004)
