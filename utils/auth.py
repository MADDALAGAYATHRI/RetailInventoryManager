import os
import json
import random
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import pandas as pd
from twilio.rest import Client

class AuthManager:
    """
    Handles user authentication with phone number and OTP verification.
    """
    
    def __init__(self, auth_dir: str = "data/auth"):
        self.auth_dir = auth_dir
        self.ensure_auth_directory()
        self.setup_twilio()
        self.otp_expiry_minutes = 5
        
    def ensure_auth_directory(self):
        """Create auth directory if it doesn't exist."""
        os.makedirs(self.auth_dir, exist_ok=True)
        os.makedirs(f"{self.auth_dir}/users", exist_ok=True)
        os.makedirs(f"{self.auth_dir}/otps", exist_ok=True)
        
    def setup_twilio(self):
        """Setup Twilio client for SMS."""
        self.twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
        
        if all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        else:
            self.twilio_client = None
            
    def hash_phone_number(self, phone_number: str) -> str:
        """Create a hash of the phone number for privacy."""
        return hashlib.sha256(phone_number.encode()).hexdigest()[:16]
        
    def normalize_phone_number(self, phone_number: str, country_code: str = "+1") -> str:
        """Normalize phone number format with country code."""
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone_number))
        
        # Remove leading country code if present
        country_digits = country_code.replace('+', '')
        if digits.startswith(country_digits):
            digits = digits[len(country_digits):]
        
        # Add the specified country code
        return country_code + digits
        
    def user_exists(self, phone_number: str, country_code: str = "+1") -> bool:
        """Check if user already exists."""
        phone_hash = self.hash_phone_number(self.normalize_phone_number(phone_number, country_code))
        user_file = f"{self.auth_dir}/users/{phone_hash}.json"
        return os.path.exists(user_file)
        
    def create_user(self, phone_number: str, name: str, country_code: str = "+1") -> Tuple[bool, str]:
        """Create a new user account."""
        try:
            normalized_phone = self.normalize_phone_number(phone_number, country_code)
            phone_hash = self.hash_phone_number(normalized_phone)
            
            if self.user_exists(phone_number, country_code):
                return False, "User already exists with this phone number"
                
            user_data = {
                'phone_hash': phone_hash,
                'name': name,
                'created_at': datetime.now().isoformat(),
                'last_login': None,
                'is_verified': False
            }
            
            user_file = f"{self.auth_dir}/users/{phone_hash}.json"
            with open(user_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2)
                
            return True, phone_hash
            
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
            
    def get_user(self, phone_number: str, country_code: str = "+1") -> Optional[Dict]:
        """Get user data by phone number."""
        try:
            phone_hash = self.hash_phone_number(self.normalize_phone_number(phone_number, country_code))
            user_file = f"{self.auth_dir}/users/{phone_hash}.json"
            
            if os.path.exists(user_file):
                with open(user_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
            
        except Exception:
            return None
            
    def update_user(self, phone_number: str, updates: Dict, country_code: str = "+1") -> bool:
        """Update user data."""
        try:
            user_data = self.get_user(phone_number, country_code)
            if not user_data:
                return False
                
            user_data.update(updates)
            
            phone_hash = self.hash_phone_number(self.normalize_phone_number(phone_number, country_code))
            user_file = f"{self.auth_dir}/users/{phone_hash}.json"
            
            with open(user_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2)
                
            return True
            
        except Exception:
            return False
            
    def generate_otp(self) -> str:
        """Generate a 6-digit OTP."""
        return str(random.randint(100000, 999999))
        
    def send_otp(self, phone_number: str, country_code: str = "+1") -> Tuple[bool, str]:
        """Send OTP via SMS."""
        try:
            if not self.twilio_client:
                return False, "SMS service not configured"
                
            normalized_phone = self.normalize_phone_number(phone_number, country_code)
            otp = self.generate_otp()
            
            # Store OTP with expiry
            phone_hash = self.hash_phone_number(normalized_phone)
            otp_data = {
                'otp': otp,
                'phone_hash': phone_hash,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(minutes=self.otp_expiry_minutes)).isoformat(),
                'used': False
            }
            
            otp_file = f"{self.auth_dir}/otps/{phone_hash}_{int(time.time())}.json"
            with open(otp_file, 'w', encoding='utf-8') as f:
                json.dump(otp_data, f, indent=2)
                
            # Send SMS
            message_body = f"Your MindGuard verification code is: {otp}. Valid for {self.otp_expiry_minutes} minutes."
            
            message = self.twilio_client.messages.create(
                body=message_body,
                from_=self.twilio_phone_number,
                to=normalized_phone
            )
            
            return True, f"OTP sent successfully. Message SID: {message.sid}"
            
        except Exception as e:
            return False, f"Failed to send OTP: {str(e)}"
            
    def verify_otp(self, phone_number: str, entered_otp: str, country_code: str = "+1") -> Tuple[bool, str]:
        """Verify the entered OTP."""
        try:
            phone_hash = self.hash_phone_number(self.normalize_phone_number(phone_number, country_code))
            otp_dir = f"{self.auth_dir}/otps"
            
            # Find the latest OTP for this phone number
            otp_files = [f for f in os.listdir(otp_dir) if f.startswith(phone_hash)]
            
            if not otp_files:
                return False, "No OTP found for this phone number"
                
            # Sort by timestamp (filename contains timestamp)
            otp_files.sort(key=lambda x: x.split('_')[1], reverse=True)
            latest_otp_file = otp_files[0]
            
            otp_file_path = f"{otp_dir}/{latest_otp_file}"
            
            with open(otp_file_path, 'r', encoding='utf-8') as f:
                otp_data = json.load(f)
                
            # Check if OTP is already used
            if otp_data.get('used', False):
                return False, "OTP has already been used"
                
            # Check if OTP is expired
            expires_at = datetime.fromisoformat(otp_data['expires_at'])
            if datetime.now() > expires_at:
                return False, "OTP has expired"
                
            # Verify OTP
            if otp_data['otp'] == entered_otp:
                # Mark OTP as used
                otp_data['used'] = True
                with open(otp_file_path, 'w', encoding='utf-8') as f:
                    json.dump(otp_data, f, indent=2)
                    
                return True, "OTP verified successfully"
            else:
                return False, "Invalid OTP"
                
        except Exception as e:
            return False, f"Error verifying OTP: {str(e)}"
            
    def login_user(self, phone_number: str, country_code: str = "+1") -> Tuple[bool, str, Optional[str]]:
        """Login user after OTP verification."""
        try:
            user_data = self.get_user(phone_number, country_code)
            if not user_data:
                return False, "User not found", None
                
            # Update last login
            self.update_user(phone_number, {
                'last_login': datetime.now().isoformat(),
                'is_verified': True
            }, country_code)
            
            return True, "Login successful", user_data['phone_hash']
            
        except Exception as e:
            return False, f"Login error: {str(e)}", None
            
    def cleanup_expired_otps(self):
        """Clean up expired OTP files."""
        try:
            otp_dir = f"{self.auth_dir}/otps"
            current_time = datetime.now()
            
            for filename in os.listdir(otp_dir):
                file_path = f"{otp_dir}/{filename}"
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        otp_data = json.load(f)
                        
                    expires_at = datetime.fromisoformat(otp_data['expires_at'])
                    
                    # Delete if expired by more than 1 hour
                    if current_time > expires_at + timedelta(hours=1):
                        os.remove(file_path)
                        
                except Exception:
                    # If file is corrupted, delete it
                    os.remove(file_path)
                    
        except Exception:
            pass  # Fail silently for cleanup