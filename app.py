from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify, send_from_directory
import os
import re
import shutil
import uuid
import json
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key in production

# Configuration
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
CATEGORIES_FILE = os.path.join(ASSETS_DIR, 'categories.json')

# Admin username/password (you should change these and ideally move to environment variables)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "welsh_learning_app"

# Site password protection
SITE_PASSWORD = "12345"  # Change this to your desired password

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav'}

# Ensure assets directory exists
os.makedirs(ASSETS_DIR, exist_ok=True)

# Initialize categories file if it doesn't exist
if not os.path.exists(CATEGORIES_FILE):
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "categories": []
        }, f, indent=2)

# Helper functions for categories
def get_categories():
    """Get all categories from the categories.json file."""
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('categories', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_categories(categories):
    """Save categories to the categories.json file."""
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump({"categories": categories}, f, indent=2)

def get_category_by_id(category_id):
    """Get a category by its ID."""
    categories = get_categories()
    for category in categories:
        if category['id'] == category_id:
            return category
    return None

def is_valid_identifier(identifier):
    """Check if the identifier contains only lowercase letters, numbers, and hyphens."""
    return bool(re.match(r'^[a-z0-9-]+$', identifier))

def is_valid_category(category_id):
    """Check if a category ID is valid and exists."""
    if not is_valid_identifier(category_id):
        return False
    return os.path.exists(os.path.join(ASSETS_DIR, category_id))

def is_valid_item(category_id, item_id):
    """Check if an item ID is valid and exists within a category."""
    if not is_valid_identifier(category_id) or not is_valid_identifier(item_id):
        return False
    return os.path.exists(os.path.join(ASSETS_DIR, category_id, item_id))

def allowed_file(filename, allowed_extensions):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_items_in_category(category_id):
    """Get all items in a category with basic info."""
    if not is_valid_category(category_id):
        return []
    
    items = []
    category_dir = os.path.join(ASSETS_DIR, category_id)
    
    for item_id in os.listdir(category_dir):
        item_dir = os.path.join(category_dir, item_id)
        welsh_path = os.path.join(item_dir, 'welsh.txt')
        
        if os.path.isdir(item_dir) and os.path.exists(welsh_path):
            welsh_word = ""
            with open(welsh_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    welsh_word = lines[0].strip()
            
            # Count files and variations
            images_count = len([f for f in os.listdir(os.path.join(item_dir, 'images')) 
                               if os.path.isfile(os.path.join(item_dir, 'images', f)) and 
                               any(f.lower().endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS)])
            
            english_audio_count = len([f for f in os.listdir(os.path.join(item_dir, 'english_audio')) 
                                      if os.path.isfile(os.path.join(item_dir, 'english_audio', f)) and 
                                      any(f.lower().endswith(ext) for ext in ALLOWED_AUDIO_EXTENSIONS)])
            
            welsh_audio_count = len([f for f in os.listdir(os.path.join(item_dir, 'welsh_audio')) 
                                    if os.path.isfile(os.path.join(item_dir, 'welsh_audio', f)) and 
                                    any(f.lower().endswith(ext) for ext in ALLOWED_AUDIO_EXTENSIONS)])
            
            english_variations_count = 0
            english_path = os.path.join(item_dir, 'english.txt')
            if os.path.exists(english_path):
                with open(english_path, 'r', encoding='utf-8') as f:
                    english_variations_count = sum(1 for line in f if line.strip())
            
            welsh_variations_count = 0
            with open(welsh_path, 'r', encoding='utf-8') as f:
                welsh_variations_count = sum(1 for line in f if line.strip())
            
            items.append({
                'id': item_id,
                'welsh': welsh_word,
                'images_count': images_count,
                'english_audio_count': english_audio_count,
                'welsh_audio_count': welsh_audio_count,
                'english_variations_count': english_variations_count,
                'welsh_variations_count': welsh_variations_count
            })
    
    return sorted(items, key=lambda x: x['id'])

def get_item_details(category_id, item_id):
    """Get detailed information about a specific item."""
    item_dir = os.path.join(ASSETS_DIR, category_id, item_id)
    
    # Get English variations
    english_variations = []
    english_path = os.path.join(item_dir, 'english.txt')
    if os.path.exists(english_path):
        with open(english_path, 'r', encoding='utf-8') as f:
            english_variations = [line.strip() for line in f if line.strip()]
    
    # Get Welsh variations
    welsh_variations = []
    welsh_path = os.path.join(item_dir, 'welsh.txt')
    if os.path.exists(welsh_path):
        with open(welsh_path, 'r', encoding='utf-8') as f:
            welsh_variations = [line.strip() for line in f if line.strip()]
    
    # Get images
    images = []
    images_dir = os.path.join(item_dir, 'images')
    if os.path.exists(images_dir):
        images = [f for f in os.listdir(images_dir) 
                 if os.path.isfile(os.path.join(images_dir, f)) and 
                 any(f.lower().endswith(ext) for ext in ALLOWED_IMAGE_EXTENSIONS)]
    
    # Get English audio
    english_audio = []
    english_audio_dir = os.path.join(item_dir, 'english_audio')
    if os.path.exists(english_audio_dir):
        english_audio = [f for f in os.listdir(english_audio_dir) 
                        if os.path.isfile(os.path.join(english_audio_dir, f)) and 
                        any(f.lower().endswith(ext) for ext in ALLOWED_AUDIO_EXTENSIONS)]
    
    # Get Welsh audio
    welsh_audio = []
    welsh_audio_dir = os.path.join(item_dir, 'welsh_audio')
    if os.path.exists(welsh_audio_dir):
        welsh_audio = [f for f in os.listdir(welsh_audio_dir) 
                      if os.path.isfile(os.path.join(welsh_audio_dir, f)) and 
                      any(f.lower().endswith(ext) for ext in ALLOWED_AUDIO_EXTENSIONS)]
    
    return {
        'id': item_id,
        'welsh': welsh_variations[0] if welsh_variations else "",
        'english_variations': english_variations,
        'welsh_variations': welsh_variations,
        'images': images,
        'english_audio': english_audio,
        'welsh_audio': welsh_audio
    }

def create_item_structure(category_id, item_id, welsh_word, english_variations, welsh_variations):
    """Create the directory structure and files for a new item within a category."""
    item_dir = os.path.join(ASSETS_DIR, category_id, item_id)
    os.makedirs(item_dir, exist_ok=True)
    os.makedirs(os.path.join(item_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(item_dir, 'english_audio'), exist_ok=True)
    os.makedirs(os.path.join(item_dir, 'welsh_audio'), exist_ok=True)
    
    # Create English variations file
    with open(os.path.join(item_dir, 'english.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(english_variations))
    
    # Create Welsh variations file
    with open(os.path.join(item_dir, 'welsh.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(welsh_variations))
    
    # Create placeholder files
    create_placeholder_file(os.path.join(item_dir, 'images', 'placeholder.jpg'), 
                           f"Placeholder image for {item_id}")
    
    create_placeholder_file(os.path.join(item_dir, 'english_audio', 'placeholder.mp3'), 
                           f"Placeholder English audio for {item_id}")
    
    create_placeholder_file(os.path.join(item_dir, 'welsh_audio', 'placeholder.mp3'), 
                           f"Placeholder Welsh audio for {welsh_word}")

def create_placeholder_file(filepath, content):
    """Create a file with placeholder content."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def update_item_variations(category_id, item_id, english_variations, welsh_variations):
    """Update the English and Welsh variations for an item."""
    item_dir = os.path.join(ASSETS_DIR, category_id, item_id)
    
    # Update English variations
    with open(os.path.join(item_dir, 'english.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(english_variations))
    
    # Update Welsh variations
    with open(os.path.join(item_dir, 'welsh.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(welsh_variations))

def delete_item_directory(category_id, item_id):
    """Delete an item directory and all its contents."""
    item_dir = os.path.join(ASSETS_DIR, category_id, item_id)
    if os.path.exists(item_dir):
        shutil.rmtree(item_dir)

def delete_category_directory(category_id):
    """Delete a category directory and all its contents."""
    category_dir = os.path.join(ASSETS_DIR, category_id)
    if os.path.exists(category_dir):
        shutil.rmtree(category_dir)
    
    # Also remove from categories.json
    categories = get_categories()
    categories = [c for c in categories if c['id'] != category_id]
    save_categories(categories)

# Add this decorator function to check for site password
def site_password_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.cookies.get('site_authenticated') == 'true':
            return redirect(url_for('site_login'))
        return f(*args, **kwargs)
    return decorated_function

# Basic security wrapper for admin routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.cookies.get('admin_authenticated') == 'true':
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Main App Routes
@app.route('/login', methods=['GET', 'POST'])
def site_login():
    if request.method == 'POST':
        password = request.form.get('password')
        
        if password == SITE_PASSWORD:
            response = redirect(url_for('index'))
            response.set_cookie('site_authenticated', 'true')
            return response
        else:
            flash('Incorrect password', 'error')
    
    return render_template('site_login.html')

@app.route('/')
@site_password_required
def index():
    """Render the main application page"""
    categories = get_categories()
    return render_template('index.html', categories=categories)

@app.route('/api/categories')
@site_password_required
def api_get_categories():
    """API endpoint to get all categories"""
    categories = get_categories()
    return jsonify(categories)

@app.route('/api/category/<category_id>/items')
@site_password_required
def api_get_items(category_id):
    """API endpoint to get all items in a category"""
    if not is_valid_category(category_id):
        return jsonify({"error": "Invalid category"}), 404
    
    items = []
    for item_id in os.listdir(os.path.join(ASSETS_DIR, category_id)):
        item_dir = os.path.join(ASSETS_DIR, category_id, item_id)
        welsh_path = os.path.join(item_dir, 'welsh.txt')
        
        if os.path.isdir(item_dir) and os.path.exists(welsh_path):
            try:
                # Get English variations
                english_texts = []
                english_path = os.path.join(item_dir, 'english.txt')
                if os.path.exists(english_path):
                    with open(english_path, 'r', encoding='utf-8') as f:
                        english_texts = [line.strip() for line in f.readlines() if line.strip()]
                
                # Default English is the directory name if no file exists
                english = item_id.replace('_', ' ')
                if english_texts:
                    english = english_texts[0]  # First entry is the primary form
                
                # Get Welsh variations
                welsh_texts = []
                with open(welsh_path, 'r', encoding='utf-8') as f:
                    welsh_texts = [line.strip() for line in f.readlines() if line.strip()]
                
                # Default Welsh if file is empty or doesn't exist
                welsh = ""
                if welsh_texts:
                    welsh = welsh_texts[0]  # First entry is the primary form
                else:
                    continue  # Skip if no Welsh word
                
                # Get all images
                images = []
                images_dir = os.path.join(item_dir, 'images')
                if os.path.exists(images_dir):
                    images = [f"/assets/{category_id}/{item_id}/images/{f}" for f in os.listdir(images_dir)
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                
                # Get all English audio files
                english_audio = []
                english_audio_dir = os.path.join(item_dir, 'english_audio')
                if os.path.exists(english_audio_dir):
                    english_audio = [f"/assets/{category_id}/{item_id}/english_audio/{f}" for f in os.listdir(english_audio_dir)
                                   if f.lower().endswith(('.mp3', '.wav'))]
                
                # Get all Welsh audio files
                welsh_audio = []
                welsh_audio_dir = os.path.join(item_dir, 'welsh_audio')
                if os.path.exists(welsh_audio_dir):
                    welsh_audio = [f"/assets/{category_id}/{item_id}/welsh_audio/{f}" for f in os.listdir(welsh_audio_dir)
                                 if f.lower().endswith(('.mp3', '.wav'))]
                
                # Add default placeholders if no files found
                if not images:
                    images = [f"/assets/{category_id}/{item_id}/images/placeholder.jpg"]
                if not english_audio:
                    english_audio = [f"/assets/{category_id}/{item_id}/english_audio/placeholder.mp3"]
                if not welsh_audio:
                    welsh_audio = [f"/assets/{category_id}/{item_id}/welsh_audio/placeholder.mp3"]
                
                # Create item object
                item = {
                    'id': item_id,
                    'english': english,
                    'welsh': welsh,
                    'englishTexts': english_texts or [english],
                    'welshTexts': welsh_texts or [welsh],
                    'images': images,
                    'englishAudio': english_audio,
                    'welshAudio': welsh_audio
                }
                
                items.append(item)
            except Exception as e:
                app.logger.error(f"Error processing item {item_id}: {str(e)}")
    
    return jsonify(items)

@app.route('/assets/<path:filepath>')
def serve_asset(filepath):
    """Serve files from the assets directory"""
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return send_from_directory(os.path.join(ASSETS_DIR, directory), filename)

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            response = redirect(url_for('admin_dashboard'))
            response.set_cookie('admin_authenticated', 'true')
            return response
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    response = redirect(url_for('admin_login'))
    response.set_cookie('admin_authenticated', '', expires=0)
    return response

@app.route('/admin')
@admin_required
def admin_dashboard():
    categories = get_categories()
    return render_template('admin/dashboard.html', categories=categories)

# Category Management
@app.route('/admin/category/add', methods=['GET', 'POST'])
@admin_required
def add_category():
    if request.method == 'POST':
        category_id = request.form.get('category_id', '').strip().lower()
        category_name = request.form.get('category_name', '').strip()
        
        # Validate input
        if not category_id or not category_name:
            flash('Category ID and name are required', 'error')
            return render_template('admin/add_category.html')
        
        # Validate ID (only letters, numbers, and hyphens)
        if not is_valid_identifier(category_id):
            flash('Category ID can only contain lowercase letters, numbers, and hyphens', 'error')
            return render_template('admin/add_category.html')
        
        # Check if it already exists
        if os.path.exists(os.path.join(ASSETS_DIR, category_id)):
            flash(f'Category "{category_id}" already exists', 'error')
            return render_template('admin/add_category.html')
        
        # Create category directory
        os.makedirs(os.path.join(ASSETS_DIR, category_id), exist_ok=True)
        
        # Add to categories.json
        categories = get_categories()
        categories.append({
            'id': category_id,
            'name': category_name
        })
        save_categories(categories)
        
        flash(f'Successfully added category: {category_name}', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_category.html')

@app.route('/admin/category/<category_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    if not is_valid_category(category_id):
        flash('Invalid category', 'error')
        return redirect(url_for('admin_dashboard'))
    
    category = get_category_by_id(category_id)
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        category_name = request.form.get('category_name', '').strip()
        
        # Validate input
        if not category_name:
            flash('Category name is required', 'error')
            return render_template('admin/edit_category.html', category=category)
        
        # Update in categories.json
        categories = get_categories()
        for cat in categories:
            if cat['id'] == category_id:
                cat['name'] = category_name
                break
        
        save_categories(categories)
        
        flash(f'Successfully updated category: {category_name}', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/category/<category_id>/delete', methods=['POST'])
@admin_required
def delete_category(category_id):
    if not is_valid_category(category_id):
        flash('Invalid category', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        delete_category_directory(category_id)
        flash(f'Successfully deleted category: {category_id}', 'success')
    except Exception as e:
        flash(f'Error deleting category: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/category/<category_id>')
@admin_required
def view_category(category_id):
    if not is_valid_category(category_id):
        flash('Invalid category', 'error')
        return redirect(url_for('admin_dashboard'))
    
    category = get_category_by_id(category_id)
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    items = get_items_in_category(category_id)
    
    return render_template('admin/view_category.html', category=category, items=items)

# Item Management
@app.route('/admin/category/<category_id>/item/add', methods=['GET', 'POST'])
@admin_required
def add_item(category_id):
    if not is_valid_category(category_id):
        flash('Invalid category', 'error')
        return redirect(url_for('admin_dashboard'))
    
    category = get_category_by_id(category_id)
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        item_id = request.form.get('item_id', '').strip().lower()
        welsh_word = request.form.get('welsh_word', '').strip()
        english_variations = request.form.get('english_variations', '').strip().split('\n')
        welsh_variations = request.form.get('welsh_variations', '').strip().split('\n')
        
        # Validate input
        if not item_id or not welsh_word:
            flash('Item ID and Welsh word are required', 'error')
            return render_template('admin/add_item.html', category=category)
        
        # Validate ID (only letters, numbers, and hyphens)
        if not is_valid_identifier(item_id):
            flash('Item ID can only contain lowercase letters, numbers, and hyphens', 'error')
            return render_template('admin/add_item.html', category=category)
        
        # Check if it already exists
        if os.path.exists(os.path.join(ASSETS_DIR, category_id, item_id)):
            flash(f'Item "{item_id}" already exists in this category', 'error')
            return render_template('admin/add_item.html', category=category)
        
        # Filter empty lines
        english_variations = [v.strip() for v in english_variations if v.strip()]
        welsh_variations = [v.strip() for v in welsh_variations if v.strip()]
        
        # Ensure primary forms are included
        if item_id.replace('-', ' ') not in english_variations:
            english_variations.insert(0, item_id.replace('-', ' '))
        if welsh_word not in welsh_variations:
            welsh_variations.insert(0, welsh_word)
        
        # Create item structure
        try:
            create_item_structure(category_id, item_id, welsh_word, english_variations, welsh_variations)
            flash(f'Successfully added item: {item_id} ({welsh_word})', 'success')
            return redirect(url_for('view_category', category_id=category_id))
        except Exception as e:
            flash(f'Error creating item: {str(e)}', 'error')
    
    return render_template('admin/add_item.html', category=category)

@app.route('/admin/category/<category_id>/item/<item_id>')
@admin_required
def view_item(category_id, item_id):
    if not is_valid_item(category_id, item_id):
        flash('Invalid item', 'error')
        return redirect(url_for('view_category', category_id=category_id))
    
    category = get_category_by_id(category_id)
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    item = get_item_details(category_id, item_id)
    
    return render_template('admin/view_item.html', category=category, item=item)

@app.route('/admin/category/<category_id>/item/<item_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_item(category_id, item_id):
    if not is_valid_item(category_id, item_id):
        flash('Invalid item', 'error')
        return redirect(url_for('view_category', category_id=category_id))
    
    category = get_category_by_id(category_id)
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    item = get_item_details(category_id, item_id)
    
    if request.method == 'POST':
        english_variations = request.form.get('english_variations', '').strip().split('\n')
        welsh_variations = request.form.get('welsh_variations', '').strip().split('\n')
        
        # Filter empty lines
        english_variations = [v.strip() for v in english_variations if v.strip()]
        welsh_variations = [v.strip() for v in welsh_variations if v.strip()]
        
        if not english_variations or not welsh_variations:
            flash('At least one English and one Welsh variation are required', 'error')
            return render_template('admin/edit_item.html', category=category, item=item)
        
        # Update variations
        try:
            update_item_variations(category_id, item_id, english_variations, welsh_variations)
            flash(f'Successfully updated item: {item_id}', 'success')
            return redirect(url_for('view_item', category_id=category_id, item_id=item_id))
        except Exception as e:
            flash(f'Error updating item: {str(e)}', 'error')
    
    return render_template('admin/edit_item.html', category=category, item=item)

@app.route('/admin/category/<category_id>/item/<item_id>/delete', methods=['POST'])
@admin_required
def delete_item(category_id, item_id):
    if not is_valid_item(category_id, item_id):
        flash('Invalid item', 'error')
        return redirect(url_for('view_category', category_id=category_id))
    
    try:
        delete_item_directory(category_id, item_id)
        flash(f'Successfully deleted item: {item_id}', 'success')
    except Exception as e:
        flash(f'Error deleting item: {str(e)}', 'error')
    
    return redirect(url_for('view_category', category_id=category_id))

# Media Management
@app.route('/admin/category/<category_id>/item/<item_id>/upload-image', methods=['POST'])
@admin_required
def upload_image(category_id, item_id):
    if not is_valid_item(category_id, item_id):
        flash('Invalid item', 'error')
        return redirect(url_for('view_category', category_id=category_id))
    
    if 'image' not in request.files:
        flash('No image file selected', 'error')
        return redirect(url_for('view_item', category_id=category_id, item_id=item_id))
    
    file = request.files['image']
    
    if file.filename == '':
        flash('No image file selected', 'error')
        return redirect(url_for('view_item', category_id=category_id, item_id=item_id))
    
    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(file.filename)
        
        # Generate unique filename if it already exists
        images_dir = os.path.join(ASSETS_DIR, category_id, item_id, 'images')
        if os.path.exists(os.path.join(images_dir, filename)):
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{uuid.uuid4().hex[:6]}{ext}"
        
        # Save file
        file.save(os.path.join(images_dir, filename))
        flash(f'Successfully uploaded image: {filename}', 'success')
    else:
        flash('Invalid file type. Only JPG, PNG, and GIF are allowed', 'error')
    
    return redirect(url_for('view_item', category_id=category_id, item_id=item_id))

@app.route('/admin/category/<category_id>/item/<item_id>/upload-audio/<audio_type>', methods=['POST'])
@admin_required
def upload_audio(category_id, item_id, audio_type):
    if not is_valid_item(category_id, item_id):
        flash('Invalid item', 'error')
        return redirect(url_for('view_category', category_id=category_id))
    
    if audio_type not in ['english_audio', 'welsh_audio']:
        flash('Invalid audio type', 'error')
        return redirect(url_for('view_item', category_id=category_id, item_id=item_id))
    
    if 'audio' not in request.files:
        flash('No audio file selected', 'error')
        return redirect(url_for('view_item', category_id=category_id, item_id=item_id))
    
    file = request.files['audio']
    
    if file.filename == '':
        flash('No audio file selected', 'error')
        return redirect(url_for('view_item', category_id=category_id, item_id=item_id))
    
    if file and allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
        filename = secure_filename(file.filename)
        
        # Generate unique filename if it already exists
        audio_dir = os.path.join(ASSETS_DIR, category_id, item_id, audio_type)
        if os.path.exists(os.path.join(audio_dir, filename)):
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{uuid.uuid4().hex[:6]}{ext}"
        
        # Save file
        file.save(os.path.join(audio_dir, filename))
        flash(f'Successfully uploaded audio: {filename}', 'success')
    else:
        flash('Invalid file type. Only MP3 and WAV are allowed', 'error')
    
    return redirect(url_for('view_item', category_id=category_id, item_id=item_id))

@app.route('/admin/category/<category_id>/item/<item_id>/delete-image/<image_name>', methods=['POST'])
@admin_required
def delete_image(category_id, item_id, image_name):
    if not is_valid_item(category_id, item_id):
        flash('Invalid item', 'error')
        return redirect(url_for('view_category', category_id=category_id))
    
    filename = secure_filename(image_name)
    image_path = os.path.join(ASSETS_DIR, category_id, item_id, 'images', filename)
    
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
            flash(f'Successfully deleted image: {filename}', 'success')
        except Exception as e:
            flash(f'Error deleting image: {str(e)}', 'error')
    else:
        flash(f'Image not found: {filename}', 'error')
    
    return redirect(url_for('view_item', category_id=category_id, item_id=item_id))

@app.route('/admin/category/<category_id>/item/<item_id>/delete-audio/<audio_type>/<audio_name>', methods=['POST'])
@admin_required
def delete_audio(category_id, item_id, audio_type, audio_name):
    if not is_valid_item(category_id, item_id):
        flash('Invalid item', 'error')
        return redirect(url_for('view_category', category_id=category_id))
    
    if audio_type not in ['english_audio', 'welsh_audio']:
        flash('Invalid audio type', 'error')
        return redirect(url_for('view_item', category_id=category_id, item_id=item_id))
    
    filename = secure_filename(audio_name)
    audio_path = os.path.join(ASSETS_DIR, category_id, item_id, audio_type, filename)
    
    if os.path.exists(audio_path):
        try:
            os.remove(audio_path)
            flash(f'Successfully deleted audio: {filename}', 'success')
        except Exception as e:
            flash(f'Error deleting audio: {str(e)}', 'error')
    else:
        flash(f'Audio file not found: {filename}', 'error')
    
    return redirect(url_for('view_item', category_id=category_id, item_id=item_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
