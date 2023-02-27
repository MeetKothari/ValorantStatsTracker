import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

agentList = {} # for eventual agents
agent_percentages = {}

# For role mapping
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
# Create a new dictionary to store all the data for the table
table_data = {}


# dynamic user retrieval, commented out for testing purposes
# username, tagline = input("Enter your username on Valorant, followed by your tagline(this is the part of your username following the '#'): ").split()

username = "meetydactyl"
tagline = "wacky"


# Define the URL to scrape
url = "https://tracker.gg/valorant/profile/riot/"+username+"%23"+tagline+"/agents?season=all"

# Send a GET request to the URL and parse the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all tags containing the playtime data for specific agents
playtime_tags = soup.find_all("div", {"class": "value"})

# Partition the tags into smaller lists of 18 tags each
partitioned_tags = [playtime_tags[i:i+19]
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
    # if agent_name in roles:
    #     # agentList[agent_name].append(roles[agent_name])
    # else:
    #     agentList[agent_name].append("Unknown")

# Calculate the total playtime and role of each agent and add them to the table_data dictionary
# the variable total_playtime is being incremented for each agent
# but it should only be incremented once for the entire list of agents. 
# This is causing the percentages to be calculated incorrectly.

# To fix this, move the calculation of total_playtime outside of 
# the loop that iterates over the agents, and only calculate it once:

total_playtime = sum(float(playtime) 
                     for playtimes in agentList.values() for playtime in playtimes)

for agent, playtimes in agentList.items():
    percentages = [(float(x)/total_playtime)*100 for x in playtimes]
    agent_percentages[agent] = percentages

    # Add the agent data to the table_data dictionary
    table_data[agent] = {"playtimes": playtimes,
                         "total_playtime": total_playtime,
                         "role": roles.get(agent, "Unknown"),
                         "percentage": percentages}


# Create a prettytable object with the required columns
table = PrettyTable()
table.field_names = ["Agent", "Playtimes (hours)", "Role Classification", "Selection Percentage"]

# Add data to the table
for agent, data in table_data.items():
    playtimes = ", ".join(data["playtimes"])
    role = data["role"]
    percentage = data["percentage"]
    table.add_row([agent, playtimes, role, percentage])


print("Here is the current functionality in this program: \n")
print("(1): Not sure what you want? This option provides a complete overview of your stats...\n")
print("(2): Print complete agent data...\n")
print("(3): Explain and calculate your 'Role Suitability' multiplier...\n")
choice = input("What would you like to do? ")


def overview():
    print_table()

# Print the table
def print_table(): 
    print(table) 

def role_suitability():
    # Create a dictionary to store the percentages for each role
    role_percentages = {"Controller": [], "Sentinel": [], "Initiator": [], "Duelist": []}
    
    # Loop through each agent and add their percentages to the appropriate list based on their role
    for agent, data in table_data.items():
        role = data["role"]
        percentages = data["percentage"]
        role_percentages[role].extend(percentages)
        # Loop through each role and find the highest percentage
        highest_percentage = 0
        highest_role = ""
        for role, percentages in role_percentages.items():
            role_percentage = sum(percentages)
            if role_percentage > highest_percentage:
                highest_percentage = role_percentage
                highest_role = role
        
    # Print the percentages for each role
    for role, percentages in role_percentages.items():
        print(f"{role} Percentage: {sum(percentages):.2f}%")

    print(f"\nBased on your stats, it's clear that your role suitability is geared toward {(highest_role)} with a pick-rate of{highest_percentage: .2f}%")

    

if int(choice) == 1:
    overview()
elif int(choice) == 2:
    print_table()
elif int(choice) == 3:
    role_suitability()
    


