import os
from datetime import datetime
from bs4 import BeautifulSoup
import re

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
    
    def _generate_summary(self, content, max_length=150):
        """
        Generate a short summary from the content.
        Takes the first sentences up to max_length characters.
        """
        # Clean up any extra whitespace
        clean_content = re.sub(r'\s+', ' ', content).strip()
        
        # Find sentence endings (period followed by space or end of string)
        sentences = re.split(r'\.(?:\s|$)', clean_content)
        
        summary = ""
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            # Add period back that was removed in the split
            potential_summary = summary + sentence.strip() + ". "
            
            # If adding this sentence exceeds max length, stop
            if len(potential_summary) > max_length:
                # If this is the first sentence and it's too long, truncate it
                if not summary:
                    return sentence.strip()[:max_length-3] + "..."
                break
                
            summary = potential_summary
            
            # If we have at least one sentence and are near max length, stop
            if summary and len(summary) > max_length * 0.7:
                break
                
        return summary.strip()
    
    def get_todays_lesson(self):
        """
        Return the page for today based on days since the start date.
        """
        start_date = datetime(2024, 1, 1)  # Project start date
        days_passed = (datetime.now() - start_date).days
        page_index = days_passed % len(self.pages)
        
        page = self.pages[page_index]
        
        # Generate summary from content
        summary = self._generate_summary(page['content'])
        
        # Format the message with the new summary
        message = f"""
        🤖 Daily ML Lesson #{page['day']}

        📚 {page['title']}
        
        📝 Today's Topic: {summary}

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