# Doggie dog clinic API
### Description
This microservice provides an API for managing dog data in "Doggie Dog Clinic". It allows you to retrieve, create, and update information about dogs. 

### Link
https://doggie-dog-clinic.onrender.com/

## Running FastAPI using Dockerfile
You can run FastAPI separately using the Dockerfile. To do this, execute the following command:

\`\`\`bash
docker build -t my-fastapi-app -f Dockerfile .
docker run -p 5555:5555 my-fastapi-app
\`\`\`

## Running using Docker Compose
You can also run the application using Docker Compose. This will allow you to run both FastAPI and the bot simultaneously. To do this, execute the following command:

\`\`\`bash
docker-compose up
\`\`\`
or
\`\`\`bash
docker-compose run -e BOT_TOKEN=your_bot_token bot
\`\`\`

### Endpoints
GET /: Returns a welcome message.

GET /dog: Returns a list of dogs. You can specify a kind parameter to filter dogs by type.

POST /dog: Creates a new dog. Requires a request body with dog information.

GET /dog/{pk}: Returns a dog with the given primary key.

PATCH /dog/{pk}: Updates a dog with the given primary key. Requires a request body with the new dog information.

### Models

Dog: A dog model that includes a name (name), primary key (pk), and type (kind).

DogType: An enumeration of available dog types (terrier, bulldog, dalmatian).

### Bot Description
The bot is designed to interact with the “Doggie Dog Clinic” API. It provides an interactive way to manage dog data. The bot uses inline keyboard buttons for user interaction. Here are the functionalities provided by the bot:

Get Welcome Message: the bot sends a welcome message to the user.
Get Records: the bot fetches records from the API.
Get List of Dogs: the bot fetches a list of dogs from the API.
Add New Dog: the bot prompts the user to enter the dog’s details (name, pk, and kind). The bot then sends a POST request to the API to create a new dog.
Get Dog Information by ID: the bot fetches information about a specific dog from the API using the dog’s ID.
Update Dog Information: the bot prompts the user to enter the updated dog’s details. The bot then sends a PATCH request to the API to update the dog’s information.

The bot also checks if the server is available before performing any actions. If the server is not available, the bot informs the user and suggests trying again later.
Please note that the bot currently only works with three kinds of dogs: terrier, bulldog, or dalmatian.

### Usage


### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Author
Albina Burlova
