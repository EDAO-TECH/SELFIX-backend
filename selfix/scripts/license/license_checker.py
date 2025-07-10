from selfix_tools import load_license

def show_license():
    license_data = load_license()
    if not license_data:
        print("❌ No valid license found.")
        return

    print(f"👤 User: {license_data['user']}")
    print(f"📅 Valid until: {license_data['valid_until']}")
    print(f"🔐 Type: {license_data['license_type']}")
    print(f"🖥️ Devices: {license_data['device_limit']}")
    print("\n✅ Features:")
    for f in license_data['features']:
        print(f"   - {f}")

if __name__ == "__main__":
    show_license()
