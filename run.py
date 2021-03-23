from app import create_app

app = create_app()  # Don't merge into `__main__`, `gunicorn` needs this to run

if __name__ == '__main__':
    app.run(debug=True)
