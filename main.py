from app import app

host = 'localhost'
port = 5000

if __name__ == '__main__':
    app.run(host=f'{host}:{port}')
