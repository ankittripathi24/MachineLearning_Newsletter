import os
from datetime import datetime
from bs4 import BeautifulSoup

class HTMLMessageFormatter:
    def __init__(self, html_path='lessons/content.html'):
        """
        Initialize the formatter with the path to the HTML file.
        """
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"HTML file not found: {html_path}")
            
        self.html_path = html_path
        self.pages = self._parse_html_into_pages()
        
    def _parse_html_into_pages(self):
        """
        Parse the HTML file and divide it into pages.
        Each h1 or h2 element is considered the start of a new page.
        """
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all major headers (h1, h2) which we'll use as page separators
        headers = soup.find_all(['h1', 'h2'])
        
        pages = []
        
        for i, header in enumerate(headers):
            # Create a page object
            page = {
                'day': i + 1,
                'title': header.get_text().strip(),
                'content': '',
                'code_examples': [],
                'resources': []
            }
            
            # Get all content until the next header
            current = header.next_sibling
            content_parts = []
            
            while current and not (current.name == 'h1' or current.name == 'h2'):
                if current.name:  # Skip if it's just a NavigableString
                    # Extract code examples
                    if current.name == 'pre' or current.name == 'code':
                        page['code_examples'].append(current.get_text().strip())
                    # Extract resources (assuming they're in <ul> with class "resources")
                    elif current.name == 'ul' and 'resources' in current.get('class', []):
                        for li in current.find_all('li'):
                            page['resources'].append(li.get_text().strip())
                    # Add to general content
                    else:
                        content_parts.append(current.get_text().strip())
                
                current = current.next_sibling
                
            page['content'] = '\n\n'.join([p for p in content_parts if p])
            pages.append(page)
            
        return pages
    
    def get_todays_lesson(self):
        """
        Return the page for today based on days since the start date.
        """
        start_date = datetime(2024, 1, 1)  # Project start date
        days_passed = (datetime.now() - start_date).days
        page_index = days_passed % len(self.pages)
        
        page = self.pages[page_index]
        
        # Format the message similarly to the original formatter
        message = f"""
        🤖 Daily ML Lesson #{page['day']}

        📚 {page['title']}

        {page['content']}
        """
        
        # Add code examples if available
        if page['code_examples']:
            message += "\n\n💻 Code Example:\n```python\n"
            message += "\n".join(page['code_examples'])
            message += "\n```"
        
        # Add resources if available
        if page['resources']:
            message += "\n\n📌 Additional Resources:\n"
            message += "\n".join(['• ' + r for r in page['resources']])
        
        return message