# API Data Fetcher and Downloader

This repository contains a technical test that uses the Django Rest framework to develop a service that consumes a public API and provides specific functionalities. In this project, we have used the public API of Rick and Morty as a data source. The main features developed include:

1. **Endpoint for Consuming a Public API:**
   - We have implemented an endpoint that consumes any provided public API. In this case, we have used the Rick and Morty API as the data source.

2. **Filters for the Endpoint:**
   - The endpoint includes up to 3 filtering options, allowing users to refine the results from the consumed API. Filters may include, for example, a character's name, species, and status.

3. **Option to Download Data in a ZIP File:**
   - We offer users the ability to download the information in a ZIP file that contains the data in JSON format. This allows users to store the data locally and use it as needed.

This project is designed in a modular and extensible way, allowing developers to add new features and consume different public APIs in the future. Good practices in Django Rest Framework development have been followed, and clear documentation for its use is provided.

## Usage Instructions

1. Clone this repository to your local machine.
2. Set up a Python virtual environment (using `virtualenv` is recommended).
3. Install project dependencies using `pip install -r requirements.txt`.
4. Run database migrations with `python manage.py migrate`.
5. Start the development server with `python manage.py runserver`.
6. Access the API via the URL provided by the development server.

### Filtering Data
To filter the data from the API or the database, you can use the following query parameters in the URL:

- `species`: Filter characters by species.
- `status`: Filter characters by status.

Example: To filter characters by species (e.g., "Human") and status (e.g., "Alive"), use the following URL:

http://localhost:8000/characters/?species=Human&status=Alive


### Downloading Data
To download the data in a ZIP file, add the `download` parameter to the URL:

- `download=true`: Download data in a ZIP file.

Example: To download the filtered data as a ZIP file, use the following URL:

http://localhost:8000/characters/?species=Human&status=Alive&download=true


If not all points were completed, the technical test is in the state where it was stopped, and additional features can be added as needed.

Thank you for reviewing this technical test! If you have any questions or suggestions, please feel free to get in touch.
