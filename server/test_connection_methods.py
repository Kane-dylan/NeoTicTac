"""
Test different connection methods for Supabase in production
"""
import os
import socket
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text
from urllib.parse import urlparse, urlunparse

load_dotenv()

def test_host_resolution():
    """Test DNS resolution for Supabase host"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    # Parse URL to get host
    parsed = urlparse(database_url)
    host = parsed.hostname
    port = parsed.port or 5432
    
    print(f"🔍 Testing DNS resolution for: {host}")
    
    try:
        # Get all IP addresses for the host
        addr_info = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        print(f"✅ DNS resolution successful for {host}")
        
        for family, socktype, proto, canonname, sockaddr in addr_info:
            family_name = "IPv4" if family == socket.AF_INET else "IPv6"
            print(f"  {family_name}: {sockaddr[0]}")
        
        # Test IPv4 only
        try:
            ipv4_addrs = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
            if ipv4_addrs:
                ipv4_addr = ipv4_addrs[0][4][0]
                print(f"✅ IPv4 address available: {ipv4_addr}")
                return ipv4_addr
        except socket.gaierror:
            print("❌ No IPv4 addresses found")
            
        return True
        
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        return False

def test_connection_with_ipv4():
    """Test connection forcing IPv4"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        return False
    
    # Parse original URL
    parsed = urlparse(database_url)
    host = parsed.hostname
    
    # Get IPv4 address
    try:
        ipv4_addrs = socket.getaddrinfo(host, 5432, socket.AF_INET, socket.SOCK_STREAM)
        if not ipv4_addrs:
            print("❌ No IPv4 addresses available")
            return False
            
        ipv4_addr = ipv4_addrs[0][4][0]
        print(f"🔍 Testing connection with IPv4: {ipv4_addr}")
        
        # Replace hostname with IPv4 address
        new_netloc = f"{parsed.username}:{parsed.password}@{ipv4_addr}:{parsed.port}"
        ipv4_url = urlunparse((
            parsed.scheme,
            new_netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        
        print(f"📝 IPv4 URL: {ipv4_url.replace(parsed.password, '***')}")
        
        # Test connection
        engine = create_engine(
            ipv4_url,
            pool_size=1,
            pool_pre_ping=True,
            connect_args={
                'connect_timeout': 15,
                'sslmode': 'require',
                'application_name': 'tictactoe-ipv4-test'
            }
        )
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ IPv4 connection successful!")
            print(f"📊 Version: {version}")
            
        engine.dispose()
        return ipv4_url
        
    except Exception as e:
        print(f"❌ IPv4 connection failed: {e}")
        return False

def test_connection_with_params():
    """Test connection with specific parameters"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        return False
    
    # Add connection parameters
    separator = '&' if '?' in database_url else '?'
    params = [
        'sslmode=require',
        'application_name=tictactoe-backend',
        'connect_timeout=20',
        'target_session_attrs=read-write'
    ]
    
    enhanced_url = database_url + separator + '&'.join(params)
    print(f"🔍 Testing connection with enhanced parameters")
    
    try:
        engine = create_engine(
            enhanced_url,
            pool_size=1,
            pool_pre_ping=True,
            pool_timeout=30
        )
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.close()
            print("✅ Enhanced connection successful!")
            
        engine.dispose()
        return enhanced_url
        
    except Exception as e:
        print(f"❌ Enhanced connection failed: {e}")
        return False

def main():
    print("🚀 Testing Supabase connection methods for production deployment\n")
    
    # Test 1: DNS Resolution
    print("=" * 50)
    print("TEST 1: DNS Resolution")
    print("=" * 50)
    ipv4_addr = test_host_resolution()
    
    # Test 2: IPv4 Connection
    print("\n" + "=" * 50)
    print("TEST 2: IPv4 Direct Connection")
    print("=" * 50)
    ipv4_url = test_connection_with_ipv4()
    
    # Test 3: Enhanced Parameters
    print("\n" + "=" * 50)
    print("TEST 3: Enhanced Parameters")
    print("=" * 50)
    enhanced_url = test_connection_with_params()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 50)
    
    if ipv4_url:
        print("✅ RECOMMENDATION: Use IPv4 direct connection")
        print(f"   URL format: {ipv4_url.split('@')[0]}@IPv4_ADDRESS:5432/...")
    elif enhanced_url:
        print("✅ RECOMMENDATION: Use enhanced parameters")
        print("   Add connection timeout and SSL settings")
    else:
        print("❌ All connection methods failed")
        print("   Check network connectivity and firewall settings")

if __name__ == "__main__":
    main()
