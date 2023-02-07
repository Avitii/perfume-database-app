# Perfume Database
A simple Python program that allows you to add, remove and view information about perfumes using barcode scanning. Please note, that for now, project is mainly focused on Polish language.

## Requirements
- Python-3.11.1
- pip
- optionally Docker

#### Python Modules
- opencv-python
- pyzbar
- rich
- sqlite3 (already included in Python 3.11.1)
- os (already included in Python 3.11.1)
- time (already included in Python 3.11.1)

## Running app
### Docker (preferred method)
I assume, that you have basic docker acknowledge. Please DM me if you need help.
1. Open terminal
2. Change the active directory to match the apllication's localization.
3. Run `docker build -t perfume-db .` (dot on the end is important).
4. And finally type `docker run -it perfume-db` to run the app.

### Other
You can also run the application without Docker, but depending on your operating system, you may need to take additional steps (such as installing additional packages). To run the application you just need to install the Python modules listed in the Requirements -> Python Modules, and for run `main.py` file (e.g. `python main.py`)

## Features
- Scan barcode from an image file.
- Option to add the scanned barcode to the database.
- Option to remove the barcode from the database.
- Option to view information about the barcode from the database.
- Clear and concise menu for easy navigation.

## Usage
1. Select a file from the list of available files (read Notes below).
2. Decode the barcode from the selected image file.
3. Choose an option from the menu:
- Add the barcode to the database by entering the brand, name, type, fragrance group, head, heart, and base.
- Remove the barcode from the database.
- View information about the barcode.
- Choose a new image file to scan.

## Notes
The program uses a local SQLite database file `database.sqlite` to store information about perfumes. The `images` directory contains example image files for testing purposes, you can replace it with own files as well as you can replace db file.

## Authors
Eryk Klimek (eryk.klimek@icloud.com)
