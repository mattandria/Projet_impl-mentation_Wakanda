# We need OS operations for this
import os, select

## \brief Classe permettant de gerer la position du moteur
class eQEP(object):
    # Modes
    MODE_ABSOLUTE = 0
    MODE_RELATIVE = 1

    ## \brief Set the mode of the eQEP hardware
    # @param mode The mode of the eQEP hardware
    def set_mode(self, mode):
        attribute = open(self.path + "/mode", "w")  # Open the mode attribute file

        attribute.write(str(mode))  # Write the desired mode into the file

        attribute.close()   # Close the file

    ## \brief Get the mode of the eQEP hardware
    # @return The mode of the eQep hardware
    def get_mode(self):
        attribute = open(self.path + "/mode", "r")  # Open the attribute file

        mode = int(attribute.readline())    # Get the value

        attribute.close()   # Close the attribute

        return mode # Return the mode

    ## \brief Set the unit timer period of the eQEP hardware
    # @param period The unit timer period of the eQEP hardware
    def set_period(self, period):
        attribute = open(self.path + "/period", "w")    # Open the mode attribute file

        attribute.write(str(period))    # Write the desired mode into the file

        attribute.close()   # Close the file

    ## \brief Get the unit timer period of the eQEP hardware
    # @return The period of the eQep hardware
    def get_period(self):
        attribute = open(self.path + "/period", "r")    # Open the attribute file

        period = int(attribute.readline())  # Get the value

        attribute.close()   # Close the attribute

        return period   # Return the period

    ## \brief Set the current position of the encoder hardware
    # @param position The new position of the encoder hardware
    def set_position(self, position):
        attribute = open(self.path + "/position", "w")  # Open the mode attribute file

        attribute.write(str(position))  # Write the desired mode into the file

        attribute.close()   # Close the file

    ## \brief Get the immediate position of the encoder hardware
    # @return The immediate position of the encoder
    def get_position(self):
        attribute = open(self.path + "/position", "r")  # Open the attribute file

        position = int(attribute.readline())    # Get the value

        attribute.close()   # Close the attribute

        return position # Return the position

    ## \brief Poll the position, returns when new data is available
    # @return This position
    def poll_position(self):
        self.poller.poll(-1)    # Poll the position file

        os.lseek(self.fd, 0, 0) # Seek to the beginning of the file to get the data

        return int(os.read(self.fd, 16))    # Return the position

    ## \brief Constructor - specify the path and the mode
    # @param path The path of the encoder
    # @param mode The desired mode: 0 (MODE_ABSOLUTE), 1 (MODE_RELATIVE)
    def __init__(self, path, mode):
        self.path = path;   # Base path of the eQEP sysfs entry

        self.set_mode(mode) # Set the mode

        self.set_position(0)    # Reset the position

        self.fd = os.open(self.path + "/position", os.O_RDONLY, os.O_NONBLOCK)  # Setup polling system

        self.poller = select.poll() # Create the poll object
        self.poller.register(self.fd, select.POLLPRI)

    ## \brief Deconstructor
    def __del__(self):
        # Cleanup polling system
        self.poller.unregister(self.fd)
        os.close(self.fd)
