import socket
import getpass
import base64

#Criando a conexão TCP com o servidor usando a porta do SMTP
serverName = "mail.labredes.info"
serverPort = 587
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((serverName, serverPort))
recv = tcp.recv(1024)

recv = recv.decode()

if recv[:3] != '220':
    print('\nResposta não recebida pelo servidor.')

#Executando o comando Helo para acessar a caixa de e-mail
heloCommand = 'HELO Lab\r\n'
tcp.send(heloCommand.encode())
recv = tcp.recv(1024)
recv = recv.decode()

if recv[:3] != '250':
    print('\nResposta não recebida pelo servidor.')
else:
    print('\nConexão estabelecida')



#Realizando autenticação do usuário
def loginSM():

    global username

    username = input("\nEntre com seu e-mail: ")
    password = getpass.getpass(prompt='\nPassword: ', stream=None)

    base64_str = ("\x00"+username+"\x00"+password).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    tcp.send(authMsg)
    recv_auth = tcp.recv(1024)

    recv = (recv_auth.decode())

    if (recv[:3] != '235'):
        print('\nResposta não recebida do servidor.')

#Função para enviar o e-mail
def enviarEmail():

    contenttype = "text/plain" #informando para o servidor que o conteúdo se trata de um texto simples
    fromaddress = username
    toaddress = input('\nDigite o destinatário: ')
    subject = input('\nDigite o assunto: ')
    msg = input('\nDigite a mensagem: ')
    endmsg = "\r\n.\r\n"

    
    # Enviando o comando MAIL FROM e imprimindo a resposta do servidor casou houver erro.
    tcp.sendall(('MAIL FROM: <'+fromaddress+'>\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('\nResposta não recebida do servidor.')
    

    # Enviando o comando RCPT e imprimindo a resposta do servidor casou houver erro.
    tcp.sendall(('RCPT TO: <'+toaddress+'>\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('\nResposta não recebida do servidor.')


    # Enviando o comando DATA e imprimindo a resposta do servidor casou houver erro.
    tcp.send(('DATA\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '354'):
        print('Resposta não recebida do servidor')


    #Enviando dados da mensagem para o destinatário
    message = 'from:' + fromaddress + '@labredes.info' + '\r\n'
    message += 'to:' + toaddress + '\r\n'
    message += 'subject:' + subject + '\r\n'
    message += 'Content-Type:' + contenttype + '\r\n'
    message += '\r\n' + msg
    tcp.sendall(message.encode())


    #Informando o fim da mensagem para o servidor e imprimindo a resposta caso houver erro
    tcp.sendall(endmsg.encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('Resposta não recebida do servidor')
    else:
        print('\nMensagem enviada com sucesso!\n')

    tcp.sendall('QUIT\r\n'.encode())

loginSM()

enviarEmail()

tcp.close()