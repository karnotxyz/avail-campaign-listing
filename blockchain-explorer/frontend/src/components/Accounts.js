import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Accounts = () => {
    const [accounts, setAccounts] = useState([]);

    useEffect(() => {
        axios.get('/api/accounts')
            .then(response => {
                setAccounts(response.data);
            })
            .catch(error => {
                console.error('Error fetching accounts:', error);
            });
    }, []);

    return (
        <div>
            <h2>Accounts</h2>
            <ul>
                {accounts.map(account => (
                    <li key={account.address}>
                        Address: {account.address}, Balance: {account.balance}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Accounts;
