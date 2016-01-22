from application import app
from cmp_hbc import HbcCompare

if __name__ == '__main__':
    HbcCompare().start()
    app.run(threaded=True)
    app.config['IS_QUIT'] = True
    print 'server quit'
