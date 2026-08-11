import subprocess as sub
import base64
import os
import ctypes
import getpass

interactive_commands = ["su", "sudo", "ssh", "passwd", "nano", "vim", "vi", "top", "htop", "python", "python3"] # Interactive Commands Initial list
print("<PSPSHW?> For custom commands write 'pspsh help'.") # Help for new users

while True:
    cwd = os.getcwd() # get current directory
    user = getpass.getuser()
    try:
        com = input(f"<PSPSHW@{user} {cwd}> ")
    except KeyboardInterrupt:
        exit()

    # PSPSHW about commands
    if com.startswith('pspshw'):
        arg = com.split(' ', maxsplit=1)[1]
        if arg.lower() == "about":
            print('Python SubProcess SHell Wrapper: PSPSHW')
            print('PSPSHW is a shell-wrapper written in python using subprocess, os and base64 modules.')
            print("It's developed by runexpl and can be found under their pspshw repo on github.")
            print("It doesn't support a lot of edge-cases, be careful while using.\n")
            print("PSPSHW by runexpl on github.com/runexpl/pspshw")
        elif arg.lower() == "help" or arg.lower() == "--help":
            print('PSPSHW custom commands help\n----------------------------')
            print("write_file: simple file writing utility, write 'write_file help' for more information.")
            print("runc: C library function runner, write 'runc help' for more information")
            print('add_interactive_command: adds commands to a list that makes the terminal handle stdin,out and err itself.')
            print('remove_interactive_command: removes commands to a list that makes the terminal handle stdin,out and err itself.')
            print('add/remove_interactive_command accept multiple entries with coma separating or single entry.\n')
            print("PSPSHW by runexpl on github.com/runexpl/pspshw")
        continue
    
    # C library runner command
    if com.startswith("runc"):
        print("Warning RunC does not support filenames with spaces.")
        arg = com.split(' ', maxsplit=3)[1].strip().lower()
        arg2 = com.split(' ', maxsplit=3)[2].strip()
        arg3 = None
        try:
            arg3 = com.split(' ', maxsplit=3)[3].strip()
        except:
            arg3 = None
        if arg == 'help' or arg == '--help':
            print('runc is a function in PSPSHW to run C code using ctypes')
            print('usage:')
            print('runc [shared library path] [function name] [ignore path check (y/N)]')
            continue
        asklib = arg
        if not asklib.startswith('/'):
            asklib = cwd + "/" + asklib
        if not os.path.exists(asklib) and str(arg3).lower() != 'y' and str(arg3).lower() != 'yes':
            warn = input('<PSPSHW!!!> Warning, provided path does not exist, do you want to continue anyways? (Y/n):').lower()
            if warn == "no" or warn == "n":
                print("Execution cancelled.")
                continue
        try:
            lib = ctypes.CDLL(asklib)
            func = getattr(lib, arg2)
            result = func()
            print("exitcode/output: " + str(result))
        except Exception as e:
            print("<PSPSHW!!!> " + str(e))
        continue
        
    # Location handling
    if com.startswith('cd'):
        arg = com.split(' ', maxsplit=1)[1]
        try:
            os.chdir(arg)
        except Exception as e:
            print(f'<PSPSHW!!!> {str(e)}')
    
    if com.strip() == "":
        continue

    if com == "exit":
        exit()

    # Write_file Base64 writing function            
    def b64writing(file, bytespassed):
        try:
            filename = file
            if not file.startswith('/'):
                filename = cwd + "/" + file
            bytes = bytespassed
            with open(f'{filename}','wb') as f:
                f.write(base64.b64decode(bytes))
            print('wrote to ' + filename)
        except Exception as e:
            print(f'<PSPSHW!!!> {str(e)}')
    
    # Write_file Lines writing function
    def linewriting(file: str):
        filename = file
        if not file.startswith('/'):
            filename = cwd + "/" + file
        print("Start writing lines; write EOF to end writing")
        lines = []
        while True:
            line = input()
            if line.lower().strip() == "eof":
                break
            lines.append(line + "\n")
        try:
            with open(f'{filename}','w+') as f:
                f.writelines(lines)
            print("wrote to " + filename)
        except Exception as e:
            print(f'<PSPSHW!!!> {str(e)}')
    
    # Unified write_file function
    if com.startswith("write_file"):
        args = com.split(' ', maxsplit=3)
        arg1 = args[1].strip().lower()
        arg2 = args[2].strip()
        arg3 = None
        if arg1 == "base64":
            arg3 = args[3].strip()

        if arg1 == "help" or arg1 == '--help':
            print("write_file is PSPSHW's file writing function.")
            print("It allows to write files through it. It has two mods:")
            print("* lines: writing line by line")
            print("* base64: write base64 encoded bytes to the file\n")
            print("Usage:")
            print("    write_file [lines/base64] [filename] [(if base64) bytes]\n")
            print("    write_file help: displays this message")

        if arg1 == "lines":
            linewriting(arg2)
        elif arg1 == "base64":
            b64writing(arg2, arg3 if arg3 else b'')
        
        continue

    # Add commands from the interactive_commands list
    if com.startswith("add_interactive_command"):
        arg = "su"
        try:
            arg = com.split(' ')[1].strip()
            try:
                args = arg.split(',')
                for onearg in args:
                    interactive_commands.append(onearg)
                continue
            except:
                interactive_commands.append(arg)
        except:
            print("<PSPSHW!!!> add_interactive_command: ")
        continue

    # Remove commands from the interactive_commands list
    if com.startswith("remove_interactive_command"):
        arg = "su"
        try:
            arg = com.split(' ')[1].strip()
            try:
                args = arg.split(',')
                for onearg in args:
                    interactive_commands.remove(onearg)
                continue
            except:
                interactive_commands.remove(arg)
        except:
            print("<PSPSHW!!!> remove_interactive_command: ")
        continue
    
    # Handle Interactive commands
    comsplitted = None
    try:
        comsplitted = com.split(' ')[0]
    except:
        comsplitted = None
    if comsplitted in interactive_commands or com in interactive_commands:
        runcom = sub.run(com, shell=True)
        continue

    runcom = sub.run(
        com,
        shell=True,
        capture_output=True,
        text=True
        )
    
    if runcom.stdout:
        print(runcom.stdout)
        
    if runcom.stderr:
        print("<PSPSHW!!!> " + runcom.stderr)
exit()
