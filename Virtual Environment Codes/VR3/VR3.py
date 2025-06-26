import viz
import vizshape
import vizfx
import vizact
import vizinfo

viz.go()

# Set background and lighting
viz.clearcolor(viz.SKYBLUE)  # Sky blue background
light = viz.addLight()
light.position(0, 10, 0)    # Light source above the field

# Add predefined ground model
ground = viz.addChild('ground.osgb')  # Load ground model
ground.setPosition(0, 0, 0)           # Position it at the origin
ground.setScale(0.8, 0.8, 0.8)
ground.collidePlane()                 # Enable collision with the ground

# Add parking spots as horizontal rectangles
parking_spot_left = vizshape.addBox(size=(4, 0.01, 3))  # Width = 2, Height = 0.01, Length = 4
parking_spot_left.setPosition(-11, 0.005, 0)  # Left parking spot
parking_spot_left.color(viz.BLACK)             # Gray color for parking spots

parking_spot_top = vizshape.addBox(size=(3, 0.01, 4))   # Width = 4, Height = 0.01, Length = 2
parking_spot_top.setPosition(0, 0.005, 11)   # Top parking spot
parking_spot_top.color(viz.BLACK)

parking_spot_right = vizshape.addBox(size=(4, 0.01, 3))  # Width = 2, Height = 0.01, Length = 4
parking_spot_right.setPosition(11, 0.005, 0)  # Right parking spot
parking_spot_right.color(viz.BLACK)




# Add a car at the center
car = viz.addChild('C:/IITGN 2nd year/Muscle Synergy Project/Vizard/VR3/car/Low-Poly-Racing-Car.fbx')  # Load the car model
car.setPosition(0, 0.2, 0)           # Center the car on the lot
car.setScale(0.01, 0.01, 0.01)         # Scale the car

# Adjust camera position to view the entire parking lot
viz.MainView.setPosition(0, 17, -17)   # Camera above and behind the lot
viz.MainView.setEuler(0, 45, 0)        # Tilt the camera to look down
viz.MainView.collision(False)

game_complete = False

# Variables to track game state
lot_size = 12  # Half the parking lot size
score = 0
current_task = 0  # 0: left parking spot, 1: top parking spot, 2: right parking spot
parking_spot_positions = [
    (-11, 0.2, 0),  # Left parking spot
    (0, 0.2, 11),   # Top parking spot
    (11, 0.2, 0)    # Right parking spot
]
parking_spot_orientations = [
    -90,   # Facing right for the left parking spot
    0,  # Facing down for the top parking spot
    90   # Facing left for the right parking spot
]


def showScoreboardAndCelebration(task_score, total_score, is_success):
    """Show the scoreboard and celebration animation for parking completion."""
    # Display 'Parked Successfully!' or 'Out of Bounds!'
    celebration_text = "Task complete" 
    celebration = viz.addText3D(celebration_text, pos=[-2, 2, 0], scale=[1, 1, 1])
    celebration.color(viz.YELLOW if is_success else viz.RED)
    
    # Display task score and total score
    scoreboard_text = f"Task Score: {task_score}\nTotal Score: {total_score}"
    scoreboard = viz.addText3D(scoreboard_text, pos=[-2, 1.5, 0], scale=[0.7, 0.7, 0.7])
    scoreboard.color(viz.WHITE)

    # Automatically remove the texts after a delay
    vizact.ontimer2(3, 0, celebration.remove)  # Remove celebration text
    vizact.ontimer2(3, 0, scoreboard.remove)   # Remove scoreboard text


# Check if the car enters the parking spot or goes out of bounds
def checkParking():
    global score, current_task, lot_size, break_in_progress, game_complete

    if game_complete or break_in_progress:
        return  # Skip checks if the game is complete or during the break

    car_pos = car.getPosition()

    # Check if all tasks are completed
    if current_task >= len(parking_spot_positions):
        if lot_size == lot_size_level2:
            print("Level 2 complete! Congratulations!")
            vizact.ontimer2(0.05, 0, lambda: viz.quit())  # Exit the program after a short delay
        else:
            print("Level 1 complete! Congratulations!")
            switchToLevel2()
        return

    
    if current_task < len(parking_spot_positions):
        park_pos = parking_spot_positions[current_task]

        # Get the bounding box dimensions of the current goalpost
        if current_task == 0:
            goalpost = parking_spot_left if lot_size == 12 else parking_spot_left_level2
        elif current_task == 1:
            goalpost = parking_spot_top if lot_size == 12 else parking_spot_top_level2
        else:
            goalpost = parking_spot_right if lot_size == 12 else parking_spot_right_level2

        # Obtain the bounding box of the goalpost in world coordinates
        bounding_box = goalpost.getBoundingBox(viz.ABS_GLOBAL)
        
        is_inside_parking = (
            bounding_box.xmin <= car_pos[0] <= bounding_box.xmax and
            bounding_box.zmin <= car_pos[2] <= bounding_box.zmax
        )


        if is_inside_parking:
            task_score = 100
            score += task_score
            print(f"Parked successfully! Your score is now {score}. Task {current_task + 1} complete!")
            showScoreboardAndCelebration(task_score, score, True)
            current_task += 1
            startBreak()
            return

        # Check if the car goes out of bounds
        if abs(car_pos[0]) > lot_size-1.5 or abs(car_pos[2]) > lot_size-1.5:
            task_score = 50
            score += task_score
            print(f"Car went out of bounds! Your score {score}. Task {current_task + 1} failed.")
            showScoreboardAndCelebration(task_score, score, False)
            current_task += 1
            startBreak()
            return


def startBreak():
    """Initiate a 5-second break and reset the car."""
    global break_in_progress
    break_in_progress = True
    print("Taking a 5-second break...")
    updateCarState()  # Reset the car's position and orientation
    vizact.ontimer2(5, 0, endBreak)

def endBreak():
    """End the break and prepare for the next task."""
    global break_in_progress
    break_in_progress = False
    if current_task < len(parking_spot_positions):  # Only print if there are valid tasks remaining
        print(f"Task {current_task + 1} starting now!")
    
def resetCarPosition():
    """Reset car position to the center of the lot."""
    car.setPosition(0, 0.2, 0)

def updateCarState():
    """Update car position based on mouse input and set a fixed orientation based on the current task."""
    global break_in_progress, current_task

    # If all tasks are completed, stop further updates
    if current_task >= len(parking_spot_positions):
        return

    # Get mouse input for car movement
    mouse_x = viz.mouse.getPosition()[0] * 2 - 1  # Scale and center
    mouse_z = viz.mouse.getPosition()[1] * 2 - 1  # Scale and center

    # Map mouse input to parking lot dimensions
    car_x = mouse_x * lot_size
    car_z = mouse_z * lot_size

    # Update the car position
    car.setPosition(car_x, 0.2, car_z)

    # Set the fixed orientation based on the current task
    fixed_orientation = parking_spot_orientations[current_task]
    car.setEuler([fixed_orientation, 0, 0])


# Global variable to track if a break is in progress
break_in_progress = False
# Add this global variable
game_complete = False

# Level 2 configurations
lot_size_level2 = 17  # Larger parking lot size for Level 2
parking_spot_positions_level2 = [
    (-16, 0.2, 0),  # Left parking spot for Level 2
    (0, 0.2, 16),   # Top parking spot for Level 2
    (16, 0.2, 0)    # Right parking spot for Level 2
]
parking_spot_orientations_level2 = [
    -90,   # Facing right for the left parking spot
    0,  # Facing down for the top parking spot
    90   # Facing left for the right parking spot
]

# Level 2 parking spots and boundaries
parking_spot_left_level2 = None
parking_spot_top_level2 = None
parking_spot_right_level2 = None
boundary_objects_level2 = []

def setupLevel2():
    global parking_spot_left_level2, parking_spot_top_level2, parking_spot_right_level2, boundary_objects_level2

    # Add larger parking spots for Level 2
    parking_spot_left_level2 = vizshape.addBox(size=(4, 0.01, 3))
    parking_spot_left_level2.setPosition(-16, 0.005, 0)
    parking_spot_left_level2.color(viz.BLACK)

    parking_spot_top_level2 = vizshape.addBox(size=(3, 0.01, 4))
    parking_spot_top_level2.setPosition(0, 0.005, 16)
    parking_spot_top_level2.color(viz.BLACK)

    parking_spot_right_level2 = vizshape.addBox(size=(4, 0.01, 3))
    parking_spot_right_level2.setPosition(16, 0.005, 0)
    parking_spot_right_level2.color(viz.BLACK)

    
def switchToLevel2():
    global lot_size, parking_spot_positions, parking_spot_orientations, current_task

    # Hide Level 1 objects
    parking_spot_left.visible(False)
    parking_spot_top.visible(False)
    parking_spot_right.visible(False)

    # Setup Level 2
    setupLevel2()

    # Update game state for Level 2
    lot_size = lot_size_level2
    parking_spot_positions[:] = parking_spot_positions_level2
    parking_spot_orientations[:] = parking_spot_orientations_level2
    current_task = 0

    # Adjust camera viewpoint for Level 2
    viz.MainView.setPosition(0, 22, -22)   # Higher and farther camera position
    viz.MainView.setEuler(0, 45, 0)        # Tilt camera to look down

    print("Welcome to Level 2! The parking spots and field are larger!")


vizact.ontimer(0, updateCarState)  # Continuously handle car state
vizact.ontimer(0.1, checkParking)  # Periodically check parking status

