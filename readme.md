# Welsh Body Parts Learning Application

A Flask-based web application for learning Welsh body part vocabulary through interactive games with multiple modes and difficulty levels.

## Features

- Multiple game modes:
  - Image to Welsh word
  - English to Welsh word
  - Welsh to English word
  - English audio to Welsh word
  - Welsh audio to English word
  - Mixed modal challenge
- Multiple difficulty levels
- Customizable number of questions
- Random selection of questions
- Score tracking and timing
- Support for multiple variations of words
- Multiple images and audio files for each body part

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone or download this repository to your local machine.

2. Navigate to the project directory in a terminal or command prompt.

3. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Setting Up Assets

1. Create an `assets` directory in the root of the project.

2. Inside the `assets` directory, create a subdirectory for each body part (e.g., `foot`, `head`, `eye`, etc.).

3. For each body part directory, create the following:
   - `english.txt`: File containing English variations of the word (one per line)
   - `welsh.txt`: File containing Welsh variations of the word (one per line)
   - `images/`: Directory for images of the body part
   - `english_audio/`: Directory for English pronunciation audio files
   - `welsh_audio/`: Directory for Welsh pronunciation audio files

4. Add at least one image file (.jpg, .png, .gif) to each `images` directory.

5. Add at least one audio file (.mp3, .wav) to each audio directory.

Example asset directory structure:
```
assets/
├── foot/
│   ├── english.txt
│   ├── welsh.txt
│   ├── images/
│   │   └── foot1.jpg
│   ├── english_audio/
│   │   └── foot.mp3
│   └── welsh_audio/
│       └── troed.mp3
└── ...
```

### Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Adding New Body Parts

To add a new body part to the application:

1. Create a new directory in the `assets` folder with the English name of the body part (e.g., `nose`).

2. Inside this directory, create:
   - `english.txt` file with English variations of the word
   - `welsh.txt` file with Welsh variations of the word
   - `images`, `english_audio`, and `welsh_audio` directories
   - Add appropriate image and audio files to their respective directories

3. The application will automatically detect the new body part when it starts up.

## License

This project is open source and available for personal and educational use.
