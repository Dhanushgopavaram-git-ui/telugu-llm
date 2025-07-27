#!/usr/bin/env python3
"""
Telugu Recipes Application Runner
A simple script to start the Flask application
"""

import os
import sys
from app import app

def main():
    """Main function to run the application"""
    print("🍛 Starting Telugu Recipes Application...")
    print("=" * 50)
    print("📱 Web Interface: http://localhost:5000")
    print("🔍 API Endpoints:")
    print("   - GET  /api/recipes")
    print("   - GET  /api/search?q=<query>")
    print("   - POST /add_recipe")
    print("=" * 50)
    print("💡 Tip: Click 'Initialize' in the web interface to add sample recipes")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 