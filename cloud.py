import os
import subprocess

def banner():
    print("\n######################################################")
    print("#                                                    #")
    print("#  Docker & Docker Compose Setup by FancybearIN      #")
    print("#                                                    #")
    print("######################################################\n")

def command_exists(command):
    result = subprocess.run(f"where {command}", shell=True, capture_output=True)
    return result.returncode == 0

def install_package(package):
    subprocess.run(f"pip install {package}", shell=True)

def remove_packages():
    print("Removing old Docker and Docker Compose installations...")
    # Uninstall any existing Docker and Docker Compose packages
    subprocess.run("pip uninstall -y docker docker-compose", shell=True)

def install_docker():
    if not command_exists("docker"):
        print("Docker is not installed. Installing Docker...")
        install_package("docker")
    else:
        print("Docker is already installed.")

def install_docker_compose():
    if not command_exists("docker-compose"):
        print("Docker Compose is not installed. Installing Docker Compose...")
        install_package("docker-compose")
    else:
        print("Docker Compose is already installed.")

def start_docker():
    subprocess.run("docker ps -a", shell=True, check=True)

def start_docker_compose():
    subprocess.run("docker-compose ps -a", shell=True, check=True)

def clone_repo():
    username = os.getlogin()
    github_dir = os.path.join(f"C:\\Users\\{username}\\github")
    os.makedirs(github_dir, exist_ok=True)
    os.chdir(github_dir)

    url = input("Enter the GitHub or GitLab URL: ")
    subprocess.run(f"git clone {url}", shell=True)
    os.chdir(os.path.basename(url).replace('.git', ''))

def create_dockerfile_node():
    version_choice = input("Do you want to use the latest Node.js version or a specific version? (latest/specific): ")

    if version_choice == "latest":
        node_version = "node:latest"
    elif version_choice == "specific":
        node_version = f"node:{input('Enter the specific Node.js version: ')}"
    else:
        print("Invalid choice. Please enter 'latest' or 'specific'.")
        return

    workdir = input("Enter the working directory location (default: /app): ") or "/app"

    with open("Dockerfile", "w") as f:
        f.write(f"FROM {node_version}\n")
        f.write(f"WORKDIR {workdir}\n")
        f.write(f"COPY package.json package-lock.json {workdir}\n")
        f.write("RUN npm install\n")
        f.write(f"COPY . {workdir}\n")
        f.write('CMD ["npm", "start"]\n')

    print("Dockerfile created successfully!")

def create_dockerfile_django():
    version_choice = input("Do you want to use the latest Python version or a specific version? (latest/specific): ")

    if version_choice == "latest":
        python_version = "python:latest"
    elif version_choice == "specific":
        python_version = f"python:{input('Enter the specific Python version: ')}"
    else:
        print("Invalid choice. Please enter 'latest' or 'specific'.")
        return

    workdir = input("Enter the working directory location (default: /app): ") or "/app"

    with open("Dockerfile", "w") as f:
        f.write(f"FROM {python_version}\n")
        f.write(f"WORKDIR {workdir}\n")
        f.write("COPY requirements.txt /app\n")
        f.write("RUN pip install -r requirements.txt\n")
        f.write("COPY . /app\n")
        f.write('CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]\n')

    print("Dockerfile created successfully!")

def create_dockerfile_flask():
    version_choice = input("Do you want to use the latest Python version or a specific version? (latest/specific): ")

    if version_choice == "latest":
        python_version = "python:latest"
    elif version_choice == "specific":
        python_version = f"python:{input('Enter the specific Python version: ')}"
    else:
        print("Invalid choice. Please enter 'latest' or 'specific'.")
        return

    workdir = input("Enter the working directory location (default: /app): ") or "/app"

    with open("Dockerfile", "w") as f:
        f.write(f"FROM {python_version}\n")
        f.write(f"WORKDIR {workdir}\n")
        f.write("COPY requirements.txt /app\n")
        f.write("RUN pip install -r requirements.txt\n")
        f.write("COPY . /app\n")
        f.write('CMD ["flask", "run", "--host=0.0.0.0"]\n')

    print("Dockerfile created successfully!")

def build_docker_image(image_name="my-app"):
    subprocess.run(f"docker build -t {image_name} .", shell=True)
    print("Docker image built successfully!")

def create_docker_compose(service_name="app", port="3000"):
    with open("docker-compose.yml", "w") as f:
        f.write("version: '3.7'\n\n")
        f.write("services:\n")
        f.write(f"  {service_name}:\n")
        f.write("    build: .\n")
        f.write(f"    ports:\n")
        f.write(f"      - \"{port}:{port}\"\n")

    print("docker-compose.yml created successfully!")

def main():
    banner()

    answer = input("Do you want to run Service Docker and Docker Compose? (y/n): ").lower()
    if answer == "y":
        install_docker()
        install_docker_compose()
        start_docker()
        start_docker_compose()

    based = input("Project based on (node/django/flask): ").lower()

    if based == "node":
        clone_repo()
        create_dockerfile_node()
    elif based == "django":
        clone_repo()
        create_dockerfile_django()
    elif based == "flask":
        clone_repo()
        create_dockerfile_flask()
    else:
        print("Invalid option. Please choose 'node', 'django', or 'flask'.")
        return

    image_name = input("Enter the image name (default: my-app): ") or "my-app"
    build_docker_image(image_name)
    
    service_name = input("Enter the service name (default: app): ") or "app"
    port = input("Enter the port to expose (default: 3000): ") or "3000"
    create_docker_compose(service_name, port)

if __name__ == "__main__":
    main()
