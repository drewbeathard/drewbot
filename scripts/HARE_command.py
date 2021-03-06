#!/usr/bin/env python

# Single HARECommand
# Publishes single MotorCommand 
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Point, Twist
from ros_pololu_servo.msg import MotorCommand
from ros_pololu_servo.msg import HARECommand

steering_cmd_msg = MotorCommand()
motor_cmd_msg = MotorCommand()

def cmd_cb( msg ):
    #globals steering_cmd_msg , motor_cmd_msg

    # Limit incoming message to steering limits
    max_angle = .78
    if msg.steering_angle > max_angle:
        msg.steering_angle = max_angle
    elif msg.steering_angle < -max_angle:
        msg.steering_angle = -max_angle

    steering_cmd_msg.position = msg.steering_angle

    # Limit the incoming throttle command
    # max_throttle = 1000
    # if msg.throttle_cmd > max_throttle:
    #     msg.throttle_cmd = max_throttle
    # elif msg.throttle_cmd < -max_throttle:
    #     msg.throttle_cmd = -max_throttle

    # Handle throttle mode
    # if msg.throttle_mode == 0:
    #     motor_cmd_msg.position = 0.0
    # elif msg.throttle_mode == 3:
    #     motor_cmd_msg.position = -1*msg.throttle_cmd
    # else:
    #     motor_cmd_msg.position = msg.throttle_cmd
    motor_cmd_msg.position = msg.throttle_cmd * -1


def msg_publisher():
    #globals steering_cmd_msg , motor_cmd_msg

    cmd_sub = rospy.Subscriber('/HARE_high_level_command', HARECommand, cmd_cb )
    msg_pub = rospy.Publisher('/pololu/command', MotorCommand, queue_size=10)
    rospy.init_node('cmd_publisher', anonymous=True)
    pub_rate = rospy.Rate(20)
    #cmd_msg = MotorCommand()

    motor_cmd_msg.joint_name = "drive_motor"
    motor_cmd_msg.position = 0
    motor_cmd_msg.speed = 1.0
    motor_cmd_msg.acceleration = 1.0

    steering_cmd_msg.joint_name = "steering_servo"
    steering_cmd_msg.position = 0.0
    steering_cmd_msg.speed = 1.0
    steering_cmd_msg.acceleration = 1.0


    while not rospy.is_shutdown():
        msg_pub.publish(motor_cmd_msg)
        msg_pub.publish(steering_cmd_msg)
        pub_rate.sleep()

if __name__ == '__main__':
    
    try:
        msg_publisher()
    except rospy.ROSInterruptException:
        print('Shutting down publisher...')
        pass
