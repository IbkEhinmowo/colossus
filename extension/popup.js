/** @format */

let intervalId = null;

function getListings(tabId) {
  return chrome.scripting.executeScript({
    target: { tabId },
    function: () => {
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
      const anchors = document.querySelectorAll(
        'a[href*="/marketplace/item/"]'
      );
      return Array.from(anchors).map((a) => {
        const href = a.getAttribute("href");
        let output = [`<a href="${href}"></a>`];
        output = output.concat(getTagWithText(a));
        return output.join("");
      });
    },
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

async function refreshAndSend() {
  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    // Refresh the page
    await chrome.tabs.reload(tab.id);
    // Wait a bit for reload to finish
    setTimeout(async () => {
      const result = await getListings(tab.id);
      const listings = result[0].result;
      await sendListingsToBackend(listings);
    }, 2000); // 2 seconds after reload
  } catch (error) {
    console.error("Error in refreshAndSend:", error);
  }
}

const startBtn = document.getElementById("startButton");
const stopBtn = document.getElementById("stopButton");
const intervalInput = document.getElementById("interval");

function setButtonStates(running) {
  startBtn.disabled = running;
  stopBtn.disabled = !running;
}

setButtonStates(false); // Initial state: Start enabled, Stop disabled

startBtn.addEventListener("click", () => {
  if (intervalId) return;
  const interval = parseInt(intervalInput.value, 10) * 1000;
  setButtonStates(true);
  refreshAndSend();
  intervalId = setInterval(refreshAndSend, interval);
});

stopBtn.addEventListener("click", () => {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
    setButtonStates(false);
  }
});

intervalInput.addEventListener("input", () => {
  if (!intervalId) {
    setButtonStates(false);
  }
});
