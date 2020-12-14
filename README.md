## Usage
### Running the API
Inside a virtual environment running Python 3:

Install dependencies
```
pip install --upgrade pip
pip install -r ./requirements.txt
```

*  Run migrations: `python manage.py migrate`
*  Create superuser and follow the instructions: `python manage.py createsuperuser`
*  Start server: `python manage.py runserver`
*  Go to `http://localhost:8000/admin/` and log in as your superuser
*  Navigate to  `http://localhost:8000/bonds/` and create and view bonds as that user
You can go back in admin and create more users and they will have their own bonds.

### Running the tests
- `python manage.py test`

## What I would do with more time
*  Spend a little bit more time on determining the best values for the model attributes' max lengths.
*  Not have a direct Bond <-> User relationship for various reasons
   * As a business object, a bond has nothing to do with 'users'. Therefore, the model should represent the financial security only – nothing more than that.
   * Use a many-to-many relationship so multiple users can have access to the same bond. This would use a junction table in the db, avoiding having a direct link to a user on the Bond object.
   * If we need to link it to other types of entities (e.g. company, exchange), should we keep adding such links via foreign keys? No because this could get messy quickly. So this initial design is seemingly not very futureproof.
*  Implement user registration and login via the API instead of relying on Django's default authentication.