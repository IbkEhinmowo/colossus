/** @format */

document
  .getElementById("myButton")
  .addEventListener("click", async function () {
    try {
      const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true,
      });

      const result = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => {
          const anchors = document.querySelectorAll(
            'a[href*="/marketplace/item/"]'
          );
          return Array.from(anchors).map((a) => {
            const text = a.innerText.trim();
            const link =
              "https://www.facebook.com" + a.getAttribute("href").split("?")[0];
            return `${text}  ${link}`;
          });
        },
      });

      const listings = result[0].result;
      console.log("Listings with link:", listings);

      // Optional: send to your Python server
      // fetch("http://localhost:5000/receive", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({ data: listings }),
      // });
    } catch (error) {
      console.error("Error getting listings:", error);
    }
  });
