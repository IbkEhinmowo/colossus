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
          function getTagWithText(node) {
            let results = [];
            if (node.nodeType === Node.ELEMENT_NODE) {
              // If this element has only text or whitespace children, output it
              const hasElementChild = Array.from(node.childNodes).some(
                (n) => n.nodeType === Node.ELEMENT_NODE
              );
              if (!hasElementChild && node.textContent.trim()) {
                // Remove all attributes
                const tag = node.tagName.toLowerCase();
                if (tag === "a") {
                  const href = node.getAttribute("href");
                  results.push(
                    `<a href="${href}">${node.textContent.trim()}</a>`
                  );
                } else {
                  results.push(`<${tag}>${node.textContent.trim()}</${tag}>`);
                }
              } else {
                // Otherwise, recurse into children
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
            // Always include the anchor tag with its href and no children
            const href = a.getAttribute("href");
            let output = [`<a href="${href}"></a>`];
            // For each descendant, get only the tag and its text
            output = output.concat(getTagWithText(a));
            return output.join("");
          });
        },
      });

      const listings = result[0].result;
      console.log("Listings with divs:", listings);

      fetch("http://127.0.0.1:8000/listings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ listings: listings }),
      });
    } catch (error) {
      console.error("Error getting listings:", error);
    }
  });
