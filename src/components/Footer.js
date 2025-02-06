import React from 'react';
import './Footer.css';

function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p>© 2025 DriveConnect Solutions. All rights reserved.</p>
                <div className="footer-links">
                    <a href="/about">About Us</a>
                    <a href="/contact">Contact</a>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
