import bluetooth # for bluetooth comm
import pyautogui # for sending input commands to os

# initial setup runs here
def initSetup():
    # set pyautogui pause to 0
    pyautogui.PAUSE = 0.0

# this will handle requests to move the cursor
def moveCursor(cordsStr):
    # splice the string and convert to integer to get the cords
    # the data wil come in like this:
    # XXXXYYYY
    # we'll seperate the X parts and Y parts
    # where the x parts are [0:4] and y parts are [4:]
    xCord = int(cordsStr[0:4])
    yCord = int(cordsStr[4:])
    # NOTE THAT X AND Y CORD ARE CHANGES IN POSITION, NOT ABSOLUTE POSITION
    # for debugging only - print out the spliced result
    print ("Result of splice:\n")
    print(xCord, " ", yCord, "\n")
    # move the cursor on the screen
    pyautogui.moveRel(xCord, yCord)
    print("Sent command to move cursor to relative coords: ", str(xCord),
          " ", str(yCord))

#this will run to handle button requests
def btnEvent(btnCom):
    # data comes in like this:
    # [L\R][D\U]
    # where first char indicates left or right
    # and second char indicates down or up event
    # check if its a right or left button event and store it
    # for when the command is invoked
    btn = ""
    if (btnCom[0] == 'L'):
        btn = "left"
    elif (btnCom[0] == 'R'):
        btn = 'right'
    # run up or down event based on the request data
    if (btnCom[1] == 'U'):
        pyautogui.mouseUp(None,None,btn)
        print("Sent command for ", btn, " button up")
    elif (btnCom[1] == 'D'):
        pyautogui.mouseDown(None,None,btn)
        print("Sent command for ", btn, " button down")

# this will interpret message requests
def msgHandle(sentData):
    #data comes in like this:
    # i(msgData)
    # where i is char that indicates msg type and 
    # (msgData) is any length of string that contains data for the
    # command
    sent = sentData
    # check the type of mesage by checking the first character
    # of the data string
    msgType = sent[0]
    # extract the data from the string
    msgData = sent[1:]
    if (msgType == "m"): # if its m, its a command to move cursor
        #take the msg data and send it to the movement handling function
        moveCursor(msgData)
    elif (msgType == "b"): # if its b, its a button command
        btnEvent(msgData)
    
# this part starts the Bt TrackPad Server
def runServer():
    # run initial setup stuff
    initSetup()
    # make a bluetooth socket for receiving commands
    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    #mac address of the BT adapter
    macBAAddress = '90:48:9a:10:4e:94'
    manID = 93 # id of device

    # port for communication
    port = bluetooth.PORT_ANY
    # max listeners
    maxBackLog = 2

    # byte size
    size = 1

    # start listening
    bindData = (macBAAddress, port)
    socket.bind(bindData)
    socket.listen(maxBackLog)
    # socket should be listening on this point

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    # uuids

    #advertise itself
    bluetooth.advertise_service( socket, "LAPTOP1",
                       service_id = uuid,
                       service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                       profiles = [ bluetooth.SERIAL_PORT_PROFILE ])

while (True): # keep listening for connections so script
    # doesn't have to restart
        try:
            print("Started listening on BT socket...\n")
            # accept incoming connection
            client, info = socket.accept()
            print("Accepted connection\n")
            # keeps track of iterations
            i = 0
            # string to store data
            s = ""
            # keeps track of count for the loop below
            while 1:
                data = client.recv(size)
                # decode the data into strings to add to string of message
                data = data.decode("utf-8")
                # and terminate this current accumulation if null char ('\0') is encountered or string is too long
                if (data == '\0' or i >= 14):
                    print(s)
                    i = 0 # reset accumulator
                    # interpret the message
                    msgHandle(s)
                    s = "" # reset variable that stores string
                else:
                    s += data
                # accumulate
                i += 1
        except:
            print("connection failure\n")
            print('\n')
            
        # close client connection
        client.close()

