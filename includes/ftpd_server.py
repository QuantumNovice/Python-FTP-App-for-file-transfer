from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
import subprocess, sys, socket


__author__ = 'Syed Haseeb Shah aka n0vice'
__email__ =  'hasi468iowa@gmail.com'
__pyversion__ = 3.5
__tested__ = ['Ubuntu-Bionic-Beaver', 'Win 7', 'Win 8', 'Win 10']

def ipselect():
    '''
    Select broadcast IP
    '''
    data = str(subprocess.check_output('ipconfig'))
    gateway = '192.168.10.'
    for i in range(2,255):
        if gateway+str(i) in data:
            return gateway+str(i)
    return '127.0.0.1'
        
def ftpserve(user, passwd, path, port=21, perm='elradfmwMT', ip=socket.gethostbyname(socket.gethostname())):
    print('Serving', path)
    authorizer = DummyAuthorizer()
    authorizer.add_user(user, passwd, path, perm=perm)
    authorizer.add_anonymous(path, perm=perm)
    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer((ip, port), handler)
    server.serve_forever()
'''
# Full r/w permissions
>>> authorizer.add_user('user', 'pwd', '/home/user', perm='elradfmw')

# Read only permissions (the same as anonymous user)
>>> authorizer.add_user('user', 'pwd', '/home/user', perm='elr')

# Full r/w permissions except user can't change directory (no CWD)
>>> authorizer.add_user('user', 'pwd', '/home/user', perm='lradfmw')

# Full read permissions. User is allowed to create new files (STOR/STOU
allowed)
>>> authorizer.add_user('user', 'pwd', '/home/user', perm='lraw')

'''

#ftpserve('ftp','ftp', 'E:/', ip=ipselect())
ftpserve('ftp','ftp',sys.argv[1], port=sys.argv[2], ip=sys.argv[3])#, perm='elraw')


