#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

from fabric.api import task, lcd, local
import os.path as p
from glob import glob

@task
def compile():

    if p.exists('ext'):
        local('rm -rf ext')
    local('mkdir -p ext')

    local('cp -Rt ext data lib doc test package.json README.md')

    with lcd('ext'):
        for src in glob('**/*.coffee'):
            local('coffee -c ' + src)
            # local('rm ' + src)

@task(default=True)
def run():
    compile()
    with lcd('addon-sdk-1.6.1'):
        local('. bin/activate; cfx -p profile --pkgdir=../ext run')

@task
def xpi():
    compile()
    with lcd('addon-sdk-1.6.1'):
        local('. bin/activate; cd ..; cfx --pkgdir=ext xpi')
