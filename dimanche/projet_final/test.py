import sysv_ipc

mq_don=sysv_ipc.MessageQueue(666,sysv_ipc.IPC_CREAT)

for i in range(100):
    mq_don.send("coucou".encode())



tt=mq_don.current_messages
print(type(mq_don))
print(type(tt))
print("ICICCCC ", tt)