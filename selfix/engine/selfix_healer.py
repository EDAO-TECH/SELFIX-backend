# /opt/SELFIX/engine/selfix_healer.py

def self_healing():
    print("🔁 Running internal SELFIX self-healing...")

    # Example healing actions:
    services_to_restart = ['selfix-backend', 'selfix-hq']
    for svc in services_to_restart:
        result = restart_service(svc)
        print(result)

    print("✅ Local self-healing complete.\n")

def restart_service(name):
    import subprocess
    try:
        subprocess.run(["systemctl", "restart", name], check=True)
        return f"[green]✅ Restarted {name}[/green]"
    except subprocess.CalledProcessError:
        return f"[red]❌ Failed to restart {name}[/red]"
