import socket
import sys
import os
import subprocess
import platform
import json

def test_port(host, port):
    """Test if a TCP port is available for binding"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind((host, port))
        result = True
    except socket.error as e:
        print(f"Port {port} is not available: {e}")
    finally:
        sock.close()
    return result

def get_system_info():
    """Get system information for diagnostics"""
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version,
        "python_path": sys.executable,
        "hostname": socket.gethostname(),
    }
    
    try:
        # Try to get IP address
        info["ip_address"] = socket.gethostbyname(socket.gethostname())
    except:
        info["ip_address"] = "Could not determine"
        
    return info

def test_localhost_variants():
    """Test different localhost addresses to check loopback configuration"""
    variants = [
        "localhost",
        "127.0.0.1",
        "::1"  # IPv6 localhost
    ]
    
    results = {}
    for variant in variants:
        try:
            ip = socket.gethostbyname(variant)
            results[variant] = {"resolved": True, "ip": ip}
            
            # Try to connect to port 80 on this address
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((ip, 80))
            s.close()
            
            if result == 0:
                results[variant]["port_80"] = "Open"
            else:
                results[variant]["port_80"] = f"Closed (code: {result})"
                
        except Exception as e:
            results[variant] = {"resolved": False, "error": str(e)}
    
    return results

def check_hosts_file():
    """Check if hosts file has proper localhost configuration"""
    hosts_file = "C:\\Windows\\System32\\drivers\\etc\\hosts" if platform.system() == "Windows" else "/etc/hosts"
    
    if not os.path.exists(hosts_file):
        return {"exists": False, "error": f"Hosts file not found at {hosts_file}"}
    
    try:
        with open(hosts_file, 'r') as f:
            content = f.read()
            
        localhost_entries = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split()
            if len(parts) >= 2 and (parts[1] == "localhost" or "localhost" in parts[1:]):
                localhost_entries.append(line)
                
        return {
            "exists": True,
            "localhost_entries": localhost_entries,
            "has_localhost": len(localhost_entries) > 0
        }
    except Exception as e:
        return {"exists": True, "error": str(e), "has_localhost": False}

if __name__ == "__main__":
    print("=" * 60)
    print("  NLP Key-Value Extractor - Network Diagnostics")
    print("=" * 60)
    
    # System info
    system_info = get_system_info()
    print("\n[System Information]")
    print(f"OS: {system_info['os']} {system_info['os_version']}")
    print(f"Python: {system_info['python_version']}")
    print(f"Python Path: {system_info['python_path']}")
    print(f"Hostname: {system_info['hostname']}")
    print(f"IP Address: {system_info['ip_address']}")
    
    # Port testing
    ports_to_test = [8000, 8080, 7500, 9000, 5000]
    host = "127.0.0.1"
    
    print(f"\n[Port Availability on {host}]")
    for port in ports_to_test:
        if test_port(host, port):
            print(f"✅ Port {port} is available")
        else:
            print(f"❌ Port {port} is NOT available")
    
    # Local socket connection test        
    print("\n[Localhost Configuration]")
    localhost_results = test_localhost_variants()
    for variant, result in localhost_results.items():
        if result["resolved"]:
            print(f"✅ {variant} resolves to {result['ip']}, Port 80: {result.get('port_80', 'Unknown')}")
        else:
            print(f"❌ {variant} failed: {result['error']}")
    
    # Check hosts file
    hosts_result = check_hosts_file()
    print("\n[Hosts File]")
    if hosts_result.get("exists", False):
        if hosts_result.get("error"):
            print(f"❌ Error reading hosts file: {hosts_result['error']}")
        elif hosts_result.get("has_localhost", False):
            print("✅ Hosts file has localhost entries:")
            for entry in hosts_result.get("localhost_entries", []):
                print(f"   {entry}")
        else:
            print("❌ No localhost entries found in hosts file")
    else:
        print(f"❌ {hosts_result.get('error', 'Unknown error with hosts file')}")
            
    # DNS resolution test
    print("\n[DNS Resolution]")
    try:
        google_ip = socket.gethostbyname("www.google.com")
        print(f"✅ DNS resolution is working (www.google.com → {google_ip})")
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
    
    print("\n[Windows Firewall Status]")
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output(["netsh", "advfirewall", "show", "currentprofile"], 
                                            text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if "State                                 ON" in output:
                print("ℹ️ Windows Firewall is ON")
                print("   This may block server connections if Python is not allowed")
            else:
                print("ℹ️ Windows Firewall appears to be OFF")
        except:
            print("❓ Could not determine Windows Firewall status")
    else:
        print("ℹ️ Not running on Windows, skipping firewall check")
    
    print("\n[Conclusion]")
    print("If all ports are available but servers still fail to start:")
    print("1. Check for antivirus or security software blocking Python")
    print("2. Try running as Administrator")
    print("3. Use the batch files created in the project root")
    print("4. Consider using different ports (edit the batch files)")
    
    print("\n" + "=" * 60)
    print("  Diagnostics Complete")
    print("=" * 60)
