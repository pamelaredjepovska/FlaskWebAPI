from src import create_app

app = create_app()

if __name__ == "__main__":
    host = app.config["TEST_HOST"]
    port = app.config["TEST_PORT"]
    app.run(host=host, port=port, debug=True)
