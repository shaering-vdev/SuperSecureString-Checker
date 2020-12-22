import subprocess

def powershellRun(filename):
    process = subprocess.Popen('powershell.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(filename.encode('utf-8'))
    return out

def encryptPassword(password):
    command = '''$x = (convertto-securestring -string "%s" -asplaintext -force | convertfrom-securestring)
    write-host $x''' % password
    out = powershellRun(command)
    output = (([x.decode("utf8") for x in out.split(b"write-host $x")])[1].split("\n"))[0]
    secureString = output
    return secureString

def decryptPassword(securePassword):
    command = '''
    $secureObject = ConvertTo-SecureString -String %s
    $decrypted = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureObject)
    $decrypted = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($decrypted)
    write-host $decrypted
    ''' % securePassword
    out = powershellRun(command)
    output = (([x.decode("utf8") for x in out.split(b"$decrypted\n")])[1].split("\n"))[0]
    return output

def testEncrypt(password,iterations):
    toEncrypt = [None] * (iterations +1)
    toDecrypt = [None] * (iterations +1)
    toEncrypt[0] = password
    for i in range(0,iterations):
        toEncrypt[i+1] = encryptPassword(toEncrypt[i])
    toDecrypt[0] = toEncrypt[iterations]
    for j in range(0, iterations):
        toDecrypt[j+1] = decryptPassword(toDecrypt[j])
    print("This is your password encrypted " + str(iterations) + " times: ")
    print(toDecrypt[0])
    print("This is your original password after being decrypted " + str(iterations) + " times: ")
    print(toDecrypt[iterations])
    
def main():
    keeper=0
    while keeper==0:
        userPass = input("Please enter a password:\n")
        userCount = input("How many times should we encrypt it?\n")
        testEncrypt(userPass,int(userCount))
        quitme = input("Type 'quit' to stop")
        if quitme == "quit":
            keeper += 1
            
main()
