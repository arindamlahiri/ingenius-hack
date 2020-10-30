var spawn = require("child_process").spawn; 
var output = []     
    
var process = spawn('python',["app1.py","hello 🚗"]);

process.stdout.on('data', (data) => { 
    output.push(data.toString())
})

process.stdout.on('close', (code) => {
    console.log(output[output.length-1])
})