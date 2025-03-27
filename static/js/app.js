/**
 * Main application for the Welsh Learning App
 */

// Global variables to store data
let categories = [];
let currentCategory = '';
let vocabularyItems = [];

/**
 * Load categories from the API
 */
async function loadCategories() {
    try {
        console.log("Fetching categories...");
        
        const response = await fetch('/api/categories');
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        categories = await response.json();
        console.log(`Loaded ${categories.length} categories`);
        
        // Update category dropdown
        updateCategoryDropdown();
        
        // If there's at least one category, load its items
        if (categories.length > 0) {
            const firstCategory = categories[0].id;
            document.getElementById('category').value = firstCategory;
            loadVocabularyItems(firstCategory);
        } else {
            console.warn("No categories available");
            enableStartButton(false);
        }
        
    } catch (error) {
        console.error("Error loading categories:", error);
        enableStartButton(false);
    }
}

/**
 * Update the category dropdown with available categories
 */
function updateCategoryDropdown() {
    const categoryDropdown = document.getElementById('category');
    categoryDropdown.innerHTML = '';
    
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        categoryDropdown.appendChild(option);
    });
    
    // Add change event listener
    categoryDropdown.addEventListener('change', () => {
        loadVocabularyItems(categoryDropdown.value);
    });
}

/**
 * Load vocabulary items for a specific category
 * @param {string} categoryId - The category ID to load items for
 */
async function loadVocabularyItems(categoryId) {
    try {
        console.log(`Loading items for category: ${categoryId}`);
        currentCategory = categoryId;
        
        // Show loading state
        enableStartButton(false, "Loading...");
        
        const response = await fetch(`/api/category/${categoryId}/items`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        vocabularyItems = await response.json();
        console.log(`Loaded ${vocabularyItems.length} items`);
        
        if (vocabularyItems.length > 0) {
            enableStartButton(true);
        } else {
            console.warn("No vocabulary items available for this category");
            enableStartButton(false, "No items available");
        }
        
    } catch (error) {
        console.error(`Error loading vocabulary items for category ${categoryId}:`, error);
        enableStartButton(false, "Error loading items");
    }
}

/**
 * Enable or disable the start button
 * @param {boolean} enabled - Whether the button should be enabled
 * @param {string} text - Text to display on the button
 */
function enableStartButton(enabled, text = "Start Game") {
    const startButton = document.getElementById('start-button');
    startButton.disabled = !enabled;
    startButton.textContent = text;
}

/**
 * Get a random image path for a vocabulary item
 * @param {Object} item - The vocabulary item
 * @returns {String} A random image path
 */
function getRandomImage(item) {
    if (!item.images || item.images.length === 0) {
        return '';
    }
    
    // Use only the first image if usePrimaryMedia is checked
    if (Game.state.usePrimaryMedia) {
        return item.images[0];
    }
    
    // Otherwise choose a random image
    return item.images[Math.floor(Math.random() * item.images.length)];
}


/**
 * Get a random English audio path for a vocabulary item
 * @param {Object} item - The vocabulary item
 * @returns {String} A random English audio path
 */
function getRandomEnglishAudio(item) {
    if (!item.englishAudio || item.englishAudio.length === 0) {
        return '';
    }
    
    // Use only the first audio file if usePrimaryMedia is checked
    if (Game.state.usePrimaryMedia) {
        return item.englishAudio[0];
    }
    
    // Otherwise choose a random audio file
    return item.englishAudio[Math.floor(Math.random() * item.englishAudio.length)];
}

/**
 * Get a random Welsh audio path for a vocabulary item
 * @param {Object} item - The vocabulary item
 * @returns {String} A random Welsh audio path
 */
function getRandomWelshAudio(item) {
    if (!item.welshAudio || item.welshAudio.length === 0) {
        return '';
    }
    
    // Use only the first audio file if usePrimaryMedia is checked
    if (Game.state.usePrimaryMedia) {
        return item.welshAudio[0];
    }
    
    // Otherwise choose a random audio file
    return item.welshAudio[Math.floor(Math.random() * item.welshAudio.length)];
}

/**
 * Get a random English text for a vocabulary item
 * @param {Object} item - The vocabulary item
 * @returns {String} A random English text
 */
function getRandomEnglishText(item) {
    if (!item.englishTexts || item.englishTexts.length === 0) {
        return item.english;
    }
    
    // Use only the first English variation if usePrimaryWords is checked
    if (Game.state.usePrimaryWords) {
        return item.englishTexts[0];
    }
    
    // Otherwise choose a random variation
    return item.englishTexts[Math.floor(Math.random() * item.englishTexts.length)];
}

/**
 * Get a random Welsh text for a vocabulary item
 * @param {Object} item - The vocabulary item
 * @returns {String} A random Welsh text
 */
function getRandomWelshText(item) {
    if (!item.welshTexts || item.welshTexts.length === 0) {
        return item.welsh;
    }
    
    // Use only the first Welsh variation if usePrimaryWords is checked
    if (Game.state.usePrimaryWords) {
        return item.welshTexts[0];
    }
    
    // Otherwise choose a random variation
    return item.welshTexts[Math.floor(Math.random() * item.welshTexts.length)];
}

// Set up event listeners
function initApp() {
    // Wait for vocabulary items to be loaded before initializing UI
    initGameUI();
    // Set up slider value displays
const difficultySlider = document.getElementById('difficulty');
const difficultyValue = document.getElementById('difficulty-value');
difficultySlider.addEventListener('input', () => {
    difficultyValue.textContent = difficultySlider.value;
});

const questionsSlider = document.getElementById('questions');
const questionsValue = document.getElementById('questions-value');
questionsSlider.addEventListener('input', () => {
    questionsValue.textContent = questionsSlider.value;
});
}

// Initialize game UI and event listeners
function initGameUI() {
    // Start game button
    startButton.addEventListener('click', () => {
        if (vocabularyItems.length > 0) {
            Game.start(vocabularyItems);
        }
    });
    
    // Play again button
    playAgainButton.addEventListener('click', () => {
        Game.reset();
    });
    
    // Audio button
    questionAudio.addEventListener('click', () => {
        Game.playQuestionAudio();
    });
    
    // Show the start screen now that everything is loaded
    UI.showStartScreen();
}

// Initialize the app when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Disable start button until data is loaded
    enableStartButton(false, "Loading...");
    
    // Load categories
    loadCategories();
    
    // Initialize the app
    initApp();
});
