# JSONXML_editor

Purpose of this application is to provide easy folder data browser.

First functionality is dealing with JSON and XML files, afterwards it can be exteded to all file types.

main GUI is OS independent (Win/Linux) based on:

- Python3
- Tkinter

## Objects

### Main module

- Implements class MainWindow, that has all helper methods involved.

### DataObject module (implements two objects)


- class JsonObject that holds all contents
- function random_json to get random type of json (object, array, hybrid)

## TODO: Refactor is close

os - This is a built-in Python library that provides a way to interact with the file system. It can be used to navigate through directories and manipulate files.

glob - This is another built-in library that can be used to search for files using patterns.

Pandas - This library is used for data manipulation and analysis. It can handle various file formats like CSV, Excel, and JSON.

Pillow - This is a fork of the Python Imaging Library (PIL) and can be used for image processing.

Geopandas - This library is used for working with geospatial data in Python. It can handle various geospatial file formats like shapefiles, GeoJSON, and GeoTIFF.

PyPDF2 - This library can be used to manipulate PDF files in Python.

docx2txt - This library can be used to extract text from Microsoft Word documents (docx).

XlsxWriter - This library can be used to create and manipulate Excel files in Python.
