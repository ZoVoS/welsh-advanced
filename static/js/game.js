/**
 * Core game logic for Welsh vocabulary learning game
 */

// Game configuration and state
const Game = {
    // Game state
    state: {
        mode: null,
        difficulty: null,
        questionCount: null,
        questions: [],
        currentQuestionIndex: 0,
        score: 0,
        selectedOption: null,
        correctAnswer: null,
        answeredCorrectly: false,
        gameComplete: false,
        startTime: null,
        endTime: null,
        timerInterval: null,
        usePrimaryWords: true,  // Default to true
        usePrimaryMedia: false,  // Default to false
        isAudioPlaying: false   // Flag to prevent double-playing audio
    },
    
    /**
     * Get a random image path for a vocabulary item
     */
    getRandomImage(item) {
        if (!item.images || item.images.length === 0) {
            return '';
        }
        
        // Use only the first image if usePrimaryMedia is checked
        if (this.state.usePrimaryMedia) {
            return item.images[0];
        }
        
        // Otherwise choose a random image
        return item.images[Math.floor(Math.random() * item.images.length)];
    },
    
    /**
     * Get a random English text for a vocabulary item
     */
    getRandomEnglishText(item) {
        if (!item.englishTexts || item.englishTexts.length === 0) {
            return item.english;
        }
        
        // Use only the first English variation if usePrimaryWords is checked
        if (this.state.usePrimaryWords) {
            return item.englishTexts[0];
        }
        
        // Otherwise choose a random variation
        return item.englishTexts[Math.floor(Math.random() * item.englishTexts.length)];
    },
    
    /**
     * Get a random Welsh text for a vocabulary item
     */
    getRandomWelshText(item) {
        if (!item.welshTexts || item.welshTexts.length === 0) {
            return item.welsh;
        }
        
        // Use only the first Welsh variation if usePrimaryWords is checked
        if (this.state.usePrimaryWords) {
            return item.welshTexts[0];
        }
        
        // Otherwise choose a random variation
        return item.welshTexts[Math.floor(Math.random() * item.welshTexts.length)];
    },
    
    /**
     * Get a random English audio path for a vocabulary item
     */
    getRandomEnglishAudio(item) {
        if (!item.englishAudio || item.englishAudio.length === 0) {
            return '';
        }
        
        // Use only the first audio file if usePrimaryMedia is checked
        if (this.state.usePrimaryMedia) {
            return item.englishAudio[0];
        }
        
        // Otherwise choose a random audio file
        return item.englishAudio[Math.floor(Math.random() * item.englishAudio.length)];
    },
    
    /**
     * Get a random Welsh audio path for a vocabulary item
     */
    getRandomWelshAudio(item) {
        if (!item.welshAudio || item.welshAudio.length === 0) {
            return '';
        }
        
        // Use only the first audio file if usePrimaryMedia is checked
        if (this.state.usePrimaryMedia) {
            return item.welshAudio[0];
        }
        
        // Otherwise choose a random audio file
        return item.welshAudio[Math.floor(Math.random() * item.welshAudio.length)];
    },
    
    /**
     * Start the game
     * @param {Array} vocabularyItems - Array of vocabulary items to use for the game
     */
    start(vocabularyItems) {
        // Get game settings
        this.state.mode = modeSelect.value;
        this.state.difficulty = parseInt(document.getElementById('difficulty').value);
        this.state.questionCount = parseInt(document.getElementById('questions').value);
        this.state.usePrimaryWords = document.getElementById('use-primary-words').checked;
        this.state.usePrimaryMedia = document.getElementById('use-primary-media').checked;
        
        // Reset state
        this.state.currentQuestionIndex = 0;
        this.state.score = 0;
        this.state.selectedOption = null;
        this.state.correctAnswer = null;
        this.state.answeredCorrectly = false;
        this.state.gameComplete = false;
        this.state.isAudioPlaying = false;
        
        // Generate questions
        this.generateQuestions(vocabularyItems);
        
        // Update UI
        UI.showGameScreen();
        UI.updateProgress(1, this.state.questionCount, 0);
        
        // Start the timer
        this.startTimer();
        
        // Show first question
        this.showQuestion();
    },
    
    /**
     * Reset the game
     */
    reset() {
        // Stop timer if running
        if (this.state.timerInterval) {
            clearInterval(this.state.timerInterval);
        }
        
        // Reset state
        this.state = {
            mode: null,
            difficulty: null,
            questionCount: null,
            questions: [],
            currentQuestionIndex: 0,
            score: 0,
            selectedOption: null,
            correctAnswer: null,
            answeredCorrectly: false,
            gameComplete: false,
            startTime: null,
            endTime: null,
            timerInterval: null,
            usePrimaryWords: document.getElementById('use-primary-words').checked,
            usePrimaryMedia: document.getElementById('use-primary-media').checked,
            isAudioPlaying: false
        };
        
        // Update UI
        UI.showStartScreen();
    },
    
    /**
 * Generate questions based on game settings
 * @param {Array} vocabularyItems - Array of vocabulary items to use for the game
 */
generateQuestions(vocabularyItems) {
    // Reset questions array
    this.state.questions = [];
    
    // Get the requested number of questions
    const requestedQuestions = this.state.questionCount;
    
    // Create a copy of the vocabulary items array
    let itemPool = [...vocabularyItems];
    
    // If we have fewer items than requested questions, we'll need to allow repeats
    const allowRepeats = vocabularyItems.length < requestedQuestions;
    
    // Generate questions until we have enough or run out of unique items
    for (let i = 0; i < requestedQuestions; i++) {
        // If we've used all items and we're allowing repeats, reset the pool
        if (itemPool.length === 0) {
            if (allowRepeats) {
                itemPool = [...vocabularyItems];
                console.log("Refilled item pool to generate more questions");
            } else {
                console.log("No more unique items available");
                break; // Stop generating questions if we don't want repeats
            }
        }
        
        // Select a random item
        const randomIndex = Math.floor(Math.random() * itemPool.length);
        const selectedItem = itemPool.splice(randomIndex, 1)[0];
        
        // For mixed mode, generate a random question and answer type for each question
        if (this.state.mode === 'mixed') {
            const questionTypes = ['image', 'english-text', 'welsh-text', 'english-audio', 'welsh-audio'];
            const answerTypes = ['welsh-text', 'english-text', 'image'];
            
            // Choose random question type
            const questionType = questionTypes[Math.floor(Math.random() * questionTypes.length)];
            
            // Choose appropriate answer type based on question type
            let answerType;

            if (questionType === 'image') {
                // Image questions should always have Welsh text answers
                answerType = 'welsh-text';
            } else if (questionType === 'english-text') {
                // English text questions should have Welsh text or image answers
                answerType = Math.random() < 0.7 ? 'welsh-text' : 'image';
            } else if (questionType === 'english-audio') {
                // English audio questions should always have Welsh text answers
                answerType = 'welsh-text';
            } else if (questionType === 'welsh-text') {
                // Welsh text questions should have English text or image answers
                answerType = Math.random() < 0.7 ? 'english-text' : 'image';
            } else if (questionType === 'welsh-audio') {
                // Welsh audio questions should ONLY have English text answers, NEVER Welsh text or images
                answerType = 'english-text';
            }
            
            // Add the question with its types
            this.state.questions.push({
                ...selectedItem,
                questionType,
                answerType
            });
        } else {
            // Add standard question
            this.state.questions.push(selectedItem);
        }
    }
    
    console.log(`Generated ${this.state.questions.length} questions from ${vocabularyItems.length} unique items, with repeats ${allowRepeats ? 'allowed' : 'not allowed'}`);
    },
    
    /**
     * Show the current question
     */
    showQuestion() {
        // Reset state for new question
        this.state.selectedOption = null;
        this.state.answeredCorrectly = false;
        
        // Update progress display
        UI.updateProgress(this.state.currentQuestionIndex + 1, this.state.questionCount, this.state.score);
        
        // Get current question
        const currentQuestion = this.state.questions[this.state.currentQuestionIndex];
        this.state.correctAnswer = currentQuestion;
        
        // Clear previous question
        UI.clearQuestion();
        
        // Configure question based on mode
        if (this.state.mode === 'mixed') {
            this.showMixedQuestion(currentQuestion);
        } else {
            this.showStandardQuestion(currentQuestion);
        }
        
        // Generate answer options
        this.generateOptions();
    },
    
    /**
     * Show question for mixed mode
     * @param {Object} question - The question object
     */
    showMixedQuestion(question) {
        const questionType = question.questionType;
        
        switch (questionType) {
            case 'image':
                UI.showImageQuestion(this.getRandomImage(question), question.english);
                break;
            
            case 'english-text':
                UI.showTextQuestion(this.getRandomEnglishText(question));
                break;
            
            case 'welsh-text':
                UI.showTextQuestion(this.getRandomWelshText(question));
                break;
            
            case 'english-audio':
                UI.showAudioQuestion(() => this.playQuestionAudio());
                // Auto-play audio after a short delay
                setTimeout(() => this.playQuestionAudio(), 300);
                break;
            
            case 'welsh-audio':
                UI.showAudioQuestion(() => this.playQuestionAudio());
                // Auto-play audio after a short delay
                setTimeout(() => this.playQuestionAudio(), 300);
                break;
        }
    },
    
    /**
     * Show question for standard modes
     * @param {Object} question - The question object
     */
    showStandardQuestion(question) {
        switch (this.state.mode) {
            case 'image-to-welsh':
                UI.showImageQuestion(this.getRandomImage(question), question.english);
                break;
                
            case 'english-to-welsh':
                UI.showTextQuestion(this.getRandomEnglishText(question));
                break;
                
            case 'welsh-to-english':
                UI.showTextQuestion(this.getRandomWelshText(question));
                break;
                
            case 'audio-to-welsh':
                UI.showAudioQuestion(() => this.playQuestionAudio());
                // Auto-play audio after a short delay
                setTimeout(() => this.playQuestionAudio(), 300);
                break;
                
            case 'welsh-audio-to-english':
                UI.showAudioQuestion(() => this.playQuestionAudio());
                // Auto-play audio after a short delay
                setTimeout(() => this.playQuestionAudio(), 300);
                break;
        }
    },
    
    /**
     * Generate answer options for the current question
     */
    generateOptions() {
        // Determine number of options based on difficulty slider
        const numOptions = this.state.difficulty;
        
        // Create array with correct answer
        const options = [this.state.correctAnswer];
        
        // Add random incorrect options
        const availableOptions = vocabularyItems.filter(item => item.id !== this.state.correctAnswer.id);
        const shuffledOptions = shuffleArray(availableOptions);
        options.push(...shuffledOptions.slice(0, numOptions - 1));
        
        // Shuffle all options
        const shuffledAllOptions = shuffleArray(options);
        
        // Determine answer type
        let answerType = '';
        if (this.state.mode === 'mixed') {
            answerType = this.state.correctAnswer.answerType;
        } else {
            // Set answer type based on standard mode
            switch (this.state.mode) {
                case 'image-to-welsh':
                case 'english-to-welsh':
                case 'audio-to-welsh':
                    answerType = 'welsh-text';
                    break;
                case 'welsh-to-english':
                case 'welsh-audio-to-english':
                    answerType = 'english-text';
                    break;
            }
        }
        
        // Generate options in UI
        UI.generateOptions(shuffledAllOptions, answerType, (optionEl, option) => this.selectOption(optionEl, option));
    },
    
    /**
     * Handle option selection
     * @param {HTMLElement} optionElement - The selected option element
     * @param {Object} selectedOption - The data for the selected option
     */
    selectOption(optionElement, selectedOption) {
        // Ignore if already answered
        if (this.state.selectedOption !== null) {
            return;
        }
        
        // Set selected option
        this.state.selectedOption = selectedOption;
        
        // Determine answer type
        let answerType = '';
        if (this.state.mode === 'mixed') {
            answerType = this.state.correctAnswer.answerType;
        } else {
            // Set answer type based on standard mode
            switch (this.state.mode) {
                case 'image-to-welsh':
                case 'english-to-welsh':
                case 'audio-to-welsh':
                    answerType = 'welsh-text';
                    break;
                case 'welsh-to-english':
                case 'welsh-audio-to-english':
                    answerType = 'english-text';
                    break;
            }
        }
        
        // Mark option and check if correct
        this.state.answeredCorrectly = UI.markOption(
            optionElement, 
            selectedOption, 
            this.state.correctAnswer.id, 
            answerType
        );
        
        // Update score if correct
        if (this.state.answeredCorrectly) {
            this.state.score++;
            UI.updateProgress(this.state.currentQuestionIndex + 1, this.state.questionCount, this.state.score);
        }
        
        // Short delay before moving to next question
        setTimeout(() => {
            this.nextQuestion();
        }, 700); // 700ms delay to show the answer
    },
    
    /**
     * Move to the next question or end the game
     */
    nextQuestion() {
        // Move to next question
        this.state.currentQuestionIndex++;
        
        if (this.state.currentQuestionIndex >= this.state.questions.length) {
            this.endGame();
        } else {
            this.showQuestion();
        }
    },
    
    /**
     * End the game and show results
     */
    endGame() {
        // Stop the timer
        const finalTime = this.stopTimer();
        
        // Update UI
        UI.showResultScreen();
        UI.updateResults(this.state.score, this.state.questions.length, finalTime);
        
        // Set game complete
        this.state.gameComplete = true;
    },
    
    /**
     * Start the timer
     */
    startTimer() {
        this.state.startTime = new Date();
        
        this.state.timerInterval = setInterval(() => {
            const now = new Date();
            const elapsedMs = now - this.state.startTime;
            const time = formatTime(elapsedMs);
            
            UI.updateTimer(time);
        }, 100);
    },
    
    /**
     * Stop the timer
     * @returns {Object} Formatted time object
     */
    stopTimer() {
        clearInterval(this.state.timerInterval);
        this.state.endTime = new Date();
        
        // Calculate total time
        const totalMs = this.state.endTime - this.state.startTime;
        return formatTime(totalMs);
    },
    
    /**
     * Play question audio
     */
    playQuestionAudio() {
        // Prevent multiple simultaneous playbacks
        if (this.state.isAudioPlaying) {
            return;
        }
        
        // Get the appropriate audio file and play it
        let audioPath;
        
        if (this.state.mode === 'mixed') {
            const questionType = this.state.correctAnswer.questionType;
            
            if (questionType === 'english-audio') {
                audioPath = this.getRandomEnglishAudio(this.state.correctAnswer);
                console.log('Playing English audio:', audioPath);
            } else if (questionType === 'welsh-audio') {
                audioPath = this.getRandomWelshAudio(this.state.correctAnswer);
                console.log('Playing Welsh audio:', audioPath);
            }
        } else {
            if (this.state.mode === 'audio-to-welsh') {
                audioPath = this.getRandomEnglishAudio(this.state.correctAnswer);
                console.log('Playing English audio:', audioPath);
            } else if (this.state.mode === 'welsh-audio-to-english') {
                audioPath = this.getRandomWelshAudio(this.state.correctAnswer);
                console.log('Playing Welsh audio:', audioPath);
            }
        }
        
        // Play the audio if we found a path
        if (audioPath) {
            try {
                this.state.isAudioPlaying = true;
                const audio = new Audio(audioPath);
                
                // Add event listener to reset the flag when audio ends
                audio.addEventListener('ended', () => {
                    this.state.isAudioPlaying = false;
                });
                
                // Add event listener to reset the flag if there's an error
                audio.addEventListener('error', () => {
                    console.error('Error playing audio');
                    this.state.isAudioPlaying = false;
                });
                
                audio.play().catch(err => {
                    console.error('Error playing audio:', err);
                    this.state.isAudioPlaying = false;
                });
            } catch (error) {
                console.error('Error creating audio player:', error);
                this.state.isAudioPlaying = false;
            }
        }
    }
};