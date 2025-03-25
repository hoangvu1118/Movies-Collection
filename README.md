# Movies-Collection
Movies Collection ProjectThis project collects data about the top 100 movies and displays them on a web-based interface. It allows users to browse movies, rate them, and manage their favorites.
FeaturesView a curated list of the top 100 movies.
Register and log in to manage personal favorites.
Rate movies and see overall ratings.
Project StructureMovies-Collection-main/
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
Install required dependencies:
pip install -r requirements.txtSet up the environment variables in the .env file.
Run the project:
python Interface.pyUsageAccess the web interface at http://localhost:5000.
Register for an account or log in.
Browse top movies, rate them, and add favorites.
DatabaseMovies_Database/Movies.db: Contains data about the top 100 movies.
User_Data/Default.db: Stores user-specific data.
LicenseThis project is licensed under the terms of the LICENSE file included in this repository.
Feel free to add or modify sections to tailor the README to your needs!
