// scripts.js

// Function to run the simulation
function runSimulation() {
    // Get input values
    const pageSequenceInput = document.getElementById('page-sequence').value;
    const cacheSizeInput = document.getElementById('cache-size').value;
    
    // Convert input values to usable data types
    const pageSequence = pageSequenceInput.split(' ').map(Number);
    const cacheSize = parseInt(cacheSizeInput);

    // Initialize the cache and simulation state
    let cache = [];
    let faultCount = 0;
    let currentOperationOutput = [];
    
    // Process each page request
    for (let i = 0; i < pageSequence.length; i++) {
        const page = pageSequence[i];
        
        // Check if the page is already in the cache
        if (cache.includes(page)) {
            // Cache hit: move the page to the most recently used position
            cache = cache.filter(p => p !== page);
            cache.push(page);
        } else {
            // Cache miss: increment fault count
            faultCount++;
            
            // If cache is full, evict the least recently used page
            if (cache.length >= cacheSize) {
                cache.shift();
            }
            
            // Add the new page to the cache
            cache.push(page);
        }

        // After each operation, store the current state of the cache and fault count
        const cacheState = cache.join(', ');
        currentOperationOutput.push(`Operation ${i + 1}: Page Request: ${page}, Cache Memory: [${cacheState}], Fault Count: ${faultCount}`);
    }

    // Display the results
    displayResults(currentOperationOutput, faultCount);
}

// Function to display the results of the simulation
function displayResults(currentOperationOutput, faultCount) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ''; // Clear previous results

    // Display operation output (cache memory state and fault count) after each operation
    currentOperationOutput.forEach(output => {
        const outputDiv = document.createElement('div');
        outputDiv.innerText = output;
        resultDiv.appendChild(outputDiv);
    });

    // Display total page faults
    const faultCountDiv = document.createElement('div');
    faultCountDiv.innerText = `Total Page Faults: ${faultCount}`;
    resultDiv.appendChild(faultCountDiv);
}
