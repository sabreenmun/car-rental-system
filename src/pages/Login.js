import React from 'react';
import { NavLink } from "react-router-dom";
import "./Login.css";

function Login() {
    return (
        <div className="login-page">
            <form className="form" id="login">
                <h1 className="form-title">Login</h1>
                <label>
                    <input type="email" name="email" placeholder="Email" />
                </label>
                <br />
                <label>
                    <input type="password" name="password" placeholder="Password" />
                </label>
                <br />
                <button type="submit">Continue</button>
                <NavLink to="/register">Don't have an account? Create one</NavLink>
            </form>
        </div>
    );
}

export default Login;
