import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, EnvironmentVariable
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    urdf_path = PathJoinSubstitution(
        [FindPackageShare("vera_description"), "urdf/robots", "vera.urdf.xacro"]
    )

    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare('vera_description'), 'rviz', 'description.rviz']
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            name='urdf', 
            default_value=urdf_path,
            description='URDF path'
        ),
        
        DeclareLaunchArgument(
            name='publish_joints', 
            default_value='true',
            description='Launch joint_states_publisher'
        ),
        
        DeclareLaunchArgument(
            name='jsp_gui',
            default_value='true',
            choices=['true', 'false'],
            description='Launch joint_state_publisher GUI'
        ),

        DeclareLaunchArgument(
            name='rviz', 
            default_value='false',
            description='Run rviz'
        ),

        DeclareLaunchArgument(
            name='use_sim_time', 
            default_value='false',
            description='Use simulation time'
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            condition=IfCondition(LaunchConfiguration("publish_joints")),
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')}
            ]
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'robot_description': Command(['xacro ', LaunchConfiguration('urdf')])
                }
            ]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path],
            condition=IfCondition(LaunchConfiguration("rviz")),
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
        
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            condition=IfCondition(LaunchConfiguration("jsp_gui"))
        )
    ])

#sources: 
#https://navigation.ros.org/setup_guides/index.html#
#https://answers.ros.org/question/374976/ros2-launch-gazebolaunchpy-from-my-own-launch-file/
#https://github.com/ros2/rclcpp/issues/940