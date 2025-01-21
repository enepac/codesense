# CodeSense: AI Codebase Navigation and Management

CodeSense is an AI-powered application designed to streamline codebase navigation and management. It allows developers to add, edit, delete, and explore repositories efficiently through a user-friendly interface. Below is the documentation of the successful steps performed to implement and refine CodeSense.

---

## Project Setup

### Backend Setup
1. **Initialize the Backend**:
   - Set up a FastAPI-based backend with PostgreSQL as the database.
   - Create an `init_db.py` script to define and initialize the database models.
   - Implement endpoints for managing repositories (GET, POST, PUT, DELETE).

2. **Key Backend Features**:
   - **Add Repository:** Ensures that duplicate repositories cannot be added.
   - **Edit Repository:** Allows updating repository details.
   - **Delete Repository:** Removes a repository and returns a success message.
   - **Pagination:** Supports fetching repositories with pagination (skip/limit parameters).

3. **Run the Backend**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Test Endpoints:** Use `curl` commands or tools like Postman to validate the backend functionality.

### Frontend Setup
1. **Initialize Frontend**:
   - Use React, Vite, and TypeScript to build the frontend.
   - Install required dependencies including TailwindCSS for styling.

2. **Setup Directory Structure**:
   - Create separate components for adding repositories (`AddRepositoryForm`) and displaying the list of repositories (`App.tsx`).

3. **Install Dependencies**:
   ```bash
   npm install axios react-toastify @tailwindcss/forms
   ```

4. **Run the Frontend**:
   ```bash
   npm run dev
   ```

---

## Key Features Implemented

### 1. Adding a Repository
- Users can add a new repository through the form.
- Real-time updates ensure the repository appears immediately after submission.
- Backend validation prevents duplicate repository names.

### 2. Editing a Repository
- Added an **Edit Button** to update repository details.
- Changes are immediately reflected on the frontend without requiring a page reload.

### 3. Deleting a Repository
- Added a **Delete Button** to remove a repository.
- The repository is deleted both on the backend and frontend without refreshing the page.

### 4. Pagination
- Supports pagination to navigate through large lists of repositories.
- Users can view repositories page by page.

---

## File Structure

```
.
├── backend
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy database models
│   ├── init_db.py        # Database initialization script
│   ├── config.py         # Database configuration
│   └── ...
├── frontend
│   ├── src
│   │   ├── App.tsx       # Main React component
│   │   ├── AddRepositoryForm.tsx  # Component for adding repositories
│   │   ├── index.css     # TailwindCSS configuration
│   │   └── ...
│   └── ...
└── README.md
```

---

## API Endpoints

### GET /repositories/
Fetch a paginated list of repositories.
- **Parameters**: `skip`, `limit`
- **Response**:
  ```json
  {
    "repositories": [
      {"id": 1, "name": "Repo1", "description": "Test", "url": "https://example.com"}
    ],
    "total": 10
  }
  ```

### POST /repositories/
Add a new repository.
- **Request Body**:
  ```json
  {"name": "Repo1", "description": "Test", "url": "https://example.com"}
  ```
- **Response**:
  ```json
  {"id": 1, "name": "Repo1", "description": "Test", "url": "https://example.com"}
  ```

### PUT /repositories/{id}/
Update repository details.
- **Request Body**:
  ```json
  {"name": "Updated Name", "description": "Updated", "url": "https://example.com"}
  ```

### DELETE /repositories/{id}/
Delete a repository by ID.
- **Response**:
  ```json
  {"message": "Repository deleted successfully"}
  ```

---

## Frontend Features

### AddRepositoryForm.tsx
- Handles the form for adding repositories.
- Validates inputs and prevents duplicate repository additions.

### App.tsx
- Displays the repository list with options to add, edit, and delete.
- Implements pagination for seamless navigation.

---

## How to Run the Application

1. **Start the Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open the frontend at: [http://localhost:3466](http://localhost:3466)

---

## Lessons Learned
- Maintaining proper state synchronization between the frontend and backend is crucial.
- Backend validation ensures data integrity and prevents duplicates.
- Pagination is essential for managing large datasets efficiently.
- Toast notifications improve user feedback for actions like add, edit, and delete.

---

## Future Improvements
- Implement search functionality to filter repositories.
- Add user authentication and authorization.
- Enhance the UI/UX for better usability.
- Integrate CI/CD pipelines for deployment.
