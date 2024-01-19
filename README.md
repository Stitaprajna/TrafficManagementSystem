# Advanced Traffic Management System 


1. We basically measure the average speed of a tracked vehicle between two rectangular counters/regions, these are called Speed Tracking Regions. 


2. This will be different from video to video, as the road orientation can be differnt, so vehicle motion might not be paraller/coming towards us. Here, we are taking two examples, one    with vehicles coming vertical and other case is horizontal. Choosing a speed-tracking region is simply taking planes on the road that, are perpendicular to the vehicles motion. All,    the speed-tracking region should be paraller to each other.


3. We will represent an object by center coordinates. With openCV we will determine if this center is inside the region.


## Calculation of speed for each vehicle

   Scaled Distance = 3.6 X distance_in_meters
   
   Average Speed  = Scaled Distance/time_in_second (Km/h) 
   
## Common Traffic Violations that can be detected using our system

1. Speed Violation or overspeeding.
   
2. Not wearing helmet while riding bike,scooty.
   
3. Not wearing seatbelt while driving a car.

4. Using mobile while driving.
   
# Creating Regions for Tracking Speed 
   ## Road Type-I
   
   ### vertical road, vehicle is moving towards us.
   ![](https://github.com/Stitaprajna/TrafficManagementSystem/blob/main/screenshots/speed-tracking-region-1.jpg)


## Road Type-II

   ### Horizontal road, vehicle is moving horizonally
   ![](https://github.com/Stitaprajna/TrafficManagementSystem/blob/main/screenshots/speed-tracking-region-2.jpg)


## Demo (Traffic Violation + Real-Time Speed Tracking)

### 1.

Input FPS: 30 fps
Output FPS: 5 fps

https://github.com/Stitaprajna/TrafficManagementSystem/assets/93129874/f364267d-5fc8-42a5-86b0-0ef0d568f495

### 2.

https://github.com/Stitaprajna/TrafficManagementSystem/assets/93129874/dd0d3289-3800-4b54-9be8-6d42f7f71cff

### 3.

https://github.com/Stitaprajna/TrafficManagementSystem/assets/93129874/afdf2356-d6dc-47a6-8bde-41f2cfd435d0



