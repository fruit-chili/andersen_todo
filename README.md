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
Detailed information about request parameters and data schemas you can find at [Swagger-ui](http://localhost/openapi) or [Postman collection](http://localhost/static/openapi/andersen_todo.postman_collection.json).
- `registration/` 
    - [POST] - New user registration.
-  `login/` 
    - [POST] - Checks the credentials and returns the JWT if the credentials are valid.
- `tasks/` 
    - [GET] - Returns all tasks list (pagination and filtration by status are available).
    - [POST] - Creates a new task.
- `tasks/own/` 
    - [GET] - Returns tasks list of auth user (pagination and filtration by status are available).
- `tasks/users/{user_id}/`
    - [GET] - Returns tasks list of user with id=user_id (pagination and filtration by status are available).
- `tasks/{task_id}/` 
    - [GET] - Returns task details.
    - [PATCH] - Updates task information (can be perform only by owner).
    - [DELETE] - Removes task (can be perform only by owner).
- `tasks/{task_id}/mark-completed` 
    - [PATCH] - Marks task with id=task_id as "Completed".
