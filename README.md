# Vacation Rental Testing Automation

## Overview

```

```

Automates the testing of vacation rental details pages for SEO and functionality.

## Project Structure

- `chromedriver/`: WebDriver binaries.
- `results/`: Directory for storing test results.
- `src/`: Source code.
  - `main.py`: Main script to run the tests.
  - `test_cases.py`: Test functions for various cases.
  - `utils.py`: Helper functions.

## Setting Up the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/tanvir-alam-sk/assign-7 vacation_rental_test
   cd vacation_rental_test

   ```
2. Place WebDriver in the `chromedriver/` directory.

3. Download All Packege
   **Create the Virtual Environment**

   ```bash
   python -m venv venv
   ```

   **[Activate the Virtual Environment Linux]()**

   ```bash
   source venv/bin/activate
   ```
   **[Activate the Virtual Environment Windows]()**

   ```bash
   venv\Scripts\activate
   ```

   **Install Dependencies**

   ```bash
   pip install -r requirements.txt

   ```

   **Create the Virtual Environment**

   ```bash
   python -m venv venv
   ```

   **Run the Script**

   ```bash
   python src/main.py
   ```

## Project Structure

```bash
vacation_rental_test/
├── chromedriver/              # WebDriver binaries
│   └── chromedriver
├── results/                   # Directory for storing results
│   └── results.xlsx
├── src/                       # Source code directory
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── test_cases.py
│   └── utils.py
├── venv/                      # Python virtual environment directory
├── requirements.txt           # Dependencies for the project
└── README.md                  # Documentation for the project
```

## Output

Results will be saved in the `results/` directory as `results/test_results.xlsx` (or `results/test_results.csv`).
