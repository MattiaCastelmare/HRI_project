#include "ros/ros.h" // basic function of ROS
#include "first_tutorial/AddTwoInts.h"

bool add(first_tutorial::AddTwoInts::Request &req, first_tutorial::AddTwoInts::Response &res){
    res.sum = req.a + req.b;
    return true;
}


int main(int argc, char **argv){
    ros::init(argc, argv, "Service_Node"); //initialize the node
    ros::NodeHandle nh; //create the node
    
    ros::ServiceServer service = nh.advertiseService("add_two_ints", add);
    
    ros::spin();

    return 0;
}