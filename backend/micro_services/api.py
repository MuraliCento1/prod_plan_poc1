from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.micro_services.endpoints.file_endpoints import api_endpoints

class App:
    def __init__(self):
        """
        Initialize the App class with a FastAPI instance and include routers.
        """
        self.app = FastAPI()
        self.include_routers()
        self.setup_cors()

    def include_routers(self):
        """
        Include all the endpoint routers in the FastAPI app instance.
        This method ensures that all defined routes are registered with the app.
        """
        self.app.include_router(api_endpoints.router)

    def setup_cors(self):
        """
        Set up CORS middleware for the FastAPI app.
        """
        origins = [
            "http://localhost:3000",  # Replace with your frontend URL
            "http://127.0.0.1:3000",  # Replace with your frontend URL
            # Add other allowed origins as needed
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def run(self, host="127.0.0.1", port=8000):
        """
        Run the FastAPI app using Uvicorn with the specified host and port.
        This method starts the ASGI server to serve the FastAPI app.

        :param host: The host address where the app will run.
        :param port: The port number on which the app will listen.
        """
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

# Instantiate the app_instance at the module level
app_instance = App()

if __name__ == "__main__":
    app_instance.run()


















