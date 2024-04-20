// Global variables to keep track of processes and state
let readingProcesses = [];
let writingProcesses = [];
let processId = 1;

// Function to update log
function updateLog(message) {
  const log = document.getElementById('log');
  log.innerHTML += `<p>${message}</p>`;
  log.scrollTop = log.scrollHeight; // Scroll to bottom
}

// Function to start reading process
function startReading() {
  if (writingProcesses.length === 0) {
    const id = processId++;
    readingProcesses.push(id);
    updateLog(`Reading Process ${id} started`);
  } else {
    updateLog(`Cannot start reading while a writing process is active`);
  }
}

// Function to stop reading process
function stopReading(id) {
  const index = readingProcesses.indexOf(id);
  if (index !== -1) {
    readingProcesses.splice(index, 1);
    updateLog(`Reading Process ${id} stopped`);
  } else {
    updateLog(`No such reading process with ID ${id} is currently running`);
  }
}

// Function to start writing process
function startWriting() {
  if (readingProcesses.length === 0 && writingProcesses.length === 0) {
    const id = processId++;
    writingProcesses.push(id);
    updateLog(`Writing Process ${id} started`);
  } else {
    updateLog(`Cannot start writing while reading or another writing process is active`);
  }
}

// Function to stop writing process
function stopWriting(id) {
  const index = writingProcesses.indexOf(id);
  if (index !== -1) {
    writingProcesses.splice(index, 1);
    updateLog(`Writing Process ${id} stopped`);
  } else {
    updateLog(`No such writing process with ID ${id} is currently running`);
  }
}

// Function to stop any process
function stopProcess(id) {
  stopReading(id);
  stopWriting(id);
}

// Function to stop all processes
function stopAllProcesses() {
  readingProcesses = [];
  writingProcesses = [];
  updateLog(`All processes stopped`);
}

// Function to show ongoing processes
function showOngoingProcesses() {
  const ongoingProcesses = [...readingProcesses, ...writingProcesses];
  if (ongoingProcesses.length > 0) {
    updateLog(`Ongoing Processes: ${ongoingProcesses.join(', ')}`);
  } else {
    updateLog(`No ongoing processes.`);
  }
}

// Event listeners for buttons
document.getElementById('startReading').addEventListener('click', startReading);

document.getElementById('startWriting').addEventListener('click', startWriting);

// Event listener for the stop button
document.getElementById('stop').addEventListener('click', function() {
    if (readingProcesses.length === 1 && writingProcesses.length === 0) {
      // Case 1: Only one process is running
      const id = readingProcesses.pop();
      updateLog(`Reading Process ${id} stopped`);
    } else if (readingProcesses.length > 1) {
      // Case 2: Multiple reading processes are running
      const input = prompt("Multiple reading processes are running. Enter the ID of the process to stop or type 'all' to stop all processes:");
      if (input && input.toLowerCase() === 'all') {
        stopAllProcesses();
      } else {
        const id = parseInt(input);
        if (!isNaN(id)) {
          stopReading(id);
        }
      }
    } else if (readingProcesses.length === 0 && writingProcesses.length === 0) {
      // Case 3: No process is running currently
      alert("No process running");
    } else if (writingProcesses.length === 1 && readingProcesses.length === 0) {
      // Case 4: Only one writing process is running
      const id = writingProcesses.pop();
      updateLog(`Writing Process ${id} stopped`);
    }
  });
  

document.getElementById('showProcesses').addEventListener('click', showOngoingProcesses);
