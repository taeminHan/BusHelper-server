import socket
import threading
from queue import Queue
import pymongo



def Send(send_queue):
    client = pymongo.MongoClient(
        "mongodb+srv://Main:1q2w3e4r@cluster0.dbjal.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('Register')
    col = db.get_collection('Login')
    print('Thread Send Start')
    while True:
        try:
            recv = send_queue.get()
            raddr = str(recv[1])
            if recv == 'Group Changed':
                print('Group Changed')
                break
            info = recv[0].split(':')
            print(info)
            category = str(info[0])
            if str(category[2:]) == 'login':  # 로그인
                doc = col.find({'ID': str(info[1]), 'PassWord': str(info[2])})  # MongoDB 로그인 정보 조회
                if list(doc):
                    msg = '1'
                    conn.sendto(msg.encode('utf-8'), (raddr[-21:-10], int(raddr[-7:-2])))
                else:
                    msg = '0'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
            elif str(category[2:]) == 'Register':  # 회원가입
                sign = {'ID': str(info[1]), 'PassWord': str(info[2]), 'Name': str(info[3]), 'CARD': str(info[4]),
                        'Phone': str(info[5])}
                col.insert_one(sign)
                doc = col.find(sign)
                if list(doc):
                    msg = '1'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
                else:
                    msg = '0'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
            elif str(category[2:]) == 'Register_ID':  # 아이디 중복 검사
                doc = col.find({'ID': str(info[1])})
                if list(doc):
                    msg = '0'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
                else:
                    msg = '1'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
        except:
            pass
def Register(conn):
    client = pymongo.MongoClient(
        "mongodb+srv://Main:1q2w3e4r@cluster0.dbjal.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('Register')
    col = db.get_collection('Login')
    print('Thread Send Start')
    while True:
        try:
            recv = send_queue.get()
            raddr = str(recv[1])
            if recv == 'Group Changed':
                print('Group Changed')
                break
            info = recv[0].split(':')
            print(info)
            category = str(info[0])
            if str(category[2:]) == 'login':  # 로그인
                doc = col.find({'ID': str(info[1]), 'PassWord': str(info[2])})  # MongoDB 로그인 정보 조회
                if list(doc):
                    msg = '1'
                    conn.sendto(msg.encode('utf-8'), (raddr[-21:-10], int(raddr[-7:-2])))
                else:
                    msg = '0'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
            elif str(category[2:]) == 'Register':  # 회원가입
                sign = {'ID': str(info[1]), 'PassWord': str(-info[2]), 'Name': str(info[3]), 'CARD': str(info[4]),
                        'Phone': str(info[5])}
                col.insert_one(sign)
                doc = col.find(sign)
                if list(doc):
                    msg = '1'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
                else:
                    msg = '0'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
            elif str(category[2:]) == 'Register_ID':  # 아이디 중복 검사
                doc = col.find({'ID': str(info[1])})
                if list(doc):
                    msg = '0'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
                else:
                    msg = '1'
                    conn.sendto(msg.encode(), (raddr[-21:-10], int(raddr[-7:-2])))
        except:
            pass

def Recv(conn, count, send_queue):
    print('Thread Recv' + str(count) + ' Start')
    while True:
        data = conn.recv(1024).decode()
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
            thread1 = threading.Thread(target=Send, args=(send_queue,))
            thread1.start()
            pass
        else:
            thread1 = threading.Thread(target=Send, args=(send_queue,))
            thread1.start()

        thread2 = threading.Thread(target=Recv, args=(conn, count, send_queue,))
        thread2.start()