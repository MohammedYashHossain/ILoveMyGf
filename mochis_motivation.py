import os
from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import random

app = Flask(__name__)

# Motivational quotes for cats (and cat lovers!)
CAT_MOTIVATIONAL_QUOTES = [
    "Purr-severe through challenges!",
    "You're simply meow-velous!",
    "Embrace your inner cat-titude!",
    "Nap like a champion, live like a legend!",
    "Be as confident as a cat on a sunny windowsill!",
    "Every day is your playground!",
    "You're pawsitively amazing!",
    "Stretch, relax, conquer!",
    "Believe in yourself like Mochi believes in naps!",
    "Your potential is as limitless as a cat's curiosity!"
]

# Ensure upload directory exists
UPLOAD_FOLDER = 'static/uploads'
MOTIVATION_FOLDER = 'static/motivated_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MOTIVATION_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MOTIVATION_FOLDER'] = MOTIVATION_FOLDER

def add_motivation_to_image(image_path):
    # Open the uploaded image
    img = Image.open(image_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    
    # Choose a random motivational quote
    quote = random.choice(CAT_MOTIVATIONAL_QUOTES)
    
    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
    
    # Get image dimensions
    width, height = img.size
    
    # Add a semi-transparent background for text readability
    draw.rectangle([0, height-100, width, height], fill=(255,255,255,180))
    
    # Add text to the image
    draw.text((10, height-90), quote, font=font, fill=(0,0,0))
    
    # Save the motivated image
    motivated_path = os.path.join(MOTIVATION_FOLDER, f'motivated_{os.path.basename(image_path)}')
    img.save(motivated_path)
    
    return motivated_path

@app.route('/mochis-motivation', methods=['GET', 'POST'])
def upload_image():
    motivated_image = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        
        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Generate motivated image
        motivated_image = add_motivation_to_image(filename)
    
    return render_template('mochis_motivation.html', motivated_image=motivated_image)

if __name__ == '__main__':
    app.run(debug=True)