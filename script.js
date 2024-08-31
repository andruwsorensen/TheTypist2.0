// ==UserScript==
// @name         DOM Extract and Simulate Typing with reCAPTCHA Position Sending
// @namespace    http://tampermonkey.net/
// @version      0.8
// @description  Extracts data from the DOM, simulates typing it into an input field, and sends reCAPTCHA position to a server
// @author       Alpine Gingy
// @match        https://www.nitrotype.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const url = 'http://127.0.0.1:5000/type';
    const urlNext = 'http://127.0.0.1:5000/next';
    const urlPause = 'http://127.0.0.1:5000/pause';
    const urlClick = 'http://127.0.0.1:5000/click';
    const urlTrack = 'http://127.0.0.1:5000/track';

    function findReCaptchaIframe() {
        return document.querySelector('iframe[title*="recaptcha" i]');
    }

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
                    if (element && element.offsetParent !== null) {
                        if (isCaptcha) {
                            setTimeout(() => {
                                const elementPosition = getElementPosition(element);
                                if (elementPosition) {
                                    sendPositionToServer(elementPosition);
                                }
                                console.log(`Detected reCAPTCHA iframe at position:`, elementPosition);
                            }, 100);
                            setTimeout(() => {
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

        observer.observe(document.body, { childList: true, subtree: true });
    }

    function getElementPosition(element) {
        if (element) {
            const rect = element.getBoundingClientRect();
            return { x: rect.left + window.scrollX, y: rect.top + window.scrollY };
        }
        return null;
    }

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

    function startTypingWhenClassAppears(className) {
        const observer = new MutationObserver((mutationsList, observer) => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const targetElement = mutation.target;
                    if (targetElement.classList.contains(className)) {
                        observer.disconnect();
                        extractAndSendText();
                        nextScreen('is-race-results');
                        break;
                    }
                }
            }
        });

        observer.observe(document.body, { attributes: true, subtree: true });
    }

    function extractAndSendText() {
        let text = Array.from(document.querySelectorAll('span.dash-letter')).map(span => span.textContent);
        text = text.join('');
        console.log(text);
        if (text.length == 0) {
            text = '1';
        }

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

    function nextScreen(className) {
        const observer = new MutationObserver((mutationsList, observer) => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const targetElement = mutation.target;
                    if (targetElement.classList.contains(className)) {
                        observer.disconnect();
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

        observer.observe(document.body, { attributes: true, subtree: true });
    }

    function detectTrackClass() {
        function checkForTrackClass() {
            const trackElement = document.querySelector('.racev3-track');
            if (trackElement) {
                console.log('Track class detected on page load');
                fetch(urlTrack, {
                    method: 'POST'
                })
                .then(response => response.text())
                .then(data => console.log('Track detected:', data))
                .catch(error => console.error('Error:', error));
            }
        }

        // Start checking when the DOM is fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', checkForTrackClass);
        } else {
            checkForTrackClass();
        }
    }

    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            fetch(urlPause, {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => console.log('Typing paused:', data))
            .catch(error => console.error('Error:', error));
        }
    });

    startTypingWhenClassAppears('is-racing');
    clickWhenElementAppears(null, true);
    clickWhenElementAppears('.daily-challenge-completed-notification--cta.btn.btn--tertiary', false);
    clickWhenElementAppears('.racev3Pre-action.btn.btn--fw.btn--primary', false);
    detectTrackClass();
})();