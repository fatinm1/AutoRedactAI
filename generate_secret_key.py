#!/usr/bin/env python3
"""
Generate Secret Key for AutoRedactAI
This script generates a secure random secret key for production use.
"""

import secrets
import string

def generate_secret_key(length=64):
    """Generate a secure random secret key."""
    # Use a combination of letters, digits, and special characters
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Generate a secure random string
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    return secret_key

def main():
    """Generate and display a secret key."""
    print("🔐 AutoRedactAI Secret Key Generator")
    print("=" * 40)
    
    # Generate a secure secret key
    secret_key = generate_secret_key(64)
    
    print(f"\n✅ Generated Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    
    print(f"\n📋 Copy this to your Railway environment variables:")
    print(f"SECRET_KEY={secret_key}")
    
    print(f"\n⚠️  Important Security Notes:")
    print(f"• Keep this key secret and secure")
    print(f"• Never commit it to version control")
    print(f"• Use different keys for different environments")
    print(f"• Store it securely in Railway environment variables")
    
    return secret_key

if __name__ == "__main__":
    main() 