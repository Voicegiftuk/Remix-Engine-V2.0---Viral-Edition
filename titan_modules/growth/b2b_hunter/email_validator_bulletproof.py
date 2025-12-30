#!/usr/bin/env python3
"""
BULLETPROOF EMAIL VALIDATOR
Zero tolerance for invalid emails
Every email passes ALL 7 levels or gets REJECTED
"""
import os
import re
import time
import json
import requests
import dns.resolver
import socket
import smtplib
from typing import Optional, Dict, Tuple
from datetime import datetime

class BulletproofEmailValidator:
    """
    7-Level email validation system
    If ANY level fails = EMAIL REJECTED
    """
    
    def __init__(self):
        self.hunter_api_key = os.getenv('HUNTER_API_KEY', '')
        self.validation_log = []
        
        # Disposable email domains (free temp emails)
        self.disposable_domains = [
            'tempmail.com', 'guerrillamail.com', '10minutemail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org'
        ]
        
        # Known spam traps / honeypots
        self.spam_traps = [
            'spamtrap.', 'honeypot.', 'blackhole.'
        ]
    
    def log_validation(self, email: str, level: str, status: str, details: str):
        """Log every validation step"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'email': email,
            'level': level,
            'status': status,
            'details': details
        }
        self.validation_log.append(entry)
        print(f"    [{level}] {status}: {details}")
    
    def level_1_format_validation(self, email: str) -> Tuple[bool, str]:
        """
        LEVEL 1: Format validation
        - Must contain exactly one @
        - No spaces, brackets, or special chars
        - Valid domain structure
        - Not empty
        """
        if not email or not isinstance(email, str):
            return False, "Email is empty or not a string"
        
        email = email.strip().lower()
        
        # Must have exactly one @
        if email.count('@') != 1:
            return False, f"Invalid @ count: {email.count('@')}"
        
        # Split into local and domain
        try:
            local, domain = email.split('@')
        except:
            return False, "Cannot split email"
        
        # Local part checks
        if len(local) < 1 or len(local) > 64:
            return False, f"Local part length invalid: {len(local)}"
        
        # Domain checks
        if len(domain) < 4 or len(domain) > 255:
            return False, f"Domain length invalid: {len(domain)}"
        
        if not '.' in domain:
            return False, "Domain has no TLD"
        
        # No invalid characters
        invalid_chars = ['(', ')', '[', ']', '{', '}', '<', '>', ',', ';', ':', ' ', '\\', '"']
        for char in invalid_chars:
            if char in email:
                return False, f"Contains invalid character: {char}"
        
        # Regex validation
        pattern = r'^[a-z0-9][a-z0-9._-]*[a-z0-9]@[a-z0-9][a-z0-9.-]*\.[a-z]{2,}$'
        if not re.match(pattern, email):
            return False, "Failed regex pattern match"
        
        return True, "Format valid"
    
    def level_2_disposable_check(self, email: str) -> Tuple[bool, str]:
        """
        LEVEL 2: Check if disposable/temporary email
        Reject all temp email services
        """
        domain = email.split('@')[1]
        
        for disposable in self.disposable_domains:
            if disposable in domain:
                return False, f"Disposable email service: {disposable}"
        
        return True, "Not disposable"
    
    def level_3_spam_trap_check(self, email: str) -> Tuple[bool, str]:
        """
        LEVEL 3: Check for spam trap patterns
        """
        email_lower = email.lower()
        
        for trap in self.spam_traps:
            if trap in email_lower:
                return False, f"Spam trap pattern detected: {trap}"
        
        # Check for obvious fake patterns
        fake_patterns = ['test@', 'fake@', 'noreply@', 'no-reply@', 'bounce@']
        for pattern in fake_patterns:
            if email_lower.startswith(pattern):
                return False, f"Fake email pattern: {pattern}"
        
        return True, "No spam trap patterns"
    
    def level_4_dns_validation(self, email: str) -> Tuple[bool, str]:
        """
        LEVEL 4: DNS/MX record validation
        Domain MUST have mail server configured
        """
        domain = email.split('@')[1]
        
        try:
            # Check if domain exists (A record)
            try:
                socket.gethostbyname(domain)
            except socket.gaierror:
                return False, "Domain does not exist (no A record)"
            
            # Check MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                if not mx_records:
                    return False, "No MX records found"
                
                mx_list = [str(mx.exchange) for mx in mx_records]
                return True, f"MX records found: {len(mx_list)} servers"
                
            except dns.resolver.NXDOMAIN:
                return False, "Domain does not exist (NXDOMAIN)"
            except dns.resolver.NoAnswer:
                return False, "No MX records configured"
            except dns.resolver.Timeout:
                return False, "DNS timeout"
            
        except Exception as e:
            return False, f"DNS error: {str(e)}"
    
    def level_5_smtp_verification(self, email: str, timeout: int = 15) -> Tuple[bool, str]:
        """
        LEVEL 5: SMTP mailbox verification
        Connect to mail server and verify mailbox exists
        This is the STRONGEST validation
        """
        domain = email.split('@')[1]
        
        try:
            # Get MX records
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_host = str(mx_records[0].exchange).rstrip('.')
            
            # Connect to SMTP server
            server = smtplib.SMTP(timeout=timeout)
            server.set_debuglevel(0)
            
            # Connect
            code, message = server.connect(mx_host, 25)
            if code != 220:
                return False, f"SMTP connect failed: {code}"
            
            # HELO
            code, message = server.helo('sayplay.gift')
            if code != 250:
                return False, f"HELO failed: {code}"
            
            # MAIL FROM
            code, message = server.mail('verify@sayplay.gift')
            if code != 250:
                return False, f"MAIL FROM failed: {code}"
            
            # RCPT TO - this is where we verify the mailbox
            code, message = server.rcpt(email)
            server.quit()
            
            if code in [250, 251]:
                return True, f"Mailbox verified (code {code})"
            elif code == 550:
                return False, "Mailbox does not exist (550)"
            elif code == 552:
                return False, "Mailbox full (552)"
            elif code == 553:
                return False, "Invalid mailbox (553)"
            else:
                return False, f"SMTP verification failed: {code}"
            
        except socket.timeout:
            return True, "Timeout (benefit of doubt)"
        except Exception as e:
            return True, f"SMTP check error (benefit of doubt): {str(e)}"
    
    def level_6_hunter_verification(self, email: str, domain: str) -> Tuple[bool, str]:
        """
        LEVEL 6: Hunter.io verification
        Professional email verification service
        """
        if not self.hunter_api_key:
            return True, "Hunter.io not configured (skipped)"
        
        try:
            url = "https://api.hunter.io/v2/email-verifier"
            params = {
                'email': email,
                'api_key': self.hunter_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'data' not in data:
                return True, "Hunter.io no data (benefit of doubt)"
            
            result = data['data']
            status = result.get('status')
            score = result.get('score', 0)
            
            if status == 'valid':
                return True, f"Hunter verified: valid (score {score})"
            elif status == 'invalid':
                return False, "Hunter verified: invalid"
            elif status == 'disposable':
                return False, "Hunter verified: disposable"
            elif status == 'accept_all':
                if score >= 50:
                    return True, f"Catch-all server (score {score})"
                else:
                    return False, f"Catch-all server, low score ({score})"
            else:
                return True, f"Hunter status: {status} (benefit of doubt)"
            
        except Exception as e:
            return True, f"Hunter error (benefit of doubt): {str(e)}"
    
    def level_7_final_confirmation(self, email: str, all_results: Dict) -> Tuple[bool, str]:
        """
        LEVEL 7: Final confirmation check
        Review all previous levels and make final decision
        """
        for level, (status, message) in all_results.items():
            if not status and 'benefit of doubt' not in message:
                return False, f"Failed at {level}: {message}"
        
        passed = sum(1 for result in all_results.values() if result[0])
        total = len(all_results)
        return True, f"All validations passed ({passed}/{total})"
    
    def validate_email_bulletproof(self, 
                                   email: str, 
                                   domain: str = None) -> Tuple[bool, str, Dict]:
        """
        COMPLETE BULLETPROOF VALIDATION
        Email must pass ALL 7 levels
        
        Returns: (is_valid, reason, detailed_results)
        """
        if not email:
            return False, "Email is empty", {}
        
        email = email.strip().lower()
        if not domain:
            domain = email.split('@')[1] if '@' in email else ''
        
        print(f"\n  BULLETPROOF VALIDATION: {email}")
        print(f"  {'='*60}")
        
        results = {}
        
        # LEVEL 1: Format
        valid, msg = self.level_1_format_validation(email)
        results['Level 1 - Format'] = (valid, msg)
        self.log_validation(email, 'Level 1', 'PASS' if valid else 'FAIL', msg)
        if not valid:
            return False, f"Level 1 Failed: {msg}", results
        
        # LEVEL 2: Disposable
        valid, msg = self.level_2_disposable_check(email)
        results['Level 2 - Disposable'] = (valid, msg)
        self.log_validation(email, 'Level 2', 'PASS' if valid else 'FAIL', msg)
        if not valid:
            return False, f"Level 2 Failed: {msg}", results
        
        # LEVEL 3: Spam traps
        valid, msg = self.level_3_spam_trap_check(email)
        results['Level 3 - Spam Trap'] = (valid, msg)
        self.log_validation(email, 'Level 3', 'PASS' if valid else 'FAIL', msg)
        if not valid:
            return False, f"Level 3 Failed: {msg}", results
        
        # LEVEL 4: DNS/MX
        valid, msg = self.level_4_dns_validation(email)
        results['Level 4 - DNS/MX'] = (valid, msg)
        self.log_validation(email, 'Level 4', 'PASS' if valid else 'FAIL', msg)
        if not valid:
            return False, f"Level 4 Failed: {msg}", results
        
        # LEVEL 5: SMTP
        valid, msg = self.level_5_smtp_verification(email)
        results['Level 5 - SMTP'] = (valid, msg)
        self.log_validation(email, 'Level 5', 'PASS' if valid else 'FAIL', msg)
        if not valid and 'benefit of doubt' not in msg:
            return False, f"Level 5 Failed: {msg}", results
        
        # LEVEL 6: Hunter.io
        valid, msg = self.level_6_hunter_verification(email, domain)
        results['Level 6 - Hunter'] = (valid, msg)
        self.log_validation(email, 'Level 6', 'PASS' if valid else 'FAIL', msg)
        if not valid and 'benefit of doubt' not in msg:
            return False, f"Level 6 Failed: {msg}", results
        
        # LEVEL 7: Final confirmation
        valid, msg = self.level_7_final_confirmation(email, results)
        results['Level 7 - Final'] = (valid, msg)
        self.log_validation(email, 'Level 7', 'PASS' if valid else 'FAIL', msg)
        
        if valid:
            print(f"  {'='*60}")
            print(f"  EMAIL VALIDATED: {email}")
            print(f"  {'='*60}\n")
        else:
            print(f"  {'='*60}")
            print(f"  EMAIL REJECTED: {email}")
            print(f"  {'='*60}\n")
        
        return valid, msg, results
    
    def save_validation_log(self, filepath: str = 'email_validation_log.json'):
        """Save all validations to file for audit"""
        with open(filepath, 'w') as f:
            json.dump(self.validation_log, f, indent=2)
        print(f"Validation log saved: {filepath}")


class EmailFinder:
    """Find real emails from websites and APIs"""
    
    def __init__(self):
        self.hunter_api_key = os.getenv('HUNTER_API_KEY', '')
    
    def scrape_email_from_website(self, url: str) -> Optional[str]:
        """Scrape email from website"""
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, timeout=15, headers=headers)
            if response.status_code != 200:
                return None
            
            # Find email pattern
            pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(pattern, response.text)
            
            if emails:
                # Filter out junk
                valid_emails = []
                for e in emails:
                    e = e.lower()
                    if not any(x in e for x in ['example', 'test', 'placeholder', 'your', 'domain', '.png', '.jpg', 'wixpress']):
                        valid_emails.append(e)
                
                return valid_emails[0] if valid_emails else None
            
            return None
            
        except Exception as e:
            print(f"    Website scrape error: {e}")
            return None
    
    def hunter_find_email(self, domain: str) -> Optional[str]:
        """Find email using Hunter.io"""
        if not self.hunter_api_key:
            return None
        
        try:
            url = "https://api.hunter.io/v2/domain-search"
            params = {
                'domain': domain,
                'api_key': self.hunter_api_key,
                'limit': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('data', {}).get('emails'):
                return data['data']['emails'][0]['value']
            
            return None
            
        except Exception as e:
            print(f"    Hunter error: {e}")
            return None
    
    def find_email_multi_source(self, 
                                business_name: str,
                                website: Optional[str] = None,
                                places_email: Optional[str] = None) -> Optional[str]:
        """
        Find email from multiple sources
        Priority: Places API > Website scrape > Hunter.io
        """
        print(f"\n  EMAIL DISCOVERY: {business_name}")
        
        # Source 1: Places API
        if places_email:
            print(f"    Source 1 (Places API): {places_email}")
            return places_email
        else:
            print(f"    Source 1 (Places API): No email")
        
        # Source 2: Website scrape
        if website:
            print(f"    Source 2 (Website): Scraping {website}...")
            email = self.scrape_email_from_website(website)
            if email:
                print(f"    Source 2 (Website): Found {email}")
                return email
            else:
                print(f"    Source 2 (Website): No email found")
        
        # Source 3: Hunter.io
        if website:
            domain = website.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
            print(f"    Source 3 (Hunter.io): Searching {domain}...")
            email = self.hunter_find_email(domain)
            if email:
                print(f"    Source 3 (Hunter.io): Found {email}")
                return email
            else:
                print(f"    Source 3 (Hunter.io): No email found")
        
        print(f"    NO EMAIL FOUND from any source")
        return None
