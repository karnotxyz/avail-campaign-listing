import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Blocks = () => {
    const [blocks, setBlocks] = useState([]);

    useEffect(() => {
        axios.get('/api/blocks')
            .then(response => {
                setBlocks(response.data);
            })
            .catch(error => {
                console.error('Error fetching blocks:', error);
            });
    }, []);

    return (
        <div>
            <h2>Blocks</h2>
            <ul>
                {blocks.map(block => (
                    <li key={block.hash}>
                        Block #{block.number} - Hash: {block.hash}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Blocks;
