<!-- @format -->

# 🏛️ Colossus

_A distributed marketplace intelligence system with Chrome extension for data harvesting and FastAPI-powered parsing backend_

## Architecture Overview

Colossus operates as a dual-layer system: a Chrome extension that harvests DOM fragments from marketplace listings, and a Python server that transforms raw HTML into structured data through intelligent parsing algorithms and sentence transformers.

### Data Flow Pipeline

```
Chrome Extension → HTML Collection → FastAPI Server → BeautifulSoup Parser → LLM Enhancement → Structured Output
```

**Data Harvesting (Chrome Extension)**

- Injects into Facebook Marketplace DOM
- Extracts listing HTML via DOM manipulation
- Streams data to backend via CORS-enabled API calls

**Backend (Python FastAPI)**

- Receives HTML payloads through `/listings` POST endpoint
- Deploys BeautifulSoup-based parsing engine
- Extracts: title, price, location, link, listing freshness
- Returns structured JSON with parsing metrics

**Intelligence Layer**

- Raw parsed data gets fed into LLM for semantic enhancement
- Improves search relevance and data quality
- Handles edge cases in marketplace formatting

### Parser Logic

The `MarketplaceParser` employs a span-based extraction strategy:

- Detects "Just Listed" indicators through text pattern matching
- Dynamically adjusts field extraction based on listing age
- Constructs absolute URLs from relative Facebook Marketplace paths
- Gracefully degrades when DOM structure varies

### Tech Stack

- **Extension**: Vanilla JavaScript with Manifest V3
- **Server**: FastAPI with Pydantic models for type safety
- **Parser**: BeautifulSoup4 for HTML traversal
- **Intelligence**: LLM integration for enhanced search capabilities

_Built for developers who appreciate clean architecture and robust data pipelines._
