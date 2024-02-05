#include "ros/ros.h" // basic function of ROS
// #include "std_msgs/String.h" //standard messages in ROS
#include "first_tutorial/person_data.h"



int main(int argc, char **argv){
    ros::init(argc, argv, "Publisher"); //first node, its name is "Publisher" initialization
    ros::NodeHandle nh; //this starts a node

    //ros::Publisher topic_pub = nh.advertise<std_msgs::String>("tutorial", 1000); // create the Publisher 
    ros::Publisher topic_pub = nh.advertise<first_tutorial::person_data>("tutorial", 1000); // create the Publisher 
    ros::Rate loop_rate(1); // how ofter we are going to create our messages 1second

    while(ros::ok()) {// until our nodes do not crash or we press Ctrl + C
        //std_msgs::String msg;
        //msg.data = "CIAO ECCHIME";

        first_tutorial::person_data person_data;
        person_data.name = "Mattia Castelmare";
        person_data.age = 25;
        person_data.color = "Red";

        // topic_pub.publish(msg); // it publishes to the topic "tutorial"
        topic_pub.publish(person_data); // it publishes to the topic "tutorial"
        ros::spinOnce();
        loop_rate.sleep();

    }

    return 0;
}