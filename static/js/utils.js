/**
 * Utility functions for the Welsh vocabulary learning game
 */

/**
 * Get a random item from an array
 * @param {Array} array - The array to select from
 * @returns {*} A random item from the array
 */
function getRandomItem(array) {
    return array[Math.floor(Math.random() * array.length)];
}

/**
 * Shuffle an array using Fisher-Yates algorithm
 * @param {Array} array - The array to shuffle
 * @returns {Array} A new shuffled array
 */
function shuffleArray(array) {
    const newArray = [...array];
    for (let i = newArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
    }
    return newArray;
}

/**
 * Format time in minutes:seconds
 * @param {number} milliseconds - Time in milliseconds
 * @returns {Object} Object containing formatted minutes and seconds
 */
function formatTime(milliseconds) {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    
    return {
        minutes: String(minutes).padStart(2, '0'),
        seconds: String(seconds).padStart(2, '0')
    };
}

/**
 * Check if two arrays have at least one common element
 * @param {Array} array1 - First array
 * @param {Array} array2 - Second array
 * @returns {boolean} True if arrays have at least one common element
 */
function haveCommonElement(array1, array2) {
    return array1.some(item => array2.includes(item));
}

/**
 * Play audio file
 * @param {string} filePath - Path to audio file
 * @returns {Promise} Promise that resolves when audio finishes playing
 */
function playAudio(filePath) {
    return new Promise((resolve, reject) => {
        try {
            const audio = new Audio(filePath);
            audio.addEventListener('ended', resolve);
            audio.addEventListener('error', reject);
            audio.play();
        } catch (error) {
            reject(error);
        }
    });
}
