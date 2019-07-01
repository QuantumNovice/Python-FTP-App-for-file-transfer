from flask import *
from io import BytesIO
from fastio import file_paths
import ftplib, os, subprocess, shutil
import urllib3, logging

__author__ = 'Syed Haseeb Shah aka n0vice'
__email__ =  'hasi468iowa@gmail.com'
__pyversion__ = 3.5
__tested__ = ['Ubuntu-Bionic-Beaver', 'Win 7', 'Win 8', 'Win 10']
__licence__ = ''

logging.basicConfig(filename='debug.log',level=logging.DEBUG)


app = Flask(__name__)

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

def homedirs():
    ''' returns list of directories we're currently serving from config file '''
    with open('config.txt') as afile:
        data = afile.read()
        afile.close()
    return [i for i in data.split('\n')]

def list_FTP(ip,port):
    ''' Returns list of files/folders inside the FTP directory '''
    ftp = ftplib.FTP()
    ftp.connect(ip, port)
    ftp.login('ftp','ftp')
    files = ftp.nlst()
    paths = ['ftp://'+ip+':'+str(port)+'/'+i for i in files]
    return files, paths

def server_root_files():
    FILES = []
    for root in serve_paths:
        for file in file_paths(root):
            FILES.append(file)
    for i in range(len(serve_paths)):
        for j in range(len(FILES)):
            if serve_paths[i] in FILES[j]:
                FILES[j] = FILES[j].replace(serve_paths[i], 'ftp://'+ip+':'+str(ports[i]))
    return FILES


#ip = ipselect() 
serve_paths = homedirs() # Paths that'll be served by FTP
ports = [2121+i for i in range(len(serve_paths))]
FILES = server_root_files()
freespace = [round(shutil.disk_usage(i).free/(1024*1024*1024), 2) for i in serve_paths]

@app.route('/')
def index():
    return render_template('index.html', homedirs=serve_paths, ip=ip, ports=ports, freespace=freespace)

@app.route('/files_list')
def files_list():
    return render_template('files.html', FILES=FILES)

@app.route('/search',methods=['POST'])
def search():
    query = request.form['query'].lower()
    result = []

    if 'type=' in query:
        query=query.replace('type=', '')
        if query in ['video']:
            for file in FILES:
                if file.lower().split('.')[-1] in ['mp4', 'avi', 'flv', 'swf','mkv','mov','wmv']:
                    result.append(file)
        elif query in ['image']:
            for file in FILES:
                if file.lower().split('.')[-1] in ['jpg', 'png', 'gif','jpeg','exif','tiff','ico','bmp','']:
                    result.append(file)
        elif query in ['book']:
            for file in FILES:
                if file.lower().split('.')[-1] in ['pdf', 'doc', 'ppt']:
                    result.append(file)

            return render_template('categorical_search.html', result=result)
    else:
        for file in FILES:
            if query in file.lower():
                result.append(file)
    return render_template('search.html', result=result)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    logging.debug('Starting App.py')
    logging.debug('Serve Directories')
	# This function automatically selects appropriate ip. This is a
	# user specific solution for now
    #ip = ipselect()
    ip = '192.168.173.1'
    for i in range(len(ports)):
        print(serve_paths[i])
        logging.debug(serve_paths[i]+' is at port '+str(ports[i]))
        if ' ' in serve_paths[i]:
            serve_paths[i] = '\"' +serve_paths[i] +'\"'
        os.system('start includes/ftpd_server.py %s %s %s' %(serve_paths[i], ports[i], ip))
    
    logging.debug('IP:'+ip)
    app.run(host=ip, port=80,debug=False)
    






















