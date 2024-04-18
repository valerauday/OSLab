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
    let history = [];

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

        // Record the state of the cache at this point in time
        history.push([...cache]);
    }

    // Display the simulation results
    displayResults(currentOperationOutput, faultCount, history, cacheSize);
}

// Function to display the results of the simulation
function displayResults(currentOperationOutput, faultCount, history, cacheSize) {
    const resultDiv = document.getElementById('result');
    const operationsOutputDiv = document.getElementById('operations-output');
    const chartDiv = document.getElementById('gantt-chart');

    // Clear previous results
    operationsOutputDiv.innerHTML = '';
    chartDiv.innerHTML = '';

    // Display operation output (cache memory state and fault count) after each operation
    currentOperationOutput.forEach(output => {
        const outputDiv = document.createElement('div');
        outputDiv.innerText = output;
        operationsOutputDiv.appendChild(outputDiv);
    });

    // Display total page faults
    const faultCountDiv = document.createElement('div');
    faultCountDiv.innerText = `Total Page Faults: ${faultCount}`;
    operationsOutputDiv.appendChild(faultCountDiv);

    // Create the Gantt chart using Plotly
    createGanttChart(history, chartDiv, cacheSize);
}

// Function to create a Gantt chart using Plotly
function createGanttChart(history, chartDiv, cacheSize) {
    // Prepare data for the Gantt chart
    const data = [];
    const pageColors = {}; // Dictionary to map pages to colors

    // Generate a color palette for different pages
    const generateColor = (() => {
        const colors = [
            '#FF5733', '#33FF57', '#3357FF', '#FF33F6', '#FFC433',
            '#33FFF5', '#8D33FF', '#FF8F33', '#33FFBD', '#FFC0CB'
        ];
        let colorIndex = 0;
        return () => colors[colorIndex++ % colors.length];
    })();

    // Create a dictionary to store the page colors
    const getPageColor = (page) => {
        if (!pageColors[page]) {
            pageColors[page] = generateColor();
        }
        return pageColors[page];
    };

    // Create a bar for each page in each time step
    for (let time = 0; time < history.length; time++) {
        const cacheState = history[time];
        
        // Iterate through each cache slot
        for (let slot = 0; slot < cacheState.length; slot++) {
            const page = cacheState[slot];
            
            // Add a trace for each page request
            data.push({
                x: [time, time + 1],
                y: [slot + 1, slot + 1],
                mode: 'lines',
                line: {
                    color: getPageColor(page),
                    width: 10
                },
                name: `Page ${page}` // Add name for each page request as a legend
            });
        }
    }

    // Plot the Gantt chart using Plotly
    Plotly.newPlot(chartDiv, data, {
        title: 'Cache Memory Allocation Over Time',
        xaxis: {
            title: 'Operation Number',
            showgrid: false,
            zeroline: false
        },
        yaxis: {
            title: 'Cache Slot',
            showgrid: false,
            zeroline: false
        },
        showlegend: true // Enable the legend
    });
}

// Attach an event listener to the "Run Simulation" button
document.getElementById('run-btn').addEventListener('click', runSimulation);
