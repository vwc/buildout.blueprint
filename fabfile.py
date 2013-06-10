import sys
from collections import OrderedDict

from ConfigParser import ConfigParser
from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import sudo
from fabric.api import task

from ade25.fabfiles import server
from ade25.fabfiles import project

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.hosts = ['6zu4']
env.webserver = '/opt/webserver/buildout.webserver'
env.code_root = '/opt/sites/plonesite/buildout.plonesite'
env.local_root = '/Users/cb/dev/vw-blueprint/buildout.blueprint'
env.sitename = 'plonesite'
env.code_user = 'root'
env.prod_user = 'www'


@task
def bo_conf():
    filename = '%s/packages.cfg' % env.local_root
    config_parser = ConfigParser(dict_type=OrderedDict)
    config_parser.read(filename)
    egglist = config_parser.get('eggs', 'addon')
    new_list = egglist + '\nmy.package'
    config_parser.set('eggs', 'addon', new_list)
    for x in config_parser.sections():
        for name, value in config_parser.items(x):
            print '  %s = %r' % (name, value)
    with open(filename, 'wb') as configfile:
        config_parser.write(configfile)
    print 'Egglist successfully updated'


def ls():
    """ Low level configuration test """
    with cd(env.code_root):
        run('ls')


def supervisorctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('bin/supervisorctl ' + ' '.join(cmd))


def deploy():
    """ Deploy current master to production server """
    project.site.update()
    project.site.estart()


def deploy_full():
    """ Deploy current master to production and run buildout """
    project.site.update()
    project.site.build()
    project.site.restart()


def rebuild():
    """ Deploy current master and run full buildout """
    project.site.update()
    project.site.build_full()
    project.site.restart()
