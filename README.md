# Greenhouse Management System - Software Engineering for Internet of Things

The IoT-Based Greenhouse Management System is an innovative solution engineered to monitor and regulate environmental conditions within multiple greenhouses. Equipped with a variety of IoT sensors, the system continuously measures key parameters such as temperature, CO2 levels, light intensity, humidity, and soil moisture. The primary objective is to maintain optimal growing conditions, thereby enhancing plant health and productivity. This system allows for real-time data monitoring and the setting of customized thresholds tailored to the specific requirements of different plant species.

![Greenhouse Management Dashboard](greenhouse.webp)

## Steps to Execute Project

1. **Install Docker Desktop**:
   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
2. **Start Docker Desktop**:
   - Ensure Docker is running before you proceed.
3. **Set up the Project**:
   - Open the project folder in the terminal and execute the following commands sequentially:
     ```
     docker-compose build
     docker-compose up
     ```

## Functional Requirements

The system is designed to meet the following functional requirements:

| ID  | Requirement Name  | Description |
|-----|-------------------|-------------|
| 1.  | Sensor Integration| Must integrate multiple precise sensors to measure environmental factors like temperature, CO2, light intensity, humidity, and soil moisture. |
| 2.  | Data Gathering    | Should support the continuous inflow of data collected from the sensors. |
| 3.  | Efficient Storage | Must store data effectively for historical analysis and trend prediction. |
| 4.  | Remote Monitoring | Should allow monitoring of the collected data through a web or mobile-based application. |
| 5.  | Data Visualization| Must present the stored data through interpretable and interactive charts and graphs. |

## Non-functional Requirements

The project also adheres to the following non-functional requirements:

| ID  | Requirement Name  | Description |
|-----|-------------------|-------------|
| 1.  | Reliability       | System must operate continuously without significant downtime. |
| 2.  | Scalability       | Should support easy addition of more sensors or functionalities as needed. |
| 3.  | Usability         | Must be user-friendly, providing intuitive navigation and interaction for users of all technical levels. |
| 4.  | Security          | Needs to ensure secure data transmission to prevent unauthorized access. |
| 5.  | Maintainability   | Should be easy to maintain and flexible to accommodate updates and enhancements. |
| 6.  | Availability      | System must be consistently available to ensure ongoing monitoring and alerting capabilities. |

## Technologies Used for Project Implementation

- **Python**: Utilized for generating synthetic datasets and backend logic.
- **Docker**: Employed for container orchestration to manage software dependencies easily.
- **Node-RED**: Used for developing the data flow and integration logic within the project.
- **Mosquitto**: Acts as the MQTT broker for reliable communication between the different project components.
- **InfluxDB**: Chosen for its time series data storage capabilities, ideal for environmental data.
- **Grafana**: Used for powerful data visualization, providing dashboards to visualize trends and real-time conditions.

## Data Visualization

The system leverages Grafana for its data visualization needs, providing a comprehensive dashboard that visualizes real-time data and historical trends. These visualizations help in quick decision-making and enhanced monitoring of the greenhouse environments.

![Greenhouse Data Visualization](Dashboard.jpg)
