import os
import cv2
from ultralytics import YOLO
from tracker import Tracker
import numpy as np
import time
from tqdm import tqdm



### Creating regions for Tracking Speed:
    ###### USER GUIDE  #####
'''
    1.What is the need of speed-tracking region?

        We basically measure the average speed of a tracked vehicle between two rectangular counters/regions, these are called speed tracking regions. 

    2.What type of roads we choose for speed tracking? How to choose the speed-tracking regions for them?

        This will be different from video to video, as the road orientation can be differnt, so vehicle motion might not be paraller/coming towards us. Here, we are taking two examples, one with vehicles coming vertical and other case is horizontal. Choosing a speed-tracking region is simply taking planes on the road that, are perpendicular to the vehicles motion. All, the speed-tracking region should be paraller to each other.

    3.How will we represent an object? And how will we know if its in the speed-tracking region?

        We will represent an object by center coordinates. With openCV we will determine if this center is inside the region.

    4.How distance  will be represented? How will average_speed be evaluated?
        scaled_distance = 18/5*distance_in_meters
        => scaled_distance = 3.6*distance_in_meters
        => average_speed  = scaled_distance/time_in_second in Km/h 

'''

### Case-1
    ## flag=0
        # vertical road, vehicle is moving towards us.
area1 = np.array([[50,60],[720+500,60],[720+500,120],[50,120]],np.int32)
area2 = np.array([[50, 180], [720+500, 180],[720+500, 240],[50, 240]],np.int32)
area3 = np.array([[50, 300], [720+500, 300], [720+500, 360],[50, 360]],np.int32)
area4 = np.array([[40, 420], [720+450, 420], [720+450, 480], [40, 480]],np.int32)
area5 = np.array([[10, 540], [720+420, 540], [720+420, 600], [10, 600]],np.int32)
area6 = np.array([[1, 660], [720+400, 660], [720+400, 700], [1, 700]],np.int32)


## Flat-Area approx 3m-4m separation
area = [area1,area2,area3,area4,area5,area6]

### Case-2
    ## flag=1
        # Horizontal road, vehicle is moving horizonally
c = np.array([[90,700],[400,709],[671,940],[337,1040]],np.int32)
b = np.array([[90+520,700],[400+520,709],[671+520,940],[337+520,1040]],np.int32)
a = np.array([[90+1000,700],[400+1000,709],[671+1000,940],[337+1000,1040]],np.int32)

## Region-array
Area = [a,b,c]



### Loading Models
    ## For detection of over-speed vehicles 
        ## pre-trained YOLOV8-nano model
model = YOLO("yolov8n.pt")
    ## For detection of people not wearing helmet and not using seatbelt
        ## Custom-trained YOLOV8-nano model
            ## Dataset size: 1039; 
                ## Classes: Without Helmet, With Helmet, no-seatbelt, Using Phone
model1 = YOLO("custom_yolov8.pt")

### DeepSort tracker
'''
    We are using 2 trackers here, one trackes the vehicles and other specifically tracks the helmets and seatbelts. Using 2 different tracker gives better results.
'''

##Only Tracking Vehicles
tracker = Tracker()

##Tracking Helmets and seatbelts
tracker1 = Tracker()




def get_overspeed_count(average_speed,speed_limit,track_id,overspeed_count,frame,x1,y1,x2,y2):
    '''
    Determines whether the vehicle has crossed the speed-limits, and updates the count of overspeed vehicles

    Args:
        average_speed: int
            Average speed of vehicle
        speed_limit: int
            Max. allowed speed by traffic 
        track_id: int
            Unique id for every vehicle
        overspeed_count: int
            number of vehicles overspeeding before
        frame: np.ndarray
            current image being tracked
        x1: int
            bounding-box(x1)
        x2: int
            bounding-box(x2)
        y1: int
            bounding-box(y1)
        y2: int
            bounding-box(y1)
    '''

    if average_speed:
        if average_speed>=speed_limit:
            if track_id in overspeed_count:
                overspeed_count[track_id] +=1
            else:
                overspeed_count[track_id] =1
            
            ## showing the warning sign
            cv2.rectangle(frame,(int(x1),int(y1)),(int(x2+100),int(y2-30)),(0,0,255),2,-1)
            cv2.putText(frame,' Warning!!! Over speeding ', (int(x1+10),int(y1-140)),0,0.75, (0,0,255), 2)
            
    return overspeed_count

                   

def get_no_of_vehicles_tracked(track_id, cx, cy,Count_of_vehicles,flag):
    '''
    Counts and updates number of vehicle tracked

    Args:
        track_id: int
            unique track id for every vehicle
        cx: int
            center-x of vehicle
        cy: int
            centre-y of vehicle
        Count_of_vehicles: int
            centre-y of vehicle
        flag: int
            whether case-1 or case-2
    '''

    is_inside_area3 = cv2.pointPolygonTest(area[2],(int(cx),int(cy)), False) ##flag=0
    is_inside_c = cv2.pointPolygonTest(Area[-1],(int(cx),int(cy)), False)  ##flag=1

    if flag == 0:
        if is_inside_area3>=0:
            Count_of_vehicles[track_id] = 1

    if flag == 1:
        if is_inside_c>=0:
            Count_of_vehicles[track_id] = 1

    return Count_of_vehicles




def get_speed_tracking_regions(flag,frame):

    '''
    Drawing the Speed-Tracking-Regions

    Args:
        flag: int
            whether case-1 or case-2
        frame: np.ndarray
            current image being tracked
    '''

    ## Vertical-Tracking 
    if flag == 0:
        for i in area:
            pts = i.reshape((-1, 1, 2))
            cv2.polylines(frame,[pts],True,(0,255,0),2)

    ## Horizontal-Tracking
        ## mostly the tracks don't look good, you can avoid plotting them
    if flag == 1:
        # for i in Area:
        #     cv2.polylines(frame,[i],True,(0,255,0),2)
        pass
        



def main(flag,input_path,video_out_path,scaled_distance,speed_limit,detection_threshold):
    
    '''
    Main function combines all the operations and gives final output as video format

    Args:
        flag: int
            whether case-1 or case-2
        input_path: str
            input video path
        video_out_path: str
            output video path
        scaled_distance: int
            distance between two consequtive speed-tracking regions
        speed_limit: int
            max. allowed speed according to traffic
        detection_threshold: float
            min score for considering it as detection
    '''

    ## to be used for speed-tracking 
    vehicle_entering = {}
    vehicle_elapsed_time = {}
    overspeed_count = {}
    Count_of_vehicles = {}
    vehicle_centre = {}
    static_vehicles = {}
    helmet_seatbelt_violation = {}
    
    
    cap = cv2.VideoCapture(input_path)
    
    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create a tqdm progress bar with the total number of frames
    progress_bar = tqdm(total=total_frames, desc="Processing Frames", unit="frame")
    
    ret, frame = cap.read()
    cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'MP4V'), cap.get(cv2.CAP_PROP_FPS),(frame.shape[1], frame.shape[0]))
    while ret:
        results = model(frame)
        results1 = model1(frame)

        ## Plotting the speed tracking region
        get_speed_tracking_regions(flag,frame)
            

        ## Locating the people not wearing helmet, not waering seat belt,using phone while driving 
        for result in results1:
            detections = []
            for r in result.boxes.data.tolist():
                ## unpacking the bounding boxes data 
                x11, y11, x22, y22, score, class_id = r
                x11 = int(x11)
                x22 = int(x22)
                y11 = int(y11)
                y22 = int(y22)
                class_id = int(class_id)
                class_name = result.names[class_id]

                ## setting detection-threshold
                if score > 0.3:
                    detections.append([x11, y11, x22, y22, score])
                ## excluding wearing helmet class
                    ## training the model on both wearing and not-wearing helmet improves the detection of no-helmet
                if class_name !='With Helmet':
                    ## plotting the boxes 
                    cv2.rectangle(frame,(x11,y11),(x22,y22),(0,0,255),2)
                    cv2.putText(frame,str(result.names[class_id]),(int(x11),int(y11)),0,0.75,(0,0,255),2)  

                    ## tracking no-helmet and no-seatbelt 
                    tracker1.update(frame, detections)
                    for track1 in tracker1.tracks:
                        bbox = track1.bbox
                        ## unpacking the bounding box data
                        x11, y11, x22, y22 = bbox
                        track_id1 = track1.track_id
                        ## updating the number of tracked traffic-violations(no helmet/no seatbelt)
                        if track_id1 in helmet_seatbelt_violation:
                            helmet_seatbelt_violation[track_id1] += 1
                        else:
                            helmet_seatbelt_violation[track_id1] = 1

        ### Detecting the vehicles
        for result in results:
            detections = []
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                class_id = int(class_id)
                class_name = result.names[class_id]

                ## setting up thresold
                if score > detection_threshold:
                    detections.append([x1, y1, x2, y2, score])

            
            ## tracking the vehicles
            tracker.update(frame, detections)

            for track in tracker.tracks:
                bbox = track.bbox
                x1, y1, x2, y2 = bbox
                track_id = track.track_id
            
                ## centre coordinates of each vehicle
                cx = int((x1+x2)/2)
                cy = int((y1+y2)/2)

                
                ## counting the vehicles tracked
                Count_of_vehicles = get_no_of_vehicles_tracked(track_id, cx, cy,Count_of_vehicles,flag)
                
                ## the font-size might vary from video type and resolution
                    ## the current video pixel format is 1080px720p and type mp4 
                        ## can choose specific font-size, location and color to display the top parameters in a better way

                ## displaying the overspeed number
                cv2.putText(frame,f'No. of Vehicles Over-Speeding : {len(overspeed_count)}',(10,30),0,0.6,(138,0,138),3)

                ## displaying the vehicles tracked
                cv2.putText(frame,f'No. of Vehicles Tracked: {len(Count_of_vehicles)}',(700,30),0,0.6,(106,51,170),3)
                
                ## displaying the helmet/seatbelt violations
                cv2.putText(frame,f'No. of Helmet violations: {len(helmet_seatbelt_violation)}',(1000,30),0,0.6,(166,51,170),3)
                
                
                if track_id in overspeed_count:
                    ## keep a track on the vehicle which is overspeeding
                    cv2.putText(frame,'Over-Speeding',(int(x1),int(y1-30)),0,0.5,(0,0,255),2)
                    cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),2,-1)

                ## displaying id of each vehicle
                cv2.putText(frame,'Id_'+str(track_id), (int(x1),int(y1-10)),0,0.75, (255,0,0), 2)
                ## display the speed-limit
                cv2.putText(frame, f'Speed Limit: {speed_limit} Km/h', (400,30),0,0.6, (0,0,255), 3)

                
                #### Case-1
                if flag == 0:
                    for i in range(len(area)-1):
                        vehicle_elapsed_time = {} ## clear time for 2nd speed-tracking region
                        ## check if the vehicle is inside the 1st speed-tracking region
                        result = cv2.pointPolygonTest(area[i],(int(cx),int(cy)), False)
                        ## initialize the previous center 
                        prev_centre = [cx,cy] 

                        if result >= 0:
                            
                            ## tracking the in-time 
                            vehicle_entering[track_id] = time.time()
                            ## previous center to check for static vehicles
                            prev_centre = [cx,cy] 
                            ## vehicles current center
                            vehicle_centre[track_id] = [cx,cy]

                            
                        if track_id in vehicle_entering and track_id not in static_vehicles:
                            ## check if  vehicle is present in the second speed-tracking region
                            result1 = cv2.pointPolygonTest(area[i+1],(int(cx),int(cy)), False)

                            if result1 >= 0:
                                if vehicle_centre[track_id] == prev_centre:
                                    ## tracking the static vehicles
                                        ## there is no mechanism to find the static vehicles using speed-tracking regions  
                                    static_vehicles[track_id] = 1
                                    average_speed = 0.0

                                else:
                                     ## tracking the out-time and then finding the time elapsed
                                    elapsed_time = time.time() - vehicle_entering[track_id]
                                    ## recording the out-time along with the vehicle
                                    vehicle_elapsed_time[track_id] = elapsed_time
                                    
                                    ## Finding the speed
                                    average_speed = scaled_distance//elapsed_time
                                
                                ## displaying average speed
                                cv2.putText(frame,f'{average_speed} Km/h', (int(x1),int(y1-50)),0,0.75, (0,255,255), 2)
                            
                                ## checking if over-speeding
                                overspeed_count = get_overspeed_count(average_speed,speed_limit,track_id,overspeed_count,frame,x1,y1,x2,y2)

                    

                ### Case-2  
                elif flag==1:
                    c = 0 ## count how many times the speed is calculated
                    for i in range(len(Area)-1):
                        c+=1
                        vehicle_elapsed_time = {} ## clear time for 2nd speed-tracking region
                        ## check if the vehicle is inside the 1st speed-tracking region
                        result = cv2.pointPolygonTest(Area[i],(int(cx),int(cy)), False)
                        ## initialize the previous center 
                        prev_centre = [cx,cy] 

                        if result >= 0:
                            ## tracking the in-time 
                            vehicle_entering[track_id] = time.time()
                            ## previous center to check for static vehicles
                            prev_centre = [cx,cy] 
                            ## vehicles current center
                            vehicle_centre[track_id] = [cx,cy]

                            
                        if track_id in vehicle_entering and track_id not in static_vehicles:
                            ## check if  vehicle is present in the second speed-tracking region
                            result1 = cv2.pointPolygonTest(Area[i+1],(int(cx),int(cy)), False)

                            if result1 >= 0:
                                if vehicle_centre[track_id] == prev_centre:
                                    ## tracking the static vehicles
                                        ## there is no mechanism to find the static vehicles using speed-tracking regions  
                                    static_vehicles[track_id] = 1
                                    average_speed = 0.0

                                else:
                                    ## tracking the out-time and then finding the time elapsed
                                    elapsed_time = time.time() - vehicle_entering[track_id]
                                    ## recording the out-time along with the vehicle
                                    vehicle_elapsed_time[track_id] = elapsed_time
                                    
                                    ## Finding the speed
                                    average_speed = scaled_distance//elapsed_time
                                
                                ## skip displaying speeds when vehicle is too close
                                    ## distance will be not be accurate 
                                if c%2==0:
                                    continue 
                                
                                ## display the speed 
                                cv2.putText(frame,f'{average_speed} Km/h', (int(x1),int(y1-50)),0,0.75, (0,255,255), 2)
                            
                   
                                ## Checking whether the vehicle overspeeds
                                ## incementing the count of over-speeding vehicles
                                overspeed_count = get_overspeed_count(average_speed,speed_limit,track_id,overspeed_count,frame,x1,y1,x2,y2)
                                
                             
        # cv2.imshow("IMG",frame)
        key = cv2.waitKey(33)
        if key == 27:
            break


        cap_out.write(frame)
        progress_bar.update(1)
        ret, frame = cap.read()

    cap.release()
    cap_out.release()
    progress_bar.close()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    ## for details about these parameter look at the user guide
    video_out_path = os.path.join('.', 'out.mp4')
    input_path = os.path.join('.','input.mp4')
    flag = 0
    scaled_distance = 12 
    speed_limit = 80 #setting-up speed limit: 80 Km/h
    detection_threshold = 0.5
    
    ### running the main function
    main(flag,input_path,video_out_path,scaled_distance,speed_limit,detection_threshold)
