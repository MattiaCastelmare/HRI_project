#include "ros/ros.h" // basic function of ROS
// #include "std_msgs/String.h" //standard messages in ROS
#include "first_tutorial/person_data.h"

// void writeMsgToLog(const std_msgs::String::ConstPtr& msg){
//     ROS_INFO("The message that we received was: %s", msg->data.c_str());
// }

void writeMsgToLog(const first_tutorial::person_data &person_data){
    ROS_INFO("Name: %s", person_data.name.c_str());
    ROS_INFO("Age: %i", person_data.age);
    ROS_INFO("Color: %s", person_data.color.c_str());
}

int main(int argc, char **argv){
    ros::init(argc, argv, "Subscriber"); //initialize the node
    ros::NodeHandle nh; //create the node
    
    ros::Subscriber topic_sub = nh.subscribe("tutorial", 1000, writeMsgToLog); // wri is the function called everytime a messages is received
    
    ros::spin();

    return 0;
}