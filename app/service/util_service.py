import subprocess

def run_shell_command(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        print(f"Command executed: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e.stderr.strip()}")