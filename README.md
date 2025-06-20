# Anki Deck Generator

A web application that converts Excel/CSV files into Anki deck packages (.apkg) that can be imported into the Anki mobile app.

## Features

- Upload Excel (.xlsx, .xls) or CSV files to generate Anki decks
- Support for multiple choice questions with randomized answer choices
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

### Basic Cards

For basic flashcards, structure your Excel/CSV file as follows:

| Front (Question) | Back (Answer) |
|------------------|---------------|
| What is Python?  | A programming language |
| What is HTML?    | HyperText Markup Language |
| What is this animal? [img:tiger.jpg] | This is a tiger |
| Identify this structure | [img:molecule.png] This is a glucose molecule |
| ...              | ... |

### Multiple Choice Questions

For multiple choice questions with randomized options, format your file like this:

| Front (Question with Options) | Back (Answer) |
|------------------|---------------|
| What is the capital of France?<br><br>A. London<br>B. Paris<br>C. Berlin<br>D. Madrid | B |
| What is the primary purpose of a database index?<br><br>A. To improve query performance<br>B. To encrypt sensitive data<br>C. To compress data<br>D. To format query outputs<br>E. To create database backups | A |

The application will:
1. Automatically detect multiple choice format (options labeled A, B, C, etc.)
2. Randomize the order of options each time the card is shown
3. Show the correct answer on the back of the card

Additional columns will be ignored.

## Multiple Choice Questions

### Benefits
- **Randomized Options**: The app shuffles answer choices each time the card is shown to ensure you learn the content, not the position
- **Standardized Format**: Perfect for exam preparation with consistent formatting
- **Full Customization**: Support for 2-5 options (labeled A through E)

### How It Works
1. Format your questions as shown above with option labels (A, B, C, etc.)
2. In the answer column, provide only the letter of the correct answer
3. The app automatically detects this format and applies the multiple choice template
4. When studying, options will appear in random order each time

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
