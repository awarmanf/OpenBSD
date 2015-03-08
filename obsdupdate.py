#!/usr/bin/env python3.4

"""
Manage OpenBSD userland, ports and kernel updates.

Usage:
  obsdupdate --fetch  (ports | src | xenocara) [(--cvs <cvsroot>)]
  obsdupdate --update (ports | src | xenocara) [(--cvs <cvsroot>)]
  obsdupdate --build  (kernel | userland | xenocara) [(--cvs <cvsroot>)]
  obsdupdate --help
  obsdupdate --version

Options:
  -h --help        Show this screen.
  -v --version     Show version.
  -f --fetch       Fetch sources from CVS.
  -u --update      Update source tree from CVS.
  -b --build       Rebuild and install a part of the system.
  -c --cvs         Define anonymous CVS root server.
"""


import os
import sys
import subprocess
import docopt


def cmd(cmd):
    subprocess.call(cmd, shell=True)


def fetch():

    """ Fetch corresponding sources from CVS. """

    print('Fetching OpenBSD '+repo+' tree from CVS...')
    cmd('cd /usr && cvs -qd '+cvsroot+' get -r'+release+' -P '+repo)


def update():

    """ Update corresponding sources from CVS. """

    print('Updating OpenBSD '+repo+' tree from CVS...')
    cmd('cd /usr/'+repo+' && cvs -d '+cvsroot+' -q up -r'+release + ' -Pd')


def build():

    """ Build and install corresponding part of the system. """

    print('Rebuilding '+repo+'...')
    if args['kernel']:
        cmd('cd /usr/src/sys/arch/'+arch+'/conf && config GENERIC.MP')
        cmd('cd /usr/src/sys/arch/'+arch+'/compile/GENERIC.MP '
            '&& make clean && make && make install')
    elif args['userland']:
        cmd('rm -rf /usr/obj/* && cd /usr/src && make obj')
        cmd('cd /usr/src/etc && env DESTDIR=/ make distrib-dirs')
        cmd('cd /usr/src && make build')
    elif args['xenocara']:
        cmd('rm -rf /usr/xobj/*')
        cmd('cd /usr/xenocara && make bootstrap && make obj && make build')


if __name__ == "__main__":
    args = docopt.docopt(__doc__, version='obsdupdate 0.2.0')

    # Configuration variables goes here.
    default_cvs_root = 'anoncvs@anoncvs.fr.openbsd.org:/cvs'
    cvsroot = args['--cvs'] if args['--cvs'] else default_cvs_root
    release = 'OPENBSD_' + os.uname()[2].replace('.', '_')
    repo = sys.argv[2]
    arch = os.uname()[4]

    # Process arguments
    if args['--fetch']:
        fetch()
    elif args['--update']:
        update()
    elif args['--build']:
        build()

    print('done')
