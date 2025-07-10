import subprocess

def vpn_check():
    try:
        output = subprocess.getoutput("ifconfig")
        if "tun" in output or "ppp" in output:
            return "pass"
        else:
            return "fail"
    except:
        return "fail"

if __name__ == "__main__":
    print("VPN Check:", vpn_check())
