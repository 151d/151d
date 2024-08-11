const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(express.static('public'));

app.post('/reset-computer', (req, res) => {
    exec('shutdown /r /t 0', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.json({ success: false, error: error.message });
        }
        console.log(`stdout: ${stdout}`);
        console.log(`stderr: ${stderr}`);
        res.json({ success: true });
    });
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
