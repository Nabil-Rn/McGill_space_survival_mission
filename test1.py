import matplotlib.pyplot as plt

# Define the parameters for each stage (These values are approximations based on Saturn V)
stages = {
    'Stage 1': {
        'thrust': 3.3e6,  # N
        'burn_time': 120,  # seconds
        'burn_rate': 12600,  # kg/s
    },
    'Stage 2': {
        'thrust': 1e6,  # N
        'burn_time': 100,  # seconds
        'burn_rate': 2000,  # kg/s
    },
    'Stage 3': {
        'thrust': 225000,  # N
        'burn_time': 180,  # seconds
        'burn_rate': 1000,  # kg/s
    }
}



def rocket_simulation(dry_mass):
    # Initial values
    initial_fuel_mass = 2_340_000  # kg
    remaining_fuel = initial_fuel_mass
    velocity = 0
    altitude = 0
    time_step = 1  # Time step for calculations in seconds

    # Lists to store data for plotting
    times = []
    velocities = []
    altitudes = []
    accelerations = []
    remaining_fuels = []

    # Variable to track cumulative time
    total_time = 0

    # Simulate each stage
    for stage_name, stage_params in stages.items():
        thrust = stage_params['thrust']
        burn_time = stage_params['burn_time']
        burn_rate = stage_params['burn_rate']

        # Calculate the initial mass at the start of the stage
        initial_mass = dry_mass + remaining_fuel
        stage_mass = initial_mass
        print(f"\nStarting {stage_name} with Initial Mass: {initial_mass:.2f} kg and Fuel: {remaining_fuel:.2f} kg")

        # Stage loop
        for t in range(0, burn_time, time_step):
            # Ensure the rocket mass doesn't become negative
            if stage_mass <= 0:
                break

            # Calculate acceleration (Thrust / Mass)
            acceleration = thrust / stage_mass

            # Update velocity and altitude
            velocity += acceleration * time_step
            altitude += velocity * time_step

            # Ensure altitude doesn't decrease due to negative velocity (basic check)
            if altitude < 0:
                altitude = 0

            # Update fuel
            remaining_fuel -= burn_rate * time_step
            if remaining_fuel < 0:
                remaining_fuel = 0

            # Update the mass for the next time step (fuel is burned)
            stage_mass = dry_mass + remaining_fuel

            # Save data for plotting
            total_time += time_step
            times.append(total_time)  # Track cumulative time
            velocities.append(velocity)
            altitudes.append(altitude)
            accelerations.append(acceleration)
            remaining_fuels.append(remaining_fuel)

        # Print remaining fuel and total mass after each stage
        total_mass = dry_mass + remaining_fuel
        print(f"\nEnd of {stage_name}:")
        print(f"  - Remaining Fuel = {remaining_fuel:.2f} kg")
        print(f"  - Total Mass = {total_mass:.2f} kg")
        print(f"  - Altitude = {altitude:.2f} m")
        print(f"  - Velocity = {velocity:.2f} m/s")
        print(f"  - Acceleration = {acceleration:.2f} m/s²")

    if altitude < 100000:
        print("Unsuccessful launch, you have crashed into Earth.")
    else:
        print("Successful launch!")

    # Plot results
    plt.figure(figsize=(12, 12))

    plt.subplot(3, 1, 1)
    plt.plot(times, velocities, label="Velocity (m/s)", color='blue')
    plt.title("Velocity vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(times, altitudes, label="Altitude (m)", color='green')
    plt.title("Altitude vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(times, accelerations, label="Acceleration (m/s²)", color='red')
    plt.title("Acceleration vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# Get user input for dry mass
dry_mass_input = float(input("Enter the dry mass of the rocket in kg: "))
rocket_simulation(dry_mass_input)



#init_v is the Final velosity after the stage 3 launch

def lunar_landing_simulation(init_v):
    # Constants
    Thrust = -9880648.74  # N
    Burn_rate = 2000  # kg/s
    init_mass = 748000.00  # kg
    Remaining_Fuel = 448000.00  # kg
    Moon_gravity = 1.62  # m/s² (Moon gravity acceleration)
    initial_height = 4478.68  # meters above the Moon's surface

    # Initial conditions
    current_velocity = init_v
    current_mass = init_mass
    current_position = initial_height
    distance_traveled = 0
    total_burn_time = 0

    # Lists to store simulation data for plotting
    time_list = []
    velocity_list = []
    position_list = []
    mass_list = []
    time_elapsed = 0  # Track total simulation time

    # Simulation parameters
    min_duration = 0.01  # Minimum time step in seconds for fine resolution
    Duration = 1  # Initial time step in seconds
    velocity_threshold = 0.1  # Threshold to switch to smaller duration steps
    safe_landing_velocity = 2.0  # Target velocity for safe landing (m/s)

    # Simulation loop
    while current_position > 0 and current_mass > init_mass - Remaining_Fuel:
        # Dynamically adjust the time step when close to the surface
        if current_position < 100 or abs(current_velocity) < velocity_threshold:
            Duration = min_duration  # Use finer time step as position or velocity approaches target

        # Record data for plotting
        time_list.append(time_elapsed)
        velocity_list.append(current_velocity)
        position_list.append(current_position)
        mass_list.append(current_mass)

        # Calculate acceleration: a = (Thrust / current_mass) - gravity
        acceleration = (Thrust / current_mass) - Moon_gravity
        vel_change = Duration * acceleration
        previous_velocity = current_velocity  # Save the previous velocity
        current_velocity += vel_change  # Update velocity

        # Calculate new position
        avg_velocity = (previous_velocity + current_velocity) / 2  # Average velocity over the time step
        current_position -= avg_velocity * Duration  # Update position

        # Calculate mass change
        mass_change = Burn_rate * Duration
        current_mass -= mass_change  # Update mass

        # Accumulate burn time and elapsed time
        total_burn_time += Duration  # Add the duration of this step to total burn time
        time_elapsed += Duration

        # Ensure mass does not go below the dry mass
        if current_mass <= init_mass - Remaining_Fuel:
            current_mass = init_mass - Remaining_Fuel
            break

        # Ensure position does not go below the Moon's surface
        if current_position <= 0:
            current_position = 0
            break

        if current_velocity > 1:
            print("You have crashed on the Moon.")
        else:
            print("You have successfully landed.")

    # Print final state at touchdown
    print("Simulation complete.")
    print(f"Final Velocity at touchdown: {current_velocity:.2f} m/s")
    print(f"Final Mass at touchdown: {current_mass:.2f} kg")

    # Plotting the data
    plt.figure(figsize=(14, 6))

    # Plot velocity over time
    plt.subplot(1, 2, 1)
    plt.plot(time_list, velocity_list, label='Velocity (m/s)', color='blue')
    plt.title('Velocity over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (m/s)')
    plt.grid(True)
    plt.legend()

    # Plot position over time
    plt.subplot(1, 2, 2)
    plt.plot(time_list, position_list, label='Position (meters)', color='green')
    plt.title('Position over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Position (meters)')
    plt.grid(True)
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()


init_v = float(input("Enter the velocity "))
lunar_landing_simulation(init_v)

