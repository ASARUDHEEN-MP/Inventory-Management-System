# Project Name: Inventory Management API

This project is designed to provide an API for managing inventory items. It allows users to perform operations such as creating, retrieving, updating, and deleting items while ensuring security and proper authentication using JWT (JSON Web Token). PostgreSQL is used as the database, and the API includes logging, testing, and authentication mechanisms.

## Features

### 1. **User Authentication**
- Users must register and login to access the API.
- Authentication is handled via JWT, with token refreshing to maintain sessions.

### 2. **Inventory Management**
- Create, update, retrieve, and delete inventory items through API endpoints.
  
### 3. **Secure API**
- All item-related operations are secured using token-based authentication to ensure only authenticated users can manage inventory items.

### 4. **PostgreSQL Database & Redis Caching**
- The project uses PostgreSQL as the primary database for storing and managing inventory items.
- Redis is used for caching frequently accessed items, reducing the load on the database and significantly improving data retrieval performance.

### 5. **Logging**
- **API Requests**: All API requests are logged to track usage.
- **Retrieval Speed**: The retrieval speed (response time) is logged before and after fetching from the cache. This helps in performance monitoring and optimization.
- **Error Logging**: Any errors encountered during request handling, such as missing items or internal server errors, are logged with detailed error messages.

These logs are stored in a file (e.g., `items.log`) to provide insights for debugging, performance tuning, and security monitoring.

### 6. **Testing**
- The project includes automated tests to ensure the reliability of API functionality.

## 1. Installation

### Clone the Repository and Set Up the Environment
Follow these steps to clone the repository and set up the virtual environment:

1. Clone the repository:
    ```bash
    git clone https://github.com/ASARUDHEEN-MP/Inventory-Management-System.git
    ```

2. Navigate into the project directory:
    ```bash
    cd Inventory-Management-System
    ```

3. Create a virtual environment:
    ```bash
    python3 -m venv env
    ```

4. Activate the virtual environment:
    - For macOS/Linux:
        ```bash
        source env/bin/activate
        ```
    - For Windows:
        ```bash
        env\Scripts\activate
        ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Create a .env File
Create a `.env` file in the project directory to store your database configuration. Use the following template:

```plaintext
# Database settings
DB_NAME='your_database_name'
DB_USER='postgres'
DB_PASSWORD='your_password'
DB_HOST='localhost'
DB_PORT=5432
```
7.Run Migrations
```bash
    python3 manage.py migrate

```
8.Start the Server
```bash
    python3 manage.py runserver
```
You can now access the API at http://127.0.0.1:8000/

9.Testing
```bash
    python3 manage.py test items 
```

## API Endpoints

### 1. User Registration
- **URL**: `http://127.0.0.1:8000/api/user/registration`
- **Method**: `POST`
- **Request Body**: 
    ```json
    {
        "username": "your_username",
        "password": "your_password",
       
    }
    ```
- **Response**: 
    - On successful registration:
        ```json
        {
            "message": "User registration is successful..."
        }
        ```
    - On error (e.g., validation errors):
        ```json
        {
            "errors": {
                "username": ["This field is required."],
                "password": ["This field is required."]
            }
        }
        ```
### 2. User Login
- **URL**: `http://127.0.0.1:8000/api/user/login`
- **Method**: `POST`
- **Request Body**: 
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
- **Response**: 
    - On successful login:
        ```json
        {
            "refresh": "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXB",
            "access": "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXB"
        }
        ```
    - On error (e.g., validation errors if password or username is null):
        ```json
        {
            "errors": {
                "username": ["This field is required."],
                "password": ["This field is required."]
            }
        }
        ```
        Or for invalid credentials:
        ```json
        {
            "errors": {
                "non_field_errors": [
                    "Invalid password."
                ]
            }
        }
        ```
        Or:
        ```json
        {
            "errors": {
                "non_field_errors": [
                    "Invalid username."
                ]
            }
        }
        ```

###  Authentication
- All endpoints require authentication. Use a valid JWT token in the Authorization header:
- - **URL**: `authorization: Bearer <your_token>`
 
 ### 3. Create Item
 Endpoint: /items/ 
 - **URL**: `http://127.0.0.1:8000/api/items`
 - Method: POST
- **Request Body**: 
    ```json
    {
        "name": "Item Name",
        "description": "Item Description"
    }
    ```
    - **Response**: 
    - On successful login:
        ```json
       {
        "name": "Item Name",
        "description": "Item Description"
       }
        ```
        - On error :
        ```json
        {
            "errors" : {
		        "name": ["This field is required."],
		        "price": ["This field is required."]
		    }
        }
        ```
### 4. Retrieve Item
 Endpoint: /items/{id}/
 - **URL**: `http://127.0.0.1:8000/api/items/{id}/`
 - Method: GET
    - **Response**: 
    - On successful login:
        ```json
       {
        "name": "Item Name",
        "description": "Item Description"
       }
        ```
         - On error :
        ```json
        {
            "errors" : {
		        "Item not found."
		    }
        }
        ```
        
        
    
 ### 5. Update Item
 Endpoint: /items/{id}/
 - **URL**: `http://127.0.0.1:8000/api/items/{id}/`
 - Method: PUT
    - **Response**:
    - - **Request Body**: 
    ```json
    {
        "name": "i am changing the name",
        "description": "Item Description"
    }
    ```
    - On successful login:
        ```json
       {
        "name": "i am changing the name",
        "description": "Item Description"
       }
        ```
         - On error :
        ```json
        {
            "errors" : {
		        "Item not found."
		    }
        }
        ```

### 6. Delete Item
 Endpoint: /items/{id}/
 - **URL**: `http://127.0.0.1:8000/api/items/{id}/`
 - Method: DELETE
    - **Response**: 
    - On successful login:
        ```json
       {
        "message": "Item deleted successfully.",
       }
        ```
         - On error :
        ```json
        {
            "errors" : {
		        "Item not found."
		    }
        }
        ```
   ### **Logging**
   The API includes detailed logging to track various events for debugging, performance monitoring, and security purposes. The logs are stored in the file `items.log` and include the following information:
   
- **Retrieval Speed**: When fetching data, the retrieval time is logged, showing whether the data was fetched from the database or the cache. This helps in tracking and optimizing performance.
  
   **Example log entries**:
   

```plaintext
INFO 2024-09-25 07:16:46,611 views POST request to /items/ from 127.0.0.1
INFO 2024-09-25 07:20:05,826 views Request to /api/items/8/ took 0.0051 seconds from DB.
INFO 2024-09-25 07:20:15,816 views GET request to /items/8 from 127.0.0.1
INFO 2024-09-25 07:20:15,817 views Request to /api/items/8/ took 0.0003 seconds because of cache.
INFO 2024-09-25 07:20:32,570 views UPDATE request to /items/ from 127.0.0.1
INFO 2024-09-25 07:20:38,987 views GET request to /items/8 from 127.0.0.1
INFO 2024-09-25 07:21:26,727 views GET request to /items/8 from 127.0.0.1
ERROR 2024-09-25 07:21:26,729 views Item with ID 8 not found.

```
 ### **testing**
 ```bash
python3 manage.py test items 
```
 **Example test entries**:
```plaintext
  python3 manage.py test items  
Found 8 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
INFO 2024-09-25 07:36:30,302 views POST request to /items/ from 127.0.0.1
..INFO 2024-09-25 07:36:31,003 views DELETE request to /items/ from 127.0.0.1
..INFO 2024-09-25 07:36:31,706 views GET request to /items/6 from 127.0.0.1
INFO 2024-09-25 07:36:31,709 views Request to /api/items/6/ took 0.0034 seconds from DB.
..INFO 2024-09-25 07:36:32,564 views UPDATE request to /items/ from 127.0.0.1
..
----------------------------------------------------------------------
Ran 8 tests in 2.978s

OK
Destroying test database for alias 'default'...

```
### **cache redis**
The redis cache is  includes for Retrieve Item to increase the speeed of the data you can check the redis cache i index 1
open terminal exit from server
 ```bash
redis-cs

```
inside that enter to the index 
 ```bash
select 1
keys *
127.0.0.1:6379[1]> keys *
1) ":1:item_6"
127.0.0.1:6379[1]> 

```
```plaintext
1) ":1:item_6"
127.0.0.1:6379[1]>
if there is not cache
127.0.0.1:6379[1]> keys *
(empty array)
127.0.0.1:6379[1]> 
```








		









