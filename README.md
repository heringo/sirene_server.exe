# sirene_server.exe

## Description
`sirene_server.exe` is a Python project that retrieves SIREN data, processes it via Pappers and LinkedIn searches, and sends it to a Google Sheets spreadsheet.

## Project Structure

```
sirene_server/
├── config/
│   ├── .env
│   └── service_account.json
├── data/
│   └── final_results.csv
├── scripts/
│   ├── run.sh
│   └── setup.sh
├── src/
│   ├── fetch_siren.py
│   ├── linkedin_search.py
│   ├── main.py
│   ├── pappers_search.py
│   └── to_gsheet.py
├── tests/
│   └── test_main.py
├── .gitignore
└── README.md
```

## Prerequisites
- Python 3.x
- pip
- Google Chrome

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/sirene_server.exe.git
    cd sirene_server.exe
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure the environment variables:
    - Create a `.env` file in the [config](http://_vscodecontentref_/2) folder with the following content:
        ```properties
        SPREADSHEET_ID=your_google_spreadsheet_id_here
        EMAIL=your_email_here
        PASSWORD=your_password_here
        SIREN_API=your_siren_api_key_here
        ```
    - Place the `service_account.json` document in the `config` folder.

4. Run the setup script:
    ```sh
    bash scripts/setup.sh
    ```

## Usage
To run the main script:
```sh
python src/main.py
```

## Tests
To run the unit tests:
```sh
python -m unittest discover -s tests
```

## VPS Configuration
The `setup.sh` script installs all necessary dependencies on a Linux VPS. To run it:
```sh
bash scripts/setup.sh
```

## Task Scheduling
The `run.sh` script runs the main script every Monday at 1 AM to get new companies from the previous week. To schedule this task, add the following line to your crontab:
```sh
0 1 * * 1 /bin/bash /path/to/your/project/sirene_server/scripts/run.sh
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss the changes you want to make.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
