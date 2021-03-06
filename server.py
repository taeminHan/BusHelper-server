import socket
import threading
from queue import Queue
import pymongo
import re
import Api


def Send(send_queue, group):
    client = pymongo.MongoClient(
        "mongodb+srv://Main:1q2w3e4r@cluster0.dbjal.gcp.mongodb.net/<dbname>"
        "?retryWrites=true&w=majority")
    db = client.get_database('Register')
    col = db.get_collection('Login')

    while True:
        try:
            recv = send_queue.get()
            # 클라이언트 IP, PORT 정규식 표현으로 처리
            client_ip = re.findall(r"(?<=raddr=\(\')\w+\.\w+\.\w+\.\w+", str(recv[1]))
            client_port = re.findall(r'\w+(?=\)>)', str(recv[1]))
            client_ip = str(client_ip[0])
            client_port = int(client_port[0])
            if recv == 'Group Changed':
                print('Group Changed')
                break
            info = recv[0].split(':')
            category = info[0]
            # 로그인
            if re.findall(r"(login)$", category):
                # MongoDB 로그인 정보 조회
                if list(col.find({'ID': str(info[1]), 'PassWord': str(info[2])})):
                    msg = '1'  # True
                    conn.sendto(msg.encode('utf-8'), (client_ip, client_port))
                else:
                    msg = '0'  # False
                    conn.sendto(msg.encode('utf-8'), (client_ip, client_port))

            # 회원가입
            elif re.findall(r"(Register)$", category):
                sign = {'ID': str(info[1]), 'PassWord': str(info[2]), 'Name': str(info[4]),
                        'CARD':str(info[3]),'Age': str(info[5]), 'CARD':str(info[6]), 'Phone':str(info[7])}

                col.insert_one(sign)
                if list(col.find(sign)):
                    msg = '1'  # True
                    conn.sendto(msg.encode('utf-8'), (client_ip, client_port))
                else:
                    msg = '0'  # False
                    conn.sendto(msg.encode('utf-8'), (client_ip, client_port))

            elif re.findall(r"(Register_ID)$", category):  # 아이디 중복 검사
                if list(col.find({'ID': str(info[1])})):
                    msg = '1'  # True
                    conn.sendto(msg.encode('utf-8'), (client_ip, client_port))
                else:
                    msg = '0'  # False
                    conn.sendto(msg.encode('utf-8'), (client_ip, client_port))
            elif re.findall("CARD", category):  # 카드 단말기
                if info[1] == '1':
                    msg = 'BBIk'
                    for i in group:
                        i.send(msg.encode('utf-8'))
                else:
                    msg = 'end_BBIk'
                    for i in group:
                        i.send(msg.encode('utf-8'))
                client.close()
            elif re.findall(r"(Bus)$", category):
                start, end = str(info[1]), str(info[2])
                Run = Api.Bus()
                Run.FindStation(start, end)
                msg = Run.FindRoute()
                conn.send(msg.encode('utf-8'))
                print(conn)
            elif re.findall(r"(Cancel)$", category):
                col = db.get_collection('Bus')
                db.get_collection('Bus').delete_one({})
        except:
            pass


def Recv(conn, count, send_queue):
    print('Thread Recv' + str(count) + ' Start')
    while True:
        data = conn.recv(1024).decode('utf-8')
        send_queue.put([data, conn, count])
        print(data)


if __name__ == '__main__':

    send_queue = Queue()
    HOST = '172.30.1.27'
    PORT = 8080
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    count = 0
    group = []
    while True:
        count = count + 1
        conn, addr = server_sock.accept()
        group.append(conn)
        print('Connected ' + str(addr))
        if count > 1:
            thread1 = threading.Thread(target=Send, args=(send_queue, group,))
            thread1.start()
            pass
        else:
            thread1 = threading.Thread(target=Send, args=(send_queue, group,))
            thread1.start()

        thread2 = threading.Thread(target=Recv, args=(conn, count, send_queue,))
        thread2.start()
