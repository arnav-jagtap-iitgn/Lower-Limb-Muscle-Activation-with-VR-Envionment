import viz
import vizshape
import vizfx
import vizact
import vizinfo
import random
import pyttsx3
import time
import serial
import csv
import time

# Initialize Vizard
viz.go()

# Start game timer
start_time = time.time()

# File to store game data
log_file = "game_log.csv"

# Create or open the file and write headers if it doesn't exist
with open(log_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Elapsed Time (s)", "Level", "Goalposition", "Task Score", "Total Score"])

## Open Serial Connection to Arduino
#arduino_port = "COM15"  # Replace with your Arduino's COM port
#baud_rate = 38400
#arduino = serial.Serial(arduino_port, baud_rate)

## Function to Check Arduino Data
#def check_sensor_data():
#    if arduino.in_waiting > 0:  # Check if data is available
#        data = arduino.readline().decode('utf-8').strip()  # Read data from Arduino
#        cleaned_data = data.split(":")[-1].strip()  # Extract numeric part, e.g., '0,0'
#        try:
#            force_values = cleaned_data.split(',')  # Split into ['0', '0']
#            force1 = float(force_values[0])
#            force2 = float(force_values[1])
#            
#            # You can adjust the logic below to use either or both values
#            if force1 <= 0.1 or force2 <= 0.1:  # Both legs lifted (example condition)
#                viz.playSound('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR1/Ding.wav')  # Play a beep sound
#                print("both legs lifted")
#            else:
#                pass  # No action needed
#        except (ValueError, IndexError) as e:
#            print("Error reading force values:", e)
#
## Add a timer to continuously check Arduino data
#vizact.ontimer(0.1, check_sensor_data)


# Initialize the TTS engine
engine = pyttsx3.init()

# Set voice properties (optional)
engine.setProperty('rate', 200)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Function to speak text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
vizact.onupdate(2, lambda: [speak_text("Please stand upright till you see the green button vanishes"), setattr(viz, 'has_spoken', True)] if not hasattr(viz, 'has_spoken') else None)
#speak_text("Please follow the arrow and stay inside the goal untill the blinking of the goalpost stops")

# Create a red box
red_box = vizshape.addBox(size=(15, 15, 15))  # You can adjust the size as needed
red_box.setPosition(0, 0.5, 0)  # Position it above the ground
red_box.color(viz.RED)  # Set the box color to red

# Function to change the box color to green
def changeToGreen():
    red_box.color(viz.GREEN)  # Change the color to green

# Function to make the box invisible
def makeInvisible():
    red_box.visible(viz.OFF)  # Make the box invisible
    print("Green box turned invisible.")
    # Delay the speech slightly to ensure the box is invisible first
    vizact.ontimer2(0.1, 0, speakGoalInstruction)

# Function to speak the instruction
def speakGoalInstruction():
    if not hasattr(viz, 'goal_instruction_spoken'):
        speak_text("Please follow the arrow and stay inside the goal until the blinking of the goalpost stops")
        setattr(viz, 'goal_instruction_spoken', True)  # Set flag to prevent repeated execution

# Start the sequence
vizact.ontimer(3, changeToGreen)  # After 3 seconds, change the box to green
vizact.ontimer2(6,0,makeInvisible)  # Call makeInvisible after 1 second

##### Set background and lighting
viz.clearcolor(viz.SKYBLUE)  # Sky blue background
light = viz.addLight()
light.position(0, 10, -35)    # Light source above the field
light.setEuler(0,10,0)

##### Add a plane for the football field
grass = viz.addTexture('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR1/grass.jpg')
field = vizshape.addPlane(size=(150, 100))  # Field size: 20x20 units
field.setPosition(0, 0, 0)               # Center the field
field.setEuler(0, 0, 0)                 # Rotate to lay flat
field.texture(grass)                # Apply the ice texture

# Function to determine the starting level
def initializeGame():
    global start_level
    start_level = random.choice([1, 0])  # Randomly choose between Level 1 or Level 2
    print(f"Chosen Start Level: {start_level}")

    setupLevel(start_level)  # Call the function to setup the level

def setupLevel(level):
    if level == 0:
        print("Starting Level 1 Setup")
        setupGame()  # Calls your original setupGame for Level 1
    elif level == 1:
        print("Starting Level 2 Setup")
        switchToLevel2()  # Immediately switch to Level 2


##### Add field lines (boundaries and center line) ((115 X 74)/4 yards)
# Top Boundary
boundary_top = vizshape.addBox(size=(115/4, 0.01, 0.1))
boundary_top.setPosition(0, 0.01, 74/8)     # At the top edge
boundary_top.color(viz.WHITE)

# Bottom Boundary
boundary_bottom = vizshape.addBox(size=(115/4, 0.01, 0.1))
boundary_bottom.setPosition(0, 0.01, -74/8) # At the bottom edge
boundary_bottom.color(viz.WHITE)

# Left Boundary
boundary_left = vizshape.addBox(size=(0.1, 0.01, 74/4))
boundary_left.setPosition(-115/8, 0.01, 0)  # Left edge
boundary_left.color(viz.WHITE)

# Right Boundary
boundary_right = vizshape.addBox(size=(0.1, 0.01, 74/4))
boundary_right.setPosition(115/8, 0.01, 0)  # Right edge
boundary_right.color(viz.WHITE)

##### Add goalposts
goal_left = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Blender/goalpost.fbx')
goal_right = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Blender/goalpost.fbx')
goal_top = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Blender/goalpost.fbx')

## Place the left goalpost
goal_left.setPosition((-115/8)-(4/3), 0.01, 0)  # Position at the left goal
goal_left.setEuler(-90, 0, 0)         # Rotate to face the field
bbox = goal_left.getBoundingBox(viz.ABS_GLOBAL)  # Get bounding box in global coordinates
width = bbox.width
height = bbox.height
depth = bbox.depth
# Target size
target_width = 4
target_height = 8/3
target_depth = 16/3
# Calculate scale factors
scale_x = target_width / width
scale_y = target_height / height
scale_z = target_depth / depth
goal_left.setScale(scale_x, scale_y, scale_z)
bbox = goal_left.getBoundingBox(viz.ABS_GLOBAL)
print("Final dimensions (width, height, depth):", 
      bbox.width, bbox.height, bbox.depth)

#$ Place the right goalpost
goal_right.setPosition((115/8)+(4/3), 0.01, 0)  # Position at the right goal
goal_right.setEuler(90, 0, 0)       # Rotate to face the field
goal_right.setScale(scale_x, scale_y, scale_z)

# Place the top goalpost
goal_top.setPosition(0, 0.01, (74/8)+(4/3))  # Position at the top goal
goal_top.setEuler(0, 0, 0)         # Rotate to face the field
goal_top.setScale(scale_x, scale_y, scale_z)

##### Add a football at the center
ball = viz.addChild('soccerball.ive')  # Load the soccer ball model
ball.setPosition(0, 0.4, 0)           # Center the ball on the field
ball.setScale(4.0, 4.0, 4.0)         # Scale the ball to make it larger

# Add a white circle on the ball
ball_circle = vizshape.addCircle(radius=0.4)  # Adjust the radius as needed
ball_circle.setPosition(0, 0.01, 0)  # Slightly above the ball's center
ball_circle.setEuler(0, 90, 0)         # Keep it flat
ball_circle.color(viz.WHITE)          # Set the color to white

##### Adjust camera position to view the entire field
viz.MainView.setPosition(0, 10, -30)   # Camera above and behind the field
viz.MainView.setEuler(0, 10, 0)        # Tilt the camera to look down
viz.MainView.collision(False)

# Variables to track game state
field_width = (115/8)+(4/3) # Half the field size (assumes 20x20 field)
field_depth = (74/8)+(4/3)
score = 0
current_task = 0  # 0: left goal, 1: top goal, 2: right goal
global goal_positions
goal_positions = [
    (-115/8, 0.2, 0),  # Left goal
    (0, 0.2, 74/8),   # Top goal
    (115/8, 0.2, 0)    # Right goal
]    

# Global variables
task_order = []  # List to hold the randomized task order

def setupGame():
    global task_order
    # Create a list of task indices [0, 1, 2] representing Left, Top, Right
    task_order = [0, 1, 2]  
    random.shuffle(task_order)  # Shuffle the list to randomize the order
    print(f"Randomized task order: {task_order}")

ball_movement_enabled = False 


# Load an arrow model
arrow_model = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR1/arrow.fbx')

# Scale and position the arrow
arrow_model.setScale(0.02, 0.02, 0.02)  # Adjust the size
arrow_model.setPosition(0, 0, 0)     # Place it above the field
arrow_model.visible(viz.OFF)

# New variables to track ball stay time inside the goalpost
ball_inside_goal = False
time_inside_goal = 0  # Time the ball has stayed inside the goalpost
goal_pause_duration = 0  # Duration the ball pauses after scoring a goal
stay_required_time = 1  # Time the ball needs to stay for full points
ball_outside_goal = False
time_outside_goal=0  # Tracks whether the ball was in a corner inside the goal

def blinkGoal(goalpost):
#    if count > 0:
        # Toggle between green and white
        current_color = goalpost.getColor()
        new_color = [0, 1, 0] if current_color == [1, 1, 1] else [0, 1, 0]
        goalpost.color(new_color)

# Check if the ball enters the goal or goes out of bounds
def checkGoal():
    global score, current_task, field_width, field_depth, break_in_progress, game_complete, ball_inside_goal, time_inside_goal, ball_outside_goal, time_outside_goal

    if game_complete or break_in_progress:
        ball_inside_goal = False
        time_inside_goal = 0
        ball_outside_goal = False
        time_outside_goal=0
        return  # Skip checks if the game is complete or during the break

    ball_pos = ball.getPosition()

    # Check if all tasks are completed
    if current_task >= len(goal_positions):
        if field_width == field_width_level2:
            print("Level 2 complete! Congratulations!")
            switchToLevel1()
        else:
            print("Level 1 complete! Congratulations!")
            switchToLevel2()
        return
    
    # Ensure the current task index is within bounds
    if current_task < len(goal_positions):
        goalpost = goal_positions[current_task]

        # Get the current task based on the randomized order
        current_task_index = task_order[current_task]
        
        arrow_model.visible(viz.ON)
        
        # Define goalpost based on the shuffled current task index
        if current_task_index == 0:
            arrow_model.setEuler(0, 90, 90)  
            arrow_model.setPosition(-2, 0, 0)     # Place it above the field
            goalpost = goal_left if field_width == (115/8)+(4/3) else goal_left_level2
        elif current_task_index == 1:
            arrow_model.setEuler(0, 90, 0)
            arrow_model.setPosition(0, 0, 2)     # Place it above the field
            goalpost = goal_top if field_depth == (74/8)+(4/3) else goal_top_level2
        else:
            arrow_model.setEuler(0, 90, -90) 
            arrow_model.setPosition(2, 0, 0)     # Place it above the field
            goalpost = goal_right if field_width == (115/8)+(4/3) else goal_right_level2

        # Obtain the bounding box of the goalpost in world coordinates
        bounding_box = goalpost.getBoundingBox(viz.ABS_GLOBAL)
        goal_min = [bounding_box.xmin, bounding_box.ymin, bounding_box.zmin]
        goal_max = [bounding_box.xmax, bounding_box.ymax, bounding_box.zmax]
        
        
        # Check if the ball is within the goalpost bounding box
        is_inside_goal = (
            goal_min[0] <= ball_pos[0] <= goal_max[0] and
            goal_min[1] <= ball_pos[1] <= goal_max[1] and
            goal_min[2] <= ball_pos[2] <= goal_max[2]
        )
        

        if is_inside_goal:
                
            if current_task_index == 0:
                goalpost = goal_left if field_width == (115/8)+(4/3) else goal_left_level2
            elif current_task_index == 1:
                goalpost = goal_top if field_depth == (74/8)+(4/3) else goal_top_level2
            else:
                goalpost = goal_right if field_width == (115/8)+(4/3) else goal_right_level2
            
            
            # Repeat the blinking effect every 0.2 sec for 1 sec
            vizact.ontimer2(0.2, 1, blinkGoal, goalpost)
            
            def resetGoalColor():
                """ Ensures the goalpost turns white after 1 sec """
                goalpost.color([1, 1, 1])  
                # White

            # Ensure after 1 sec, goalpost turns white
            vizact.ontimer2(1, 1, resetGoalColor)
                
            if not ball_inside_goal:
                ball_inside_goal = True
                time_inside_goal = 0  # Reset stay timer
                print("Ball entered the goalpost area. Timer started.")

            # Increment the stay timer if the ball stays inside
            time_inside_goal += viz.elapsed()
            
            if time_inside_goal >= 1:
                task_score = 100
                print(f"Goal! You earned {task_score} points. Total score: {score + task_score}.")
                score += task_score
                current_task += 1
                pauseBallInGoal()
                with open(log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    elapsed_time = time.time() - start_time  # Calculate elapsed time
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
                    if current_task_index == 0:
                        goalposition = 'L'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    elif current_task_index == 1:
                        goalposition = 'T'
                        level = 1 if field_depth == (74/8)+(4/3) else 2
                    else:
                        goalposition = 'R'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    writer.writerow([timestamp, elapsed_time, level, goalposition, task_score, score])
                return
                
        else:
            if ball_inside_goal and 0 < time_inside_goal < 1:
                task_score = 80
                print(f"Ball left the goal early. You earned {task_score} points. Total score: {score + task_score}.")
                score += task_score
                current_task += 1
                startBreak()
                with open(log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    elapsed_time = time.time() - start_time  # Calculate elapsed time
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
                    if current_task_index == 0:
                        goalposition = 'L'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    elif current_task_index == 1:
                        goalposition = 'T'
                        level = 1 if field_depth == (74/8)+(4/3) else 2
                    else:
                        goalposition = 'R'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    writer.writerow([timestamp, elapsed_time, level, goalposition, task_score, score])
                return
            
            ball_inside_goal = False
            time_inside_goal = 0

        # Check if the ball is outside the goalpost and field
        is_outside_goalpost = not is_inside_goal
        is_outside_field = (
            abs(ball_pos[0]) > field_width - 0.5 or abs(ball_pos[2]) > field_depth - 0.5
        )
        is_outside = is_outside_goalpost and is_outside_field

        if is_outside:
            if not ball_outside_goal:
                ball_outside_goal = True
                time_outside_goal = 0  # Reset stay timer
                print("Ball is outside the goalpost and field. Timer started.")
            
            time_outside_goal += viz.elapsed()
            
            if time_outside_goal >= 1:
                task_score = 60
                print(f"Ball stayed outside! You earned {task_score} points. Total score: {score + task_score}.")
                score += task_score
                current_task += 1
                startBreak()
                with open(log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    elapsed_time = time.time() - start_time  # Calculate elapsed time
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
                    if current_task_index == 0:
                        goalposition = 'L'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    elif current_task_index == 1:
                        goalposition = 'T'
                        level = 1 if field_depth == (74/8)+(4/3) else 2
                    else:
                        goalposition = 'R'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    writer.writerow([timestamp, elapsed_time, level, goalposition, task_score, score])
                return
        else:
            if ball_outside_goal and 0 < time_outside_goal < 1:
                task_score = 40
                print(f"Ball briefly left the goal and field. You earned {task_score} points. Total score: {score + task_score}.")
                score += task_score
                current_task += 1
                startBreak()
                with open(log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    elapsed_time = time.time() - start_time  # Calculate elapsed time
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
                    if current_task_index == 0:
                        goalposition = 'L'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    elif current_task_index == 1:
                        goalposition = 'T'
                        level = 1 if field_depth == (74/8)+(4/3) else 2
                    else:
                        goalposition = 'R'
                        level = 1 if field_width == (115/8)+(4/3) else 2
                    writer.writerow([timestamp, elapsed_time, level, goalposition, task_score, score])
                return
            
            ball_outside_goal = False
            time_outside_goal = 0

        
def resetGoalTimer():
    """Reset the goal timer."""
    global goal_timer, goal_timer_active
    goal_timer = 0
    goal_timer_active = False
    
def startBreak():
    """Initiate a 5-second break and reset the ball."""
    global break_in_progress
    break_in_progress = True
    resetBallPosition()
    print("Taking a 5-second break...")
    vizact.ontimer2(3, 0, endBreak)  # Resume after 5 seconds

def endBreak():
    """End the break and allow the game to continue."""
    global break_in_progress
    break_in_progress = False
    if current_task < len(goal_positions):  # Only print if there are valid tasks remaining
        print(f"Task {current_task + 1} starting now!")

def pauseBallInGoal():
    """Pause the ball in the goal for a specified duration and then reset it."""
    global ball_movement_enabled
    global break_in_progress
    break_in_progress = True

    ball_movement_enabled = False  # Disable ball movement
    print("Ball paused in the goal for celebration.")
    
    # Wait for the pause duration, then reset
    vizact.ontimer2(goal_pause_duration, 0, resetBallPosition)
    print("Taking a 5-second break...")
    
    # Reset the goalpost color back to white after the break
    vizact.ontimer2(goal_pause_duration, 0, lambda: [goal.color([1, 1, 1]) for goal in [goal_left, goal_right, goal_top]])
    
    vizact.ontimer2(5, 0, endBreak)  # Resume after 5 seconds

# Reset ball position to center
def resetBallPosition():
    """Reset ball position to the center of the field and disable movement."""
    global ball_movement_enabled, ball_inside_goal
    ball_inside_goal = False
    ball.setPosition(0, 0.4, 0)  # Center the ball
    ball_movement_enabled = False  # Ensure movement remains disabled
    print("Ball reset to center position.")
    
    
##### Initially disable ball movement 

    

# Update ball position based on mouse input
def updateBallPosition():
    global ball_movement_enabled
    ball_movement_enabled = True
    # Prevent ball movement during break
    if break_in_progress or not ball_movement_enabled:
        return  # Skip updating ball position
    
    mouse_x = viz.mouse.getPosition()[0] * 2 - 1  # Scale and center
    mouse_z = viz.mouse.getPosition()[1] * 2 - 1  # Scale and center

    # Map mouse position to field size
    ball_x = mouse_x * field_width
    ball_z = mouse_z * field_depth

    # Update ball position
    ball.setPosition(ball_x, 0.4, ball_z)
    
    
    

##### Global variable to track if a break is in progress
break_in_progress = False
# Add this global variable
game_complete = False

##### Level 2 configurations
field_width_level2 = (115/6)+(4/3)  # Half the field size for Level 2
field_depth_level2 = (74/6)+(4/3)
goal_positions_level2 = [
    (-115/6, 0.2, 0),  # Left goal for Level 2
    (0, 0.2, 115/6),   # Top goal for Level 2
    (115/6, 0.2, 0)    # Right goal for Level 2
]

# Goalpost and boundary objects for Level 2
goal_left_level2 = None
goal_right_level2 = None
goal_top_level2 = None
boundary_objects_level2 = []

def setupLevel2():
    global goal_left_level2, goal_right_level2, goal_top_level2, boundary_objects_level2

    # Create larger goalposts for Level 2
    goal_left_level2 = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Blender/goalpost.fbx')
    goal_right_level2 = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Blender/goalpost.fbx')
    goal_top_level2 = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Blender/goalpost.fbx')

    # Position and scale Level 2 goalposts ((115 X 74)/3 yards)
    goal_left_level2.setPosition((-115/6)-(4/3), 0.01, 0)
    goal_left_level2.setScale(scale_x, scale_y, scale_z)
    goal_left_level2.setEuler(-90, 0, 0)

    goal_right_level2.setPosition((115/6)+(4/3), 0.01, 0)
    goal_right_level2.setScale(scale_x, scale_y, scale_z)
    goal_right_level2.setEuler(90, 0, 0)

    goal_top_level2.setPosition(0, 0.01, (74/6)+(4/3))
    goal_top_level2.setScale(scale_x, scale_y, scale_z)
    goal_top_level2.setEuler(0, 0, 0)

    # Create larger boundaries for Level 2
    boundary_objects_level2 = [
        vizshape.addBox(size=(115/3, 0.01, 0.1)),  # Top boundary
        vizshape.addBox(size=(115/3, 0.01, 0.1)),  # Bottom boundary
        vizshape.addBox(size=(0.1, 0.01, 74/3)),  # Left boundary
        vizshape.addBox(size=(0.1, 0.01, 74/3))   # Right boundary
    ]
    boundary_objects_level2[0].setPosition(0, 0.01, 74/6)  # Top boundary
    boundary_objects_level2[1].setPosition(0, 0.01, -74/6)  # Bottom boundary
    boundary_objects_level2[2].setPosition(-115/6, 0.01, 0)  # Left boundary
    boundary_objects_level2[3].setPosition(115/6, 0.01, 0)   # Right boundary
    for boundary in boundary_objects_level2:
        boundary.color(viz.WHITE)  
    

def switchToLevel2():
    global field_width, field_depth, goal_positions, current_task

    # Hide Level 1 objects
    goal_left.visible(False)
    goal_right.visible(False)
    goal_top.visible(False)
    boundary_top.visible(False)
    boundary_bottom.visible(False)
    boundary_left.visible(False)
    boundary_right.visible(False)
    
    # Setup Level 2
    setupLevel2()

    # Update game state for Level 2
    field_width = field_width_level2
    field_depth = field_depth_level2
    goal_positions[:] = goal_positions_level2
    current_task = 0

    # Adjust camera viewpoint for Level 2
    viz.MainView.setPosition(0, 10, -35)   # Higher and farther camera position
    viz.MainView.setEuler(0, 10, 0)        # Tilt camera to look down
    
    # Reset ball position and disable movement
    resetBallPosition()
    ball_movement_enabled = False

    print("Welcome to Level 2! The field and goalposts have expanded!")
    # to randomise the tasks
    setupGame()

def switchToLevel1():
    global field_width, field_depth, goal_positions, current_task
    
    goal_left.visible(True)
    goal_right.visible(True)
    goal_top.visible(True)
    boundary_top.visible(True)
    boundary_bottom.visible(True)
    boundary_left.visible(True)
    boundary_right.visible(True)


    # Hide Level 1 objects
    goal_left_level2.visible(False)
    goal_right_level2.visible(False)
    goal_top_level2.visible(False)
    boundary_objects_level2[0].visible(False)
    boundary_objects_level2[1].visible(False)
    boundary_objects_level2[2].visible(False)
    boundary_objects_level2[3].visible(False)

    # Update game state for Level 1
    field_width = (115/8)+(4/3) # Half the field size (assumes 20x20 field)
    field_depth = (74/8)+(4/3)
    current_task = 0
    goal_positions = [
    (-115/8, 0.2, 0),  # Left goal
    (0, 0.2, 74/8),   # Top goal
    (115/8, 0.2, 0)    # Right goal
    ]
    
    ##### Adjust camera position to view the entire field
    viz.MainView.setPosition(0, 10, -30)   # Camera above and behind the field
    viz.MainView.setEuler(0, 10, 0)        # Tilt the camera to look down
        
    # Reset ball position and disable movement
    resetBallPosition()
    ball_movement_enabled = False

    print("Welcome to Level 1! The field and goalposts have reduced!")
    # to randomise the tasks
    setupGame()


# Call the initialization function at the start
initializeGame()  # At the beginning of your code

##### Register continuous callbacks
vizact.ontimer(0, updateBallPosition)
vizact.ontimer(0.1, checkGoal)