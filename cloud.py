import os
import subprocess
import platform
import sys
import shutil

def banner():
    print("\n######################################################")
    print("#                                                    #")
    print("#       Docker & Docker Compose Setup Script         #")
    print("#                                                    #")
    print("######################################################\n")

def command_exists(command):
    """
    Check if a command exists on the system.
    """
    return shutil.which(command) is not None

def check_privileges():
    """
    Ensure the script is running with sufficient privileges on Linux.
    """
    if platform.system() == "Linux" and os.geteuid() != 0:
        print("❌ This script must be run as root or with sudo privileges on Linux.")
        sys.exit(1)

def install_docker():
    """
    Install Docker based on the operating system.
    """
    system = platform.system()
    if command_exists("docker"):
        print("✅ Docker is already installed.")
        return

    print("🚀 Installing Docker...")
    try:
        if system == "Linux":
            # Update package information
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            # Install required packages
            subprocess.run(["sudo", "apt-get", "install", "-y", 
                            "ca-certificates", "curl", "gnupg", "lsb-release"], check=True)
            # Add Docker's official GPG key
            subprocess.run(["curl", "-fsSL", 
                            "https://download.docker.com/linux/ubuntu/gpg", 
                            "|", "sudo", "gpg", "--dearmor", 
                            "-o", "/usr/share/keyrings/docker-archive-keyring.gpg"], check=True, shell=True)
            # Set up the stable repository
            subprocess.run(['echo', 
                            '"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
                            https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"', 
                            "|", "sudo", "tee", "/etc/apt/sources.list.d/docker.list", ">", "/dev/null"], check=True, shell=True)
            # Install Docker Engine
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", 
                            "docker-ce", "docker-ce-cli", "containerd.io"], check=True)
            # Add current user to docker group
            subprocess.run(["sudo", "usermod", "-aG", "docker", os.getlogin()], check=True)
            print("✅ Docker installation completed on Linux.")
        elif system == "Darwin":
            # Check if Homebrew is installed
            if not command_exists("brew"):
                print("🔍 Homebrew not found. Installing Homebrew...")
                subprocess.run(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                    shell=True,
                    check=True
                )
                print("✅ Homebrew installed successfully.")
            # Install Docker using Homebrew
            subprocess.run(["brew", "install", "--cask", "docker"], check=True)
            print("✅ Docker installation initiated on macOS. Please start Docker Desktop manually.")
        elif system == "Windows":
            # Determine if running on PowerShell or CMD
            shell = "powershell" if "pwsh" in os.environ.get("SHELL", "").lower() else "cmd"
            docker_installer_url = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
            installer_path = os.path.join(os.getcwd(), "DockerDesktopInstaller.exe")
            print("🔽 Downloading Docker Desktop Installer...")
            subprocess.run([
                shell, 
                "/C" if shell == "cmd" else "-Command", 
                f"Invoke-WebRequest -Uri {docker_installer_url} -OutFile {installer_path}"
            ], check=True)
            print("📥 Running Docker Desktop Installer...")
            subprocess.run([installer_path], check=True)
            print("✅ Docker installation initiated on Windows. Please follow the installer prompts and restart your system if required.")
        else:
            print("❌ Unsupported operating system. Please install Docker manually.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred during Docker installation: {e}")
        sys.exit(1)

def install_docker_compose():
    """
    Install Docker Compose based on the operating system.
    """
    system = platform.system()
    if command_exists("docker-compose") or command_exists("docker compose"):
        print("✅ Docker Compose is already installed.")
        return

    print("🚀 Installing Docker Compose...")
    try:
        if system == "Linux":
            compose_version = "v2.20.2"
            download_url = f"https://github.com/docker/compose/releases/download/{compose_version}/docker-compose-$(uname -s)-$(uname -m)"
            subprocess.run([
                "sudo", "curl", "-L", download_url, "-o", "/usr/local/bin/docker-compose"
            ], check=True, shell=True)
            subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/docker-compose"], check=True)
            print("✅ Docker Compose installation completed on Linux.")
        elif system == "Darwin":
            print("ℹ️ Docker Compose comes bundled with Docker Desktop on macOS.")
            print("✅ Docker Compose should be available after starting Docker Desktop.")
        elif system == "Windows":
            print("ℹ️ Docker Compose comes bundled with Docker Desktop on Windows.")
            print("✅ Docker Compose should be available after starting Docker Desktop.")
        else:
            print("❌ Unsupported operating system. Please install Docker Compose manually.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred during Docker Compose installation: {e}")
        sys.exit(1)

def verify_docker_installation():
    """
    Verify if Docker is installed and running properly.
    """
    print("🔍 Verifying Docker installation...")
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE)
        print("✅ Docker is installed and working correctly.")
    except subprocess.CalledProcessError:
        print("❌ Docker is not installed or not working correctly.")
        sys.exit(1)

def verify_docker_compose_installation():
    """
    Verify if Docker Compose is installed and running properly.
    """
    print("🔍 Verifying Docker Compose installation...")
    try:
        # Check for both v1 and v2
        if command_exists("docker-compose"):
            subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.PIPE)
        else:
            subprocess.run(["docker", "compose", "version"], check=True, stdout=subprocess.PIPE)
        print("✅ Docker Compose is installed and working correctly.")
    except subprocess.CalledProcessError:
        print("❌ Docker Compose is not installed or not working correctly.")
        sys.exit(1)

def clone_repo():
    """
    Clone a Git repository to the local system.
    """
    print("🔗 Cloning repository...")
    repo_url = input("Enter the Git repository URL: ").strip()
    if not repo_url:
        print("❌ Repository URL cannot be empty.")
        sys.exit(1)
    try:
        subprocess.run(["git", "clone", repo_url], check=True)
        repo_name = os.path.basename(repo_url.rstrip("/")).replace('.git', '')
        os.chdir(repo_name)
        print(f"✅ Repository '{repo_name}' cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository: {e}")
        sys.exit(1)

def create_dockerfile_node():
    """
    Create a Dockerfile for a Node.js application.
    """
    print("📝 Creating Dockerfile for Node.js application...")
    node_version = input("Enter Node.js version (e.g., 14, 16, 18) or leave blank for latest: ").strip() or "latest"
    port = input("Enter the application port (default 3000): ").strip() or "3000"
    dockerfile_content = f"""# Dockerfile for Node.js Application
FROM node:{node_version}
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE {port}
CMD ["npm", "start"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Dockerfile created successfully.")



def create_dockerfile_django():
    """
    Create a Dockerfile for a Django application with error handling.
    """
    try:
        print("📝 Creating Dockerfile for Django application...")
        python_version = input("Enter Python version (e.g., 3.8, 3.9, 3.10) or leave blank for latest: ").strip() or "latest"
        port = input("Enter the application port (default 8000): ").strip() or "8000"
        
        # Base Dockerfile content
        dockerfile_content = f"""# Dockerfile for Django Application
FROM python:{python_version}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
"""
        
        # Check if requirements.txt exists
        if os.path.isfile("requirements.txt"):
            dockerfile_content += """
COPY requirements.txt /app/
RUN pip install -r requirements.txt
"""
        else:
            print("⚠️ Warning: 'requirements.txt' not found. Skipping dependency installation.")
        
        # Continue with the rest of the Dockerfile content
        dockerfile_content += f"""
COPY . /app/
EXPOSE {port}
CMD ["python", "manage.py", "runserver", "0.0.0.0:{port}"]
"""

        # Write the Dockerfile content to a file
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        print("✅ Dockerfile created successfully.")
    
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


def create_dockerfile_flask():
    """
    Create a Dockerfile for a Flask application with error handling.
    """
    try:
        print("📝 Creating Dockerfile for Flask application...")
        python_version = input("Enter Python version (e.g., 3.8, 3.9, 3.10) or leave blank for latest: ").strip() or "latest"
        port = input("Enter the application port (default 5000): ").strip() or "5000"
        
        # Base Dockerfile content
        dockerfile_content = f"""# Dockerfile for Flask Application
FROM python:{python_version}
WORKDIR /app
"""
        
        # Check if requirements.txt exists
        if os.path.isfile("requirements.txt"):
            dockerfile_content += """
COPY requirements.txt /app/
RUN pip install -r requirements.txt
"""
        else:
            print("⚠️ Warning: 'requirements.txt' not found. Skipping dependency installation.")
        
        # Continue with the rest of the Dockerfile content
        dockerfile_content += f"""
COPY . /app/
EXPOSE {port}
CMD ["python", "app.py"]
"""

        # Write the Dockerfile content to a file
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        print("✅ Dockerfile created successfully.")

        # Build the Docker image
        image_name = input("Enter the Docker image name (default: my-app): ").strip() or "my-app"
        print(f"🐳 Building Docker image '{image_name}'...")
        result = subprocess.run(["docker", "build", "-t", image_name, "."], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to build Docker image: {result.stderr}")
            # Additional suggestion
            print("🔧 Possible fixes:")
            print("   - Ensure that all required build tools and libraries are installed.")
            print("   - Verify that the versions of the dependencies in 'requirements.txt' are compatible.")
            print("   - Try using an earlier version of Python or dependencies if the issue persists.")
            print("   - If you're using 'scikit-learn', try using a binary wheel instead of building from source.")
        else:
            print(f"✅ Docker image '{image_name}' built successfully.")
    
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# Example usage




def build_docker_image():
    """
    Build the Docker image.
    """
    image_name = input("Enter the Docker image name (default: my-app): ").strip() or "my-app"
    print(f"🐳 Building Docker image '{image_name}'...")
    try:
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
        print(f"✅ Docker image '{image_name}' built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build Docker image: {e}")
        sys.exit(1)

def create_docker_compose():
    """
    Create a docker-compose.yml file.
    """
    service_name = input("Enter the service name (default: app): ").strip() or "app"
    port = input("Enter the port to expose (default: same as application port): ").strip()
    if not port:
        # Attempt to read port from Dockerfile
        try:
            with open("Dockerfile", "r") as f:
                for line in f:
                    if line.startswith("EXPOSE"):
                        port = line.split()[1]
                        break
        except FileNotFoundError:
            print("❌ Dockerfile not found. Cannot determine port automatically.")
            sys.exit(1)
    compose_content = f"""version: '3.8'

services:
  {service_name}:
    build: .
    ports:
      - "{port}:{port}"
    volumes:
      - .:/app
    restart: unless-stopped
"""
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    print("✅ docker-compose.yml file created successfully.")

def main():
    banner()
    check_privileges()
    
    install_choice = input("Do you want to install Docker and Docker Compose? (y/n): ").strip().lower()
    if install_choice == 'y':
        install_docker()
        install_docker_compose()
        print("\n⏳ Verifying installations...")
        verify_docker_installation()
        verify_docker_compose_installation()
    else:
        print("⚠️ Skipping Docker installation.")

    project_setup = input("Do you want to set up a Dockerized project now? (y/n): ").strip().lower()
    if project_setup == 'y':
        clone_repo()
        project_type = input("Select project type (node/django/flask): ").strip().lower()
        if project_type == "node":
            create_dockerfile_node()
        elif project_type == "django":
            create_dockerfile_django()
        elif project_type == "flask":
            create_dockerfile_flask()
        else:
            print("❌ Invalid project type selected.")
            sys.exit(1)
        build_docker_image()
        create_docker_compose()
        print("\n🎉 All set! You can now run your application using Docker Compose:")
        print("👉 Command: docker-compose up -d")
    else:
        print("🚪 Exiting setup. Goodbye!")

if __name__ == "__main__":
    main()
