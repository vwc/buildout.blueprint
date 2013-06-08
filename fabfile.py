from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import sudo

from ade25.fabfiles import server


def webserver():
    env.use_ssh_config = True
    env.forward_agent = True
    env.port = '22222'
    env.user = 'root'
    env.hosts = ['6zu0']
    env.webserver = '/opt/webserver/buildout.webserver'
    env.code_root = '/opt/sites/plonesite/buildout.plonesite'
    env.sitename = 'plonesite'
    env.code_user = 'root'
    env.prod_user = 'www'


def ls():
    """ Low level configuration test """
    with cd(env.code_root):
        run('ls')


def uptime():
    """ Server uptime """
    run('uptime')


def load():
    """ Server average system load """
    run('cat /proc/loadavg')


def memory():
    """ Server memory usage """
    run('free')


def disk():
    """ Server disk and filesystem usage """
    run('df -ha')


def supervisor():
    """ Webserver process status """
    with cd(env.webserver):
        run('bin/supervisorctl status')


def status():
    """ General system status information """
    # General health of the server.
    uptime()
    load()
    memory()
    disk()
    supervisor()


def update():
    """ Update buildout from git/master """
    with cd(env.code_root):
        run('nice git pull')


def build():
    """ Run buildout deployment profile """
    with cd(env.code_root):
        run('bin/buildout -Nc deployment.cfg')


def build_full():
    """ Run buildout deployment profile and enforce updates """
    with cd(env.code_root):
        run('bin/buildout -c deployment.cfg')


def restart():
    """ Restart instance """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart instance-%(sitename)s' % env)


def supervisorctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('bin/supervisorctl ' + ' '.join(cmd))


def deploy():
    """ Deploy current master to production server """
    update()
    restart()


def deploy_full():
    """ Deploy current master to production and run buildout """
    update()
    build()
    restart()


def rebuild():
    """ Deploy current master and run full buildout """
    update()
    build_full()
    restart()
