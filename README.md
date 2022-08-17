# CM3070-Final-Project

# How to run the application

1. Open the git bash terminal in the VS Code editor.

2. Navigate to the directory containing the source code.

3. Activate the virtual environment:

`source venv/Scripts/activate `

4. Install Python packages with pip and requirements.txt

`pip install -r requirements.txt`

4. Navigate to the project directory

`cd holistic_mental_health_platform`

5. Start the server

`python manage.py runserver 127.0.0.1:8080`

### Navigate to the landing page of the application by navigating to the following address:

http://127.0.0.1:8080

## REST API

### To access the API endpoints I have created, ensure that the server is running and then navigate to the following pages:

- Client or service provider by username

http://127.0.0.1:8080/api/user/kristy/

- List of all users

http://127.0.0.1:8080/api/users

- All blog articles

http://127.0.0.1:8080/api/blog-articles

- Blog articles by category

http://127.0.0.1:8080/api/blog-by-category/nutrition/

- Blog article by pk

http://127.0.0.1:8080/api/blog-article/13/

- All discussions

http://127.0.0.1:8080/api/all-discussions

- Discussions by category

http://127.0.0.1:8080/api/discussions-by-category/yoga/

- Discussion by ID

http://127.0.0.1:8080/api/discussion/5/

- Bookings by client username

http://127.0.0.1:8080/api/client-bookings

- All bookings by SP

http://127.0.0.1:8080/api/service-provider-bookings

- All group sessions

http://127.0.0.1:8080/api/group-sessions

- Group sessions by category

http://127.0.0.1:8080/api/group-sessions-by-category/meditation/

- Group sessions by SP

http://127.0.0.1:8080/api/service-provider-group-sessions

- Group sessions joined by client

http://127.0.0.1:8080/api/client-group-sessions

## Unit Tests

### How to run the unit tests:

1. Open the git bash terminal in the VS Code editor.

2. Navigate to the directory containing the source code.

3. Activate the virtual environment:

`source venv/Scripts/activate `

4. Install Python packages with pip and requirements.txt

`pip install -r requirements.txt`

4. Navigate to the project directory

`cd holistic_mental_health_platform`

5. Run the tests

a) Run ALL tests

`python manage.py test`

b) Only run tests in the 'apps' directory

`python manage.py test apps/tests/`

c) Run only the API tests in the 'rest_api' directory

`python manage.py test rest_api/tests/ `

## User credentials

### Admin user
**Username**: admin 

**Email**: admin@mail.com 

**Password**: admin0123456 

---

### Service Provider User
**Username**: jane_therapist 

Password: bettermentalhealth7824 

---

### Client User
**Username**: kristy 

**Password**: bettermentalhealth7824 

