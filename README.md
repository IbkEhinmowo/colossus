<!-- @format -->

# 🏛️ Colossus

_Colossus: Because why manually browse when you can automate, parse, and flex your data muscles?_

## What Is This?

Colossus is a distributed marketplace intelligence system. It’s a Chrome extension that snatches up marketplace listings, then hands them off to a Python FastAPI backend that parses and enhances for whatever use case.

## How Does It Work?

### The Gist

```
Chrome Extension → HTML Collector → FastAPI Server → BeautifulSoup Parser → LLM Wizardry → Structured Output
```

### Chrome Extension

- Injects itself into Facebook Marketplace
- Grabs listing HTML 
- Yeets data to the backend via API calls

### Backend (Python FastAPI)

- Accepts HTML payloads at `/listings` (POST only)
- BeautifulSoup-based parsing engine slices, dices, and extracts:
  - Title
  - Price
  - Location
  - Link
  - Listing freshness (is it hot off the press?)
- Returns JSON so clean you could eat off it

### Intelligence Layer

- Parsed data gets a special treatment with an LLM for semantic enhancement
- Search relevance and data quality go from “meh” to “chef’s kiss”
- Handles edge cases like a pro (even when Marketplace changes its mind)

### Parser Logic 

- Detects “Just Listed” with regex wizardry (if Facebook decides to change the HTML structure, might stop working)
- Adjusts field extraction based on listing age (because time is an illusion)
- Converts relative URLs to absolute,
- Gracefully degrades when Facebook gets weird

## Tech Stack

- **Extension**: Vanilla JavaScript, Manifest V3 and some audacity
- **Server**: FastAPI + Pydantic (type safety...)
- **Parser**: BeautifulSoup4 
- **Intelligence**: LLM integration for search that actually works


## Use Cases

Colossus helps you grab and organize Facebook Marketplace data. If you use this for whatever reason, hope they don't ban you (not liable for that). Here’s what you can do:

- Watch for new listings
- Compare prices
- Send alerts to bots or users
- Build datasets for research
- Cut down on manual copy-paste
- Use with a Discord bot to organize ur data in channels and update you when necessary
- Power a full web app for searching and viewing listings

Example: Set Colossus to scan Marketplace every minute. It grabs listings and sends them to your database and Discord, or a web app.

_Colossus: For devs who like their data pipelines robust, their architecture clean, and their README’s just a little bit extra._

and btw its named colossus after the colossal titan in aot
