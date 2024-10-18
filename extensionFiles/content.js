// Function to hide blocked accounts' parent article by finding the correct parent element
function hideBlockedUser(username) {
    document.querySelectorAll(`span.css-1jxf684`).forEach(span => {
        if (span.textContent === username) {
            // Find the closest article element with data-testid="tweet"
            const parentArticle = span.closest('article[data-testid="tweet"]');
            if (parentArticle) {
                parentArticle.style.display = 'none';  // Method 1: display none
                parentArticle.setAttribute('hidden', 'true');  // Method 2: hidden attribute
                parentArticle.style.visibility = 'hidden';  // Method 3: visibility hidden
                parentArticle.style.opacity = '0';  // Method 4: opacity 0
            }
        }
    });
}

// Function to remove a user from the cached blocklist
function removeUserFromCache(username) {
    let cachedBlocklist = JSON.parse(localStorage.getItem('blockedAccounts') || "[]");

    if (cachedBlocklist.includes(username)) {
        cachedBlocklist = cachedBlocklist.filter(user => user !== username);
        
        // Update the cached blocklist in localStorage
        localStorage.setItem('blockedAccounts', JSON.stringify(cachedBlocklist));
    }
}

// Function to hide all blocked users on page load
function hideAllBlockedUsers(blockedAccounts) {
    blockedAccounts.forEach(username => hideBlockedUser(username));
}

// Monitor the page for dynamically loaded content
function observeDOMChanges(blockedAccounts) {
    const observer = new MutationObserver(() => {
        hideAllBlockedUsers(blockedAccounts);
    });

    // Start observing the entire document for changes (new posts being loaded)
    observer.observe(document.body, { childList: true, subtree: true });
}

// Fetch blocked users from the JSON file within the extension
async function loadBlockedAccounts() {
    try {
        const response = await fetch(browser.runtime.getURL('blocked_users.json'));
        if (!response.ok) {
            throw new Error(`Failed to fetch blocked users: ${response.statusText}`);
        }
        const blockedAccounts = await response.json();
        return blockedAccounts;
    } catch (error) {
        console.error("Error loading blocked accounts:", error);
        return [];
    }
}

// Compare cached blocklist with the file and update if there are new names
async function compareCacheAndFile() {
    const cachedBlocklist = JSON.parse(localStorage.getItem('blockedAccounts') || "[]");
    const fileBlocklist = await loadBlockedAccounts();

    const newUsernames = fileBlocklist.filter(username => !cachedBlocklist.includes(username));

    if (newUsernames.length > 0) {
        const updatedBlocklist = [...new Set([...cachedBlocklist, ...newUsernames])];
        localStorage.setItem('blockedAccounts', JSON.stringify(updatedBlocklist));
        return updatedBlocklist;
    } else {
        return cachedBlocklist;
    }
}

// Initialize the process
function init() {
    compareCacheAndFile().then(blockedAccounts => {
        hideAllBlockedUsers(blockedAccounts);  // Hide blocked users on page load
        observeDOMChanges(blockedAccounts);    // Observe DOM changes for dynamically loaded content
    });
}

// Example usage: removeUserFromCache('@exampleUser');
init();
