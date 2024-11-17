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
    """Simulates the rocket launch through different stages and returns the data for plotting."""
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

        # Stage loop
        for _ in range(0, burn_time, time_step):
            if stage_mass <= 0:
                break

            # Calculate acceleration, velocity, altitude, and fuel consumption
            acceleration = thrust / stage_mass
            velocity += acceleration * time_step
            altitude += velocity * time_step
            remaining_fuel -= burn_rate * time_step
            remaining_fuel = max(remaining_fuel, 0)

            # Update the mass for the next time step (fuel is burned)
            stage_mass = dry_mass + remaining_fuel

            # Save data for plotting
            total_time += time_step
            times.append(total_time)
            velocities.append(velocity)
            altitudes.append(altitude)
            accelerations.append(acceleration)
            remaining_fuels.append(remaining_fuel)

    success = altitude >= 100000
    return times, velocities, altitudes, accelerations, remaining_fuels, success

def lunar_landing_simulation(init_v):
    """Simulates the lunar landing sequence and returns the data for plotting."""
    Thrust = -9880648.74  # N
    Burn_rate = 2000  # kg/s
    init_mass = 748000.00  # kg
    Remaining_Fuel = 448000.00  # kg
    Moon_gravity = 1.62  # m/s²
    initial_height = 4478.68  # meters

    current_velocity = init_v
    current_mass = init_mass
    current_position = initial_height
    time_elapsed = 0
    Duration = 1
    min_duration = 0.01
    velocity_threshold = 0.1

    time_list = []
    velocity_list = []
    position_list = []

    while current_position > 0 and current_mass > init_mass - Remaining_Fuel:
        if current_position < 100 or abs(current_velocity) < velocity_threshold:
            Duration = min_duration

        acceleration = (Thrust / current_mass) - Moon_gravity
        vel_change = Duration * acceleration
        previous_velocity = current_velocity
        current_velocity += vel_change

        avg_velocity = (previous_velocity + current_velocity) / 2
        current_position -= avg_velocity * Duration

        mass_change = Burn_rate * Duration
        current_mass -= mass_change
        time_elapsed += Duration

        time_list.append(time_elapsed)
        velocity_list.append(current_velocity)
        position_list.append(current_position)

    success = current_velocity <= 1
    return time_list, velocity_list, position_list, success
