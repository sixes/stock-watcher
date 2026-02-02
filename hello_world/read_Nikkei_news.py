import imaplib
import email
from email.header import decode_header
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# Your email credentials
USERNAME = os.getenv('READ_NEWS_EMAIL_NAME') 
PASSWORD = os.getenv('READ_NEWS_EMAIL_PASSWORD') # Use App Password if 2FA is enabled
IMAP_SERVER = 'imap.gmail.com'

def clean(subject):
    decoded_bytes, encoding = decode_header(subject)[0]
    if isinstance(decoded_bytes, bytes):
        return decoded_bytes.decode(encoding if encoding else 'utf-8')
    return decoded_bytes

def extract_paragraphs(html_content):
    try:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        #print("get text:" + soup.get_text())
        
        head_lines_h1 = [p.get_text(strip=True) for p in soup.find_all("h1")]
        #logger.debug("===========================================")
        #logger.debug("h1" + "\n".join(head_lines_h1))

        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]

        head_lines_h4 = [p.get_text(strip=True) for p in soup.find_all("h4")]
        #logger.debug("h4" + "\n".join(head_lines_h4))
        #logger.debug("==========================================!!!!!!!!!!!!!!!=")
        
        
        paragraphs.extend(head_lines_h1)
        paragraphs.extend(head_lines_h4)
        #logger.debug(soup.get_text())
        return soup.get_text()
    except Exception as e:
        print(f"Error extracting paragraphs: {e}")
        return []


def rm_duplicate(paragraphs):
    ret = set()
    update_para = []
    for para in paragraphs:
        if para not in ret or "\n" == para:
            ret.add(para)
            update_para.append(para)
    return update_para

def filter_promotions(contents):
    pro = ("Get important stories about Japan", "Discover the Nikkei Asia app", "Advertisement", "If you are interested in sponsoring our media", 
        "You have received this email because", "If you no longer wish to receive email", "Subscription options", "A weekly lineup of Asia", 
        "1-3-7  Otemachi  Chiyoda-ku  Tokyo  100-8066  Japan", "A must-read column examining", "Was this email forwarded to you?", "Subscribe for $1", "View in browser", "All Newsletters",
        "Explore Nikkei Asia's newsletters", "Japan Update", "The inside story on the Asia tech trends that matter", "Please do not reply to this email. If you have any questions  visit our FAQs",
        "Nikkei Inc. No reproduction without permission.")
    ret = []
    for paragraphs in contents:
        #logger.debug("before split:" + paragraphs)
        paragraphs = paragraphs.splitlines()
        #logger.debug((paragraphs))                
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            p = re.sub(r'[\s{2,}]', ' ', p)
            ret.append(p)
    final = []
    full_matches = ("Subscribe", "China Up Close", "#techAsia", "Your Week in Asia", "|")
    for item in ret:
        found = False
        if "Read more" in item or "Selected for you" in item:
            #final.append("\n")
            continue
        for ad in pro:
            if ad in item:
                found = True
                break
        found_fm = False
        for fm in full_matches:
            found_fm = False
            if item == fm:
                found_fm = True
                break
        if not found and not found_fm:
            final.append(item)
    final = rm_duplicate(final)
    final = "\n\n".join(final)
    
    print(final)
    return final


def read_nikkei_news():
    all_paragraphs = []  # List to hold all extracted paragraphs
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        if not USERNAME or not PASSWORD:
            logger.error("Email credentials not found")
            return "Email credentials not found"
        mail.login(USERNAME, PASSWORD)
        mail.select('inbox')

        # Get today's date in the format DD-Mon-YYYY (e.g., "03-Jan-2025")
        today = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

        # Search for emails from "nikkei" received today
        status, messages = mail.search(None, f'(FROM "nikkei" ON "{today}")')
        if status != "OK" or not messages[0]:
            print(f"No emails found from Nikkei on {today}.")
            return ""

        email_ids = messages[0].split()
        print(f"Nikkei News Emails Received on {today}:")
        print(email_ids)
        
        for email_id in email_ids:
            try:
                # Fetch the email
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status != "OK":
                    print(f"Failed to fetch email ID {email_id}")
                    continue

                # Parse the email
                msg = email.message_from_bytes(msg_data[0][1])
                subject = clean(msg['subject'])
                
                print(f"Subject: {subject}")
                print(f"To: {msg['to']}")
                print(f"From: {msg['from']}")
                print(f"Date: {msg['date']}")
                

                # Process email parts
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/html":
                        html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        paragraphs = extract_paragraphs(html_content)
                        all_paragraphs.append(paragraphs)  # Add extracted paragraphs to the list

                print("-" * 50)
            except Exception as e:
                print(f"Error processing email ID {email_id}: {e}")
    except Exception as e:
        print(f"Error connecting to email server: {e}")
    finally:
        try:
            mail.logout()
        except:
            pass

    return filter_promotions(all_paragraphs)  # Return all paragraphs as a single string

if __name__ == "__main__":
    content_string = read_nikkei_news()
    #print(content_string)  # Print or use the returned string as needed
    #with open("nikkei.news", "w") as f:
    #    f.write(content_string)

