import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Blocks from './components/Blocks';
import Transactions from './components/Transactions';
import Accounts from './components/Accounts';

const App = () => {
    return (
        <Router>
            <div>
                <h1>Blockchain Explorer</h1>
                <Switch>
                    <Route exact path="/" component={Blocks} />
                    <Route path="/transactions" component={Transactions} />
                    <Route path="/accounts" component={Accounts} />
                </Switch>
            </div>
        </Router>
    );
};

export default App;
