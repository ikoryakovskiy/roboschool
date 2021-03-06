from roboschool.scene_abstract import cpp_household
#from roboschool.scene_stadium import SinglePlayerStadiumScene
from roboschool.gym_forward_walker import RoboschoolForwardWalker
from roboschool.gym_mujoco_xml_env import RoboschoolMujocoXmlEnv
import gym, gym.spaces, gym.utils, gym.utils.seeding
import numpy as np
import os, sys

class RoboschoolForwardWalkerMujocoXMLGRL(RoboschoolForwardWalker, RoboschoolMujocoXmlEnv):

    # reward weights
    rwAlive = 0
    rwFail = -75
    rwForward = 3
    rwTime = -1.5
    rwWork = 1

    def __init__(self, fn, robot_name, action_dim, obs_dim, power):
        RoboschoolMujocoXmlEnv.__init__(self, fn, robot_name, action_dim, obs_dim)
        RoboschoolForwardWalker.__init__(self, power)

class RoboschoolHopperGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["foot", "thigh"] # diamiter of thigh is larger then leg, hence leg does not tocun the ground
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "hopper.xml", "torso", action_dim=3, obs_dim=15, power=0.75)
    def alive_bonus(self, z, pitch):
        alive = self.rwAlive if z > 0.6 and abs(pitch) < 1.5 and not self.feet_contact[1] else self.rwFail
        sick = 0 if z > 0.8 and abs(pitch) < 1.0 else 1
        return (alive, sick)

class RoboschoolHopperBalancingGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["foot", "thigh"]
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "hopper.xml", "torso", action_dim=3, obs_dim=15, power=0.75)
        # obs_dim = 8 (global orientation) + action_dim*2 (angles+velocities) + 1 (contact) = 15
        # actual return includes contacts of both foot and thigh and forward promotion => 17
        self.rwForward = 0
        self.rwTime = 0
    def alive_bonus(self, z, pitch):
        alive = self.rwAlive if z > 0.6 and abs(pitch) < 1.5 and not self.feet_contact[1] else self.rwFail
        sick = 0 if z > 0.8 and abs(pitch) < 1.0 else 1
        return (alive, sick)

class RoboschoolHopperBalancingGRL_TF(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["foot", "thigh"]
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "hopper_tf.xml", "torso", action_dim=3, obs_dim=15, power=0.75)
        # obs_dim = 8 (global orientation) + action_dim*2 (angles+velocities) + 1 (contact) = 15
        # actual return includes contacts of both foot and thigh and forward promotion => 17
        self.rwForward = 0
        self.rwTime = 0
    def alive_bonus(self, z, pitch):
        alive = self.rwAlive if z > 0.6 and abs(pitch) < 1.5 and not self.feet_contact[1] else self.rwFail
        sick = 0 if z > 0.8 and abs(pitch) < 1.0 else 1
        return (alive, sick)

class RoboschoolWalker2dGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["foot", "foot_left", "thigh", "thigh_left"]
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "walker2d.xml", "torso", action_dim=6, obs_dim=22, power=0.40)
        #self.rwForward = 2
        #self.sick = -1
    def alive_bonus(self, z, pitch):
        alive = self.rwAlive if z > 0.6 and abs(pitch) < 1.5 and not self.feet_contact[2] and not self.feet_contact[3] else self.rwFail
        sick = 0 if z > 0.8 and abs(pitch) < 1.0 else 1
        return (alive, sick)
    def robot_specific_reset(self):
        RoboschoolForwardWalkerMujocoXMLGRL.robot_specific_reset(self)
        for n in ["foot_joint", "foot_left_joint"]:
            self.jdict[n].power_coef = 30.0

class RoboschoolWalker2dBalancingGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["foot", "foot_left", "thigh", "thigh_left"]
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "walker2d.xml", "torso", action_dim=6, obs_dim=22, power=0.40)
        # obs_dim = 8 (global orientation) + action_dim*2 (angles+velocities) + 2 (contact) = 22
        # actual return is 25
        self.rwForward = 0
        self.rwTime = 0
        #self.sick = -1
    def alive_bonus(self, z, pitch):
        alive = self.rwAlive if z > 0.6 and abs(pitch) < 1.5 and not self.feet_contact[2] and not self.feet_contact[3] else self.rwFail
        sick = 0 if z > 0.8 and abs(pitch) < 1.0 else 1
        return (alive, sick)
    def robot_specific_reset(self):
        RoboschoolForwardWalkerMujocoXMLGRL.robot_specific_reset(self)
        for n in ["foot_joint", "foot_left_joint"]:
            self.jdict[n].power_coef = 30.0

class RoboschoolWalker2dBalancingGRL_TF(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["foot", "foot_left", "thigh", "thigh_left"]
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "walker2d_tf.xml", "torso", action_dim=6, obs_dim=22, power=0.40)
        # obs_dim = 8 (global orientation) + action_dim*2 (angles+velocities) + 2 (contact) = 22
        # actual return is 25
        self.rwForward = 0
        self.rwTime = 0
        #self.sick = -1
    def alive_bonus(self, z, pitch):
        alive = self.rwAlive if z > 0.6 and abs(pitch) < 1.5 and not self.feet_contact[2] and not self.feet_contact[3] else self.rwFail
        sick = 0 if z > 0.8 and abs(pitch) < 1.0 else 1
        return (alive, sick)
    def robot_specific_reset(self):
        RoboschoolForwardWalkerMujocoXMLGRL.robot_specific_reset(self)
        for n in ["foot_joint", "foot_left_joint"]:
            self.jdict[n].power_coef = 30.0

class RoboschoolWalker2d2GRL(RoboschoolWalker2dGRL):
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "walker2d2.xml", "torso", action_dim=6, obs_dim=22, power=0.40)
        #self.rwForward = 2
        #self.sick = -1

class RoboschoolWalker2d2BalancingGRL(RoboschoolWalker2dBalancingGRL):
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "walker2d2.xml", "torso", action_dim=6, obs_dim=22, power=0.40)
        self.rwForward = 0
        self.rwTime = 0
        #self.sick = -1

class RoboschoolHalfCheetahGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["ffoot", "fshin", "fthigh",  "bfoot", "bshin", "bthigh"]  # track these contacts with ground
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "half_cheetah.xml", "torso", action_dim=6, obs_dim=26, power=0.90)
        # obs_dim = 8 (global orientation) + action_dim*2 (angles+velocities) + 6 (contact) = 26
        # actual return is 27
    def alive_bonus(self, z, pitch):
        # Use contact other than feet to terminate episode: due to a lot of strange walks using knees
        no_contacts = not self.feet_contact[1] and not self.feet_contact[2] and not self.feet_contact[4] and not self.feet_contact[5]
        alive = self.rwAlive if no_contacts and abs(pitch) < 1.0 else self.rwFail
        sick = 0
        return (alive, sick)
    def robot_specific_reset(self):
        RoboschoolForwardWalkerMujocoXMLGRL.robot_specific_reset(self)
        self.jdict["bthigh"].power_coef = 120.0
        self.jdict["bshin"].power_coef  = 90.0
        self.jdict["bfoot"].power_coef  = 60.0
        self.jdict["fthigh"].power_coef = 140.0
        self.jdict["fshin"].power_coef  = 60.0
        self.jdict["ffoot"].power_coef  = 30.0

class RoboschoolHalfCheetahBalancingGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["ffoot", "fshin", "fthigh",  "bfoot", "bshin", "bthigh"]  # track these contacts with ground
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "half_cheetah.xml", "torso", action_dim=6, obs_dim=26, power=0.90)
        self.rwForward = 0
        self.rwTime = 0
    def alive_bonus(self, z, pitch):
        # Use contact other than feet to terminate episode: due to a lot of strange walks using knees
        no_contacts = not self.feet_contact[1] and not self.feet_contact[2] and not self.feet_contact[4] and not self.feet_contact[5]
        alive = self.rwAlive if no_contacts and abs(pitch) < 1.0 else self.rwFail
        sick = 0
        return (alive, sick)
    def robot_specific_reset(self):
        RoboschoolForwardWalkerMujocoXMLGRL.robot_specific_reset(self)
        self.jdict["bthigh"].power_coef = 120.0
        self.jdict["bshin"].power_coef  = 90.0
        self.jdict["bfoot"].power_coef  = 60.0
        self.jdict["fthigh"].power_coef = 140.0
        self.jdict["fshin"].power_coef  = 60.0
        self.jdict["ffoot"].power_coef  = 30.0

class RoboschoolAntGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ['front_left_foot', 'front_right_foot', 'left_back_foot', 'right_back_foot']
    def __init__(self):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, "ant.xml", "torso", action_dim=8, obs_dim=28, power=2.5)
    def alive_bonus(self, z, pitch):
        alive = self.rwAlive if z > 0.26 else self.rwFail
        sick = 0 if z > 0.26 else 1
        return (alive, sick)  # 0.25 is central sphere rad, die if it scrapes the ground


## 3d Humanoid ##

class RoboschoolHumanoidGRL(RoboschoolForwardWalkerMujocoXMLGRL):
    foot_list = ["right_foot", "left_foot"]
    TASK_WALK, TASK_STAND_UP, TASK_ROLL_OVER, TASKS = range(4)

    def __init__(self, model_xml='humanoid_symmetric.xml'):
        RoboschoolForwardWalkerMujocoXMLGRL.__init__(self, model_xml, 'torso', action_dim=17, obs_dim=44, power=0.41)
        # 17 joints, 4 of them important for walking (hip, knee), others may as well be turned off, 17/4 = 4.25
        self.electricity_cost  = 4.25*RoboschoolForwardWalkerMujocoXMLGRL.electricity_cost
        self.stall_torque_cost = 4.25*RoboschoolForwardWalkerMujocoXMLGRL.stall_torque_cost
        self.initial_z = 0.8

    def robot_specific_reset(self):
        RoboschoolForwardWalkerMujocoXMLGRL.robot_specific_reset(self)
        self.motor_names  = ["abdomen_z", "abdomen_y", "abdomen_x"]
        self.motor_power  = [100, 100, 100]
        self.motor_names += ["right_hip_x", "right_hip_z", "right_hip_y", "right_knee"]
        self.motor_power += [100, 100, 300, 200]
        self.motor_names += ["left_hip_x", "left_hip_z", "left_hip_y", "left_knee"]
        self.motor_power += [100, 100, 300, 200]
        self.motor_names += ["right_shoulder1", "right_shoulder2", "right_elbow"]
        self.motor_power += [75, 75, 75]
        self.motor_names += ["left_shoulder1", "left_shoulder2", "left_elbow"]
        self.motor_power += [75, 75, 75]
        self.motors = [self.jdict[n] for n in self.motor_names]
        self.humanoid_task()

    def humanoid_task(self):
        self.set_initial_orientation(self.TASK_WALK, yaw_center=0, yaw_random_spread=np.pi/16)

    def set_initial_orientation(self, task, yaw_center, yaw_random_spread):
        self.task = task
        cpose = cpp_household.Pose()
        yaw = yaw_center + self.np_random.uniform(low=-yaw_random_spread, high=yaw_random_spread)
        if task==self.TASK_WALK:
            pitch = 0
            roll = 0
            cpose.set_xyz(self.start_pos_x, self.start_pos_y, self.start_pos_z + 1.4)
        elif task==self.TASK_STAND_UP:
            pitch = np.pi/2
            roll = 0
            cpose.set_xyz(self.start_pos_x, self.start_pos_y, self.start_pos_z + 0.45)
        elif task==self.TASK_ROLL_OVER:
            pitch = np.pi*3/2 - 0.15
            roll = 0
            cpose.set_xyz(self.start_pos_x, self.start_pos_y, self.start_pos_z + 0.22)
        else:
            assert False
        cpose.set_rpy(roll, pitch, yaw)
        self.cpp_robot.set_pose_and_speed(cpose, 0,0,0)
        self.initial_z = 0.8

    def apply_action(self, a):
        assert( np.isfinite(a).all() )
        for i, m, power in zip(range(len(self.motors)), self.motors, self.motor_power):
            m.set_motor_torque( float(power*self.power*np.clip(a[i], -1, +1)) )

    def alive_bonus(self, z, pitch):
        alive = 2*self.rwAlive if z > 0.78 else self.rwFail
        sick = 0 if z > 0.78 else 1
        return (alive, sick)   # 2 here because 17 joints produce a lot of electricity cost just from policy noise, living must be better than dying
