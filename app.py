import os
import pandas as pd
import genanki
import random
import zipfile
import io
import shutil
import uuid
import re
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['IMAGE_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create uploads and images directories if they don't exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['IMAGE_FOLDER']]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_random_id():
    return random.randrange(1 << 30, 1 << 31)

def process_content_for_images(content, image_files, deck_id):
    """Process content to find image tags and replace with proper Anki image references"""
    if not content or not image_files:
        return content
    
    # Create a temporary directory for this deck to store images
    deck_image_dir = os.path.join(app.config['IMAGE_FOLDER'], str(deck_id))
    if not os.path.exists(deck_image_dir):
        os.makedirs(deck_image_dir)
    
    # Find image references in the format [img:filename.jpg]
    img_pattern = r'\[img:(\w+\.(?:jpg|png|jpeg|gif))\]'
    matches = re.findall(img_pattern, content)
    
    # Dictionary to keep track of processed images
    media_files = []
    
    # Replace each image reference with Anki's image syntax
    for img_name in matches:
        # Check if the image is in uploaded files
        for uploaded_img in image_files:
            if uploaded_img.filename == img_name:
                # Save the image to the deck's image directory
                img_path = os.path.join(deck_image_dir, secure_filename(img_name))
                uploaded_img.save(img_path)
                media_files.append((img_path, img_name))
                break
    
    # Replace image tags with Anki's image HTML
    for img_name in matches:
        content = content.replace(f'[img:{img_name}]', f'<img src="{img_name}">')
    
    return content, media_files

def create_anki_deck(file_path, deck_name, image_files):
    """Create an Anki deck from an Excel file with image support"""
    # Read Excel file
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # Validate dataframe has at least two columns
    if len(df.columns) < 2:
        raise ValueError("Excel file must contain at least two columns (front and back)")
    
    # Create unique IDs for the deck and model
    deck_id = generate_random_id()
    model_id = generate_random_id()
    
    # Create Anki model (card template)
    model = genanki.Model(
        model_id,
        'Image Model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
            },
        ])
    
    # Create deck
    deck = genanki.Deck(deck_id, deck_name)
    
    # Keep track of all media files
    all_media_files = []
    
    # Add notes to deck
    for index, row in df.iterrows():
        # Use the first two columns for front and back
        front = str(row[df.columns[0]])
        back = str(row[df.columns[1]])
        
        # Process front and back for image tags
        front_processed, front_media = process_content_for_images(front, image_files, deck_id)
        back_processed, back_media = process_content_for_images(back, image_files, deck_id)
        
        # Add all media files to the master list
        all_media_files.extend(front_media)
        all_media_files.extend(back_media)
        
        # Create note and add to deck
        note = genanki.Note(
            model=model,
            fields=[front_processed, back_processed]
        )
        deck.add_note(note)
    
    # Create package with media files
    package = genanki.Package(deck)
    
    # Add media files to the package
    for file_path, file_name in all_media_files:
        package.media_files.append(file_path)
    
    # Save to a temporary in-memory file
    temp_file = io.BytesIO()
    package.write_to_file(temp_file)
    temp_file.seek(0)
    
    # Clean up media files after package is created
    # But keep the main directory
    if os.path.exists(os.path.join(app.config['IMAGE_FOLDER'], str(deck_id))):
        shutil.rmtree(os.path.join(app.config['IMAGE_FOLDER'], str(deck_id)))
    
    return temp_file

@app.route('/')
def index():
    # Create a unique session ID for this upload session
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    deck_name = request.form.get('deck_name', 'My Anki Deck')
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    # Get all image files from the form
    image_files = request.files.getlist('images')
    valid_images = []
    
    # Validate image files
    for img in image_files:
        if img and img.filename != '' and allowed_file(img.filename, ALLOWED_IMAGE_EXTENSIONS):
            valid_images.append(img)
    
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Generate Anki deck with images
            deck_file = create_anki_deck(file_path, deck_name, valid_images)
            
            # Delete the uploaded file after processing
            os.remove(file_path)
            
            # Send the generated deck file for download
            return send_file(
                deck_file,
                as_attachment=True,
                download_name=f"{deck_name.replace(' ', '_')}.apkg",
                mimetype='application/octet-stream'
            )
        except Exception as e:
            flash(f"Error creating Anki deck: {str(e)}")
            return redirect(url_for('index'))
    else:
        flash(f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed for the data file")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
