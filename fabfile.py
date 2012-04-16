#!/usr/bin/env python
# encoding: utf-8

from os.path import exists
from fabric.api import task, lcd, env, local, run, cd, put
import tempfile as tf

env.user = 'sharat87'
env.hosts = ['sharat87.webfactional.com']

@task(default=True)
def up():

    tmp_loc = tf.mkdtemp(prefix='fab-')
    local('cp -R . ' + tmp_loc + '/app')

    with lcd(tmp_loc + '/app'):

        local('rm -rf kindlegen chrome fabfile.py*')
        local('tar -cjf ../pack.tar.bz2 *')

        with cd('~/webapps/kindlestack/htdocs'):
            run('rm -Rf ./*')

        put('../pack.tar.bz2', '~/webapps/kindlestack/htdocs')
        local('rm ../pack.tar.bz2')

    local('rm -Rf "' + tmp_loc + '"')

    with cd('~/webapps/kindlestack'):

        with cd('htdocs'):
            run('tar -xjf pack.tar.bz2')
            run('rm pack.tar.bz2')
            run('mv requirements.txt ..')
            run('mv env_prod.py env.py')

        run('pip install --install-option="--install-scripts=$PWD/bin" '
                '--install-option="--install-lib=$PWD/lib/python2.7" '
                '-r requirements.txt')

        run('rm requirements.txt')

@task
def pack_ext():
    """Pack browser extension(s)."""

    if exists('kindle-stack-chrome.zip'):
        local('rm kindle-stack-chrome.zip')

    with lcd('chrome'):
        local('zip -r ../kindle-stack-chrome.zip ./*')
