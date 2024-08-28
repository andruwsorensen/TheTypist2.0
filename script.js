    // ==UserScript==
    // @name         DOM Extract and Simulate Typing
    // @namespace    http://tampermonkey.net/
    // @version      0.2
    // @description  Extracts data from the DOM and simulates typing it into an input field
    // @author       Your Name
    // @match        *://*/*
    // @grant        none
    // ==/UserScript==

    // click on this recaptcha-checkbox it is a class, maybe just an event would work to click on it
    // also this was not a button it was the other thing
    // then press on this button btn btn--primary btn--fw

    (function() {
        'use strict';

        const url = 'http://127.0.0.1:5000/type';
        const urlNext = 'http://127.0.0.1:5000/next';
        
        const urlPause = 'http://127.0.0.1:5000/pause';

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
                body: JSON.stringify({ text: text})
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
    })();
