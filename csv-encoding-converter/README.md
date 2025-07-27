# CSV Encoding Converter

A simple Python script to read a CSV file with a potentially incorrect encoding and save it with the standard `UTF-8-SIG` format. This is particularly useful for fixing issues where special characters (like accents or non-Latin alphabets) do not display correctly in software like Microsoft Excel.

## Technologies Used

* **Python**
* **pandas** library for CSV manipulation

## Features

* Reads an input file named `input_file.csv`.
* Gracefully handles `UnicodeDecodeError` by attempting a fallback encoding.
* Supports common encodings like `UTF-8` and `ISO-8859-1`.
* Outputs a corrected file named `output_file.csv`.
* Saves the output with `UTF-8-SIG` (UTF-8 with BOM), ensuring maximum compatibility with Excel and other spreadsheet programs.

## How to Use

1.  Clone the project or download the script into a directory.

2.  Install the necessary dependency:
    ```bash
    pip install pandas
    ```

3.  Place your source CSV file in the same directory and **rename it to `input_file.csv`**.

### Running the Script

In your terminal, navigate to the project directory and run:

```bash
python main.py