// JOYSTICK -> HARE pub sub

// subscribes to /joy topic
// publishes to HARE_high_level_command topic
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include <ros_pololu_servo/HARECommand.h>
class TeleopCar
{
public:
  TeleopCar();

private:
  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);

  ros::NodeHandle nh_;

  int linear_, angular_;
  double l_scale_, a_scale_;
  ros::Publisher vel_pub_;
  ros::Subscriber joy_sub_;

};


TeleopCar::TeleopCar():
  linear_(1),
  angular_(2)
{

  nh_.param("axis_angular", angular_, angular_);
  nh_.param("axis_linear", linear_, linear_);
  nh_.param("scale_angular", a_scale_, a_scale_);
  nh_.param("scale_linear", l_scale_, l_scale_);


  vel_pub_ = nh_.advertise<ros_pololu_servo::HARECommand>("HARE_high_level_command", 1);


  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 10, &TeleopCar::joyCallback, this);

}

void TeleopCar::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
  ros_pololu_servo::HARECommand harecommand;
  harecommand.steering_angle = a_scale_*joy->axes[0];
  // harecommand.throttle_cmd = (.5 * joy->axes[2]) - (.5 * joy->axes[5]);
  harecommand.throttle_cmd = (.5*joy->axes[5])+((-.5 * joy->axes[2]));
  harecommand.throttle_mode = 0;

  // twist.angular.z = a_scale_*joy->axes[angular_];
  // twist.linear.x = l_scale_*joy->axes[linear_];
  vel_pub_.publish(harecommand);
}


int main(int argc, char** argv)
{
  ros::init(argc, argv, "teleop_car");
  TeleopCar teleop_car;

  ros::spin();
}