import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from primrose_interfaces.msg import TellTails, TellTail

from .TopicTracker import TopicTracker

tell_tall_names = [
    "main_battery_warning", "motor_temp", "suspension_actuators",
    "suspension_transit", "controller_temp", "tilt_warning",
    "check_engine", "high_battery_charge", "spot_turning",
    "charging", "auto_trench", "battery_fault",
    "cruise_control", "conveyor"

]


class SystemDiagnosticsRoutine(Node):

    def __init__(self):
        super().__init__('SystemDiagnosticsRoutine')
        self.tell_tails = TopicTracker(self, "system_diagnostics/tell_tails", TellTails,
                                       is_publisher=True)
        self.get_logger().info("SystemDiagnosticsRoutine initialized")
        self.timer = self.create_timer(0.2, self.main)

    def main(self):
        msg = TellTails()
        for name in tell_tall_names:
            msg.tell_tails.append(TellTail(name=name, color=0, hover_text="No Data", flashing=True))
        self.tell_tails.value = msg


def main(args=None):
    rclpy.init(args=args)

    sdr = SystemDiagnosticsRoutine()

    rclpy.spin(sdr)

    sdr.destroy_node()
    rclpy.shutdown()
