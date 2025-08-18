/** @format */

let intervalId = null;
let running = false;

function getRandomInterval(base) {
  const variance = 6000; // ±6 seconds in ms
  return base + (Math.random() * 2 - 1) * variance;
}

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
    await fetch("http://3.138.111.254:8000/listings", {
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
    // Wait 2 seconds for reload to finish
    setTimeout(async () => {
      const result = await getListings(tab.id);
      const listings = result[0].result;
      await sendListingsToBackend(listings);
    }, 2000);
  } catch (error) {
    console.error("Error in refreshAndSend:", error);
  }
}

const startBtn = document.getElementById("startButton");
const stopBtn = document.getElementById("stopButton");
const intervalInput = document.getElementById("interval");

function setButtonStates(runningState) {
  startBtn.disabled = runningState;
  stopBtn.disabled = !runningState;
}

setButtonStates(false); // Initial state: start enabled, stop disabled

async function startRefreshing() {
  const baseInterval = parseInt(intervalInput.value, 10) * 1000;
  if (running) return;

  running = true;
  setButtonStates(true);

  async function loop() {
    if (!running) return;
    await refreshAndSend();
    if (!running) return;
    const nextInterval = getRandomInterval(baseInterval);
    intervalId = setTimeout(loop, nextInterval);
  }

  loop();
}

startBtn.addEventListener("click", startRefreshing);

stopBtn.addEventListener("click", () => {
  running = false;
  if (intervalId) {
    clearTimeout(intervalId);
    intervalId = null;
  }
  setButtonStates(false);
});

intervalInput.addEventListener("input", () => {
  if (!running) {
    setButtonStates(false);
  }
});
