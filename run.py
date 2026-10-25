from app import create_app

from prometheus_client import start_http_server

app = create_app()

if __name__ == '__main__':

    app.run(host='0.0.0.0',port=5000)
