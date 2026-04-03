import subprocess
import socket
import platform
import concurrent.futures

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    split_ip = my_ip.rfind('.')
    return my_ip[:split_ip + 1]

def check_ping(ip):
    my_system = platform.system()
    if my_system == "Windows":
        result = subprocess.run(['ping', '-n', '1', '-w', '500', ip], capture_output=True)
        if result.returncode == 0:
            return ip
    elif my_system == "Linux":
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True)
        if result.returncode == 0:
            return ip

def main():
    print("== Сканер Сетевых Устройств ==\n")
    
    my_ip = get_my_ip()
    all_ips = []
    
    for i in range(1, 255):
        ip = f"{my_ip}{i}"
        all_ips.append(ip)

    print(f"Ваша подсеть: {my_ip}0/24")
    print("Начинаю сканирование сети...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exe:
        results = exe.map(check_ping, all_ips)

    print("Найденные устройства: \n")
    for item in results:
        if item != None:
            print(item)
    
    print("\nСканирование завершено.")
    
if __name__ == "__main__":
    main()