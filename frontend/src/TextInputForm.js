import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Paper, Box } from '@mui/material';

const TextInputForm = () => {
    const [inputValue, setInputValue] = useState('');
    const [responseHtml, setResponseHtml] = useState('');

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/device/inputis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: inputValue }),
            });
            if (response.ok) {
                const htmlResponse = await response.text();
                setResponseHtml(htmlResponse);
                setInputValue('');
            } else {
                console.error('Failed to submit input');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <Container maxWidth="sm">
            <Paper elevation={3} style={{ padding: '16px', marginTop: '32px' }}>
                <Typography variant="h5" component="h1" gutterBottom>
                    Input Form
                </Typography>
                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Text Input"
                        variant="outlined"
                        fullWidth
                        value={inputValue}
                        onChange={handleInputChange}
                        required
                        style={{ marginBottom: '16px' }}
                    />
                    <Button
                        variant="contained"
                        color="primary"
                        type="submit"
                        fullWidth
                    >
                        Submit
                    </Button>
                </form>
                <Box mt={2}>
                    <Typography variant="h6">Response:</Typography>
                    <div dangerouslySetInnerHTML={{ __html: responseHtml }} />
                </Box>
            </Paper>
        </Container>
    );
};

export default TextInputForm;
