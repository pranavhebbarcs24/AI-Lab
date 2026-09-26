roomA = input("Enter status of Room A (Dirty/Clean): ").lower()
roomB = input("Enter status of Room B (Dirty/Clean): ").lower()

location = input("Enter current location (A/B): ").upper()
direction = input("Enter direction (left/right): ").lower()

# Wall between Room A and Room B
wall_between = input("Is there a wall between Room A and Room B? (yes/no): ").lower()

while roomA == "dirty" or roomB == "dirty":

    # ---------------- ROOM A ----------------
    if location == "A":

        if roomA == "dirty":
            print("Cleaning Room A...")
            roomA = "clean"

        else:
            # Try to move from A to B
            if wall_between == "yes":
                print("Wall detected between Room A and Room B!")
                print("Cannot move from Room A to Room B.")
                break
            else:
                print("Moving right from Room A to Room B...")
                direction = "right"
                location = "B"

    # ---------------- ROOM B ----------------
    elif location == "B":

        if roomB == "dirty":
            print("Cleaning Room B...")
            roomB = "clean"

        else:
            # Try to move from B to A
            if wall_between == "yes":
                print("Wall detected between Room A and Room B!")
                print("Cannot move from Room B to Room A.")
                break
            else:
                print("Moving left from Room B to Room A...")
                direction = "left"
                location = "A"


# Final status
if roomA == "clean" and roomB == "clean":
    print("\nGoal State Reached!")
else:
    print("\nGoal State Not Reached because movement is blocked.")

print("Room A:", roomA)
print("Room B:", roomB)
print("Final Location:", location)
print("Final Direction:", direction)

