/**
 * UI management for the Welsh vocabulary learning game
 */

// DOM elements
const startScreen = document.getElementById('start-screen');
const gameScreen = document.getElementById('game-screen');
const resultScreen = document.getElementById('result-screen');

const categorySelect = document.getElementById('category');
const modeSelect = document.getElementById('mode');
const difficultySelect = document.getElementById('difficulty');
const questionsSelect = document.getElementById('questions');
const startButton = document.getElementById('start-button');

const currentQuestionEl = document.getElementById('current-question');
const totalQuestionsEl = document.getElementById('total-questions');
const scoreEl = document.getElementById('score');
const timerDisplay = document.getElementById('timer');

const questionImage = document.getElementById('question-image');
const questionText = document.getElementById('question-text');
const questionAudio = document.getElementById('question-audio');
const optionsContainer = document.getElementById('options');

const finalScoreEl = document.getElementById('final-score');
const finalTotalEl = document.getElementById('final-total');
const finalTimeEl = document.getElementById('final-time');
const playAgainButton = document.getElementById('play-again-button');

/**
 * UI functions
 */
const UI = {
    /**
     * Show the start screen
     */
    showStartScreen() {
        startScreen.style.display = 'flex';
        gameScreen.style.display = 'none';
        resultScreen.style.display = 'none';
    },

    /**
     * Show the game screen
     */
    showGameScreen() {
        startScreen.style.display = 'none';
        gameScreen.style.display = 'flex';
        resultScreen.style.display = 'none';
    },

    /**
     * Show the result screen
     */
    showResultScreen() {
        startScreen.style.display = 'none';
        gameScreen.style.display = 'none';
        resultScreen.style.display = 'flex';
    },

    /**
     * Update the timer display
     * @param {Object} time - Formatted time object with minutes and seconds
     */
    updateTimer(time) {
        timerDisplay.textContent = `${time.minutes}:${time.seconds}`;
    },

    /**
     * Update current question and score display
     * @param {number} currentIndex - Current question index (1-based)
     * @param {number} total - Total number of questions
     * @param {number} score - Current score
     */
    updateProgress(currentIndex, total, score) {
        currentQuestionEl.textContent = currentIndex;
        totalQuestionsEl.textContent = total;
        scoreEl.textContent = score;
    },

    /**
     * Update final score and time on result screen
     * @param {number} score - Final score
     * @param {number} total - Total questions
     * @param {Object} time - Formatted time object with minutes and seconds
     */
    updateResults(score, total, time) {
        finalScoreEl.textContent = score;
        finalTotalEl.textContent = total;
        finalTimeEl.textContent = `${time.minutes}:${time.seconds}`;
    },

    /**
     * Clear previous question content
     */
    clearQuestion() {
        // Hide all question elements
        questionImage.style.display = 'none';
        questionText.style.display = 'none';
        questionAudio.style.display = 'none';
        
        // Clear their content
        questionImage.src = '';
        questionText.textContent = '';
        
        // Clear options
        optionsContainer.innerHTML = '';
    },

    /**
     * Display image question
     * @param {string} imageSrc - Image source path
     * @param {string} altText - Alt text for the image
     */
    showImageQuestion(imageSrc, altText) {
        // Create a new Image object to preload the image
        const img = new Image();
        
        // Add loading spinner or placeholder while the image loads
        questionText.textContent = "Loading...";
        questionText.style.display = 'block';
        
        // When the image is loaded, update the UI
        img.onload = function() {
            // Hide the loading text
            questionText.style.display = 'none';
            
            // Now set the src and show the image
            questionImage.src = imageSrc;
            questionImage.alt = ""; // Empty alt text to avoid giving away the answer
            questionImage.style.display = 'block';
        };
        
        // If there's an error loading the image
        img.onerror = function() {
            questionText.textContent = "Error loading image";
            questionText.style.display = 'block';
        };
        
        // Start loading the image
        img.src = imageSrc;
    },

    /**
     * Display text question
     * @param {string} text - Question text
     */
    showTextQuestion(text) {
        questionText.textContent = text;
        questionText.style.display = 'block';
    },

    /**
     * Show audio button for question
     * @param {Function} audioCallback - Function to call when audio button is clicked
     */
    showAudioQuestion(audioCallback) {
        questionText.textContent = "Listen and translate:";
        questionText.style.display = 'block';
        questionAudio.style.display = 'block';
        questionAudio.onclick = audioCallback;
    },

    /**
     * Generate answer options
     * @param {Array} options - Array of option objects
     * @param {string} answerType - Type of answer (welsh-text, english-text, image)
     * @param {Function} selectCallback - Callback when option is selected
     */
    generateOptions(options, answerType, selectCallback) {
        optionsContainer.innerHTML = '';
        
        options.forEach(option => {
            const optionEl = document.createElement('div');
            optionEl.className = 'option';
            
            if (answerType === 'image') {
                // Display image as option
                const img = document.createElement('img');
                img.src = getRandomImage(option);
                img.alt = option.english;
                img.style.width = '100%';
                img.style.height = '100px';
                img.style.objectFit = 'contain';
                optionEl.appendChild(img);
                optionEl.dataset.id = option.id;
            } else if (answerType === 'welsh-text') {
                // Display Welsh text
                optionEl.textContent = getRandomWelshText(option);
            } else if (answerType === 'english-text') {
                // Display English text
                optionEl.textContent = getRandomEnglishText(option);
            }
            
            optionEl.addEventListener('click', () => selectCallback(optionEl, option));
            optionsContainer.appendChild(optionEl);
        });
    },

    /**
     * Mark options as correct or incorrect
     * @param {HTMLElement} selectedOption - The option element that was selected
     * @param {Object} selectedData - Data for the selected option
     * @param {string} correctId - ID of the correct answer
     * @param {string} answerType - Type of answer (welsh-text, english-text, image)
     * @returns {boolean} Whether the selection was correct
     */
    markOption(selectedOption, selectedData, correctId, answerType) {
        const options = optionsContainer.querySelectorAll('.option');
        let isCorrect = false;
        
        if (answerType === 'image') {
            // For image answers, check by dataset ID
            isCorrect = selectedOption.dataset.id === correctId;
        } else {
            // For text answers
            isCorrect = selectedData.id === correctId;
        }
        
        options.forEach(option => {
            let optionData;
            
            if (answerType === 'image') {
                // For image answers, get data from dataset ID
                const optionId = option.dataset.id;
                optionData = vocabularyItems.find(item => item.id === optionId);
            } else if (answerType === 'welsh-text') {
                // For Welsh text, find by Welsh text content
                const optionText = option.textContent;
                optionData = vocabularyItems.find(item => 
                    item.welshTexts && item.welshTexts.includes(optionText));
            } else if (answerType === 'english-text') {
                // For English text, find by English text content
                const optionText = option.textContent;
                optionData = vocabularyItems.find(item => 
                    item.englishTexts && item.englishTexts.includes(optionText));
            }
            
            // Skip if option data not found
            if (!optionData) return;
            
            // Highlight correct and incorrect options
            if (optionData.id === correctId) {
                option.classList.add('correct');
            } else if (option === selectedOption && !isCorrect) {
                option.classList.add('incorrect');
            }
        });
        
        return isCorrect;
    }
};