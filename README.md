# Global-Biodiversity-Information-App
This repository contains the code for the Global Biodiversity Information Dashboard, a Shiny application that provides an interactive platform for exploring global biodiversity data. The app allows users to visualize species occurrences on a map, search for species by vernacular or scientific name, and view detailed summaries of observations.

## Features:
* **Interactive Map:** Visualize species occurrences based on user-selected criteria.
* **Species Search:** Search for species by vernacular or scientific name with autocomplete functionality.
* **Detailed Species** Summary: View comprehensive information about species occurrences, including location, date, and individual counts.

## Tools Used:
**Python:** The backend logic of the app.
**Shiny for Python:** For the interactive web application framework.
**DuckDB:** Efficient data processing for large datasets.
**Folium:** For creating dynamic maps with species location markers.
**Custom CSS:** For implementing a custom mode theme.
**PIL (Pillow):** Python Imaging Library, used for handling image processing

# Installation
## Prerequisites
**Ensure you have the following installed:**
* Python 3.x
* pip (Python package installer)
## Steps
1. Clone the Repository:

git clone https://github.com/japhstronics/Global-Biodiversity-Information-App.git

2. Create a Virtual Environment(Windows):

* pip install pipenv
* pipenv shell

  
## Install Dependencies:
* pipenv install -r requirements.txt

## Run the Application:
* python app.py
## Usage
Once the application is running, open a web browser and navigate to http://localhost:8000. You can then interact with the dashboard, search for species, and visualize data on the map.

## Project Structure

shiny-biodiversity-dashboard/
│
├── app.py                   # Main application entry point
├── modules/
│   ├── sidebar_module.py    # Contains the UI logic for the sidebar
│   └── main_content_module.py # Contains the UI logic for the main content area
├── data/
│   └── import_data.py       # Script for importing and processing data
├── static/
│   ├── css/
│   │   └── dark-theme.css   # Custom CSS for custom mode theme
├── templates/
│   └── index.html           # HTML templates for the app (if any)
├── .gitignore               # Specifies files and directories to be ignored by Git
├── requirements.txt         # List of dependencies for the project
└── README.md                # This README file

## Contributing
Contributions are welcome! Please follow these steps:

## Fork the repository.
Create a new branch (git checkout -b feature-branch-name).
Make your changes.
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch-name).
Submit a pull request.
Please ensure your code adheres to the coding standards and includes tests for any new functionality.

## License
open source

## Contact
If you have any questions, feel free to reach out:

Email: japhetsibanda.js@gmail.com
GitHub: japhstronics
