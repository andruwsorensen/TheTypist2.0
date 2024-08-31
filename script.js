// ==UserScript==
// @name         DOM Extract and Simulate Typing with reCAPTCHA Position Sending
// @namespace    http://tampermonkey.net/
// @version      0.6
// @description  Extracts data from the DOM, simulates typing it into an input field, and sends reCAPTCHA position to a server
// @author       Alpine Gingy
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const url = 'http://127.0.0.1:5000/type';
    const urlNext = 'http://127.0.0.1:5000/next';
    const urlPause = 'http://127.0.0.1:5000/pause';
    const urlClick = 'http://127.0.0.1:5000/click'; // URL to send captcha position to

    // Function to find reCAPTCHA iframe
    function findReCaptchaIframe() {
        return document.querySelector('iframe[title*="recaptcha" i]');
    }

    // Function to click elements when they appear on the screen and send position to the server
    function clickWhenElementAppears(selector, isCaptcha) {
        const observer = new MutationObserver((mutationsList, observer) => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList' || mutation.type === 'subtree') {
                    let element;
                    if (isCaptcha) {
                        element = findReCaptchaIframe();
                    } else {
                        element = document.querySelector(selector);
                    }
                    if (element && element.offsetParent !== null) { // Check if the element is visible
                        if (isCaptcha) {
                            setTimeout( () => {
                                const elementPosition = getElementPosition(element);
                                if (elementPosition) {
                                    sendPositionToServer(elementPosition);
                                }
                                console.log(`Detected reCAPTCHA iframe at position:`, elementPosition);
                            }, 100);
                            setTimeout( () => {
                                location.reload()
                            }, 5000);
                        } else {
                            element.click();
                        }
                        observer.disconnect();
                    }
                }
            }
        });

        // Start observing the document body or a specific element
        observer.observe(document.body, { childList: true, subtree: true });
    }

    function getElementPosition(element) {
        if (element) {
            const rect = element.getBoundingClientRect();
            return { x: rect.left + window.scrollX, y: rect.top + window.scrollY };
        }
        return null;
    }

    // Function to send the position to the server
    function sendPositionToServer(position) {
        fetch(urlClick, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(position)
        })
        .then(response => response.text())
        .then(data => console.log('Position sent:', data))
        .catch(error => console.error('Error:', error));
    }

    // Function to start typing when the class "is-racing" appears
    function startTypingWhenClassAppears(className) {
        const observer = new MutationObserver((mutationsList, observer) => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const targetElement = mutation.target;
                    if (targetElement.classList.contains(className)) {
                        observer.disconnect(); // Stop observing once the class is detected
                        extractAndSendText(); // Start typing simulation
                        nextScreen('is-race-results'); // Call nextScreen with the appropriate class
                        break;
                    }
                }
            }
        });

        // Start observing the document body or a specific element
        observer.observe(document.body, { attributes: true, subtree: true });
    }

    // Function to extract text and send it to the server
    function extractAndSendText() {
        let text = Array.from(document.querySelectorAll('span.dash-letter')).map(span => span.textContent);
        text = text.join('');

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }

    // Function to handle moving to the next screen
    function nextScreen(className) {
        const observer = new MutationObserver((mutationsList, observer) => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const targetElement = mutation.target;
                    if (targetElement.classList.contains(className)) {
                        observer.disconnect(); // Stop observing once the class is detected
                        // Send a POST request to the server
                        fetch(urlNext, {
                            method: 'POST'
                        })
                        .then(response => response.text())
                        .then(data => console.log('Next action triggered:', data))
                        .catch(error => console.error('Error:', error));
                        break;
                    }
                }
            }
        });

        // Start observing the document body or a specific element
        observer.observe(document.body, { attributes: true, subtree: true });
    }

    // Detect when the tab visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            // Tab is inactive or hidden
            fetch(urlPause, {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => console.log('Typing paused:', data))
            .catch(error => console.error('Error:', error));
        }
    });

    // Start watching for the "is-racing" class to appear
    startTypingWhenClassAppears('is-racing');

    // Watch for the appearance of the reCAPTCHA iframe and send its position
    clickWhenElementAppears(null, true);

    clickWhenElementAppears('.daily-challenge-completed-notification--cta.btn.btn--tertiary', false);

    clickWhenElementAppears('.racev3Pre-action.btn.btn--fw.btn--primary', false);

    // Test click in garage
    //clickWhenElementAppears('.season-reward-mini-previewImg', false);
})();