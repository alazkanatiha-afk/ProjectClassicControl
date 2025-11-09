import pygame
import time
import serial
import math
import threading
from dataclasses import dataclass
from typing import Optional

@dataclass
class FlightCommand:
    """Flight command structure"""
    throttle: float = 0.0    # 0-1
    roll: float = 0.0        # -1 to 1
    pitch: float = 0.0       # -1 to 1  
    yaw: float = 0.0         # -1 to 1
    arm: bool = False
    mode: str = "MANUAL"

class XboxController:
    """Xbox controller input handler"""
    
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.controller = None
        self.running = False
        
        # Controller mapping (Xbox One controller)
        self.AXIS_LEFT_X = 0      # Roll
        self.AXIS_LEFT_Y = 1      # Pitch
        self.AXIS_RIGHT_X = 3     # Yaw
        self.AXIS_RT = 5          # Throttle (right trigger)
        self.AXIS_LT = 4          # Throttle down (left trigger)
        
        # Button mapping
        self.BUTTON_A = 0         # Arm/Disarm
        self.BUTTON_B = 1         # Emergency stop
        self.BUTTON_Y = 3         # Mode switch
        self.BUTTON_START = 7     # Start/Stop system
        
    def connect(self):
        """Connect to Xbox controller"""
        if pygame.joystick.get_count() == 0:
            print("No controller found!")
            return False
            
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        print(f"Connected to: {self.controller.get_name()}")
        return True
        
    def read_inputs(self) -> FlightCommand:
        """Read controller inputs and return flight command"""
        pygame.event.pump()
        
        if not self.controller:
            return FlightCommand()
            
        # Read analog sticks (with deadzone)
        def apply_deadzone(value, deadzone=0.1):
            return value if abs(value) > deadzone else 0.0
            
        # Roll (left stick X)
        roll = apply_deadzone(self.controller.get_axis(self.AXIS_LEFT_X))
        
        # Pitch (left stick Y, inverted)
        pitch = apply_deadzone(-self.controller.get_axis(self.AXIS_LEFT_Y))
        
        # Yaw (right stick X)
        yaw = apply_deadzone(self.controller.get_axis(self.AXIS_RIGHT_X))
        
        # Throttle (right trigger - left trigger)
        rt = (self.controller.get_axis(self.AXIS_RT) + 1) / 2  # Convert -1,1 to 0,1
        lt = (self.controller.get_axis(self.AXIS_LT) + 1) / 2
        throttle = max(0, rt - lt)  # Net throttle
        
        # Buttons
        arm = self.controller.get_button(self.BUTTON_A)
        emergency = self.controller.get_button(self.BUTTON_B)
        
        # Mode switching
        mode = "MANUAL"
        if self.controller.get_button(self.BUTTON_Y):
            mode = "STABILIZE"
            
        return FlightCommand(
            throttle=throttle,
            roll=roll,
            pitch=pitch,
            yaw=yaw,
            arm=arm and not emergency,
            mode=mode
        )

class FlightController:
    """Interface to flight controller board"""
    
    def __init__(self, port="/dev/ttyUSB0", baudrate=57600):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.armed = False
        
    def connect(self):
        """Connect to flight controller via serial"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to flight controller on {self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to flight controller: {e}")
            return False
            
    def send_command(self, cmd: FlightCommand):
        """Send flight command to aircraft"""
        if not self.serial_conn:
            return
            
        # Create MAVLink-style command (simplified)
        # In real implementation, use proper MAVLink protocol
        command_string = f"RC {int(cmd.throttle*1000)} {int(cmd.roll*500+1500)} {int(cmd.pitch*500+1500)} {int(cmd.yaw*500+1500)} {int(cmd.arm)}\n"
        
        try:
            self.serial_conn.write(command_string.encode())
        except Exception as e:
            print(f"Error sending command: {e}")
            
    def arm_aircraft(self, arm: bool):
        """Arm/disarm the aircraft"""
        self.armed = arm
        arm_cmd = "ARM\n" if arm else "DISARM\n"
        if self.serial_conn:
            self.serial_conn.write(arm_cmd.encode())

class SafetySystem:
    """Safety monitoring and failsafe system"""
    
    def __init__(self):
        self.last_command_time = time.time()
        self.failsafe_triggered = False
        self.max_command_gap = 0.5  # 500ms max gap between commands
        
    def update(self, cmd: FlightCommand) -> FlightCommand:
        """Update safety system and apply failsafes"""
        current_time = time.time()
        
        # Check for command timeout
        if current_time - self.last_command_time > self.max_command_gap:
            if not self.failsafe_triggered:
                print("FAILSAFE: Command timeout - reducing throttle")
                self.failsafe_triggered = True
            
            # Apply failsafe - reduce throttle, level aircraft
            cmd.throttle = min(cmd.throttle, 0.3)
            cmd.roll = cmd.roll * 0.5
            cmd.pitch = cmd.pitch * 0.5
            
        else:
            self.failsafe_triggered = False
            
        self.last_command_time = current_time
        return cmd

class AircraftControlSystem:
    """Main control system"""
    
    def __init__(self):
        self.controller = XboxController()
        self.flight_controller = FlightController()
        self.safety = SafetySystem()
        self.running = False
        self.armed = False
        
    def initialize(self):
        """Initialize all systems"""
        print("Initializing Aircraft Control System...")
        
        if not self.controller.connect():
            return False
            
        if not self.flight_controller.connect():
            print("Warning: Flight controller not connected - running in simulation mode")
            
        print("System initialized successfully!")
        return True
        
    def run(self):
        """Main control loop"""
        self.running = True
        print("Starting control loop...")
        print("Controls:")
        print("  Left Stick: Roll/Pitch")
        print("  Right Stick X: Yaw") 
        print("  Right Trigger: Throttle Up")
        print("  Left Trigger: Throttle Down")
        print("  A Button: Arm/Disarm")
        print("  B Button: Emergency Stop")
        print("  Y Button: Stabilize Mode")
        print("  START Button: Exit")
        
        try:
            while self.running:
                # Read controller inputs
                cmd = self.controller.read_inputs()
                
                # Apply safety systems
                cmd = self.safety.update(cmd)
                
                # Handle arming
                if cmd.arm and not self.armed:
                    print("ARMING AIRCRAFT")
                    self.armed = True
                    self.flight_controller.arm_aircraft(True)
                elif not cmd.arm and self.armed:
                    print("DISARMING AIRCRAFT")
                    self.armed = False
                    self.flight_controller.arm_aircraft(False)
                
                # Only send flight commands when armed
                if self.armed:
                    self.flight_controller.send_command(cmd)
                
                # Display status
                status = f"Armed: {self.armed} | Throttle: {cmd.throttle:.2f} | Roll: {cmd.roll:.2f} | Pitch: {cmd.pitch:.2f} | Yaw: {cmd.yaw:.2f}"
                print(f"\r{status}", end="", flush=True)
                
                # Check for exit
                if self.controller.controller.get_button(self.controller.BUTTON_START):
                    break
                    
                time.sleep(0.02)  # 50Hz update rate
                
        except KeyboardInterrupt:
            print("\nShutdown requested...")
            
        finally:
            self.shutdown()
            
    def shutdown(self):
        """Shutdown system safely"""
        print("\nShutting down...")
        if self.armed:
            self.flight_controller.arm_aircraft(False)
        
        if self.flight_controller.serial_conn:
            self.flight_controller.serial_conn.close()
            
        pygame.quit()
        self.running = False

# Example usage
if __name__ == "__main__":
    system = AircraftControlSystem()
    
    if system.initialize():
        system.run()
    else:
        print("Failed to initialize system")