roomA = input("Enter status of Room A (Dirty/Clean): ").lower()
roomB = input("Enter status of Room B (Dirty/Clean): ").lower()
location = input("Enter current location (A/B): ").upper()
while roomA == "dirty" or roomB == "dirty":
    if location == "A":
        if roomA == "dirty":

            print("Cleaning Room A...")

            roomA = "clean"
        else:

            print("Moving to Room B...")

            location = "B"
    else:

        if roomB == "dirty":

            print("Cleaning Room B...")

            roomB = "clean"
        else:

            print("Moving to Room A...")

            location = "A"
print("\nGoal State Reached!")

print("Room A:", roomA)

print("Room B:", roomB) 
