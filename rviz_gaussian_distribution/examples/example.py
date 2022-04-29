#! /usr/bin/env python
import random
import actionlib
import numpy as np
import rospy
import rviz_gaussian_distribution_msgs.msg as rgd_msgs
import std_msgs.msg as std_msgs


# ==================================================================================================
#
#   ROS Publisher Method
#
# ==================================================================================================
def publish_distribution(id_):
    """
    Publish Gaussian distributions

    Args:
        id_ (int):

    """
    # Generate random 3D points．
    center_x = random.random() * 4 - 2
    center_y = random.random() * 4 - 2
    x = center_x + (np.random.random(size=100) * (0.5 + random.random() * 2))
    y = center_y + (np.random.random(size=100) * (0.5 + random.random() * 2))

    # Calc parameters of Gaussian distribution．
    mu_x = np.mean(x)
    mu_y = np.mean(y)
    sigma_x = np.std(x)
    sigma_y = np.std(y)
    covariance = (np.sum(x * y) / len(x)) - (mu_x * mu_y)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Publish
    publisher = rospy.Publisher("/input/add", rgd_msgs.GaussianDistribution, queue_size=1)
    rospy.sleep(0.1)

    msg = rgd_msgs.GaussianDistribution(
        mean_x=mu_x, mean_y=mu_y,
        std_x=sigma_x, std_y=sigma_y,
        covariance=covariance,
        r=r, g=g, b=b,
        id=id_
    )
    publisher.publish(msg)


def publish_remove(id_):
    """
    Remove published distributions

    Args:
        id_ (int):

    """
    publisher = rospy.Publisher("/input/remove", std_msgs.Int16, queue_size=1)
    rospy.sleep(0.1)

    # Publish
    msg = std_msgs.Int16(id_)
    publisher.publish(msg)


def publish_clear():
    """
    Clear published distributions

    """
    publisher = rospy.Publisher("/input/clear", std_msgs.Empty, queue_size=1)
    rospy.sleep(0.1)

    msg = std_msgs.Empty()
    publisher.publish(msg)


# ==================================================================================================
#
#   ROS Action Method
#
# ==================================================================================================
def action_distribution(id_):
    """
    Publish Gaussian distributions using Actionlib

    Args:
        id_ (int):

    """
    # Generate random 3D points．
    center_x = random.random() * 4 - 2
    center_y = random.random() * 4 - 2
    x = center_x + (np.random.random(size=100) * (0.5 + random.random() * 2))
    y = center_y + (np.random.random(size=100) * (0.5 + random.random() * 2))

    # Calc parameters of Gaussian distribution．
    mu_x = np.mean(x)
    mu_y = np.mean(y)
    std_x = np.std(x)
    std_y = np.std(y)
    covariance = (np.sum(x * y) / len(x)) - (mu_x * mu_y)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Publish
    add_action = actionlib.SimpleActionClient("/action/add", rgd_msgs.AddAction)
    add_action.wait_for_server()
    msg = rgd_msgs.GaussianDistribution(
        mean_x=mu_x, mean_y=mu_y,
        std_x=std_x, std_y=std_y,
        covariance=covariance,
        r=r, g=g, b=b,
        id=id_
    )
    add_action.send_goal(rgd_msgs.AddGoal(msg))
    add_action.wait_for_result()


def action_remove(id_):
    """
    Remove published distributions using Actionlib

    Args:
        id_ (int):

    """
    remove_action = actionlib.SimpleActionClient("/action/remove", rgd_msgs.RemoveAction)
    remove_action.wait_for_server()

    remove_action.send_goal(rgd_msgs.RemoveGoal(id_))
    remove_action.wait_for_result()


def action_clear():
    """
    Clear published distributions using Actionlib

    """
    clear_action = actionlib.SimpleActionClient("/action/clear", rgd_msgs.ClearAction)
    clear_action.wait_for_server()

    clear_action.send_goal(rgd_msgs.ClearGoal())
    clear_action.wait_for_result()


# ==================================================================================================
#
#   __main__
#
# ==================================================================================================
if __name__ == "__main__":
    rospy.init_node("example_client")
    rospy.sleep(2.0)

    # Publish Gaussian distributions
    for i in range(5):
        if not rospy.is_shutdown():
            publish_distribution(id_=i)
            rospy.sleep(1.0)

    # Remove published distributions
    for i in range(2):
        if not rospy.is_shutdown():
            publish_remove(id_=i)
            rospy.sleep(1.0)

    # Clear published distributions
    publish_clear()
    rospy.sleep(1.0)

    # Action send Gaussian distributions
    for i in range(5):
        if not rospy.is_shutdown():
            action_distribution(id_=i)
            rospy.sleep(1.0)

    # Remove published distributions
    for i in range(2):
        if not rospy.is_shutdown():
            action_remove(id_=i)
            rospy.sleep(1.0)

    # Clear published distributions
    action_clear()
    rospy.sleep(1.0)
