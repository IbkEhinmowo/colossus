/** @format */

function updateButtonStates(running) {
  document.getElementById("startButton").disabled = running;
  document.getElementById("stopButton").disabled = !running;
}

// Check extension refresh status when popup opens
chrome.runtime.sendMessage({ type: "GET_STATUS" }, (response) => {
  if (chrome.runtime.lastError) {
    console.error("Error getting status:", chrome.runtime.lastError);
    updateButtonStates(false);
  } else if (response && response.running) {
    updateButtonStates(true);
  } else {
    updateButtonStates(false);
  }
});

document.getElementById("startButton").addEventListener("click", () => {
  const interval = parseInt(document.getElementById("interval").value, 10);
  chrome.runtime.sendMessage(
    { type: "START_REFRESH", interval },
    (response) => {
      if (chrome.runtime.lastError) {
        console.error("Error sending START_REFRESH:", chrome.runtime.lastError);
      } else if (response && response.status === "started") {
        updateButtonStates(true);
      } else {
        console.warn("Unexpected response for START_REFRESH:", response);
      }
    }
  );
});

document.getElementById("stopButton").addEventListener("click", () => {
  chrome.runtime.sendMessage({ type: "STOP_REFRESH" }, (response) => {
    if (chrome.runtime.lastError) {
      console.error("Error sending STOP_REFRESH:", chrome.runtime.lastError);
    } else if (response && response.status === "stopped") {
      updateButtonStates(false);
    } else {
      console.warn("Unexpected response for STOP_REFRESH:", response);
    }
  });
});
