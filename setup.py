from subprocess import call

if __name__ == "__main__":
    call("pip install pyserial", shell=True)
    call("pip install smbus2", shell=True)
    call("pip install keras", shell=True)
    call("pip install tensorflow", shell=True)

    print "Setup complete"
