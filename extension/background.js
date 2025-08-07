/** @format */

// Background service worker initialized
console.log("Background service worker started");
// Handle start/stop messages by creating or clearing alarms
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Received message:", message);
  if (message.type === "START_REFRESH") {
    const intervalSec = message.interval || 60;
    // Save interval for scheduling
    chrome.storage.local.set({ refreshIntervalSec: intervalSec });
    // Immediate refresh
    runRefreshAndSend();
    // Schedule next alarm at intervalSec seconds
    chrome.alarms.create("refreshMarketplace", {
      when: Date.now() + intervalSec * 1000,
    });
    sendResponse({ status: "started" });
  } else if (message.type === "STOP_REFRESH") {
    chrome.alarms.clear("refreshMarketplace", (wasCleared) => {
      sendResponse({ status: wasCleared ? "stopped" : "none" });
    });
    return true; // will respond asynchronously
    return true; // will respond asynchronously
  } else if (message.type === "GET_STATUS") {
    // Check if an alarm exists
    chrome.alarms.get("refreshMarketplace", (alarm) => {
      sendResponse({ running: !!alarm });
    });
    return true; // will respond asynchronously
  }
  // For async sendResponse in STOP_REFRESH and GET_STATUS, return true is implicit after those cases
});
// Message handler for start, stop, and status
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "START_REFRESH") {
    const intervalSec = message.interval || 60;
    // Clear existing alarms, run immediate, and schedule periodic alarm
    chrome.alarms.clear("refreshMarketplace", () => {
      runRefreshAndSend();
      const periodMin = intervalSec / 60;
      chrome.alarms.create("refreshMarketplace", {
        periodInMinutes: periodMin,
      });
      sendResponse({ status: "started" });
    });
    return true; // will respond asynchronously
  }
  if (message.type === "STOP_REFRESH") {
    chrome.alarms.clear("refreshMarketplace", (wasCleared) => {
      sendResponse({ status: wasCleared ? "stopped" : "none" });
    });
    return true; // will respond asynchronously
  }
  if (message.type === "GET_STATUS") {
    chrome.alarms.get("refreshMarketplace", (alarm) => {
      sendResponse({ running: !!alarm });
    });
    return true; // will respond asynchronously
  }
  return false;
});

function runRefreshAndSend() {
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    if (!tabs.length) return;
    const tab = tabs[0];
    chrome.tabs.reload(tab.id, {}, () => {
      setTimeout(() => {
        chrome.scripting.executeScript(
          {
            target: { tabId: tab.id },
            func: getListingsScript,
          },
          async (results) => {
            if (results && results[0] && results[0].result) {
              await sendListingsToBackend(results[0].result);
            }
          }
        );
      }, 2000);
    });
  });
}
// Trigger refresh when alarm fires
// Handle alarm trigger and schedule next one
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "refreshMarketplace") {
    runRefreshAndSend();
    // Reschedule next alarm based on saved interval
    chrome.storage.local.get("refreshIntervalSec", (data) => {
      const interval = data.refreshIntervalSec || 60;
      chrome.alarms.create("refreshMarketplace", {
        when: Date.now() + interval * 1000,
      });
    });
  }
});
// Trigger refresh on periodic alarm
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "refreshMarketplace") {
    runRefreshAndSend();
  }
});

function getListingsScript() {
  function getTagWithText(node) {
    let results = [];
    if (node.nodeType === Node.ELEMENT_NODE) {
      const hasElementChild = Array.from(node.childNodes).some(
        (n) => n.nodeType === Node.ELEMENT_NODE
      );
      if (!hasElementChild && node.textContent.trim()) {
        const tag = node.tagName.toLowerCase();
        if (tag === "a") {
          const href = node.getAttribute("href");
          results.push(`<a href="${href}">${node.textContent.trim()}</a>`);
        } else {
          results.push(`<${tag}>${node.textContent.trim()}</${tag}>`);
        }
      } else {
        node.childNodes.forEach((child) => {
          results = results.concat(getTagWithText(child));
        });
      }
    }
    return results;
  }
  const anchors = document.querySelectorAll('a[href*="/marketplace/item/"]');
  return Array.from(anchors).map((a) => {
    const href = a.getAttribute("href");
    let output = [`<a href="${href}"></a>`];
    output = output.concat(getTagWithText(a));
    return output.join("");
  });
}

async function sendListingsToBackend(listings) {
  try {
    await fetch("http://127.0.0.1:8000/listings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ listings }),
    });
  } catch (error) {
    console.error("Error sending listings:", error);
  }
}
