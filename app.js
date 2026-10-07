const express = require('express');
const multer = require('multer');
const pdfParse = require('pdf-parse');
const mammoth = require('mammoth');
const http = require('http');

const app = express();
app.use(express.json());
app.use(express.static('public'));

const profiles = [];


// Configure multer
const storage = multer.memoryStorage();
const upload = multer({
  storage,
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedMimeTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ];
    
    if (allowedMimeTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only PDF and DOCX are allowed.'), false);
    }
  }
});

// Extractor middleware/handler
app.post('/extract', (req, res) => {
  upload.single('cv')(req, res, async (err) => {
    if (err instanceof multer.MulterError) {
      if (err.code === 'LIMIT_FILE_SIZE') {
        return res.status(400).json({ error: 'File is too large. Max size is 5MB.' });
      }
      return res.status(400).json({ error: err.message });
    } else if (err) {
      return res.status(400).json({ error: err.message });
    }

    if (!req.file) {
      return res.status(400).json({ error: 'No file provided.' });
    }

    try {
      let extractedText = '';

      if (req.file.mimetype === 'application/pdf') {
        const data = await pdfParse(req.file.buffer);
        extractedText = data.text;
      } else if (req.file.mimetype === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        const result = await mammoth.extractRawText({ buffer: req.file.buffer });
        extractedText = result.value;
      }

      res.status(200).json({ text: extractedText });
    } catch (error) {
      console.error('Extraction error:', error);
      res.status(500).json({ error: 'Failed to extract text from the file.' });
    }
  });
});

app.post('/parse', (req, res) => {
  const text = req.body.text;
  if (!text) {
    return res.status(400).json({ error: 'No text provided' });
  }

  const postData = JSON.stringify({ text });
  const options = {
    hostname: 'localhost',
    port: 8000,
    path: '/parse',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  const pythonReq = http.request(options, (pythonRes) => {
    let data = '';
    pythonRes.on('data', (chunk) => { data += chunk; });
    pythonRes.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        res.status(pythonRes.statusCode).json(parsed);
      } catch (e) {
        res.status(500).json({ error: 'Invalid response from NLP service' });
      }
    });
  });

  pythonReq.on('error', (e) => {
    console.error(`Problem with NLP request: ${e.message}`);
    res.status(500).json({ error: 'Failed to connect to NLP service' });
  });

  pythonReq.write(postData);
  pythonReq.end();
});

app.post('/profile', (req, res) => {
  const profile = req.body;
  if (!profile.name && !profile.email) {
    return res.status(400).json({ error: 'Profile must have at least a name or email' });
  }
  
  profile.id = profiles.length + 1;
  profiles.push(profile);
  
  res.status(201).json({ message: 'Profile saved successfully', profile });
});

app.get('/profiles', (req, res) => {
  res.status(200).json(profiles);
});


module.exports = app;
