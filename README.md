# Doggie dog clinic API
### Description
This microservice provides an API for managing dog data in "Doggie Dog Clinic". It allows you to retrieve, create, and update information about dogs.

### Endpoints
GET /: Returns a welcome message.

GET /dog: Returns a list of dogs. You can specify a kind parameter to filter dogs by type.

POST /dog: Creates a new dog. Requires a request body with dog information.

GET /dog/{pk}: Returns a dog with the given primary key.

PATCH /dog/{pk}: Updates a dog with the given primary key. Requires a request body with the new dog information.


### Models
Dog: A dog model that includes a name (name), primary key (pk), and type (kind).


DogType: An enumeration of available dog types (terrier, bulldog, dalmatian).

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Author
Albina Burlova
