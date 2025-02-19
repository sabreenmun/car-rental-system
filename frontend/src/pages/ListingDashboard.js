import React, { useEffect } from 'react';
import { useHistory } from 'react-router-dom';

function Dashboard() {
    const history = useHistory();

    useEffect(() => {
        const token = localStorage.getItem("authToken");
        if (!token) {
            history.push("/login"); // Redirect to login if no token is found
        }
    }, [history]);

    return (
        <div className="dashboard">
            <h1>Welcome to the Dashboard!</h1>
            {/* Add dashboard content here */}
        </div>
    );
}

export default Dashboard;
