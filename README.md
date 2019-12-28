# Rapidly-Exploring Random Tree Practice

*Shangzhou Ye, MSR, Northwestern Univerisity*

**Skills: RRT, Python, navigational & motion planner, sampling methods**

## Demo:

## Overview

This is the repository for the RRT Challenge, MSR Hackathon, Sep. 2019. It includes the implementation of Rapidly-Exploring Random Tree (RRT), a fundamental path planning algorithm.

The pseudocode for the algorithm is as follows:

## Modules

### simplerrt.py

- A simple RRT algorithm in 2-D with the domain of [0,100]![$\times$](https://render.githubusercontent.com/render/math?math=%24%5Ctimes%24)[0,100] and incremental distance as 1.

- The figure below shows the algorithma after 500 and 5000 iterations. The RRT expanded in the free space with pretty uniform coverage over the whole space after 5000 iterations.

### obstaclerrt.py

- Circular obstacles are added to the domain. Collision checking is added into the algorithm.

- The algorithm would terminate when it reached the goal, and plot the path.

- The plot below shows two trails with same initial and goal position.

## How to run the code

- The script is written in python 2.7