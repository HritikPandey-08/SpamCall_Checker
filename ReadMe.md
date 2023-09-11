# Spam Detector and Phone Number Lookup REST API

This is a REST API designed to be consumed by a mobile app that allows users to register, login, identify spam numbers and search for people by phone number or name. It's built using the Django framework with a relational database and ORM for data persistence.


### User
- A registered user of the app who can have zero or more personal contacts.
- Registered users must provide a name, phone number, and password during registration.
- Users can optionally add an email address to their profile.
- Each user can only register once with a particular phone number.

### Global Database
- The combination of all registered users and their personal contacts.
- User's phone contacts are automatically imported into the app's database (not implemented here).

### Spam
- Users can mark a phone number as spam.
- Spam information is shared in the global database.
- Spam status is associated with phone numbers, whether or not they belong to registered users or contacts.

### Search
- Users can search for people by name or phone number in the global database.
- Search results display name, phone number, and spam likelihood.
- Search results prioritize exact name matches, followed by partial name matches, and exact phone number matches.

## Data Model

The following data is stored for each user:
- Name
- Phone Number (unique)
- Email Address

## API Endpoints

1. **User Registration and Profile**
    - `POST /api/user/register/`: Register a new user with name, phone number, and password.
    - `POST /api/user/login/`: Login a exists user.
    
2. **Spam**
    - `POST api/spam/mark/`: Mark a phone number as spam.
    - `GET api/spam/`: Get the spam likelihood for a specific phone number.

3. **Search**
    - `GET api/spam/search/?query={search_query}/`: Search for people by name.
    - `GET api/spam/search/?query={phone_number}/`: Search for people by phone number.


## Security

- Authentication is implemented using JWT (JSON Web Tokens).
- User registration requires a strong password.
- Permissions are set to ensure users can only access their own data.
- Proper validation and sanitization of input data to prevent security vulnerabilities.

## Testing

Unit tests and integration tests should be written to ensure the correctness of the API. Tools like Django's testing framework can be used.

## Performance and Scalability

The API should be designed to handle a large number of users and contacts efficiently. Consideration for database indexing and optimization should be made.

## Directory Structure

- `requirements.txt`: Lists project dependencies.
- `README.md`: Project documentation.
- `LICENSE`: License information.

## Getting Started

1. Clone this repository.
2. Create a virtual environment and activate it.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Read ReadMe.txt
5. Make database migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Create a superuser account with `python manage.py createsuperuser`.
7. Run the development server with `python manage.py runserver`.

## Contributing

Contributions are welcome. Please follow the project's coding and testing guidelines and open a pull request with your changes.

## Dependencies

- Python (>=3.6)
- Django
- djangorestframework-simplejwt
- djangorestframework
- PostgreSQL 
- psycopg2
