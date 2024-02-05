#include "ros/ros.h" // basic function of ROS
#include "first_tutorial/AddTwoInts.h"



int main(int argc, char **argv){
    ros::init(argc, argv, "Addition_Service_Client_Node"); //initialize the node
    ros::NodeHandle nh; //create the node
    
    ros::ServiceClient client = nh.serviceClient<first_tutorial::AddTwoInts>("add_two_ints");

    first_tutorial::AddTwoInts srv;
    srv.request.a = 2;
    srv.request.b = 4;

    if(client.call(srv)){
        ROS_INFO("The sum of your two integers is: %ld", srv.response.sum);
    }
    else{
        ROS_INFO("Failed to call the service");
        return 1;
    }

    return 0;
}