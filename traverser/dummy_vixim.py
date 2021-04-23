# -*- coding: utf-8 -*-
"""
Connect to and control ViX microstepper drives
"""

# Standard library imports:
import random
import time
# Third party imports:
import serial

# Default motion values:
DEFAULT_VEL = 2
DEFAULT_ACCEL = 10
DEFAULT_DECEL = 10

class VixIM(object):
    """
    Connect to and control ViX IM device
    """
    def __init__(self, port=None, baud_rate=9600, timeout=1, drives=2,
                 vel=None, accel=None, decel=None, limits=None):
        """
        Init VixIM object
        """
        # Serial port / device:
        self.serial_port = port
        # Baud rate:
        self.baud_rate = baud_rate
        # Serial timeout:
        self.timeout = timeout
        # Connected status:
        self.serial_connected = False
        # Serial connection:
        self.serial_conn = None
        # Number of drives:
        self.drives = drives
        # Initial velocity setting:
        if not vel:
            vel = DEFAULT_VEL
        self.vel = vel
        # Initial acceleration and deceleration setting:
        if not accel:
            accel = DEFAULT_ACCEL
        self.accel = accel
        if not decel:
            decel = DEFAULT_DECEL
        self.decel = decel
        # Axes limits. If not specified, set a default:
        if not limits:
            self.limits = {
                1: 150000,
                2: 150000
            }
        else:
            self.limits = limits
        # Dict for storing status:
        self.status = {}
        # Init status information:
        for i in range(1, self.drives + 1):
            # Create dict:
            self.status[i] = {
                'status': 0,
                'pos': None,
                'vel': None,
                'accel': None,
                'decel': None,
                'limit': self.limits[i]
            }

    def __repr__(self):
        """
        Representation of the VixIM object
        """
        # Serial information:
        rep = '<ViX IM device, port={0}, baud rate={1}>'
        rep = rep.format(self.serial_port, self.baud_rate)
        # Return the representation:
        return rep

    def __str__(self):
        """
        Printable representation of the VixIM object
        """
        # Serial information:
        rep = '<ViX IM device, port={0}, baud rate={1}'
        rep = rep.format(self.serial_port, self.baud_rate, self.timeout)
        # Add drive information:
        for i in range(1, self.drives + 1):
            rep = rep + ', Drive {0} :: pos: {1}, vel: {2}, accel: {3}, '
            rep = rep + 'decel: {4}'
            rep = rep.format(i, self.status[i]['pos'], self.status[i]['vel'],
                             self.status[i]['accel'], self.status[i]['decel'])
            rep = rep + ', limit: {0}'
            rep = rep.format(self.status[i]['limit'])
        rep = rep + '>'
        # Return the representation:
        return rep

    def check_connect(self):
        """
        Check the serial connection:
        """
        # If not connected, give up:
        if not self.serial_connected:
            err_msg = 'Device {0} does not appear to be connected'
            err_msg = err_msg.format(self.serial_port)
            return False, err_msg
        # Otherwise, we appear to be connected:
        err_msg = 'Device {0} appears to be connected'
        err_msg = err_msg.format(self.serial_port)
        return True, err_msg

    def __check_conn_run(self, run_cmd, kwargs=None):
        """
        Check connection status, and run commands if o.k.
        """
        # Check the connection:
        conn_status, err_msg = self.check_connect()
        # If not connected, give up:
        if not conn_status:
            return False, err_msg
        # If no arguments:
        if not kwargs:
            # Run the command:
            status, err_msg = run_cmd()
        else:
            # Run the command with args:
            status, err_msg = run_cmd(**kwargs)
        # Return the output:
        return status, err_msg

    def connect(self):
        """
        Initiate serial connection
        """
        # If port and baud rate are not defined, give up:
        if not self.serial_port:
            # Return error message:
            err_msg = 'Device name / serial port not configured'
            return False, err_msg
        if not self.baud_rate:
            # Return error message:
            err_msg = 'Baud rate not configured'
            return False, err_msg
        # If already connected, return True:
        if self.serial_conn and self.serial_connected:
            # Return message:
            err_msg = 'Serial device appears to be connected'
            return True, err_msg
        # Try to connect over serial:
        try:
            # Create serial device:
            self.serial_conn = True
            # Set connected status:
            self.serial_connected = True
            # Return a message:
            err_msg = 'Connected to device at {0}'.format(self.serial_port)
            return True, err_msg
        except Exception as ex_ception:
            # Connection failed ... :
            self.serial_conn = None
            self.serial_connected = False
            # Return error message:
            err_msg = 'Connection Error : {0}'.format(ex_ception)
            return False, err_msg

    def __disconnect(self):
        """
        Close serial connection
        """
        # Update status:
        self.serial_conn = None
        self.serial_connected = False
        # Return a message:
        err_msg = 'Disconnected from device at {0}'
        err_msg = err_msg.format(self.serial_port)
        return True, err_msg

    def disconnect(self):
        """
        Close serial connection wrapper
        """
        # Check status and run command:
        status, err_msg = self.__check_conn_run(self.__disconnect)
        return status, err_msg

    def __serial_write(self, run_cmd, output=True):
        """
        Write a command to serial connection and optionally read one line of
        output
        """
        # Return:
        return 'Message written to serial device'

    def __drive_wait(self, drive=1, max_loop=5000):
        """
        Wait until drive is not moving and not busy
        """
        # Presume moving and busy:
        is_moving = 1
        is_ready = 1
        # Init loop count:
        loop_count = 0
        while is_moving != 0 and is_ready != 0 and loop_count < max_loop:
            # Check status of drive ...
            if loop_count < 3:
                is_moving = 1
                is_ready = 1
            else:
                is_moving = 0
                is_ready = 0
            # Increment the loop count:
            loop_count += 1
            # Wait and try again:
            time.sleep(0.01)
        # If things do not appear to be ready ... :
        if is_moving == 1 or is_ready == 1 or loop_count >= max_loop:
            # Return an error:
            err_msg = 'Drive does not appear to be ready'
            return False, err_msg
        # Else, device appears to be ready:
        err_msg = 'Drive appears to be ready'
        return True, err_msg

    def __send_msg(self, msg, drive=1, wait=True, output=True):
        """
        Send a message to the drive. Wait for completion if requested. Try to
        capture any output.
        """
        # If waiting:
        if wait:
            # Check drive is ready:
            dev_status, err_msg = self.__drive_wait(drive)
            # If things are not ready:
            if not dev_status:
                return dev_status, err_msg
        # Send the message:
        run_cmd = '{0}{1}'.format(drive, msg)
        cmd_out = self.__serial_write(run_cmd)
        # Create output message:
        serial_out = None
        # If waiting:
        if wait:
            # Wait for drive to be ready again:
            self.__drive_wait(drive)
        # Return any output:
        return True, serial_out

    def send_msg(self, msg, drive=1, wait=True, output=True):
        """
        Send a message to the drive wrapper
        """
        # Create a dict of arguments:
        f_args = {
            'msg': msg,
            'drive': drive,
            'wait': wait,
            'output': output
        }
        # Check conneciton and run:
        status, err_msg = self.__check_conn_run(self.__send_msg, f_args)
        return status, err_msg

    def __update_drive_status(self, drive=1):
        """
        Get status of drives and update
        """
        # Set a position if no current position set:
        if self.status[drive]['pos'] is None:
            self.status[drive]['pos'] = random.randrange(
                0, self.limits[drive]
            )
        # Set a velocity if no current velocity set:
        if self.status[drive]['vel'] is None:
            self.status[drive]['vel'] = self.vel
        # Set acceleration if no current acceleration set:
        if self.status[drive]['accel'] is None:
            self.status[drive]['accel'] = self.accel
        # Set deceleration if no current deceleration set:
        if self.status[drive]['decel'] is None:
            self.status[drive]['decel'] = self.decel
        # Return a message:
        err_msg = 'Drive {0} status updated'.format(drive)
        return True, err_msg

    def update_drive_status(self, drive=1):
        """
        Get status of drives and update wrapper
        """
        # Create a dict of arguments:
        f_args = {
            'drive': drive
        }
        # Check conneciton and run:
        status, err_msg = self.__check_conn_run(self.__update_drive_status,
                                                f_args)
        return status, err_msg

    def update_drives_status(self):
        """
        Get status of all drives
        """
        # For each drive:
        for i in range(1, self.drives + 1):
            # Update drive status:
            drive_status, err_msg = self.update_drive_status(i)
            # Check that worked ... :
            if not drive_status:
                # Return the error:
                return False, err_msg
        # Return True, no message:
        return True, None

    def start(self):
        """
        Connect via serial and initialise devices
        """
        # Connect via serial:
        ser_status, err_msg = self.connect()
        # Check status:
        if not ser_status:
            # Connection seems to have failed:
            return False, err_msg
        # Start up messages for each device. These are:
        #   * Switch device on
        #   * Stop device
        #   * Kill device
        #   * Set velocity
        #   * Set acceleration
        #   * Set deceleration
        #   * Go to position 0 (via continuous move)
        #   * Set position to 0
        start_msgs = [
            'ON',
            'S',
            'K',
            'V{0}'.format(self.vel),
            'AA{0}'.format(self.accel),
            'AD{0}'.format(self.decel),
            'MC',
            'H-',
            'V0.5',
            'G',
            'W(PA,0)'
        ]
        # For each drive:
        for i in range(1, self.drives + 1):
            # Otherwise, start things up. For each start up message:
            for start_msg in start_msgs:
                # Send the message and get status:
                cmd_status, err_msg = self.send_msg(msg=start_msg, drive=i)
                # If that failed ... :
                if not cmd_status:
                    # Return error message:
                    err_msg = err_msg + ' [{0}{1}]'
                    err_msg = err_msg.format(i, start_msg)
                    return False, err_msg
            # Update drive status:
            drive_status, err_msg = self.update_drive_status(i)
            # Check that worked ... :
            if not drive_status:
                # Return the error:
                return False, err_msg
            # Set 'status' to 1, to mark as active:
            self.status[i]['status'] = 1
            # Set position to 0:
            self.status[i]['pos'] = 0
        # Return a message:
        time.sleep(1)
        err_msg = 'Start up complete'
        return True, err_msg

    def __stop(self, switch_off=False):
        """
        Stop devices and optionally switch off
        """
        # Stop messages for each device. These are:
        #   * Stop drive
        #   * Switch device off (optional)
        if switch_off:
            stop_msgs = [
                'S',
                'OFF'
            ]
        else:
            stop_msgs = [
                'S'
            ]
        # For each drive:
        for i in range(1, self.drives + 1):
            # For each message:
            for stop_msg in stop_msgs:
                # Don't wait before stopping:
                if stop_msg == 'S':
                    wait = False
                else:
                    wait = True
                # Send the message and get status:
                cmd_status, err_msg = self.send_msg(msg=stop_msg, drive=i,
                                                    wait=wait)
                # If that failed ... :
                if not cmd_status:
                    # Return error message:
                    err_msg = err_msg + ' [{0}{1}]'
                    err_msg = err_msg.format(i, stop_msg)
                    return False, err_msg
            # Update drive status:
            self.update_drive_status(i)
            self.status[i]['status'] = 0
        # Return a message:
        err_msg = 'Stop complete'
        return True, err_msg

    def stop(self, switch_off=False):
        """
        Stop devices and disconnect wrapper
        """
        # Create a dict of arguments:
        f_args = {
            'switch_off': switch_off
        }
        # Check status and run command:
        status, err_msg = self.__check_conn_run(self.__stop, f_args)
        return status, err_msg

    def __go_home(self):
        """
        Tell devices to go home
        """
        # Go home messages for each drive
        #   * Stop drive
        #   * Go home via continuous move
        gh_msgs = [
            'S',
            'MC',
            'H-',
            'V0.5',
            'G'
        ]
        # For each drive:
        for i in range(1, self.drives + 1):
            # For each message:
            for gh_msg in gh_msgs:
                # Send the message and get status:
                cmd_status, err_msg = self.send_msg(msg=gh_msg, drive=i,
                                                    wait=False)
                # If that failed ... :
                if not cmd_status:
                    # Return error message:
                    err_msg = err_msg + ' [{0}{1}]'
                    err_msg = err_msg.format(i, gh_msg)
                    return False, err_msg
            # Set position to 0:
            self.status[i]['pos'] = 0
        # Return a message:
        err_msg = 'Go home in progress'
        return True, err_msg

    def go_home(self):
        """
        Tell devices to go home wrapper
        """
        # Check status and run command:
        status, err_msg = self.__check_conn_run(self.__go_home)
        return status, err_msg

    def __drive_go(self, drive=1, direction='f', vel=None, accel=None,
                   decel=None):
        """
        Set the drive going ...
        """
        # List for go messages:
        go_msgs = []
        # Current status velocity:
        curr_vel = self.status[drive]['vel']
        # If velocity is set and it doesn't match ... :
        if vel and vel != curr_vel:
            # Add velocity setting message:
            cmd_msg = 'V{0}'.format(vel)
            go_msgs.append(cmd_msg)
        # Current status accel:
        curr_accel = self.status[drive]['accel']
        # If accel is set and it doesn't match ... :
        if accel and accel != curr_accel:
            # Add accel setting message:
            cmd_msg = 'AA{0}'.format(accel)
            go_msgs.append(cmd_msg)
        # Current status decel:
        curr_decel = self.status[drive]['decel']
        # If decel is set and it doesn't match ... :
        if decel and decel != curr_decel:
            # Add decel setting message:
            cmd_msg = 'AD{0}'.format(accel)
            go_msgs.append(cmd_msg)
        # Add message to set direction:
        if direction == 'f':
            cmd_msg = 'H+'
            go_msgs.append(cmd_msg)
        else:
            cmd_msg = 'H-'
            go_msgs.append(cmd_msg)
        # Add message to set movement to continuous:
        cmd_msg = 'MC'
        go_msgs.append(cmd_msg)
        # For each message:
        for go_msg in go_msgs:
            # Send the message and get status:
            cmd_status, err_msg = self.send_msg(msg=go_msg, drive=drive)
            # If that failed ... :
            if not cmd_status:
                # Return error message:
                err_msg = err_msg + ' [{0}{1}]'
                err_msg = err_msg.format(drive, go_msg)
                return False, err_msg
        # Set things moving:
        cmd_msg = 'G'
        inc_dist = 0.05 * self.status[drive]['limit']
        if direction == 'b':
            inc_dist = inc_dist * -1
        new_pos = round(
            self.status[drive]['pos'] + inc_dist
        )
        if new_pos > self.status[drive]['limit']:
            new_pos = self.status[drive]['limit']
        if new_pos < 0:
            new_pos = 0
        self.status[drive]['pos'] = new_pos
        # Send the message and get status:
        cmd_status, err_msg = self.send_msg(msg=cmd_msg, drive=drive,
                                            wait=False)
        # If that failed ... :
        if not cmd_status:
            # Return error message:
            err_msg = err_msg + ' [{0}{1}]'
            err_msg = err_msg.format(drive, cmd_msg)
            return False, err_msg
        # Return a message:
        err_msg = 'Drive {0} is moving'.format(drive)
        return True, err_msg

    def drive_go(self, drive=1, direction='f', vel=None, accel=None,
                 decel=None):
        """
        Set the drive going wrapper ...
        """
        # Create a dict of arguments:
        f_args = {
            'drive': drive,
            'direction': direction,
            'vel': vel,
            'accel': accel,
            'decel': decel
        }
        # Check connection and run:
        status, err_msg = self.__check_conn_run(self.__drive_go, f_args)
        return status, err_msg

    def __drive_goto(self, drive=1, pos=0, vel=None, accel=None,
                   decel=None):
        """
        Set the drive going to specified location
        """
        # Update drive status first:
        self.update_drive_status(drive)
        # List for set up messages:
        go_msgs = []
        # Current status velocity:
        curr_vel = self.status[drive]['vel']
        # If velocity is set and it doesn't match ... :
        if vel and vel != curr_vel:
            # Add velocity setting message:
            cmd_msg = 'V{0}'.format(vel)
            go_msgs.append(cmd_msg)
        # Current status accel:
        curr_accel = self.status[drive]['accel']
        # If accel is set and it doesn't match ... :
        if accel and accel != curr_accel:
            # Add accel setting message:
            cmd_msg = 'AA{0}'.format(accel)
            go_msgs.append(cmd_msg)
        # Current status decel:
        curr_decel = self.status[drive]['decel']
        # If decel is set and it doesn't match ... :
        if decel and decel != curr_decel:
            # Add decel setting message:
            cmd_msg = 'AD{0}'.format(accel)
            go_msgs.append(cmd_msg)
        # Add message to set movement to incremental:
        cmd_msg = 'MI'
        go_msgs.append(cmd_msg)
        # Work out distance to travel:
        dist = pos - self.status[drive]['pos']
        # Add message to set distance:
        cmd_msg = 'D{0}'.format(dist)
        go_msgs.append(cmd_msg)
        # For each message:
        for go_msg in go_msgs:
            # Send the message and get status:
            cmd_status, err_msg = self.send_msg(msg=go_msg, drive=drive)
            # If that failed ... :
            if not cmd_status:
                # Return error message:
                err_msg = err_msg + ' [{0}{1}]'
                err_msg = err_msg.format(drive, go_msg)
                return False, err_msg
        # Set things moving:
        cmd_msg = 'G'
        # Update position:
        self.status[drive]['pos'] = pos
        # Send the message and get status:
        cmd_status, err_msg = self.send_msg(msg=cmd_msg, drive=drive,
                                            wait=True)
        # If that failed ... :
        if not cmd_status:
            # Return error message:
            err_msg = err_msg + ' [{0}{1}]'
            err_msg = err_msg.format(drive, cmd_msg)
            return False, err_msg
        # Return a message:
        err_msg = 'Drive {0} moved to {1}'.format(drive, pos)
        return True, err_msg

    def drive_goto(self, drive=1, pos=0, vel=None, accel=None,
                 decel=None):
        """
        Set the drive going wrapper ...
        """
        # Create a dict of arguments:
        f_args = {
            'drive': drive,
            'pos': pos,
            'vel': vel,
            'accel': accel,
            'decel': decel
        }
        # Check connection and run:
        status, err_msg = self.__check_conn_run(self.__drive_goto, f_args)
        # Update status and return:
        self.update_drive_status(drive)
        return status, err_msg

    def __drive_stop(self, drive=1):
        """
        Stop the drive ...
        """
        # Stop the drive:
        cmd_msg = 'S'
        # Send the message and get status:
        cmd_status, err_msg = self.send_msg(msg=cmd_msg, drive=drive,
                                            wait=False)
        # If that failed ... :
        if not cmd_status:
            # Return error message:
            err_msg = err_msg + ' [{0}{1}]'
            err_msg = err_msg.format(drive, cmd_msg)
            return False, err_msg
        # Return a message:
        err_msg = 'Drive {0} stopped'.format(drive)
        return True, err_msg

    def drive_stop(self, drive=1):
        """
        Stop the drive wrapper ...
        """
        # Create a dict of arguments:
        f_args = {
            'drive': drive
        }
        # Check connection and run:
        status, err_msg = self.__check_conn_run(self.__drive_stop, f_args)
        # Update drive status:
        self.update_drive_status(drive)
        return status, err_msg
