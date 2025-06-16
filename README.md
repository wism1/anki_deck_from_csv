# Anki Deck Generator

A web application that converts Excel/CSV files into Anki deck packages (.apkg) that can be imported into the Anki mobile app.

## Features

- Upload Excel (.xlsx, .xls) or CSV files to generate Anki decks
- Support for images on both front and back of flashcards
- Simple and intuitive user interface
- Immediate download of generated Anki deck packages
- Ready to import into your iPhone Anki app

## Requirements

- Python 3.7+
- Flask
- pandas
- genanki
- openpyxl (for Excel file processing)

## Installation

1. Clone or download this repository
2. Install dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Start the application:

```
python app.py
```

2. Open your web browser and go to `http://127.0.0.1:5000/`
3. Upload an Excel or CSV file
   - The file should have at least two columns
   - The first column will be used for the front of the flashcard
   - The second column will be used for the back of the flashcard
4. Enter a name for your deck
5. Click "Generate Anki Deck"
6. Download the generated .apkg file
7. Import the file into your Anki app on your iPhone

## Excel/CSV File Format

Your Excel or CSV file should be structured as follows:

| Front (Question) | Back (Answer) |
|------------------|---------------|
| What is Python?  | A programming language |
| What is HTML?    | HyperText Markup Language |
| What is this animal? [img:tiger.jpg] | This is a tiger |
| Identify this structure | [img:molecule.png] This is a glucose molecule |
| ...              | ... |

Additional columns will be ignored.

## Using Images in Flashcards

You can include images in both the front and back of your flashcards:

1. Prepare your image files (supported formats: PNG, JPG, JPEG, GIF)
2. Upload these images through the application's image upload field
3. Reference images in your Excel/CSV file using the format `[img:filename.jpg]`

### Image Reference Examples

- To add an image to a question: `What is this? [img:picture.jpg]`
- To add an image to an answer: `This is a bicycle [img:bicycle.png]`
- To use just an image as a question: `[img:map.jpg]`

**Important:** The image filename reference must match exactly (case-sensitive) with the uploaded image file.

## Importing into Anki on iPhone

1. Transfer the .apkg file to your iPhone (e.g., via email, AirDrop, cloud storage)
2. Open the file with Anki
3. The deck will be automatically imported and ready to use
