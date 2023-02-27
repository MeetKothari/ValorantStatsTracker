import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

agentList = {}
roles = {
    "Brimstone": "Controller",
    "Viper": "Controller",
    "Astra": "Controller",
    "Cypher": "Sentinel",
    "Killjoy": "Sentinel",
    "Sova": "Initiator",
    "Breach": "Initiator",
    "Skye": "Initiator",
    "Phoenix": "Duelist",
    "Jett": "Duelist",
    "Reyna": "Duelist",
    "Fade": "Initiator",
    "Harbor": "Controller",
    "Yoru": "Duelist",
    "Chamber": "Sentinel",
    "Neon": "Duelist",
    "Sage": "Sentinel",
    "Omen": "Controller",
    "Raze": "Duelist",
    "KAY/O": "Initiator"
}


# Define the URL to scrape
url = "https://tracker.gg/valorant/profile/riot/meetydactyl%23wacky/agents?season=all"

# Send a GET request to the URL and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all tags containing the playtime data for specific agents
playtime_tags = soup.find_all("div", {"class": "value"})

# Partition the tags into smaller lists of 18 tags each
partitioned_tags = [playtime_tags[i:i+18]
                    for i in range(0, len(playtime_tags), 19)]

# Create a dictionary to store the partitioned tags
tag_dict = {}

# Loop through each partition and add it to the dictionary with a unique key
for i, tags in enumerate(partitioned_tags):
    tag_dict[f"list_{i+1}"] = tags

# Loop through each partition and add the first two values to the agentList dictionary
for key, value in tag_dict.items():
    # Get the name of the agent
    agent_name = value[0].text
    # Initialize the list for the agent if it doesn't exist
    if agent_name not in agentList:
        agentList[agent_name] = []
    # Append the second value to the list for the agent
    playtime_str = value[1].text
    if "hrs" in playtime_str:
        playtime = playtime_str.split()[0]
    else:
        playtime = playtime_str
    agentList[agent_name].append(playtime)
    if agent_name in roles:
        agentList[agent_name].append(roles[agent_name])
    else:
        agentList[agent_name].append("Unknown")

# Create a new dictionary to store all the data for the table
table_data = {}

# Calculate the total playtime and role of each agent and add them to the table_data dictionary
for agent, playtimes in agentList.items():
    total_playtime = 0
    for playtime_str in playtimes:
        # Check if the playtime string contains "hrs"
        if "hrs" in playtime_str:
            # If it does, extract the numerical value and convert it to a float
            playtime = float(playtime_str.split()[0])
        else:
            # Otherwise, check if the string is numeric before converting it to a float
            if playtime_str.isnumeric():
                playtime = float(playtime_str)
            else:
                # Handle the case where the string is not numeric (e.g. a period '.')
                playtime = 0
        total_playtime += playtime
    # Calculate the percentage based on the role of the agent
    role = roles.get(agent, "Unknown")
    role_playtime = sum([float(x.split()[
                        0]) for x in playtimes if "hrs" in x and roles.get(agent, "Unknown") == role])
    percentage = f"{(role_playtime / total_playtime) * 100:.2f}%" if total_playtime > 0 else "N/A"
    # Add the agent data to the table_data dictionary
    table_data[agent] = {"playtimes": playtimes,
                         "total_playtime": total_playtime,
                         "role": role,
                         "percentage": percentage}

# Create a prettytable object with the required columns
table = PrettyTable()
table.field_names = ["Agent", "Playtimes (hrs)", "Role", "Percentage"]

# Add data to the table
for agent, data in table_data.items():
    playtimes = ", ".join(data["playtimes"])
    role = data["role"]
    percentage = data["percentage"]
    table.add_row([agent, playtimes, role, percentage])

# Print the table
print(table)
