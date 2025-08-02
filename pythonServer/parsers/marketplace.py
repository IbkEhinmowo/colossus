from bs4 import BeautifulSoup
from models.listing import ParsedListing

class MarketplaceParser:
    def parse(self, html: str) -> ParsedListing:
        soup = BeautifulSoup(html, 'html.parser')
        A = soup.find('a')
        link = "https://facebook.com" + A['href'] if A and 'href' in A.attrs else 'error: no link found'
        spans = soup.find_all('span')
        is_just_listed = spans[0].text.lower() == 'just listed' if len(spans) else False
        if is_just_listed:
            price = spans[1].text if len(spans) > 1 else ''
            title = spans[2].text if len(spans) > 2 else ''
            location = spans[3].text if len(spans) > 3 else ''
        else:   
            price = spans[0].text if len(spans) > 0 else ''
            title = spans[1].text if len(spans) > 1 else ''
            location = spans[2].text if len(spans) > 2 else ''  
                

        return ParsedListing(
            
            title=title,
            price=price,
            location=location,
            link=link,
            is_just_listed=is_just_listed
        )
