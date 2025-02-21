#
# header comment! Overview, name, etc.
#
import sqlite3
import matplotlib.pyplot as plt

##################################################################  
#
# print_stats
# PASSED
#
# Given a connection to the database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General Statistics:")
    
    # Number of Red Light Cameras
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")
    row = dbCursor.fetchone() # Get results as a Python tuple (retrieves next row of query)
    print("  Number of Red Light Cameras:", f"{row[0]:,}") # formatted string printing element at index 0 with commas to separate thousands

    # Start of manually entered general statistics (following roughly same format as given example above)

    # Number of Speed Cameras
    dbCursor.execute("SELECT COUNT(*) FROM SpeedCameras;")
    numSpeedCameras = dbCursor.fetchone() 
    print("  Number of Speed Cameras:", f"{numSpeedCameras[0]:,}")  

    # Number of Red Light Camera Violation Entries
    dbCursor.execute("SELECT COUNT(Num_Violations) FROM RedViolations")
    numRedViolations = dbCursor.fetchone()
    print("  Number of Red Light Camera Violation Entries:", f"{numRedViolations[0]:,}")

    # Number of Speed Camera Violation Entries
    dbCursor.execute("SELECT COUNT(Num_Violations) FROM SpeedViolations")
    numSpeedViolations = dbCursor.fetchone()
    print("  Number of Speed Camera Violation Entries:", f"{numSpeedViolations[0]:,}")

    # Range of Dates in the Database
    dbCursor.execute("SELECT MIN(Violation_Date), MAX(Violation_Date) FROM RedViolations")
    dateRange = dbCursor.fetchall()  # fetchall() used here: Get all the rows in the result as a Python list of tuples
    print("  Range of Dates in the Database:", dateRange[0][0], "-", dateRange[0][1])   # print result as double array because of fetchall()

    # Total Number of Red Light Camera Violations
    dbCursor.execute("SELECT SUM(Num_Violations) FROM RedViolations")
    sumRedViolations = dbCursor.fetchone()
    print("  Total Number of Red Light Camera Violations:", f"{sumRedViolations[0]:,}")

    # Total Number of Speed Camera Violations
    dbCursor.execute("SELECT SUM(NUM_Violations) FROM SpeedViolations")
    sumSpeedViolations = dbCursor.fetchone()
    print("  Total Number of Speed Camera Violations:", f"{sumSpeedViolations[0]:,}")


##################################################################  
#
# main
#
def main():
    dbConn = sqlite3.connect('chicago-traffic-cameras.db')

    print("Project 1: Chicago Traffic Camera Analysis")
    print("CS 341, Spring 2025")
    print()
    print("This application allows you to analyze various")
    print("aspects of the Chicago traffic camera database.")
    print()
    print_stats(dbConn)
    print()

    while True:
        userOption = main_menu()
        if userOption == "1":
            command_one(dbConn)
        elif userOption == "2":
            command_two(dbConn)
        elif userOption == "3":
            command_three(dbConn)
        elif userOption == "4":
            command_four(dbConn)
        elif userOption == "5":
            command_five(dbConn)
        elif userOption == "6":
            command_six(dbConn)
        elif userOption == "7":
            command_seven(dbConn)
        elif userOption == "8":
            command_eight(dbConn)
        elif userOption == "9":
            command_nine(dbConn)
        elif userOption == 'x':
            print("Exiting program.")
            break
        else:
            print("Error, unknown command, try again...")
            print()

##################################################################  
#
# main_menu
#
def main_menu():
    print("Select a menu option: ")
    print("  1. Find an intersection by name")
    print("  2. Find all cameras at an intersection")
    print("  3. Percentage of violations for a specific date")
    print("  4. Number of cameras at each intersection")
    print("  5. Number of violations at each intersection, given a year")
    print("  6. Number of violations by year, given a camera ID")
    print("  7. Number of violations by month, given a camera ID and year")
    print("  8. Compare the number of red light and speed violations, given a year")
    print("  9. Find cameras located on a street")
    print("or x to exit the program.")

    return input("Your choice --> ")
    #print()

##################################################################  
#
# command_one: Find intersection by name
# PASSED
#
def command_one(dbConn):
    print()
    userInput = input("Enter the name of the intersection to find (wildcards _ and % allowed): ")
    
    # Get Intersection_ID and Intersection from 'Intersections' table where the Intersection contains userInput, ordering by names from A - Z
    dbCursor = dbConn.cursor()
    intersectionQuery = """SELECT Intersection_ID, Intersection 
    FROM Intersections 
    WHERE Intersection like ? 
    ORDER BY Intersection"""

    # Execute function takes second paramater to replace ? in intersectionQuery
    dbCursor.execute(intersectionQuery, [userInput]) 
    cmndOne = dbCursor.fetchall()

    # Output - Intersection_ID : Intersection (Will repeatedly print rows until condition fulfilled)
    for row in cmndOne:
        print(row[0], ":", row[1])

    # If cmndOne is empty, output exception statement
    if len(cmndOne) == 0:
        print("No intersections matching that name were found.")
    
    print()

##################################################################  
#
# command_two: Find all cameras at an intersection
# PASSED
#
def command_two(dbConn):
    print()
    userInput = input("Enter the name of the intersection (no wildcards allowed): ")

    # RED LIGHT CAMS ONLY -> Get Camera_ID & Address from 'RedCameras' table joining 'Intersection' when Intersection_ID's are the same where Intersection contains userInput, order by ID
    dbCursor = dbConn.cursor()
    redCamsQuery = """SELECT RedCameras.Camera_ID as redID, RedCameras.Address 
    FROM RedCameras 
    JOIN Intersections on RedCameras.Intersection_ID = Intersections.Intersection_ID 
    WHERE Intersections.Intersection like ? 
    GROUP BY redID 
    ORDER BY redID"""

    # Execute function takes second paramater to replace ? in redCamsQuery
    dbCursor.execute(redCamsQuery, [userInput])
    redCamsQuery = dbCursor.fetchall()

    # Only print Camera_ID : Intersection if redCamsQuery doesn't return anything, otherwise throw exception statement
    print()
    if len(redCamsQuery) != 0:
        print("Red Light Cameras:")
        for row in redCamsQuery:
            print("  ", row[0], ":", row[1])
    else:
        print("No red light cameras found at that intersection.")

    # ----------------------------------------------
    # SPEED CAMS ONLY -> Same format as above but replacing instances of 'RedCameras' table with 'SpeedCameras'
    speedCamsQuery = """SELECT SpeedCameras.Camera_ID as camID, SpeedCameras.Address 
    FROM SpeedCameras 
    JOIN Intersections on SpeedCameras.Intersection_ID = Intersections.Intersection_ID 
    WHERE Intersections.Intersection like ? 
    GROUP by camID 
    ORDER by camID"""

    dbCursor.execute(speedCamsQuery, [userInput])
    speedCamsQuery = dbCursor.fetchall()

    # Only print Camera_ID : Intersection if speedCamsQuery doesn't return anything, otherwise throw exception statement
    print()
    if len(speedCamsQuery) != 0:
        print("Speed Cameras:")
        for row in speedCamsQuery:
            print("  ", row[0], ":", row[1])
    else:
        print("No speed cameras found at that intersection.")

    print()

##################################################################  
#
# command_three: Percentage of violations for a specific date
# PASSED
#
def command_three(dbConn):
    print()
    userInput = input("Enter the date that you would like to look at (format should be YYYY-MM-DD): ")

    # RED CAMERA VIOLATIONS ONLY -> Get Sum of all Num_Violations from 'RedViolations' table where violation_date is useInput
    dbCursor = dbConn.cursor()
    redViolationsQuery = """SELECT SUM(Num_Violations)
    FROM RedViolations
    WHERE RedViolations.Violation_Date = ?"""

    dbCursor.execute(redViolationsQuery, [userInput])
    redViolationsQuery = dbCursor.fetchone()

    # ----------------------------------------------
    # SPEED CAMERA VIOLATIONS ONLY -> Same format as RedCameras but changed for Speed Camera information
    speedViolationsQuery = """SELECT SUM(Num_Violations)
    FROM SpeedViolations
    WHERE SpeedViolations.Violation_Date = ?"""

    dbCursor.execute(speedViolationsQuery, [userInput])
    speedViolationsQuery = dbCursor.fetchone()

    # Only need to check if redViolations[0] != None because there will always be a violation on a given date within the data's date range. Otherwise, throw exception statement
    if redViolationsQuery[0] != None:
        # Calculate total by getting sum of red camera violations along with sum of speed camera violations.
        # Then get percentage by dividing respective camera by total and then multiplying by 100
        tot = redViolationsQuery[0] + speedViolationsQuery[0]
        redPercent = (redViolationsQuery[0] / tot) * 100
        speedPercent = (speedViolationsQuery[0] / tot) * 100

        # Output respective data along with calculated percentage from above formatted to 3 digits after the decimal. 
        print("Number of Red Light Violations:", f"{redViolationsQuery[0]:,}", f"({redPercent:.3f}%)")
        print("Number of Speed Violations:", f"{speedViolationsQuery[0]:,}", f"({speedPercent:.3f}%)")
        print("Total Number of Violations:", f"{tot:,}")
    else:
        print("No violations on record for that date.")

    print()


##################################################################  
#
# command_four: Number of cameras at each intersection
# PASSED
#
def command_four(dbConn):
    print()
    dbCursor = dbConn.cursor()

    # RED CAMS ONLY -> Selection Intersection, Intersection_ID, and COUNT(Camera_ID) from 'RedCameras' joining 'Intersections' 
    # on same Intersection_ID's and then grouping by intersection along with ordering by proper formatting
    redCamsQuery = """SELECT Intersections.Intersection as name, Intersections.Intersection_ID as ID, COUNT(Camera_ID) as count
    FROM RedCameras
    JOIN Intersections on RedCameras.Intersection_ID = Intersections.Intersection_ID
    GROUP BY Intersection
    ORDER BY count desc, ID desc, name asc"""

    dbCursor.execute(redCamsQuery)
    redCamsQuery = dbCursor.fetchall()
    
    # RED CAMS ONLY -> Getting total count of Camera_ID's from 'RedCameras' table without any restrictions
    # Necessary for calculating red camera percentage for output
    redTotQuery = """SELECT COUNT(Camera_ID) from RedCameras"""
    dbCursor.execute(redTotQuery)
    redTotQuery = dbCursor.fetchone()

    i = 0
    print("Number of Red Light Cameras at Each Intersection")

    # Whenever data found, calculate percentage an then output -> Intersection (Intersection_ID) : Count (Percentage)
    for rows in redCamsQuery:
        redCamsPercent = (redCamsQuery[i][2] / redTotQuery[0]) * 100
        print("  ", f"{redCamsQuery[i][0]}", f"({redCamsQuery[i][1]})", ":", f"{redCamsQuery[i][2]}", f"({redCamsPercent:.3f}%)")
        i += 1

    # ----------------------------------------------
    # SPEED CAMS ONLY -> Same format as redCamsQuery but replacing 'RedCameras' table with 'SpeedCameras'
    speedCamsQuery = """SELECT Intersections.Intersection as name, Intersections.Intersection_ID as ID, COUNT(Camera_ID) as count
    FROM SpeedCameras
    JOIN Intersections on SpeedCameras.Intersection_ID = Intersections.Intersection_ID
    GROUP BY Intersection
    ORDER BY count desc, ID desc, name asc"""
    dbCursor.execute(speedCamsQuery)
    speedCamsQuery = dbCursor.fetchall()

    # SPEED CAMS ONLY -> Getting total count of Camera_ID's from 'SpeedCameras' table without any restrictions
    speedTotQuery = """SELECT COUNT(Camera_ID) from SpeedCameras"""
    dbCursor.execute(speedTotQuery)
    speedTotQuery = dbCursor.fetchone()

    print()
    print("Number of Speed Cameras at Each Intersection")
    
    j = 0

    # Whenever data found, calculate percentage an then output -> Intersection (Intersection_ID) : Count (Percentage)
    # Same format as above print but with 'j' instead
    for rows in speedCamsQuery:
        speedCamsPercent = (speedCamsQuery[j][2] / speedTotQuery[0]) * 100
        print("  ", f"{speedCamsQuery[j][0]}", f"({speedCamsQuery[j][1]})", ":", f"{speedCamsQuery[j][2]}", f"({speedCamsPercent:.3f}%)")
        j += 1

    print()

##################################################################  
#
# command_five: Number of violations at each intersection, given a year
#
def command_five(dbConn):
    print()
    dbCursor = dbConn.cursor()

    userInput = input("Enter the year that you would like to analyze: ")

    # Chagne userInput to wildcardUserInput due to use of 'like' in below query
    wildcardUserInput = "%" + userInput + "%"

    # RED VIOLATIONS ONLY -> Get Intersection, Intersection_ID, Sum(Num_Violations) From RedViolations joining Intersections when Intersection_ID's are the same
    redViolationsQuery = """SELECT Intersections.Intersection as name, Intersections.Intersection_ID as id, SUM(RedViolations.Num_Violations) as count
    FROM RedViolations
    JOIN RedCameras on RedViolations.Camera_ID = RedCameras.Camera_ID
    JOIN Intersections on Intersections.Intersection_ID = RedCameras.Intersection_ID
    WHERE RedViolations.Violation_Date like ?
    GROUP BY name, id
    ORDER BY count desc, id desc"""

    dbCursor.execute(redViolationsQuery, [wildcardUserInput])
    redViolationsQuery = dbCursor.fetchall()

    # RED VIOLATIONS ONLY -> Get total number of red violations for percentage calculations
    redTotQuery = """SELECT SUM(Num_Violations)
    FROM RedViolations
    WHERE Violation_Date like ?"""

    dbCursor.execute(redTotQuery, [wildcardUserInput])
    redTotQuery = dbCursor.fetchone()

    print()
    print("Number of Red Light Violations at Each Intersection for " + userInput)

    i = 0
    
    # RED VIOLATIONS ONLY -> Print Intersection (Intersection_ID) : Sum(Num_Violations) (Percentage) if length of query not 0. Otherwise throw excpetion.
    if len(redViolationsQuery) != 0:
        for rows in redViolationsQuery:
            redPercent = (redViolationsQuery[i][2] / redTotQuery[0]) * 100
            print(" ", f"{redViolationsQuery[i][0]}", f"({redViolationsQuery[i][1]})", ":", f"{redViolationsQuery[i][2]:,}", f"({redPercent:.3f}%)")
            i += 1
        print("Total Red Light Violations in " + userInput, ":", f"{redTotQuery[0]:,}")
    else:
        print("No red light violations on record for that year.")

    # ----------------------------------------------
    # SPEED VIOLATIONS ONLY -> Exact same formatting as portion for red violations except replacing RedViolations table with SpeedViolations when applicable
    speedViolationsQuery = """SELECT Intersections.Intersection as name, Intersections.Intersection_ID as id, SUM(SpeedViolations.Num_Violations) as count
    FROM SpeedViolations
    JOIN SpeedCameras on SpeedViolations.Camera_ID = SpeedCameras.Camera_ID
    JOIN Intersections on Intersections.Intersection_ID = SpeedCameras.Intersection_ID
    WHERE SpeedViolations.Violation_Date like ?
    GROUP BY name, id
    ORDER BY count desc, id desc"""
    
    dbCursor.execute(speedViolationsQuery, [wildcardUserInput])
    speedViolationsQuery = dbCursor.fetchall()

    # SPEED VIOLATIONS ONLY -> Get total number of violations for percentage calculation
    speedTotQuery = """SELECT SUM(Num_Violations) 
    FROM SpeedViolations 
    WHERE Violation_Date like ?"""

    dbCursor.execute(speedTotQuery, [wildcardUserInput])
    speedTotQuery = dbCursor.fetchone()

    print()
    print("Number of Speed Violations at Each Intersection for " + userInput)

    j = 0

    # SPEED VIOLATIONS ONLY -> Print Intersection (Intersection_ID) : Sum(Num_Violations) (Percentage) if length of query not 0. Otherwise throw excpetion.
    if len(speedViolationsQuery) != 0:
        for rows in speedViolationsQuery:
            speedPercent = (speedViolationsQuery[j][2] / speedTotQuery[0]) * 100
            print(" ", f"{speedViolationsQuery[j][0]}", f"({speedViolationsQuery[j][1]})", ":", f"{speedViolationsQuery[j][2]:,}", f"({speedPercent:.3f}%)")
            j += 1
        print("Total Speed Violations in " + userInput, ":", f"{speedTotQuery[0]:,}")
    else:
        print("No speed violations on record for that year.")

    print()

##################################################################  
#
# command_six(): Number of violations by year, given a camera ID
#
def command_six(dbConn):
    print()
    dbCursor = dbConn.cursor()

    userInput = input("Enter a camera ID: ")

    # Change to wildcard again for use of 'like' in query below
    wildcardUserInput = "%" + userInput + "%"

    # RED VIOLATIONS ONLY -> Separate data by year and the sum for that whole year by asking for Camera_ID first
    redsQuery = """SELECT strftime('%Y', Violation_Date) as date, SUM(Num_Violations)
    FROM RedViolations
    WHERE Camera_ID like ?
    GROUP BY date
    ORDER BY date asc"""

    dbCursor.execute(redsQuery, [wildcardUserInput])
    redsQuery = dbCursor.fetchall()

    # ----------------------------------------------
    # SPEED VIOLATIONS ONLY -> Same format as violationsQuery besides RedViolations becomming SpeedViolations
    speedsQuery = """SELECT strftime('%Y', Violation_Date) as date, SUM(Num_Violations)
    FROM SpeedViolations
    WHERE Camera_ID like ?
    GROUP BY date
    ORDER BY date asc"""

    dbCursor.execute(speedsQuery, [wildcardUserInput])
    speedsQuery = dbCursor.fetchall()

    i = 0
    j = 0

    # Combine both violationsQuery and speedsQuery to print Year : Sum of violations for that year respectively. Otherwise throw excpetion statement
    if redsQuery:    
        print("Yearly Violations for Camera " + userInput)
        for rows in redsQuery:
            print(f"{redsQuery[i][0]}", ":", f"{redsQuery[i][1]:,}")
            i += 1
    elif speedsQuery:
        print("Yearly Violations for Camera " + userInput)
        for rows in speedsQuery:
            print(f"{speedsQuery[j][0]}", ":", f"{speedsQuery[j][1]:,}")
            j += 1
    else:
        print("No cameras matching that ID were found in the database.")
        print()
        return

    # Plotting code by importing matplotlib.pyplot as plt
    print()
    userPlot = input("Plot? (y/n) ")
    if userPlot == 'y':
        # To plot we need X and Y vectors
        x = []
        y = []

        # RED PLOTTING ONLY -> When data found in redsQuery, plot the years in x axis and number of violations in y axis
        if redsQuery:
            redsYears = int(redsQuery[0][0])
            for row in redsQuery:
                x.append(redsYears)
                y.append(row[1])
                redsYears += 1

        # SPEED PLOTTING ONLY -> When data found in redsQuery, plot the years in x axis and number of violations in y axis
        if speedsQuery:
            speedsYears = int(speedsQuery[0][0])
            for row in speedsQuery:
                x.append(speedsYears)
                y.append(row[1])
                speedsYears += 1

        # Plotting labels (x axis, y axis, title)
        plt.xlabel("Year")
        plt.ylabel("Number of Violations")
        plt.title("Yearly Violations for Camera " + userInput)

        # Etc. plotting formatting
        plt.ioff()
        plt.plot(x, y)
        plt.show()

    # Alternate case where userPlot is anything but 'y'
    else:
        print()
        return
    
    print()

##################################################################  
#
# command_seven(): Number of violations by month, given a camera ID and year
#
def command_seven(dbConn):
    print()
    dbCursor = dbConn.cursor()

    userID = input("Enter a camera ID: ")

    # RED ID ONLY -> First only ask for camera ID only to properly handle exception where no ID's were found in database before asking for userYear.
    redIDQuery = """SELECT strftime('%m', Violation_Date) as month, strftime('%Y', Violation_Date) as year, SUM(Num_Violations)
    FROM RedViolations
    WHERE Camera_ID = ?
    GROUP BY month
    ORDER BY month asc"""

    dbCursor.execute(redIDQuery, [userID])
    redIDQuery = dbCursor.fetchall()

    # ----------------------------------------------
    # SPEED ID ONLY -> First only ask for camera ID only to properly handle exception where no ID's were found in database before asking for userYear.
    speedIDQuery = """SELECT strftime('%m', Violation_Date) as month, strftime('%Y', Violation_Date) as year, SUM(Num_Violations)
    FROM SpeedViolations
    WHERE Camera_ID = ?
    GROUP BY month
    ORDER BY month asc"""

    dbCursor.execute(speedIDQuery, [userID])
    speedIDQuery = dbCursor.fetchall()

    # Exception case handling where no ID's were found. If ID was found, then finally ask for year below. Otherwise, print exception and return.
    if len(redIDQuery) == 0 and len(speedIDQuery) == 0:
        print("No cameras matching that ID were found in the database.")
        print()
        return

    userYear = input("Enter a year: ")

    # Change to wildcard for use of 'like' in both redQuery and speedQuery
    wildcardYear = "%" + userYear + "%"

    # RED INFO ONLY -> Essentially same query as redIDQuery but including year because not fulfilling exception case
    redQuery = """SELECT strftime('%m', Violation_Date) as month, strftime('%Y', Violation_Date) as year, SUM(Num_Violations)
    FROM RedViolations
    WHERE Camera_ID = ? AND year like ? 
    GROUP BY month
    ORDER BY month asc"""

    dbCursor.execute(redQuery, [userID, wildcardYear])
    redQuery = dbCursor.fetchall()

    i = 0

    print("Monthly Violations for Camera " + userID, " in " + userYear)

    # RED INFO ONLY -> Print month/year : total number of violations for the specified camera ID in specified year
    for rows in redQuery:
        print(f"{redQuery[i][0]}/"f"{redQuery[i][1]}", ":", f"{redQuery[i][2]:,}")
        i += 1

    # ----------------------------------------------
    # SPEED INFO ONLY -> Same format as redQuery but replacing RedViolations with SpeedViolations
    speedQuery = """SELECT strftime('%m', Violation_Date) as month, strftime('%Y', Violation_Date) as year, SUM(Num_Violations)
    FROM SpeedViolations
    WHERE Camera_ID = ? AND year like ? 
    GROUP BY month
    ORDER BY month asc"""

    dbCursor.execute(speedQuery, [userID, wildcardYear])
    speedQuery = dbCursor.fetchall()

    j = 0

    # SPEED INFO ONLY -> Print month/year : total number of violations for the specified camera ID in specified year
    for rows in speedQuery:
        print(f"{speedQuery[j][0]}/"f"{speedQuery[j][1]}", ":", f"{speedQuery[j][2]:,}")
        j += 1

    # Plotting code by importing matplotlib.pyplot as plt
    print()
    userPlot = input("Plot? (y/n) ")
    # To plot we need X and Y vectors
    if userPlot == 'y':
        x = []
        y = []

        # RED PLOTTING ONLY -> When data found in redsQuery, plot months in x axis and number of violations in y axis
        if redQuery:
            violationMonths = int(redQuery[0][0])
            for row in redQuery:
                x.append(violationMonths)
                y.append(row[2])
                violationMonths += 1

        # SPEED PLOTTING ONLY -> When data found in redsQuery, plot months in x axis and number of violations in y axis
        if speedQuery:
            speedMonths = int(speedQuery[0][0])
            for row in speedQuery:
                x.append(speedMonths)
                y.append(row[2])
                speedMonths += 1

        # Plotting labels (x axis, y axis, title)
        plt.xlabel("Month")
        plt.ylabel("Number of Violations")
        plt.title("Monthly Violations for Camera " + userID + " (" + userYear + ")")

        # Etc. plotting formatting
        plt.ioff()
        plt.plot(x, y)
        plt.show()

    # Alternate case where userPlot is anything but 'y'
    else:
        print()
        return

    print()

##################################################################  
#
# command_eight(): Compare the number of red light and speed violations, given a year
#
def command_eight(dbConn):
    print()
    dbCursor = dbConn.cursor()

    userYear = input("Enter a year: ")

    # FIRST FIVE RED ONLY -> Get Violation_Date and total number of violations given a year. Print the first 5 elements starting from beginning of applicable data.
    firstFiveRed = """SELECT Violation_Date as date, SUM(Num_Violations)
    FROM RedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date
    LIMIT 5"""

    dbCursor.execute(firstFiveRed, [userYear])
    firstFiveRed = dbCursor.fetchall()

    i = 0

    print("Red Light Violations:")

    # FIRST FIVE RED ONLY -> Only print the FIRST five applicable dates along with their number of red light violations
    for rows in firstFiveRed:
        print(f"{firstFiveRed[i][0]}", f"{firstFiveRed[i][1]}")
        i += 1
    
    # LAST FIVE RED ONLY -> Same format as firstFiveRed but ordering by descending order. This gets the last 5 applicable dates
    lastFiveRed = """SELECT Violation_Date as date, SUM(Num_Violations)
    FROM RedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date desc
    LIMIT 5"""

    dbCursor.execute(lastFiveRed, [userYear])
    lastFiveRed = dbCursor.fetchall()

    j = 0

    # Use .reverse() here because lastFiveRed gets dates from very last (ex: 2014-12-31 then 2014-12-30 ...)
    # .reverse() Allows the last five to reverse such that 2014-12-31 would appear last rather than appearing first
    lastFiveRed.reverse()

    # LAST FIVE RED ONLY -> Only print the LAST five applicable dates along with their number of red light violations
    for rows in lastFiveRed:
        print(f"{lastFiveRed[j][0]}", f"{lastFiveRed[j][1]}")
        j += 1

    # ----------------------------------------------
    # FIRST FIVE SPEED ONLY -> Same format as firstFiveRed but replacing RedViolations with SpeedViolations
    firstFiveSpeed = """SELECT Violation_Date as date, SUM(Num_Violations)
    FROM SpeedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date
    LIMIT 5"""

    dbCursor.execute(firstFiveSpeed, [userYear])
    firstFiveSpeed = dbCursor.fetchall()

    a = 0
    
    print("Speed Violations:")

    # FIRST FIVE SPEED ONLY -> Only print the FIRST five applicable dates along with their number of speed violations
    for rows in firstFiveSpeed:
        print(f"{firstFiveSpeed[a][0]}", f"{firstFiveSpeed[a][1]}")
        a += 1

    # LAST FIVE SPEED ONLY -> Same format as lastFiveRed but replacing RedViolations with SpeedViolations
    lastFiveSpeed = """SELECT Violation_Date as date, SUM(Num_Violations)
    FROM SpeedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date desc
    LIMIT 5"""

    dbCursor.execute(lastFiveSpeed, [userYear])
    lastFiveSpeed = dbCursor.fetchall()

    b = 0

    # Another use of .reverse() for the same purpose as lastFiveRed.reverse()
    lastFiveSpeed.reverse()

    # LAST FIVE SPEED ONLY -> Only print the LAST five applicable dates along with their number of speed violations
    for rows in lastFiveSpeed:
        print(f"{lastFiveSpeed[b][0]}", f"{lastFiveSpeed[b][1]}")
        b += 1

    # RED DAYS ONLY -> Get all red days strictly for plotting purposes
    redDaysQuery = """SELECT strftime('%j', violation_date) as date, SUM(Num_Violations)
    FROM RedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date"""

    dbCursor.execute(redDaysQuery, [userYear])
    redDaysQuery = dbCursor.fetchall()

    # SPEED DAYS ONLY -> Same purpose as redDaysQuery but for speed days
    speedDaysQuery = """SELECT strftime('%j', violation_date) as date, SUM(Num_Violations)
    FROM SpeedViolations
    WHERE strftime('%Y', Violation_Date) = ?
    GROUP BY date
    ORDER BY date"""

    dbCursor.execute(speedDaysQuery, [userYear])
    speedDaysQuery = dbCursor.fetchall()

    # Plotting code by importing matplotlib.pyplot as plt
    print()
    userPlot = input("Plot? (y/n) ")
    # To plot we need X and Y vectors
    if userPlot == 'y':
        redX = []
        redY = []
        speedX = []
        speedY = []

        # RED PLOTTING ONLY -> When data found in redDaysQuery, plot days in x axis and number of violations in y axis
        redDays = int(redDaysQuery[0][0])
        if redDaysQuery:
            for row in redDaysQuery:
                redX.append(redDays)
                redY.append(row[1])
                redDays += 1

        # SPEED PLOTTING ONLY -> When data found in speedDaysQuery, plot days in x axis and number of violations in y axis
        speedDays = int(speedDaysQuery[0][0])
        if speedDaysQuery:
            for row in speedDaysQuery:
                speedX.append(speedDays)
                speedY.append(row[1])
                speedDays += 1   

        # Plotting labels (x axis, y axis, title)
        plt.xlabel("Day")
        plt.ylabel("Number of Violations")
        plt.title("Violations Each Day of " + userYear)

        # Etc. formatting
        plt.ioff()
        plt.plot(redX, redY, color = 'red', label = 'Red Light')
        plt.plot(speedX, speedY, color = 'orange', label = 'Speed')

        plt.legend()
        plt.show()

    # Exception case where userPlot is anything but 'y'
    else:
        print()
        return

##################################################################  
#
# command_nine(): Find cameras located on a street
#
def command_nine(dbConn):
    print()
    dbCursor = dbConn.cursor()

    userStreet = input("Enter a street name: ")

    # Change to wildcardUserStreet due to use of 'like' in redQuery and speedQuery
    wildcardUserStreet = "%" + userStreet + "%"

    # RED INFO ONLY -> Get camera_ID, address, latitude, longitude from RedCameras when given an address, being grouped by camera_ID
    redQuery = """SELECT Camera_ID as ID, Address, Latitude, Longitude
    FROM RedCameras
    WHERE Address like ?
    GROUP BY ID
    ORDER BY ID asc"""

    dbCursor.execute(redQuery, [wildcardUserStreet])
    redQuery = dbCursor.fetchall()

    # ----------------------------------------------
    # SPEED INFO ONLY -> Same format as redQuery but replacing 'RedCameras' with 'SpeedCameras'
    speedQuery = """SELECT Camera_ID as ID, Address, Latitude, Longitude
    FROM SpeedCameras
    WHERE Address like ?
    GROUP BY ID
    ORDER BY ID asc"""

    dbCursor.execute(speedQuery, [wildcardUserStreet])
    speedQuery = dbCursor.fetchall()

    # Exception case handling if no cameras are found in either RedCameras or SpeedCameras tables. If not, continue below to print information
    if len(redQuery) == 0 and len(speedQuery) == 0:
        print("There are no cameras located on that street.")
        print()
        return

    print()
    print("List of Cameras Located on Street: " + userStreet)
    print("  Red Light Cameras:")

    i = 0

    # RED INFO ONLY -> Print camera_id : full address (latitude, longitude)
    for rows in redQuery:
        print("     " f"{redQuery[i][0]} : " f"{redQuery[i][1]}", "(" f"{redQuery[i][2]}" ",", f"{redQuery[i][3]}" ")")
        i += 1

    j = 0
    
    # SPEED INFO ONLY -> Print camera_id : full address (latitude, longitude)
    print("  Speed Cameras:")
    for rows in speedQuery:
        print("     " f"{speedQuery[j][0]} : " f"{speedQuery[j][1]}", "(" f"{speedQuery[j][2]}" ",", f"{speedQuery[j][3]}" ")")
        j += 1 
    
    # Plotting code by importing matplotlib.pyplot as plt
    print()
    userPlot = input("Plot? (y/n) ")
    if userPlot == 'y':
        # RED ONLY -> Lists to store coordinates and camera IDs
        xRed = []
        yRed = []  
        idRed = []  

        # SPEED ONLY -> Lists to store coordinates and camera IDs
        xSpeed = [] 
        ySpeed = []  
        idSpeed = [] 

        # RED ONLY -> Longitude, latitude, camera_ID
        for row in redQuery:
            xRed.append(row[3])  
            yRed.append(row[2]) 
            idRed.append(str(row[0])) 

        # SPEED ONLY -> Longitude, latitude, camera_ID
        for row in speedQuery:
            xSpeed.append(row[3])  
            ySpeed.append(row[2])  
            idSpeed.append(str(row[0]))  

        # COPIED CODE FROM PDF
        image = plt.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]  # area covered by the map
        plt.imshow(image, extent=xydims)
        plt.title("Cameras on Street: " + userStreet)

        # Plot data points (Red data = red, Speed data = orange)
        plt.plot(xRed, yRed, color = 'red', marker = 'o')
        plt.plot(xSpeed, ySpeed, color = 'orange', marker = 'o')

        # Annotate each point with respective camera ID
        i = 0
        for camID in idRed:
            plt.annotate(camID, (xRed[i], yRed[i]))
            i += 1

        j = 0
        for camID in idSpeed:
            plt.annotate(camID, (xSpeed[j], ySpeed[j]))
            j += 1

        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.show()

    # Exception case where userPlot is anything but 'y'
    else:
        print()
        return
            
# Go to main()
if __name__ == "__main__":
    main()