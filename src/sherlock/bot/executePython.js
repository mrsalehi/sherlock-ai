const { spawn } = require('child_process');

// Define the command and argument for the Python script
const pythonScript = '../main.py';

function executePython(query) {
    return new Promise((res) => {
        // Spawn the Python script process with the argument
        const pythonProcess = spawn('python', [pythonScript, "--query", query])


        // Handle the output from the Python script
        pythonProcess.stdout.on('data', (data) => {
            // Handle the output as needed
            console.log(`Python script output: ${data}`);
            res(data.toString())
        });

        // Handle errors that may occur during execution
        pythonProcess.on('error', (err) => {
            console.error('Failed to start Python script:', err);
        });

        // Handle the process exit event
        pythonProcess.on('close', (code) => {
            console.log(`Python script process exited with code ${code}`);
        });
    })
}

// executePython("What is langchain?", (data) => console.log(data.toString()))

module.exports = {
    executePython
}