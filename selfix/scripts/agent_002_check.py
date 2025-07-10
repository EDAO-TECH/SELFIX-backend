import os

def agent_check():
    try:
        path = "/opt/SELFIX/agents/agent_002.py"
        if not os.path.exists(path):
            return "fail"
        with open(path, "r") as f:
            contents = f.read()
            if "final_version = True" in contents:
                return "pass"
            else:
                return "fail"
    except:
        return "fail"

if __name__ == "__main__":
    print("Agent 002 Check:", agent_check())
