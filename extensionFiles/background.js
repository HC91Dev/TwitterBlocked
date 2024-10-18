// Listener for messages from content scripts and popup
browser.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("Received message:", request); // Debug log

    if (request.action === "getBlockedUsers") {
        const blockedUsers = localStorage.getItem("blockedAccounts");
        console.log("Blocked users from localStorage:", blockedUsers); // Debug log

        if (blockedUsers) {
            sendResponse({ users: JSON.parse(blockedUsers) });
        } else {
            sendResponse({ users: [] });
        }
    } 
    
    else if (request.action === "clearCache") {
        // Clear localStorage in the background context
        console.log("Clearing blocklist cache in background script...");
        localStorage.removeItem('blockedAccounts'); // Clear cache

        // Respond back to the popup or content script to confirm cache was cleared
        sendResponse({ success: true });
    }

    return true; // Keep the message channel open for asynchronous responses
});

// Example of using alarms to run periodic tasks
browser.alarms.create("periodicCheck", { periodInMinutes: 5 });

browser.alarms.onAlarm.addListener(alarm => {
    if (alarm.name === "periodicCheck") {
        console.log("Running periodic check...");
        // Perform periodic background tasks, e.g., refreshing blocklist
    }
});

// Example of reacting to browser events
browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url.includes('x.com')) {
        console.log('Twitter page loaded, checking for blocked users...');
        // You can trigger content scripts or run some logic here
    }
});
