# Importing the create_app function from the app package
from app import create_app

# Creating the Flask app instance
app = create_app()

# Running the app on a non-standard port
if __name__ == "__main__":
    app.run(port=5001, debug=True)
