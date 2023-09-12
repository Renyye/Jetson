
while True:
    cmd = input("请输入操作指令, 1: 手动投喂, 2: 关闭自动投喂, 3: 终止程序\n")
    if cmd == '1':
        print("距离上次投喂猫已经过" + "分钟" + "秒")
        print("距离上次投喂狗已经过" + "分钟" + "秒")
        op = '0'
        while op != '1' or op != '2' or op != '3':
            op = input("请输入投喂对象, 1: 猫, 2: 狗, 3: 返回上级页面\n")
            if op == '1':
            # 控制猫粮投喂
                break
            elif op == '2':
            # 控制狗粮投喂
                break
            elif op == '3':
                break
                
    elif cmd == '2':
        # 关闭自动投喂
        print("自动投喂已关闭")
        pass
    
    elif cmd == '3':
        print("程序已终止")
        break