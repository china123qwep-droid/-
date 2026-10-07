#这行代码可以扫描开放的端口，如果发现开放80端口，则询问是否发送请求，并输出目标网站的状态码和内容
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
target="192.0.0.1"
def scan_port(target,port):
#还是使用ipv4 tcp 连接好一点
    serve=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        serve.settimeout(3)
        serve.connect((target,port))
        # serve.sendall(example.encode("utf-8"))
        #data=serve.recv(1024)
        return port
        #print(data.decode("utf-8"),end="")     
    except socket.timeout:
        return None
    except ConnectionRefusedError:
        return None
    finally:
        serve.close()
port1=int(input("please input start port:"))
port2=int(input("\n please input end port:"))
if port1>port2 or port1<1 or port2>65535:
    raise ValueError("Invalid port range. Please enter a valid range between 1 and 65535.")
else:
    ports=list(range(port1,port2+1))
#使用threading模块，以20线程完成端口扫描
    with ThreadPoolExecutor(max_workers=20) as executor:
        results=executor.map(lambda port: scan_port(target,port),ports)
    open_ports=[port for port in results if port is not None ]
    print(f"open port:{open_ports}")
#如果80端口开放并且这个作为单独的代码而不是被用于模块的话，询问是否发送请求
if __name__=="__main__" and 80 in open_ports:
    print("do you want to send a request to the target? (y/n)")
    choice=input().lower()
    if choice=="y":
        session=requests.session()
        session.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        url=f"http://{target}"
        response=session.get(url,timeout=5)
#输出目标网站的状态码和内容，解码时忽略错误
        print(f"Response status code: {response.status_code}")
        print(f"\nResponse content: {response.content.decode('utf-8', errors='ignore')}")
        response.close()
    elif choice=="n":
        print("Request not sent.")
    else:
        print("Invalid choice. Request not sent.")






