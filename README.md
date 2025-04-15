# README.md

# Test Automation Project

This project is designed for automating tests for a web application. It follows a page object model structure to organize the code and improve maintainability.

## Project Structure

- **pages/**: Contains classes that represent different pages of the application.
  - `home_page.py`: Contains the `HomePage` class for interacting with the home page.
  - `careers_page.py`: Contains the `CareersPage` class for interacting with the careers page.
  - `jobs_entrance_page.py`: Contains the `JobsEntrancePage` class for interacting with the jobs entrance page.
  - `filter_jobs_page.py`: Contains the `FilterJobsPage` class for applying filters on job listings.
  - `elements/nav_bar.py`: Contains the `NavBar` class for interacting with navigation bar elements.

- **tests/**: Contains test cases for the application.
  - `base_test.py`: Contains the `BaseTest` class for setting up the test environment.
  - `test_insider.py`: Contains various test cases utilizing the `BaseTest` class.

- **utils/**: Contains utility functions used across the project.
  - `utils.py`: Contains common utility functions.

- **requirements.txt**: Lists the dependencies required for the project.

- **conftest.py**: Configures pytest fixtures and hooks.

## Getting Started

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the tests using `pytest`.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.