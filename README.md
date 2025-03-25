# Movies-Collection
This project collects data about the top 100 movies and displays them on a web-based interface. It allows users to browse movies, rate them, and manage their favorites.

### Features
+ View a curated list of the top 100 movies.
+ Register and log in to manage personal favorites.
+ Rate movies and see overall ratings.
  
**Project Structure**
```Text
Movies-Collection-main/
├── Interface.py              # Main entry point for the interface
├── Source.py                 # Core logic for handling movies data
├── Movies_Database/          # Contains the movies database
├── User_Data/                # User-specific data storage
├── instance/                 # Instance folder for SQLite
├── static/
│   └── css/                 # Stylesheets and images
├── templates/               # HTML templates for rendering pages
├── .env                     # Environment variables (e.g., secrets, API keys)
├── LICENSE                  # Project license
├── README.md                # Project documentationSetup InstructionsInstall Python (version 3.12 or compatible).
```
## Setup Instructions
1. Install Python (version 3.12 or compatible).
2. Install required dependencies:
> pip install -r requirements.txt
>
3. Set up the environment variables in the .env file.
4. Run the project:
> python Interface.py
>
**Usage**
+ Access the web interface at http://localhost:5000.
+ Register for an account or log in.
+ Browse top movies, rate them, and add favorites.
  
**Database**
+ Movies_Database/Movies.db: Contains data about the top 100 movies.
+ User_Data/Default.db: Stores user-specific data.

**License** 
+ This project is licensed under the terms of the LICENSE file included in this repository.


