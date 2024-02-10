const express = require('express');
const axios = require('axios');
const app = express();
const port = 5000;

// API routes
app.get('/api/blocks', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:9944/blocks');
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching blocks:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/api/transactions', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:9944/transactions');
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching transactions:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/api/accounts', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:9944/accounts');
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching accounts:', error);
        res.status(500).send('Internal Server Error');
    }
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
