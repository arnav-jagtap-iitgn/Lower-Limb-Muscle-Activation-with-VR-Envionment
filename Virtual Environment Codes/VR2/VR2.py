import viz
import vizshape
import vizfx
import vizact
import vizinfo
import random

viz.go()

##### Set background and lighting
viz.clearcolor(viz.SKYBLUE)  # Sky blue background
light = viz.addLight()
light.position(0, 10, 0)    # Light source above the field

##### Add a plane for the football field
grass = viz.addTexture('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR1/grass.jpg')
field = vizshape.addPlane(size=(150, 100))  # Field size: 100X60 units
field.setPosition(0, 0, 0)               # Center the field
field.setEuler(0, 0, 0)                 # Rotate to lay flat
field.texture(grass)                # Apply the ice texture

##### Add field lines (boundaries and center line)
# Top Boundary
boundary_top = vizshape.addBox(size=(100/4, 0.01, 0.1))
boundary_top.setPosition(0, 0.01, 60/8)     # At the top edge
boundary_top.color(viz.WHITE)

# Bottom Boundary
boundary_bottom = vizshape.addBox(size=(100/4, 0.01, 0.1))
boundary_bottom.setPosition(0, 0.01, -60/8) # At the bottom edge
boundary_bottom.color(viz.WHITE)

# Left Boundary
boundary_left = vizshape.addBox(size=(0.1, 0.01, 60/4))
boundary_left.setPosition(-100/8, 0.01, 0)  # Left edge
boundary_left.color(viz.WHITE)

# Right Boundary
boundary_right = vizshape.addBox(size=(0.1, 0.01, 60/4))
boundary_right.setPosition(100/8, 0.01, 0)  # Right edge
boundary_right.color(viz.WHITE)

##### Add goalposts
goal_left = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/hockey_gate/hockey_gate.fbx')
goal_right = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/hockey_gate/hockey_gate.fbx')
goal_top = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/hockey_gate/hockey_gate.fbx')

## Place the left goalpost
goal_left.setPosition((-100/8)-(1/3), 0.01, 0)  # Position at the left goal
goal_left.setEuler(-90, 0, 0)         # Rotate to face the field
bbox = goal_left.getBoundingBox(viz.ABS_GLOBAL)  # Get bounding box in global coordinates
width = bbox.width
height = bbox.height
depth = bbox.depth
# Target size
target_width = 8*1.75/4
target_height = 8*1.75/(2*3)
target_depth = 8*1.75/(3)
# Calculate scale factors
scale_x = target_width / width
scale_y = target_height / height
scale_z = target_depth / depth
goal_left.setScale(scale_x, scale_y, scale_z)
bbox = goal_left.getBoundingBox(viz.ABS_GLOBAL)
print("Final dimensions (width, height, depth):", 
      bbox.width, bbox.height, bbox.depth)
      
# Place the right goalpost
goal_right.setPosition((100/8)+(1/3), 0.01, 0)  # Position at the right goal
goal_right.setEuler(90, 0, 0)       # Rotate to face the field
goal_right.setScale(scale_x, scale_y, scale_z)

# Place the top goalpost
goal_top.setPosition(0, 0.01, (60/8)+(1/3))  # Position at the top goal
goal_top.setEuler(0, 0, 0)         # Rotate to face the field
goal_top.setScale(scale_x, scale_y, scale_z)

# Add a hockey ball at the center
ball = viz.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/puck/hockey_ball.fbx')  # Load the hockey ball OBJ file
ball.setPosition(0, 0.01, 0)           # Center the ball on the field
ball.setEuler(0, 90, 0)                  # Adjust rotation if needed
ball.setScale(0.3, 0.3, 0.3)          # Scale the ball to match the field size

# Add a hockey stick near the ball
hockey_stick = viz.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/hockey_stick/hockey_stick.fbx')  # Load the hockey stick OBJ file
hockey_stick.setPosition(0,0.01, 0)            # Place the stick near the ball
hockey_stick.setEuler(0, 0, 0)                  # Adjust rotation if needed
hockey_stick.setScale(0.1, 0.1, 0.1)            # Scale the stick to match the ball

# Add a white circle on the ball
ball_circle = vizshape.addCircle(radius=0.2)  # Adjust the radius as needed
ball_circle.setPosition(0, 0.01, 0)  # Slightly above the ball's center
ball_circle.setEuler(0, 90, 0)         # Keep it flat
ball_circle.color(viz.WHITE)          # Set the color to white

##### Adjust camera position to view the entire field
viz.MainView.setPosition(0, 20, -20)   # Camera above and behind the field
viz.MainView.setEuler(0, 40, 0)        # Tilt the camera to look down
viz.MainView.collision(False)

# Variables to track game state
# Variables to track game state
field_width = (100/8)+(4/3) # Half the field size (assumes 100x60 yards field)
field_depth = (60/8)+(4/3)
score = 0
current_task = 0  # 0: left goal, 1: top goal, 2: right goal
global goal_positions
goal_positions = [
    (-100/8, 0.2, 0),  # Left goal
    (0, 0.2, 60/8),   # Top goal
    (100/8, 0.2, 0)    # Right goal
]
# Global variables
task_order = []  # List to hold the randomized task order

def setupGame():
    global task_order
    # Create a list of task indices [0, 1, 2] representing Left, Top, Right
    task_order = [0, 1, 2]  
    random.shuffle(task_order)  # Shuffle the list to randomize the order
    print(f"Randomized task order: {task_order}")

# to randomise the tasks
setupGame()

ball_movement_enabled = False 

# Global variable to track the current instruction message
current_instruction = None

def showInstructionMessage(message, color, duration):
    """Display an on-screen instruction message, replacing any existing one."""
    global current_instruction
    
    # Remove the previous instruction if it exists
    if current_instruction:
        current_instruction.remove()
        current_instruction = None
        
    screen_width, screen_height = viz.MainWindow.getSize()  # Get the screen dimensions

    # Adjust positions for the top-left corner
    # Using normalized screen coordinates: x=[0,1] and y=[0,1]
    
    msg_pos = [0.03, 0.90, 0]  # Slightly below celebration
    
    # Display the new instruction
    current_instruction = viz.addText(message, parent=viz.SCREEN, pos=msg_pos, scale=[0.3, 0.4, 0.4])
    current_instruction.color(color)
    
    # Automatically remove the instruction after the specified duration
    vizact.ontimer2(duration, 0, lambda: removeCurrentInstruction())

def removeCurrentInstruction():
    """Remove the current instruction message."""
    global current_instruction
    if current_instruction:
        current_instruction.remove()
        current_instruction = None
 
# At the beginning of the game (Level 1 start)
showInstructionMessage("Level 1 Starting!", color=viz.BLACK, duration=3)

def showScoreboardAndCelebration(task_score, total_score, is_goal):
    """Show the scoreboard and celebration animation for a completed task in the top-right corner."""
    screen_width, screen_height = viz.MainWindow.getSize()  # Get the screen dimensions

    # Adjust positions for the top-right corner
    # Using normalized screen coordinates: x=[0,1] and y=[0,1]
    celebration_pos = [0.75, 0.95, 0]  # Top-right for celebration
    scoreboard_pos = [0.75, 0.90, 0]  # Slightly below celebration

    # Display 'Task complete!'
    celebration_text = "Task complete!" 
    celebration = viz.addText(celebration_text, parent=viz.SCREEN, pos=celebration_pos, scale=[0.4, 0.5, 0.5])
    celebration.color(viz.BLACK)

    # Display task score and total score
    scoreboard_text = f"Task Score: {task_score}\nTotal Score: {total_score}"
    scoreboard = viz.addText(scoreboard_text, parent=viz.SCREEN, pos=scoreboard_pos, scale=[0.3, 0.4, 0.4])
    scoreboard.color(viz.BLACK)

    # Automatically remove the texts after a delay
    vizact.ontimer2(3, 0, celebration.remove)  # Remove celebration text
    vizact.ontimer2(3, 0, scoreboard.remove)   # Remove scoreboard text
  
    
# Load an arrow model
arrow_model = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR1/arrow.fbx')

# Scale and position the arrow
arrow_model.setScale(0.02, 0.02, 0.02)  # Adjust the size
arrow_model.setPosition(0, 0, 0)     # Place it above the field
arrow_model.visible(viz.OFF)

# New variables to track ball stay time inside the goalpost
ball_inside_goal = False
time_inside_goal = 0  # Time the ball has stayed inside the goalpost
goal_pause_duration = 3  # Duration the ball pauses after scoring a goal
stay_required_time = 1  # Time the ball needs to stay for full points
last_corner_state = False  # Tracks whether the ball was in a corner inside the goal

##### Check if the ball enters the goal or goes out of bounds
def checkGoal():
    global score, current_task, field_width, field_depth, break_in_progress, game_complete, ball_inside_goal, time_inside_goal, last_corner_state

    if game_complete or break_in_progress:
        return  # Skip checks if the game is complete or during the break

    ball_pos = ball.getPosition()

    # Check if all tasks are completed
    if current_task >= len(goal_positions):
        if field_width == field_width_level2:
            print("Level 2 complete! Congratulations!")
            vizact.ontimer2(0.05, 0, lambda: viz.quit())  # Exit the program after a short delay
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
            goalpost = goal_left if field_width == (100/8)+(4/3) else goal_left_level2
        elif current_task_index == 1:
            arrow_model.setEuler(0, 90, 0)
            arrow_model.setPosition(0, 0, 2)     # Place it above the field
            goalpost = goal_top if field_depth == (60/8)+(4/3) else goal_top_level2
        else:
            arrow_model.setEuler(0, 90, -90)  
            arrow_model.setPosition(2, 0, 0)     # Place it above the field
            goalpost = goal_right if field_width == (100/8)+(4/3) else goal_right_level2

        # Obtain the bounding box of the goalpost in world coordinates
        bounding_box = goalpost.getBoundingBox(viz.ABS_GLOBAL)
        goal_min = [bounding_box.xmin, bounding_box.ymin, bounding_box.zmin]
        goal_max = [bounding_box.xmax, bounding_box.ymax, bounding_box.zmax]
        
        # Calculate the 20% area of the goal (corners)
        corner_width = ((field_width-(4/3))*2-7)/4
        corner_depth = ((field_depth-(4/3))*2-7)/4
        
        # Determine the goalpost type and check ball position accordingly
        if current_task_index == 0:  # Left goalpost
            is_in_left_corner = False
            is_in_right_corner = False  # No right corner in left goal
            is_in_bottom_corner = (
                (goal_min[2] >= ball_pos[2] >= goal_min[2]-corner_depth and
                goal_min[0] <= ball_pos[0] <= goal_max[0])
            )
            is_in_top_corner = (
                (goal_max[2] <= ball_pos[2] <= goal_max[2]+corner_depth and
                goal_min[0] <= ball_pos[0] <= goal_max[0]) 
            )
        elif current_task_index == 1:  # Top goalpost
            is_in_left_corner = (
                (goal_min[0] >= ball_pos[0] >= goal_min[0]-corner_depth and
                goal_min[2] <= ball_pos[2] <= goal_max[2])
            )
            is_in_right_corner = (
                (goal_max[0] <= ball_pos[0] <= goal_max[0]+corner_depth and
                goal_min[2] <= ball_pos[2] <= goal_max[2])
            )
            is_in_top_corner = False  # No top corner in the top goal
            is_in_bottom_corner = False  # No bottom corner in the top goal
        elif current_task_index == 2:  # Right goalpost
            is_in_left_corner = False  # No left corner in the right goal
            is_in_right_corner = False
            is_in_bottom_corner = (
                (goal_min[2] >= ball_pos[2] >= goal_min[2]-corner_depth and
                goal_min[0] <= ball_pos[0] <= goal_max[0])
            )
            is_in_top_corner = (
                (goal_max[2] <= ball_pos[2] <= goal_max[2]+corner_depth and
                goal_min[0] <= ball_pos[0] <= goal_max[0]) 
            )
        
        # Check if the ball is within the goalpost bounding box
        is_inside_goal = (
            goal_min[0] <= ball_pos[0] <= goal_max[0] and
            goal_min[1] <= ball_pos[1] <= goal_max[1] and
            goal_min[2] <= ball_pos[2] <= goal_max[2]
        )

        if is_inside_goal or is_in_left_corner or is_in_right_corner or is_in_top_corner or is_in_bottom_corner:                
            if not ball_inside_goal:
                ball_inside_goal = True
                time_inside_goal = 0  # Reset stay timer
                print("Ball entered the goalpost area. Timer started.")

            # Increment the stay timer if ball stays inside
            time_inside_goal += viz.elapsed()  # Increment timer by elapsed time
            
            # Update corner state
            last_corner_state = (
                is_in_left_corner or is_in_right_corner or 
                is_in_top_corner or is_in_bottom_corner
            )

            if time_inside_goal >= stay_required_time:
                if is_in_left_corner or is_in_right_corner or is_in_top_corner or is_in_bottom_corner:
                    # Award 60 points if the ball is in the corner
                    task_score = 80
                    score += task_score
                    print(f"Ball entered the corner! You earned {task_score} points. Total score: {score}.")
                    showScoreboardAndCelebration(task_score, score, True)
                    current_task += 1
                    pauseBallInGoal() # Pause the ball for the goal pause duration
                else:
                    task_score = 100
                    score += task_score
                    print(f"Goal! You earned {task_score} points. Total score: {score}.")
                    showScoreboardAndCelebration(task_score, score, True)
                    current_task += 1
                    pauseBallInGoal()  # Pause the ball for the goal pause duration
                    
            if current_task==3 and field_width == (100/8)+(4/3):
                showInstructionMessage("Level 1 Complete! Congratulations!", color=viz.BLACK, duration=3)
            elif current_task==3 and field_width != (100/8)+(4/3):
                showInstructionMessage("Level 2 Complete! Congratulations!", color=viz.BLACK, duration=3)
            return
        else:
            # Reset the state for the next check
            ball_inside_goal = False
            if time_inside_goal >0 and time_inside_goal < stay_required_time:
                # Ball left prematurely before reaching the required stay time
                if last_corner_state:
                    task_score = 60
                else:
                    task_score = 80
                score += task_score
                print(f"Ball left the goal early. You earned {task_score} points. Total score: {score}.")
                showScoreboardAndCelebration(task_score, score, False)
                startBreak()  # Reset ball to the center
                current_task += 1
                time_inside_goal = 0
                last_corner_state = False
            
        # Check if the ball goes out of bounds
        if abs(ball_pos[0]) > field_width-0.5 or abs(ball_pos[2]) > field_depth-0.5:
            task_score = 60
            score += task_score 
            print(f"Ball went out of bounds! Your score {score}. Task {current_task + 1} failed.")
            showScoreboardAndCelebration(task_score, score, False)  # Show scoreboard without celebration
            current_task += 1
            if current_task==3 and field_width == (100/8)+(4/3):
                showInstructionMessage("Level 1 Complete! Congratulations!", color=viz.BLACK, duration=3)
            elif current_task==3 and field_width != (100/8)+(4/3):
                showInstructionMessage("Level 2 Complete! Congratulations!", color=viz.BLACK, duration=3)
            startBreak()  # Start the 5-second break
            return

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
    vizact.ontimer2(5, 0, endBreak)  # Resume after 5 seconds

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
    vizact.ontimer2(5, 0, endBreak)  # Resume after 5 seconds

# Reset ball position to center
def resetBallPosition():
    """Reset ball position to the center of the field and disable movement."""
    global ball_movement_enabled, ball_inside_goal
    ball_inside_goal = False
    ball.setPosition(0, 0.1, 0)  # Center the ball
    hockey_stick.setPosition(0, 0.1, 0)  # Place stick near the ball
    ball_movement_enabled = False  # Ensure movement remains disabled
    print("Ball reset to center position.")
   
##### Initially disable ball movement 
def onKeyDown(key):
    global ball_movement_enabled

    if key == viz.KEY_RETURN or key == " ":  # Enter or Space key
        ball_movement_enabled = not ball_movement_enabled  # Toggle movement
        if ball_movement_enabled:
            print("Ball movement enabled.")
        else:
            print("Ball movement paused.")    

### Update ball position based on mouse input
def updateBallPosition():
    viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
    global current_task
    # Prevent ball movement during break
    if break_in_progress or not ball_movement_enabled:
        return  # Skip updating ball position
        
    mouse_x = viz.mouse.getPosition()[0] * 2 - 1  # Scale and center
    mouse_z = viz.mouse.getPosition()[1] * 2 - 1  # Scale and center

    # Map mouse position to field size
    ball_x = mouse_x * field_width
    ball_z = mouse_z * field_depth

    # Update ball position
    ball.setPosition(ball_x, 0.1, ball_z)
    hockey_stick.setPosition(ball_x, 0.1, ball_z)  # Place stick near the ball
    
    if task_order[current_task]==0:
        hockey_stick.setEuler(-90, 0, 0)                  # Adjust rotation if needed
        # Update stick position near the ball
        hockey_stick.setPosition(ball_x+0.5, 0.1, ball_z)  # Place stick near the ball
        
    if task_order[current_task]==1:
        hockey_stick.setEuler(0, 0, 0)                  # Adjust rotation if needed
        # Update stick position near the ball
        hockey_stick.setPosition(ball_x , 0.1, ball_z)  # Place stick near the ball
    
    if task_order[current_task]==2:
        hockey_stick.setEuler(-270, 0, 0)                  # Adjust rotation if needed
        # Update stick position near the ball
        hockey_stick.setPosition(ball_x-0.5, 0.1, ball_z)  # Place stick near the ball
        


# Global variable to track if a break is in progress
break_in_progress = False
# Add this global variable
game_complete = False

# Level 2 configurations
field_width_level2 = (100/6)+(4/3)  # Half the field size for Level 2
field_depth_level2 = (60/6)+(4/3)
goal_positions_level2 = [
    (-100/6, 0.2, 0),  # Left goal for Level 2
    (0, 0.2, 100/6),   # Top goal for Level 2
    (100/6, 0.2, 0)    # Right goal for Level 2
]

# Goalpost and boundary objects for Level 2
goal_left_level2 = None
goal_right_level2 = None
goal_top_level2 = None
boundary_objects_level2 = []

def setupLevel2():
    global goal_left_level2, goal_right_level2, goal_top_level2, boundary_objects_level2

    # Create larger goalposts for Level 2
    goal_left_level2 = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/hockey_gate/hockey_gate.fbx')
    goal_right_level2 = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/hockey_gate/hockey_gate.fbx')
    goal_top_level2 = vizfx.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR2/hockey_gate/hockey_gate.fbx')

    # Position and scale Level 2 goalposts ((115 X 74)/3 yards)
    goal_left_level2.setPosition((-100/6)-(1/3), 0.01, 0)
    goal_left_level2.setScale(scale_x, scale_y, scale_z)
    goal_left_level2.setEuler(-90, 0, 0)

    goal_right_level2.setPosition((100/6)+(1/3), 0.01, 0)
    goal_right_level2.setScale(scale_x, scale_y, scale_z)
    goal_right_level2.setEuler(90, 0, 0)

    goal_top_level2.setPosition(0, 0.01, (60/6)+(1/3))
    goal_top_level2.setScale(scale_x, scale_y, scale_z)
    goal_top_level2.setEuler(0, 0, 0)

    # Create larger boundaries for Level 2
    boundary_objects_level2 = [
        vizshape.addBox(size=(100/3, 0.01, 0.1)),  # Top boundary
        vizshape.addBox(size=(100/3, 0.01, 0.1)),  # Bottom boundary
        vizshape.addBox(size=(0.1, 0.01, 60/3)),  # Left boundary
        vizshape.addBox(size=(0.1, 0.01, 60/3))   # Right boundary
    ]
    boundary_objects_level2[0].setPosition(0, 0.01, 60/6)  # Top boundary
    boundary_objects_level2[1].setPosition(0, 0.01, -60/6)  # Bottom boundary
    boundary_objects_level2[2].setPosition(-100/6, 0.01, 0)  # Left boundary
    boundary_objects_level2[3].setPosition(100/6, 0.01, 0)   # Right boundary
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
    viz.MainView.setPosition(0, 30, -30)   # Higher and farther camera position
    viz.MainView.setEuler(0, 40, 0)        # Tilt camera to look down
    
    # Reset ball position and disable movement
    resetBallPosition()
    ball_movement_enabled = False

    print("Welcome to Level 2! The field and goalposts have expanded!")
    showInstructionMessage("Welcome to Level 2!", color=viz.BLACK, duration=3)
    # to randomise the tasks
    setupGame()
    
    
# Register continuous callbacks
vizact.ontimer(0, updateBallPosition)
vizact.ontimer(0.1, checkGoal)