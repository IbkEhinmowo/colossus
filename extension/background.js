/** @format */

let intervalId = null;
let refreshInterval = 60000; // default 60s

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "START_REFRESH") {
    if (intervalId) return;
    refreshInterval = message.interval || 60000;
    runRefreshAndSend();
    intervalId = setInterval(runRefreshAndSend, refreshInterval);
    sendResponse({ status: "started" });
  }
  if (message.type === "STOP_REFRESH") {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
      sendResponse({ status: "stopped" });
    }
  }
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
