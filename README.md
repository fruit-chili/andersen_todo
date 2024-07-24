# ToDo list (Andersen tech task)

## Common information  
Simple RESTful application for managing a task list (ToDo list) based on Django (DRF) and PostreSQL. Made as Python technical task for Andersen.

## Installation
1. Clone repository to your local machine.  
2. Run the following command in the shell prompt from the repository’s root directory:  
`docker compose up`  
3. When the containers start up, open one more shell and run commands (from the repository’s root directory):  
`docker compose exec web python manage.py migrate`  
`docker compose exec web python manage.py collectstatic` (type 'yes' after if required)   

## Testing
There are three options for API testing available:
1. [Swagger-ui](http://localhost/openapi)  
2. [Postman collection](http://localhost/static/openapi/andersen_todo.postman_collection.json)  
3. `pytest andersen_todo/tasks/tests.py` (requires python with pytest, requests)  

## Endpoints
- `registration/` textext
    - [POST] - textext
-  `login/` textext
    - [POST] - textext
- `tasks/` textext
    - [GET] - textext
    - [POST] - textext