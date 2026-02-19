# pls ignore how inefficient the code is :3

import pandas as pd
import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

def generate_emails():

    # RECIPIENTS

    listEmail = ["Eric Masters <esmaster@purdue.edu>", "Richard Moodie <rmoodie@purdue.edu>", "Rob Ward <robward@purdue.edu>", "Carson Hamner <chamner@purdue.edu>"]

    TO = "".join(random.sample(listEmail, 1))
    listEmail.remove(TO)

    ccMails = [0, 1, 2]
    numOfCC = random.choice(ccMails)

    CC = ""
    listCC = ()
    if numOfCC != 0:
        listCC = random.sample(listEmail, numOfCC)
        CC = ', '.join(listCC)

    # NAME

    name = pd.read_excel("names.xlsx")

    first = list(name["First"].sample(1))
    first = "".join(first).strip()
    last = list(name["Last"][0:1000].sample(1))
    last = "".join(last).title().strip()

    GPA = str(round(random.uniform(3, 4), 2))

    # VARIATION POOLS
    greetingsSingle = [
        "Hey Coach",
        "Hi Coach",
        "Dear Coach",
        "Good morning",
        "Good afternoon",
        "Good evening",
        "Good morning Coach",
        "Good afternoon Coach",
        "Good evening Coach",
        "Coach",
        "Hello",
        "Hello Purdue Coach",
        "Hello Coach",
        "Dear Purdue Coach",
    ]

    greetingsMulti = [
        "Dear Coaches",
        "Hi Coaches",
        "Greetings Coaches",
        "Hey Coaches",
        "Good morning",
        "Good afternoon",
        "Good evening",
        "Good morning Coaches",
        "Good afternoon Coaches",
        "Good evening Coaches",
        "Hello",
        "Hello Purdue Coaches",
        "Hello Coaches",
        "Dear Purdue Coaches",

    ]

    league = random.randint(0, 10)
    leagues = ""
    if league == 0:
        leagues = "GA"
    elif league >= 5:
        leagues = "ECNL-RL"
    else:
        leagues = "ECNL"

    leagues = "ECNL"

    # GA

    gaClubs = [
        "Florida United",
        "Indy Premier SC",
        "West Florida Flames",
        "St. Louis Development Academy",
        "Space Coast United",
        "SoCal Reds FC",
        "Pinecrest Premier Soccer",
        "Palm Beach Kicks",
        "New York SC",
        "Midwest United",
        "Las Vegas Sports Academy",
        "LA Surf Soccer Club",
        "Keystone FC",
        "HTX",
        "Colorado United",
        "Central Illinois United",
        "Bayside FC",
        "Baltimore Celtic Soccer Club",
        "ALBION SC Las Vegas",
        "ALBION SC San Diego",
        "TopHat",
        "Santa Clara Sporting",
        "Real Futbol Academy"
    ]

    # ECNL

    allConf = [
        "Mid-Atlantic All Conference",
        "Midwest All Conference",
        "Northern Cal All Conference",
        "North Atlantic All Conference",
        "New England All Conference",
        "Northwest All Conference",
        "Ohio Valley All Conference",
        "Southeast All Conference",
        "Southwest All Conference",
        "Texas All Conference",
    ]

    midAtlClubs = [
        "Richmond United",
        "Wilmington Hammerheads",
        "Beach FC",
        "NC Fusion",
        "VDA",
        "NC Courage",
        "NCFC Youth",
        "Charlotte SA",
        "Arlington Soccer",
        "Fairfax Virginia Union",
    ]

    midWestClubs = [
        "Eclipse Select SC",
        "Kansas City Athletics",
        "Sporting Iowa",
        "Michigan Hawks Magic",
        "Chicago Inter Soccer",
        "Sporting Blue Valley",
        "FC Wisconsin",
        "Missouri Rush",
        "Gretna Elite Academy",
        "Rockford Raptors",
        "SLSG Navy",
        "Nationals Soccer Club",
        "Liverpool FC IA Michigan",
        "Michigan Hawks",
        "SLSG Green",
        "Minnesota Thunder"
    ]

    newEngClubs = [
        "World Class FC",
        "Connecticut FC",
        "FC Stars Blue",
        "FSA FC",
        "SUSA FC",
        "East Meadow SC",
        "Scorpions SC",
        "FC Stars White",
        "Select",
    ]

    norAtlClubs = [
        "Bethesda SC",
        "FC DELCO",
        "HEX FC Bucks",
        "Maryland United FC",
        "Match Fit Surf",
        "PDA Blue",
        "PDA White",
        "Penn Fusion SA",
        "Philadelphia Ukrainian Nationals",
        "Pipeline SC"
    ]

    norCalClubs = [
        "Bay Area Surf",
        "COSC",
        "COSC (G11)",
        "Davis Legacy",
        "De Anza Force",
        "Marin FC",
        "Mustang SC",
        "MVLA",
        "Placer United",
        "Pleasanton RAGE",
        "San Juan SC",
        "Santa Rosa United"
    ]

    nwClubs = [
        "Boise Thorns FC",
        "Eastside FC",
        "La Roca FC",
        "Oregon Surf",
        "PacNW SC",
        "Portland Thorns",
        "Seattle United",
        "Utah Avalanche",
        "Washington Premier",
        "XF Academy"
    ]

    ohioClubs = [
        "Cleveland Force SC",
        "FC Alliance",
        "FC Pride Elite",
        "GTFC Impact",
        "Indy Eleven Pro Academy",
        "Internationals SC",
        "Ohio Elite SA",
        "Ohio Premier",
        "Pittsburgh Riverhounds",
        "Racing Louisville Academy",
        "Tennessee SC",
        "WNY Flash"
    ]

    seClubs = [
        "Alabama FC",
        "Atlanta Fire United",
        "CESA Liberty",
        "Concorde Fire Platinum",
        "Concorde Fire Premier",
        "FC Prime",
        "FL Premier FC",
        "Florida Krush",
        "Florida West",
        "GSA",
        "Jacksonville FC",
        "Orlando Pride",
        "South Carolina United",
        "Sporting Jax",
        "Tampa Bay United",
        "United Futbol Academy"
    ]

    swClubs = [
        "LV Heat Surf",
        "Arizona Arsenal",
        "Beach FC (CA)",
        "Eagles SC",
        "LA Breakers FC",
        "LAFC So Cal",
        "Legends FC",
        "Legends FC San Diego",
        "Pateadores",
        "Phoenix Rising",
        "Rebels SC",
        "San Diego Surf",
        "SLAMMERS FC",
        "Slammers FC HB Koge",
        "So Cal Blues",
        "Sporting CA USA",
        "Utah Royals FC-AZ",
    ]

    texasClubs = [
        "Albion Hurricanes FC",
        "Challenge SC",
        "Classics Elite",
        "Colorado Rapids",
        "Colorado Rush Academy Blue",
        "Dallas Texans",
        "DKSC",
        "FC Dallas",
        "OK Energy FC",
        "Real Colorado Athletico",
        "Real Colorado National",
    ]

    midAtlSched = [
        "- Sep 06, 2025: Richmond United v Wilmington Hammerheads (West Creek)",
        "- Sep 05, 2025: Beach FC v NC Fusion (Hampton Roads Soccer Complex)",
        "- Sep 06, 2025: VDA v NC Courage (Long Park)",
        "- Sep 06, 2025: NCFC Youth v Charlotte SA (WRAL)",
        "- Sep 07, 2025: VDA v Wilmington Hammerheads (Howison Park)",
        "- Sep 07, 2025: Richmond United v NC Courage (West Creek)",
        "- Sep 07, 2025: Beach FC v Charlotte SA (Hampton Roads Soccer Complex)",
        "- Sep 13, 2025: NCFC Youth v Beach FC (WRAL)",
        "- Sep 20, 2025: NC Fusion v Richmond United (Truist Soccer Complex)",
        "- Sep 20, 2025: NC Courage v Arlington Soccer (WRAL Soccer Complex)",
        "- Sep 20, 2025: Charlotte SA v VDA (OrthoCarolina Sportsplex)",
        "- Sep 20, 2025: Wilmington Hammerheads v Fairfax Virginia (NCINO Sports Park)",
        "- Sep 21, 2025: Charlotte SA v Richmond United (OrthoCarolina Sportsplex)",
        "- Sep 21, 2025: NC Courage v Fairfax Virginia Union (WRAL Soccer Complex)",
        "- Sep 21, 2025: Wilmington Hammerheads v Arlington Soccer (NCINO Sports Park)",
        "- Sep 21, 2025: NC Fusion v VDA (Truist Soccer Complex)",
        "- Sep 27, 2025: Arlington Soccer v VDA (Long Bridge Park)",
        "- Oct 04, 2025: Arlington Soccer v NCFC Youth (Long Bridge Park)",
        "- Oct 04, 2025: VDA v Beach FC (Long Park)",
        "- Oct 04, 2025: NC Fusion v Wilmington Hammerheads (Truist Soccer Complex at Bryan Park)",
        "- Oct 04, 2025: Fairfax Virginia Union v Richmond United (James W Robinson HS)",
        "- Oct 05, 2025: VDA v NCFC Youth (Howison Park)",
        "- Oct 05, 2025: Richmond United v Beach FC",
        "- Oct 14, 2025: NCFC Youth v NC Courage (WRAL)",
        "- Oct 18, 2025: NCFC Youth v Fairvax Virginia Union (WRAL)",
        "- Oct 19, 2025: Charlotte SA v NC Courage (OrthoCarolina Sportsplex)",
        "- Oct 25, 2025: Wilmington Hammerheads v NCFC Youth (NCINO Sports Park)",
        "- Oct 25, 2025: NC Courage v Beach FC (WRAL Soccer Complex)",
        "- Oct 25, 2025: Charlotte SA v NC Fusion (OrthoCarolina Sportsplex)",
        "- Oct 26, 2025: Wilmington Hammerheads v Beach FC (NCINO Sports Park)",
        "- Nov 01, 2025: NCFC Youth v Richmond United (WRAL)",
        "- Nov 01, 2025: Fairfax Virginia Union v NC Fusion (James W Robinson HS)",
        "- Nov 01, 2025: Arlington Soccer Charlotte SA (Long Bridge Park)",
        "- Nov 01, 2025: NC Courage v Wilmington Hammerheads (WRAL Soccer Complex)",
        "- Nov 02, 2025: Fairfax Virginia Union v Charloote SA (WT Woodson High School)",
        "- Nov 02, 2025: Arlington Soccer v NC Fusion (Long Bridge Park)",
        "- Nov 09, 2025: Fairfax Virginia v VDA (James W Robinson HS)",
        "- Nov 15, 2025: Arlington Soccer v Fairfax Virginia Union (Long Bridge Park)",
        "- Nov 22, 2025: NC Courage v NC Fusion (WRAL Soccer Complex)",
        "- Nov 22, 2025: Beach FC v Fairfax Virginia Union (Hampton Roads Soccer Complex)",
        "- Nov 23, 2025: Richmond United v Arlington Soccer (Ukrop Park)",
        "- Dec 14, 2025: Wilmington Hammerheads v Charlotte SA (NCINO Sports Park)",
        "- Dec 14, 2025: NC Fusion v NCFC Youth (Truist Soccer Complex at Bryan Park)",
        "- Jan 18, 2026: Beach FC v Arlington Soccer (Hampton Roads Soccer Complex)",
        "- Jan 18, 2026: VDA v Richmond United (Howison Park)",

    ]

    midWestSched = [
        "- Aug 30, 2025: Eclipse Select SC v Kansas City Athletics (Deerpath Community Park Lake Forest)",
        "- Aug 30, 2025: Sporting Iowa v Michigan Hawks Magic (Hy-Vee Multiplex)",
        "- Aug 30, 2025: Chicago Inter Soccer v Sporting Blue Valley (Chicago Inter Complex)",
        "- Aug 30, 2025: FC Wisconsin v Missouri Rush (FC Wisconsin Soccer Park)",
        "- Aug 30, 2025: Michigan Hawks v Gretna Elite Academy (Hy-Vee Multiplex)",
        "- Aug 31, 2025: Sporting Iowa v Michigan Hawks (Hy-Vee Multiplex)",
        "- Aug 31, 2025: Eclipse Select SC v Sporting Blue Valley (Nike Park)",
        "- Aug 31, 2025: Michigan Hawks Magic v Gretna Elite Academy (Hy-Vee Multiplex)",
        "- Aug 31, 2025: Chicago Inter Soccer v Kansas City Athletics (Chicago Inter Complex)",
        "- Sep 06, 2025: Kansas City Athletics v Rockford Raptors (Paragon Star Soccer Complex)",
        "- Sep 06, 2025: SLSG Navy v Nationals Soccer Club (WWT Soccer Park)",
        "- Sep 06, 2025: SLSG Green v Liverpool FC IA Michigan (WWT Soccer Park)",
        "- Sep 06, 2025: Gretna Elite Academy v Eclipse Select SC (CHI Nebraska MultiSport Complex",
        "- Sep 06, 2025: Sporting Blue Valley v FC Wisconsin (Scheels Overland Park Soccer Complex)",
        "- Sep 06, 2025: Sporting Iowa v Chicago Inter Soccer (Nebraska Multisport Complex)",
        "- Sep 07, 2025: Eclipse Select SC v Sporting Iowa (CHI Health Multisport Complex)",
        "- Sep 07, 2025: SLGS Navy v Liverpool FC IA Michigan (WWT Soccer Park)",
        "- Sep 07, 2025: Kansas City Athletics v FC Wisconsin (Paragon Star Soccer Complex)",
        "- Sep 07, 2025: Gretna Elite Academy v Chicago Inter Soccer (CHI Nebraska Multisport Complex)",
        "- Sep 07, 2025: Sporting Blue Valley v Rockford Raptors (Scheels Overland Park Soccer Complex)",
        "- Sep 07, 2025: SLSG Green v Nationals Soccer Club (WWT Soccer Park)",
        "- Sep 13, 2025: Gretna Elite Academy v Kansas City Athletics (Gretna Sports Complex)",
        "- Sep 13, 2025: Sporting Iowa v Missouri Rush (Gretna Sports Complex)",
        "- Sep 14, 2025: Gretna Elite Academy v Missouri Rush (Gretna Sports Complex)",
        "- Sep 14, 2025: Michigan Hawks Magic v Michigan Hawks (Schoolcraft Turf)",
        "- Sep 14, 2025: Liverpool FC IA Michigan v Nationals Soccer Club (UWM Sports Complex)",
        "- Sep 14, 2025: SLGS Navy v SLSG Green (WWT Soccer Park)",
        "- Sep 20, 2025: Kansas City Athletics v Michigan Hawks (Paragon Star Soccer Complex)",
        "- Sep 20, 2025: Gretna Elite Academy v Sporting Iowa (Gretna Sports Complex)",
        "- Sep 20, 2025: Chicago Inter Soccer v Nationals Soccer Club (Chicago Inter Complex)",
        "- Sep 20, 2025: Eclipse Select SC v SLGS Navy (Redmond Recreational Complex)",
        "- Sep 20, 2025: Liverpool FC IA Michigan v Missouri Rush (Chicago Inter Complex)",
        "- Sep 20, 2025: Sporting Blue Valley v Michigan Hawks Magic (Olathe District Activity Center)",
        "- Sep 20, 2025: Rockford Raptors v FC Wisconsin (Mercyhealth Sportscore Two)",
        "- Sep 21, 2025: FC Wisconsin v Chicago Inter Soccer (FC Wisconsin Soccer Park)",
        "- Sep 21, 2025: Eclipse Select SC v Nationals Soccer Club (Deerpath Community Park Lake Forst)",
        "- Sep 21, 2025: Sporting Blue Valley v Michigan Hawks (Scheels Overland Park Soccer Complex)",
        "- Sep 21, 2025: Kansas City Athletics v Michigan Hawks Magic (Paragon Star Soccer Complex)",
        "- Sep 21, 2025: Rockford Raptors v SLGS Navy (Mercyhealth Sportscore Two)",
        "- Sep 27, 2025: Kansas City Athletics v SLSG Green (Paragon Star Soccer Complex)",
        "- Sep 27, 2025: Sporting Blue Valley v Missouri Rush (Scheels Overload Park Soccer Complex)",
        "- Oct 04, 2025: Gretna Elite Academy v Sporting Blue Valley (Gretna Sports Complex)",
        "- Oct 04, 2025: Liverpool FC IA Michigan v FC Wisconsin (UWM Sports Complex)",
        "- Oct 04, 2025: Michigan Hawks v SLGS Navy (Schoolcraft Turf)",
        "- Oct 04, 2025: Eclipse Select SC v Chicago Inter Soccer (Lewis University)",
        "- Oct 04, 2025: Nationals Soccer Club v Rockford Raptors (Oakland University Upper Fields)",
        "- Oct 04, 2025: Michigan Hawks Magic v SLSG Green (Jaycee Park)",
        "- Oct 04, 2025: Sporting Iowa v Kansas City Athletics (Hy-Vee Multiplex)",
        "- Oct 05, 2025: Liverpool FC IA Michigan v Rockford Raptors (UWM Sports Complex)",
        "- Oct 05, 2025: Michigan Hawks Magic v SLGS Navy (St. Joe's Sports Dome)",
        "- Oct 05, 2025: Nationals Soccer Club v FC Wisconsin (Evolution Sportsplex)",
        "- Oct 05, 2025:  Michigan Hawks v SLSG Green (Jaycee Park)",
        "- Oct 05, 2025: Sporting Iowa v Sporting Blue Valley (Hy-Vee Multiplex)",
        "- Oct 11, 2025: FC Wisconsin v Michigan Hawks (FC Wisconsin Soccer Park)",
        "- Oct 11, 2025: Rockford Raptors v Michigan Hawks Magic (Mercyhealth Sportscore Two)",
        "- Oct 11, 2025: Sporting Iowa v SLSG Green (Hy-Vee Multiplex)",
        "- Oct 11, 2025: Gretna Elite Academy v SLGS Navy (Grimseplex)",
        "- Oct 12, 2025: FC Wisconsin v Michigan Hawks Magic (FC Wisconsin Soccer Park)",
        "- Oct 12, 2025: Gretna Elite Academy v SLSG Green (Grimesplex)",
        "- Oct 12, 2025: Sporting Iowa v SLGS Navy (Hy-Vee Multiplex)",
        "- Oct 12, 2025: Rockford Raptors v Michigan Hawks (Mercyhealth Sportscore Two)",
        "- Oct 18, 2025: Eclipse Select SC v Liverpool FC IA Michigan (Redmond Recreational Complex)",
        "- Oct 18, 2025: Chicago Inter Soccer v SLSG Green (Chicago Inter Complex)",
        "- Oct 18, 2025: Nationals Soccer Club v Missouri Rush (Chicago Inter Complex)",
        "- Oct 19, 2025: Chicago Inter Soccer v Liverpool FC IA Michigan (Chicago Inter Complex)",
        "- Oct 19, 2025: Eclipse Select SC v SLSG Green (Deerpath Community Park Lake Forest)",
        "- Oct 25, 2025: Rockford Raptors v Sporting Iowa (Mercyhealth Sportscore Two)",
        "- Oct 25, 2025: Nationals Soccer Club v Kansas City Athletics (Oakland University Grizz Dome)",
        "- Oct 25, 2025: FC Wisconsin v Gretna Elite Academy (FC Wisconsin Soccer Park)",
        "- Oct 25, 2025: Missouri Rush v Eclipse Select SC ( Missouri Rush Sports Park)",
        "- Oct 25, 2025: Liverpool FC IA Michigan v Sporting Blue Valley (UWM Sports Complex)",
        "- Oct 26, 2025: Rockford Raptors v Gretna Elite Academy (Mercyhealth Sportscore Two)",
        "- Oct 26, 2025: FC Wisconsin v Sporting Iowa (FC Wisconsin Soccer Park)",
        "- Oct 26, 2025: Nationals Soccer Club v Sporting Blue Valley (Oakland University Grizz Dome)",
        "- Oct 26, 2025: Liverpool FC IA Michigan v Kansas City Athletics (UWM Sports Complex)",
        "- Nov 01, 2025: Missouri Rush v Rockford Raptors (Missouri Rush Sports Park)",
        "- Nov 01, 2025: Michigan Hawks v Eclipse Select SC (Schoolcraft Turf)",
        "- Nov 01, 2025: SLSG Green v FC Wisconsin (WWT Soccer Park)",
        "- Nov 01, 2025: Gretna Elite Academy v Liverpool FC IA Michigan (Gretna Sports Complex)",
        "- Nov 01, 2025: SLGS Navy v Kansas City Athletics (WWT Soccer Park)",
        "- Nov 01, 2025: Michigan Hawks Magic v Chicago Inter Soccer (Jaycee Park)",
        "- Nov 01, 2025: Nationals Soccer Club v Sporting Iowa (Gretna East High School)",
        "- Nov 02, 2025: Liverpool FC IA Michigan v Sporting Iowa (Gretna East High School)",
        "- Nov 02, 2025: Missouri Rush v Kansas City Athletics (Missouri Rush Sports Park)",
        "- Nov 02, 2025: SLGS Navy v FC Wisconsin (WWT Soccer Park)",
        "- Nov 02, 2025: SLSG Green v Rockford Raptors (WWT Soccer Park)",
        "- Nov 02, 2025: Gretna Elite Academy v Nationals Soccer Club (Gretna Sports Complex)",
        "- Nov 02, 2025: Michigan Hawks v Chicago Inter Soccer (St. Joe's Sports Dome)",
        "- Nov 02, 2025: Michigan Hawks Magic v Eclipse Select SC (Northville High School)",
        "- Nov 08, 2025: Minnesota Thunder v FC Wisconsin (Academy of Holy Angels)",
        "- Nov 08, 2025: Michigan Hawks v Liverpool FC IA Michigan (St. Joe's Sports Dome)",
        "- Nov 08, 2025: Rockford Raptors v Eclipse Select SC (Mercyhealth Sportscore Two)",
        "- Nov 08, 2025: Michigan Hawks Magic v Missouri Rush (Jaycee Park)",
        "- Nov 09, 2025: Kansas City Athletics v Sporting Blue Valley (Paragon Star Soccer Complex)",
        "- Nov 09, 2025: Michigan Hawks v Missouri Rush (Schoolcraft Turf)",
        "- Nov 22, 2025: SLSG Green v Missouri Rush (Missouri Rush Sports Park)",
        "- Nov 22, 2025: FC Wisconsin v Eclipse Select SC (FC Wisconsin Soccer Park)",
        "- Nov 22, 2025: Sporting Blue Valley v SLGS Navy (Pinnacle National Development Center)",
        "- Nov 22, 2025: Kansas City Athletics v Minnesota Thunder (KC Current Training Facility)",
        "- Nov 23, 2025: SLGS Navy v Missouri Rush (WWT Soccer Park)",
        "- Nov 23, 2025: Sporting Blue Valley v Minnesota Thunder (Pinnacle National Development Center)",
        "- Dec 05, 2025: Minnesota Thunder v SLGS Navy (KC Current Training Facility)",
        "- Dec 13, 2025: Missouri Rush v Minnesota Thunder (Missouri Rush Sports Park)",
        "- Dec 13, 2025: Nationals Soccer Club v Michigan Hawks (Evolution Sportsplex)",
        "- Dec 14, 2025: Missouri Rush v Chicago Inter Soccer (Missouri Rush Sports Park)",
        "- Dec 20, 2025: Michigan Hawks v Minnesota Thunder (St. Joe's Sports Dome)",
        "- Dec 20, 2025: Nationals Soccer Club v Michigan Hawks Magic (Evolution Sportsplex)",
        "- Dec 21, 2025: Michigan Hawks Magic v Minnesota Thunder (Legacy Center Sports Complex)",
        "- Jan 04, 2026: Rockford Raptors v Chicago Inter Soccer (Mercyhealth Sportscore Two)",
        "- Jan 17, 2026: Minnesota Thunder v Sporting Iowa (Academy of Holy Angels)",
        "- Jan 24, 2026: Minnesota Thunder v Gretna Elite Academy (Academy of Holy Angels)",
        "- Jan 31, 2026: Michigan Hawks Magic v Liverpool FC IA Michigan (St. Joe's Sports Dome)",
        "- Jan 31, 2026: Nationals Soccer Club v Minnesota Thunder (Michigan Stars Sports Complex)",
        "- Feb 01, 2026: SLGS Navy v Chicago Inter Soccer (WWT Soccer Park)",
        "- Feb 01, 2026: Minnesota Thunder v Liverpool FC IA Michigan (UVM Sports Complex)",
        "- Feb 01, 2026: SLSG Green v Sporting Blue Valley (WWT Soccer Park)",
        "- Feb 07, 2026: Minnesota Thunder v Chicago Inter Soccer (Academy of Holy Angels)",
        "- Feb 21, 2026: Minnesota Thunder v Eclipse Select SC (Academy of Holy Angels)",
        "- Feb 28, 2026: Minnesota Thunder v Rockford Raptors (Academy of Holy Angels)",
        "- Mar 15, 2026: SLSG Green v Minnesota Thunder (WWT Soccer Park)"
    ]

    newEngSched = [
        "- Dec 13, 2025: World Class FC v Connecticut FC United",
        "- Dec 13, 2025: FC Stars Blue v FSA FC (FC Stars Soccer Complex)",
        "- Dec 13, 2025: SUSA FC v East Meadow SC (The SUSA Orlin & Cohen Sports Complex)",
        "- Dec 13, 2025: Scorpions SC v FC Stars White (Forekicks III)",
        "- Dec 14, 2025: World Class FC v SUSA FC (Orangetown Soccer Complex)",
        "- Dec 20, 2025: East Meadow SC v World Class FC (East Meadow Field of Dreams)",
        "- Feb 07, 2026: Select v FSA FC (Union Point Sports Complex)",
        "- Feb 28, 2026: Connecticut FC United v World Class FC",
        "- Mar 01, 2026: Connecticut FC United v FSA FC",
        "- Mar 01, 2026: FC Stars Blue v FC Stars White (FC Stars Soccer Complex)",
        "- Mar 07, 2026: FC Stars White v Connecticut FC United",
        "- Mar 07, 2026: East Meadow SC v Scorpions SC",
        "- Mar 07, 2026: SUSA FC v Select",
        "- Mar 07, 2026: FC Stars Blue v World Class FC",
        "- Mar 08, 2026: FC Stars Blue v Connecticut FC United",
        "- Mar 08, 2026: SUSA FC v Scorpions SC",
        "- Mar 08, 2026: East Meadow SC v Select",
        "- Mar 08, 2026: FC Stars White v World Class FC",
        "- Mar 14, 2026: East Meadow SC v Connecticut FC United",
        "- Mar 14, 2026: SUSA FC v FSA FC",
        "- Mar 14, 2026: FC Stars White v Select (FC Stars Soccer Complex)",
        "- Mar 14, 2026: FC Stars Blue v Scorpions SC (FC Stars Soccer Complex)",
        "- Mar 15, 2026: SUSA FC v Connecticut FC United",
        "- Mar 15, 2026: East Meadow SC v FSA FC (East Meadow Field of Dreams)",
        "- Mar 15, 2026: FC Stars White v Scorpions SC (FC Stars Soccer Complex)",
        "- Mar 21, 2026: Select v FC Stars Blue",
        "- Mar 21, 2026: FSA FC v FC Stars White (FSA-Farmington Sports Arena)",
        "- Mar 22, 2026: Select v FC Stars White",
        "- Mar 22, 2026: FSA FC v FC Stars Blue (FSA-Farmington Sports Arena)",
        "- Mar 28, 2026: FC Stars White v FC Stars Blue (FC Stars Soccer Complex)",
        "- Apr 11, 2026: World Class FC v FSA FC",
        "- Apr 11, 2026: Select v Scorpions SC",
        "- Apr 11, 2026: FC Stars White v East Meadow SC (FC Stars Soccer Complex)",
        "- Apr 11, 2026: FC Stars Blue v SUSA FC (FC Stars Soccer Complex)",
        "- Apr 12, 2026: FSA FC v Scorpions SC (FSA-Farmington Sports Arena)",
        "- Apr 12, 2026: FC Stars Blue v East Meadow SC (FC Stars Soccer Complex)",
        "- Apr 12, 2026: FC Stars White v SUSA FC (FC Stars Soccer Complex)",
        "- Apr 18, 2026: Scorpions SC v Connecticut FC United",
        "- Apr 18, 2026: FC Stars White v FSA FC",
        "- Apr 18, 2026: Select v World Class FC",
        "- Apr 19, 2026: Select v Connecticut FC United",
        "- Apr 19, 2026: Scorpions SC v World Class FC",
        "- Apr 25, 2026: SUSA FC v FC Stars Blue",
        "- Apr 25, 2026: World Class FC v Scorpions SC",
        "- Apr 25, 2026: Connecticut FC United v Select",
        "- Apr 25, 2026: East Meadow SC v FC Stars White",
        "- Apr 26, 2026: East Meadow SC v FC Stars Blue",
        "- Apr 26, 2026: Connecticut FC United v Scorpions SC",
        "- Apr 26, 2026: World Class FC v Select",
        "- Apr 26, 2026: SUSA FC v FC Stars White",
        "- May 02, 2026: Scorpions SC v Select",
        "- May 02, 2026: SUSA FC v World Class FC",
        "- May 02, 2026: FSA FC v Connecticut FC United (FSA-Farmington Sports Arena)",
        "- May 03, 2026: Scorpions SC v FSA FC",
        "- May 03, 2026: FC Stars Blue v Select (FC Stars Soccer Complex)",
        "- May 05, 2026: East Meadow SC v SUSA FC",
        "- May 09, 2026: Scorpions SC v FC Stars Blue",
        "- May 09, 2026: World Class FC v East Meadow SC",
        "- May 09, 2026: FSA FC v Select (FSA-Farmington Sports Arena)",
        "- May 10, 2026: FSA FC v World Class FC (FSA-Farmington Sports Arena)",
        "- May 16, 2026: World Class FC v FC Stars Blue",
        "- May 16, 2026: Select v East Meadow SC",
        "- May 16, 2026: Scorpions SC v SUSA FC",
        "- May 16, 2026: Connecticut FC United v FC Stars White",
        "- May 17, 2026: Connecticut FC United v FC Stars Blue",
        "- May 17, 2026: Scorpions SC v East Meadow SC",
        "- May 17, 2026: Select v SUSA FC",
        "- May 17, 2026: World Class FC v FC Stars White",
        "- Jun 06, 2026: Connecticut FC United v SUSA FC",
        "- Jun 06, 2026: FSA FC v East Meadow SC (FSA-Farmington Sports Arena)",
        "- Jun 07, 2026: Connecticut FC United v East Meadow SC",
        "- Jun 07, 2026: FSA FC v SUSA FC (FSA-Farmington Sports Arena)",
    ]

    norAtlSched = [
        "- Feb 21, 2026: Pipeline SC v Match Fit Surf (Notre Dame Prepatory School)",
        "- Feb 28, 2026: HEX FC Bucks v Maryland United FC",
        "- Feb 28, 2026: Bethesda SC v Match Fit Surf",
        "- Feb 28, 2026: FC DELCO v Philadelphia Ukrainian Nationals",
        "- Feb 28, 2026: PDA Blue v Penn Fusion SA (PDA Main Complex)",
        "- Feb 28, 2026: Pipeline SC v PDA White (Notre Dame Prepatory School)",
        "- Mar 01, 2026: Penn Fusion SA v Maryland United FC",
        "- Mar 01, 2026: FC DELCO v PDA Blue",
        "- Mar 01, 2026: Bethesda SC v PDA White",
        "- Mar 07, 2026: FC DELCO v Bethesda SC ",
        "- Mar 07, 2026: Philadelphia Ukrainian Nationals v PDA Blue",
        "- Mar 07, 2026: Maryland United FC v PDA White",
        "- Mar 07, 2026: HEX FC Bucks v Pipeline SC (Council Rock South High School)",
        "- Mar 08, 2026: PDA White v Philadelphia Ukrainian Nationals ",
        "- Mar 08, 2026: Maryland United FC v Pipeline SC",
        "- Mar 15, 2026: HEX FC Bucks v PDA Blue (Council Rock South High School)",
        "- Mar 28, 2026: PDA White v PDA Blue",
        "- Mar 28, 2026: Penn Fusion SA v HEX FC Bucks (USTC)",
        "- Mar 28, 2026: Match Fit Surf v Philadelphia Ukrainian Nationals (Morris Catholic High School)",
        "- Mar 28, 2026: Pipeline SC v FC DELCO (Mercy High School)",
        "- Mar 29, 2026: Maryland United FC v FC DELCO",
        "- Apr 11, 2026: Philadelphia Ukrainian Nationals v Maryland United FC",
        "- Apr 11, 2026: FC DELCO v Match Fit Surf",
        "- Apr 11, 2026: Bethesda SC v PDA Blue",
        "- Apr 11, 2026: Pipeline SC v Penn Fusion SA (Notre Dame Prepatory School)",
        "- Apr 18, 2026: Maryland United FC v Bethesda SC",
        "- Apr 18, 2026: Match Fit Surf v PDA Blue (Morris Catholic High School)",
        "- Apr 19, 2026: Match Fit Surf v Penn Fusion SA (Morris Catholic High School)",
        "- Apr 19, 2026: HEX FC Bucks v Philadelphia Ukrainian Nationals (Council Rock South High School)",
        "- Apr 19, 2026: Penn Fusion SA v PDA White (USTC)",
        "- Apr 25, 2026: PDA White v FC DELCO",
        "- Apr 26, 2026: Philadelphia Ukrainian Nationals v Penn Fusion SA",
        "- Apr 26, 2026: Bethesda SC v Pipeline SC",
        "- Apr 26, 2026: Match Fit Surf v HEX FC Bucks (Morris Catholic High School)",
        "- May 02, 2026: Penn Fusion SA v FC DELCO",
        "- May 02, 2026: PDA White v HEX FC Bucks",
        "- May 02, 2026: Match Fit Surf v Maryland United FC",
        "- May 02, 2026: PDA Blue v Pipeline SC (PDA Main Complex)",
        "- May 03, 2026: Philadelphia Ukrainian Nationals v Bethesda SC",
        "- May 03, 2026: FC DELCO v HEX FC Bucks",
        "- May 03, 2026: PDA White v Match Fit Surf",
        "- May 03, 2026: PDA Blue v Maryland United FC (PDA Main Complex)",
        "- May 09, 2026: Bethesda SC v HEX FC Bucks",
        "- May 16, 2026: Bethesda SC v Penn Fusion SA",
        "- May 16, 2026: Pipeline SC v Philadelphia Ukrainian Nationals (Notre Dame Prepatory School)",
    ]

    norCalSched = [
        "- Aug 23, 2025: Placer United v MVLA (Davis Legacy Soccer Complex)",
        "- Aug 23, 2025: Davis Legacy v Mustang SC (Davis Legacy Soccer Complex)",
        "- Aug 23, 2025: Pleasanton RAGE v Marin FC (Val Vista)",
        "- Aug 23, 2025: Bay Area Surf v Santa Rosa United (Gunderson High School)",
        "- Aug 24, 2025: De Anza Force v Placer United (De Anza College)",
        "- Aug 24, 2025: Santa Rosa United v Mustang SC (Trione Fields)",
        "- Aug 24, 2025: Pleasanton RAGE v MVLA (Val Vista)",
        "- Aug 24, 2025: Davis Legacy v COSC (Davis Legacy Soccer Complex)",
        "- Aug 24, 2025: Marin FC v Bay Area Surf (Dominican University)",
        "- Sep 06, 2025: Marin FC v COSC (Marin Academy)",
        "- Sep 06, 2025: MVLA v Mustang SC (Foothill College)",
        "- Sep 06, 2025: San Juan SC v Pleasanton RAGE (San Juan Soccer Complex)",
        "- Sep 06, 2025: Placer United v Davis Legacy (Del Oro High School)",
        "- Sep 06, 2025: Bay Area Surf v De Anza Force (Kathleen MacDonald High School)",
        "- Sep 07, 2025: COSC v MVLA (Fresno State Soccer Stadium)",
        "- Sep 07, 2025: De Anza Force v Pleasanton RAGE (De Anza College)",
        "- Sep 07, 2025: San Juan SC v Placer United (San Juan Soccer Complex)",
        "- Sep 07, 2025: Davis Legacy v Bay Area Surf (Davis Legacy Soccer Complex)",
        "- Sep 07, 2025: Mustang SC v Marin FC (Provident Field @ MSC)",
        "- Sep 13, 2025: Bay Area Surf v Mustang SC (Kathleen MacDonald High School)",
        "- Sep 13, 2025: De Anza Force v Davis Legacy (De Anza College)",
        "- Sep 13, 2025: Marin FC v Placer United (College of Marin)",
        "- Sep 13, 2025: San Juan SC v MVLA (San Juan Soccer Complex)",
        "- Sep 20, 2025: MVLA v Marin FC (Foothill College)",
        "- Sep 20, 2025: Pleasanton RAGE v Davis Legacy (Val Vista)",
        "- Sep 20, 2025: San Juan SC v Santa Rosa United (San Juan Soccer Complex)",
        "- Sep 20, 2025: Placer United v Bay Area Surf (Whitney High School)",
        "- Sep 20, 2025: Mustang SC v COSC (Provident Field @ MSC)",
        "- Sep 27, 2025: MVLA v Santa Rosa United (Foothill College)",
        "- Sep 27, 2025: Mustang SC v Placer United (Provident Field @ MSC)",
        "- Sep 27, 2025: San Juan SC v Bay Area Surf (San Juan Soccer Complex)",
        "- Sep 27, 2025: COSC v Pleasanton RAGE (Fresno State Soccer Stadium)",
        "- Sep 27, 2025: Marin FC v De Anza Force (Marin Catholic High School)",
        "- Sep 28, 2025: Mustang SC v Pleasanton RAGE (Provident Field @ MSC)",
        "- Sep 28, 2025: Santa Rosa United v Marin FC (Trione Fields)",
        "- Sep 28, 2025: De Anza Force v San Juan SC (De Anza College)",
        "- Sep 28, 2025: Bay Area Surf v MVLA (Kathleen MacDonald High School)",
        "- Sep 28, 2025: Placer United v COSC (Placer High School)",
        "- Oct 04, 2025: Placer United v Pleasanton RAGE (Whitney High School)",
        "- Oct 04, 2025: COSC v Bay Area Surf (Edison High School)",
        "- Oct 04, 2025: San Juan SC v Marin FC (San Juan Soccer Complex)",
        "- Oct 04, 2025: Santa Rosa United v De Anza Force (Trione Fields)",
        "- Oct 04, 2025: Davis Legacy v MVLA (Davis Legacy Soccer Complex)",
        "- Oct 18, 2025: Placer United v Santa Rosa United (Davis Legacy Soccer Complex)",
        "- Oct 18, 2025: San Juan SC v COSC (San Juan Soccer Complex)",
        "- Oct 18, 2025: De Anza Force v Mustang SC (De Anza College)",
        "- Oct 18, 2025: Bay Area Surf v Pleasanton RAGE (Kathleen MacDonald High School)",
        "- Oct 18, 2025: Marin FC v Davis Legacy (Marin Catholic High School)",
        "- Oct 25, 2025: Mustang SC v San Juan SC (Provident Field @ MSC)",
        "- Oct 25, 2025: Pleasanton RAGE v Santa Rosa United (Val Vista)",
        "- Oct 25, 2025: COSC v Marin FC (Buchanan High School)",
        "- Oct 25, 2025: Davis Legacy v Placer United (Davis Legacy Soccer Complex)",
        "- Oct 25, 2025: De Anza Force v MVLA (De Anza College)",
        "- Nov 01, 2025: De Anza Force v Bay Area Surf (De Anza College)",
        "- Nov 01, 2025: Mustang SC v Davis Legacy (Provident Field @ MSC)",
        "- Nov 01, 2025: MVLA v Placer United (Foothill College)",
        "- Nov 01, 2025: Pleasanton RAGE v San Juan SC (Val Vista)",
        "- Nov 01, 2025: COSC v Santa Rosa United (Clovis High School)",
        "- Nov 02, 2025: MVLA v Pleasanton RAGE (Foothill College)",
        "- Nov 02, 2025: Bay Area Surf v San Juan SC (Kathleen MacDonald High School)",
        "- Nov 02, 2025: COSC v Davis Legacy (Fresno State Soccer Stadium)",
        "- Nov 02, 2025: Placer United v De Anza Force (Placer High School)",
        "- Nov 08, 2025: De Anza Force v COSC (De Anza College)",
        "- Nov 08, 2025: Marin FC v Pleasanton RAGE (De Anza High School)",
        "- Nov 08, 2025: Mustang SC v Bay Area Surf (Provident Field @ MSC)",
        "- Nov 08, 2025: MVLA v San Juan SC (Foothill College)",
        "- Mar 14, 2026: MVLA v COSC",
        "- Mar 14, 2026: Santa Rosa United v Bay Area Surf (Trione Fields)",
        "- Mar 14, 2026: San Juan SC v Mustang SC (San Juan Soccer Complex)",
        "- Mar 14, 2026: Davis Legacy v Pleasanton RAGE (Davis Legacy Soccer Complex)",
        "- Mar 14, 2026: Placer United v Marin FC (Placer Valley Soccer Complex)",
        "- Mar 15, 2026: Davis Legacy v Santa Rosa United (Playfields Park)",
        "- Mar 21, 2026: Mustang SC v De Anza Force",
        "- Mar 21, 2026: Pleasanton RAGE v COSC (G11)",
        "- Mar 21, 2026: Placer United v San Juan SC (Placer Valley Soccer Complex)",
        "- Mar 21, 2026: Santa Rosa United v MVLA (Trione Fields)",
        "- Mar 21, 2026: Davis Legacy v Marin FC (Davis Legacy Soccer Complex)",
        "- Apr 04, 2026: Bay Area Surf v Davis Legacy",
        "- Apr 04, 2026: Marin FC v Mustang SC",
        "- Apr 04, 2026: MVLA v De Anza Force",
        "- Apr 04, 2026: Santa Rosa United v San Juan SC (Trione Fields)",
        "- Apr 04, 2026: COSC v Placer United (Edison High School)",
        "- Apr 11, 2026: Santa Rosa United v COSC",
        "- Apr 18, 2026: Marin FC v San Juan SC",
        "- Apr 18, 2026: MVLA v Bay Area Surf",
        "- Apr 18, 2026: Placer United v Mustang SC",
        "- Apr 18, 2026: Santa Rosa United v Pleasanton RAGE (Trione Fields)",
        "- Apr 18, 2026: Davis Legacy v De Anza Force (Davis Legacy Soccer Complex)",
        "- Apr 18, 2026: COSC v De Anza Force (Edison High School)",
        "- Apr 19, 2026: Bay Area Surf v Marin FC",
        "- Apr 19, 2026: De Anza Force v Santa Rosa United",
        "- Apr 19, 2026: Mustang SC v MVLA",
        "- Apr 19, 2026: Pleasanton RAGE v Placer United",
        "- Apr 19, 2026: San Juan SC v Davis Legacy (San Juan Soccer Complex)",
        "- Apr 25, 2026: De Anza Force v Marin FC",
        "- Apr 25, 2026: Davis Legacy v MVLA",
        "- Apr 25, 2026: Pleasanton RAGE v Bay Area Surf",
        "- Apr 25, 2026: COSC v San Juan SC (Edison High School)",
        "- Apr 25, 2026: Santa Rosa United v Placer United (Trione Fields)",
        "- May 02, 2026: Bay Area Surf v COSC (G11)",
        "- May 02, 2026: Marin FC v MVLA",
        "- May 02, 2026: Pleasanton RAGE v Mustang SC",
        "- May 02, 2026: Santa Rosa United v Davis Legacy (Trione Fields)",
        "- May 02, 2026: San Juan SC v De Anza Force (San Juan Soccer Complex)",
        "- May 09, 2026: Bay Area Surf v Placer United",
        "- May 09, 2026: Marin FC v Santa Rosa United",
        "- May 09, 2026: Pleasanton RAGE v De Anza Force",
        "- May 09, 2026: COSC v Mustang SC (Edison High School)",
        "- May 09, 2026: Davis Legacy v San Juan SC (Davis Legacy Soccer Complex)",
    ]

    nwSched = [
        "- Nov 09, 2025: Utah Avalanche v La Roca FC (St. Joseph Catholic High School)",
        "- Dec 13, 2025: Washington Premier v Oregon Surf (WPFC Field Complex)",
        "- Dec 13, 2025: XF Academy v La Roca FC (Marymoor Park)",
        "- Dec 13, 2025: Eastside FC v Utah Avalanche (Preston Park Athletic Fields)",
        "- Dec 13, 2025: PacNW SC v Boise Thorns FC (Valley Ridge)",
        "- Dec 13, 2025: Seattle United v Portland Thorns (Ingraham High School)",
        "- Dec 14, 2025: Eastside FC v La Roca FC (Preston Park Athletic Fields)",
        "- Dec 14, 2025: XF Academy v Utah Avalanche (Marymoor Park)",
        "- Dec 14, 2025: Seattle United v Oregon Surf (Ingraham High School)",
        "- Dec 14, 2025: Boise Thorns FC v PacNW SC (North SeaTac Park)",
        "- Dec 14, 2025: Washington Premier v Portland Thorns (WPFC Field Complex)",
        "- Jan 10, 2026: Seattle United v Boise Thorns FC (Shoreline A/B Fields)",
        "- Jan 10, 2026: Eastside FC v PacNW SC (Preston Park Athletic Fields)",
        "- Jan 11, 2026: Seattle United v PacNW SC (Shoreline A/B Fields)",
        "- Jan 11, 2026: Eastside FC v Boise Thorns FC (Preston Park Athletic Fields)",
        "- Jan 17, 2026: Eastside FC v Oregon Surf (Valley Ridge)",
        "- Jan 17, 2026: PacNW SC v Portland Thorns (Valley Ridge)",
        "- Jan 18, 2026: Eastside FC v Portland Thorns (Valley Ridge)",
        "- Jan 18, 2026: PacNW SC v Oregon Surf (Valley Ridge)",
        "- Jan 18, 2026: XF Academy v Seattle United (Marymoor Park)",
        "- Jan 24, 2026: Seattle United v Utah Avalanche (Shoreline A/B Fields)",
        "- Jan 24, 2026: Washington Premier v La Roca FC (WPFC Field Complex)",
        "- Jan 25, 2026: Seattle United v La Roca FC (Shorecrest High School)",
        "- Jan 25, 2026: Washington Premier v Utah Avalanche (WPFC Field Complex)",
        "- Jan 31, 2026: Portland Thorns v XF Academy (Gordon Faber Recreation Complex)",
        "- Jan 31, 2026: Seattle United v Washington Premier (Magnuson Park)",
        "- Jan 31, 2026: Oregon Surf v Boise Thorns FC (Mountain View Champions Park)",
        "- Feb 01, 2026: Portland Thorns v Boise Thorns FC (Gordon Faber Recreation Complex)",
        "- Feb 01, 2026: Oregon Surf v XF Academy (Mountain View Champions Park)",
        "- Feb 07, 2026: PacNW SC v XF Academy (Valley Ridge)",
        "- Feb 07, 2026: Eastside FC v Seattle United (Preston Park Athletic Fields)",
        "- Feb 07, 2026: Washington Premier v Boise Thorns FC (WPFC Field Complex)",
        "- Feb 08, 2026: Washington Premier v PacNW SC (WPFC Field Complex)",
        "- Feb 08, 2026: XF Academy v Boise Thorns FC (Marymoor Park)",
        "- Feb 21, 2026: Washington Premier v Eastside FC (WPFC Field Complex)",
        "- Feb 21, 2026: Portland Thorns v Utah Avalanche (Gordon Faber Recreation Complex)",
        "- Feb 21, 2026: Seattle United v XF Academy (Genesee Park Playfield)",
        "- Feb 21, 2026: Oregon Surf v La Roca FC (PCC Rock Creek)",
        "- Feb 22, 2026: Washington Premier v XF Academy (WPFC Field Complex)",
        "- Feb 22, 2026: Seattle United v Eastside FC (Shoreline A/B Fields)",
        "- Feb 22, 2026: Portland Thorns v La Roca FC (Gordon Faber Recreation Complex)",
        "- Feb 22, 2026: Oregon Surf v Utah Avalanche (PCC Rock Creek)",
        "- Feb 28, 2026: Eastside FC v XF Academy (Preston Park Athletic Fields)",
        "- Mar 01, 2026: Boise Thorns FC v Portland Thorns (Timberline High School)",
        "- Mar 01, 2026: PacNW SC v Washington Premier (Starfire Sports)",
        "- Mar 07, 2026: La Roca FC v Boise Thorns FC (La Roca FC Utah County Complex)",
        "- Mar 07, 2026: Utah Avalanche v PacNW SC (Judge Memorial High School)",
        "- Mar 07, 2026: Eastside FC v Washington Premier (Preston Park Athletic Fields)",
        "- Mar 07, 2026: Portland Thorns v Oregon Surf (Gordon Faber Recreation Complex)",
        "- Mar 08, 2026: Utah Avalanche v Boise Thorns FC (Westminster College)",
        "- Mar 08, 2026: La Roca FC v PacNW SC (La Roca FC Utah County Complex)",
        "- Mar 14, 2026: XF Academy v Portland Thorns (Marymoor Park)",
        "- Mar 14, 2026: Boise Thorns v Oregon Surf",
        "- Mar 21, 2026: La Roca FC v Eastside FC",
        "- Mar 21, 2026: Portland Thorns v Seattle United",
        "- Mar 21, 2026: Utah Avalanche v XF Academy (Murray City Park)",
        "- Mar 21, 2026: Oregon Surf v Washington Premier (PCC Rock Creek)",
        "- Mar 22, 2026: La Roca FC v XF Academy (La Roca FC Utah County Complex)",
        "- Mar 22, 2026: Utah Avalanche v Eastside FC (Murray City Park)",
        "- Mar 22, 2026: Portland Thorns v Washington Premier (Mountain View Champions Park)",
        "- Mar 22, 2026: Oregon Surf v Seattle United (PCC Rock Creek)",
        "- Apr 11, 2026: Portland Thorns v PacNW SC",
        "- Apr 11, 2026: Boise Thorns v XF Academy",
        "- Apr 11, 2026: La Roca FC v Washington Premier (La Roca Park)",
        "- Apr 11, 2026: Utah Avalanche v Seattle United (St. Joseph Catholic High School)",
        "- Apr 11, 2026: Oregon Surf v Eastside FC (Mountain View Champions Park)",
        "- Apr 12, 2026: La Roca FC v Seattle United (La Roca Park)",
        "- Apr 12, 2026: Utah Avalanche v Washington Premier (St. Joseph Catholic High School)",
        "- Apr 12, 2026: Portland Thorns v Eastside FC (Gordon Faber Recreation Complex)",
        "- Apr 12, 2026: Oregon Surf v PacNW SC (Mountain View Champions Park)",
        "- Apr 18, 2026: Utah Avalanche v Portland Thorns (Murray City Park)",
        "- Apr 18, 2026: La Roca FC v Oregon Surf (Regional Athletic Complex)",
        "- Apr 19, 2026: Boise Thorns FC v Eastside FC",
        "- Apr 19, 2026: La Roca FC v Portland Thorns (Regional Athletic Complex)",
        "- Apr 19, 2026: Utah Avalanche v Oregon Surf (Murray City Park)",
        "- Apr 25, 2026: Boise Thorns FC v La Roca FC",
        "- Apr 25, 2026: PacNW SC v Utah Avalanche",
        "- Apr 25, 2026: XF Academy v Eastside FC",
        "- Apr 26, 2026: Boise Thorns FC v Utah Avalanche",
        "- Apr 26, 2026: La Roca FC v PacNW SC",
        "- Apr 26, 2026: Washington Premier v Seattle United (WPFC Field Complex)",
        "- May 02, 2026: Boise Thorns FC v Seattle United",
        "- May 02, 2026: Oregon Surf v Portland Thorns",
        "- May 02, 2026: PacNW SC v Eastside FC",
        "- May 02, 2026: XF Academy v Washington Premier",
        "- May 02, 2026: La Roca FC v Utah Avalanche (La Roca Park)",
        "- May 09, 2026: XF Academy v Oregon Surf",
        "- May 09, 2026: PacNW SC v Seattle United",
        "- May 09, 2026: Boise Thorns FC v Washington Premier",
    ]

    ohioNorSched = [
        "- Nov 22, 2025: Pittsburgh Riverhounds v Racing Louisville Academy (Montour Junction Sports Complex)",
        "- Nov 22, 2025: WNY Flash v Ohio Elite SA (Flash Fields)",
        "- Nov 22, 2025: Ohio Premier v Internationals SC (Kilbourne Run Sports Park)",
        "- Nov 22, 2025: GTFC Impact v Cleveland Force SC (Rossford Soccer Center Dome)",
        "- Nov 23, 2025: WNY Flash v Racing Louisville Academy (Flash Fields)",
        "- Nov 23, 2025: Ohio Premier v Cleveland Force SC (Kilbourne Run Sports Park)",
        "- Nov 23, 2025: Pittsburgh Riverhounds v Ohio Elite SA (Montour Junction Sports Complex)",
        "- Nov 23, 2025: GTFC Impact v Internationals SC (Rossford Soccer Center Dome)",
        "- Dec 13, 2025: GTFC Impact v Ohio Premier SC (Rossford Soccer Center Dome)",
        "- Jan 17, 2026: Pittsburgh Riverhounds v WNY Flash (Montour Junction Sports Complex)",
        "- Feb 28, 2026: GTFC Impact v Tennessee SC (Rossford Soccer Center Dome)",
        "- Feb 28, 2026: Ohio Premier v FC Alliance (OP Training Facility)",
        "- Mar 01, 2026: GTFC Impact v FC Alliance (Rossford Soccer Center Dome)",
        "- Mar 01, 2026: Ohio Premier v Tennessee SC (OP Training Facility)",
        "- Mar 07, 2026: GTFC Impact v WNY Flash (Rossford Soccer Center Dome)",
        "- Mar 07, 2026: Ohio Premier v Pittsburgh Riverhounds (OP Training Facility)",
        "- Mar 08, 2026: GTFC Impact v Pittsburgh Riverhounds (Rossford Soccer Center Dome)",
        "- Mar 08, 2026: Ohio Premier v WNY Flash (OP Training Facility)",
        "- Mar 14, 2026: Pittsburgh Riverhounds v Internationals SC",
        "- Mar 14, 2026: WNY Flash v Cleveland Force SC (Flash Fields)",
        "- Mar 15, 2026: Pittsburgh Riverhounds v Cleveland Force SC",
        "- Mar 15, 2026: WNY Flash v Internationals SC (Flash Fields)",
        "- Mar 22, 2026: Internationals SC v Cleveland Force SC (Pinnacle Sports)",
        "- Apr 11, 2026: Cleveland Force SC v GTFC Impact (Victory Park)",
        "- Apr 11, 2026: Internationals SC v Ohio Premier (Pinnacle Sports)",
        "- Apr 12, 2026: Cleveland Force SC v Ohio Premier (Victory Park)",
        "- Apr 12, 2026: Internationals SC v GTFC Impact (Pinnacle Sports)",
        "- Apr 18, 2026: Cleveland Force SC v Tennessee SC",
        "- Apr 18, 2026: Pittsburgh Riverhounds v Ohio Premier",
        "- Apr 18, 2026: WNY Flash v GTFC Impact (Sahlen's Sports Park)",
        "- Apr 18, 2026: Internationals SC v FC Alliance (Pinnacle Sports)",
        "- Apr 19, 2026: Cleveland Force SC v FC Alliance",
        "- Apr 19, 2026: Pittsburgh Riverhounds v GTFC Impact",
        "- Apr 19, 2026: WNY Flash v Ohio Premier (Sahlen's Sports Park)",
        "- Apr 19, 2026: Internationals SC v Tennessee SC (Pinnacle Sports)",
        "- May 02, 2026: Cleveland Force SC v WNY Flash",
        "- May 02, 2026: Internationals SC v Pittsburgh Riverhounds",
        "- May 02, 2026: GTFC Impact v Indy Eleven Pro Academy (Rossford Soccer Center Dome)",
        "- May 02, 2026: Ohio Premier v FC Pride Elite (OP Training Facility)",
        "- May 03, 2026: Cleveland Force SC v Pittsburgh Riverhounds",
        "- May 03, 2026: Internationals SC v WNY Flash",
        "- May 03, 2026: GTFC Impact v FC Pride Elite (Rossford Soccer Center Dome)",
        "- May 03, 2026: Ohio Premier v Indy Eleven Pro Academy (OP Training Facility)",
        "- May 16, 2026: WNY Flash v Pittsburgh Riverhounds (Flash Fields)",
        "- May 16, 2026: Cleveland Force SC v Internationals SC (Victory Park)",
        "- May 17, 2026: Ohio Premier v GTFC Impact (OP Training Facility)",
    ]

    ohioSouSched = [
        "- Nov 22, 2025: Indy Eleven Pro Academy v Tennessee SC (Grand Park)",
        "- Nov 22, 2025: FC Pride Elite v FC Alliance (Pride Performance Center)",
        "- Nov 23, 2025: Indy Eleven Pro Academy v FC Alliance (Grand Park)",
        "- Nov 23, 2025: FC Pride Elite v Tennessee SC (Pride Performance Center)",
        "- Dec 13, 2025: FC Pride Elite v Indy Eleven Pro Academy (Pride Performance Center)",
        "- Jan 31, 2026: FC Alliance v Tennessee SC (Hardin Valley Academy Stadium)",
        "- Feb 14, 2026: Racing Louisville Academy v FC Pride Elite (Lynn Family Sports Vision & Training Facility)",
        "- Feb 14, 2026: Ohio Elite SA v Indy Eleven Pro Academy (Seven Hills School)",
        "- Feb 15, 2026: Racing Louisville Academy v Indy Eleven Pro Academy (Lynn Family Sports Vision & Training Facility)",
        "- Feb 15, 2026: Ohio Elite SA v FC Pride Elite (Seven Hills School)",
        "- Feb 21, 2026: Tennessee SC v WNY Flash (Bethesda Sports Park)",
        "- Feb 21, 2026: FC Alliance v Pittsburgh Riverhounds (Hardin Valley Academy Stadium)",
        "- Feb 22, 2026: Tennessee SC v Pittsburgh Riverhounds (Bethesda Sports Park)",
        "- Feb 22, 2026: FC Alliance v WNY Flash (Hardin Valley Academy Stadium)",
        "- Mar 01, 2026: Racing Louisville Academy v Ohio Elite SA (Shelbyville High School)",
        "- Mar 07, 2026: Tennessee SC v Indy Eleven Pro Academy",
        "- Mar 07, 2026: FC Alliance v FC Pride Elite (Hardin Valley Academy Stadium)",
        "- Mar 07, 2026: Ohio Elite SA v Cleveland Force SC (Seven Hills School)",
        "- Mar 07, 2026: Racing Louisville Academy v Internationals SC (Lynn Family Sports Vision & Training Facility)",
        "- Mar 08, 2026: Tennessee SC v FC Pride Elite (Richard Siegel Soccer Complex)",
        "- Mar 08, 2026: FC Alliance v Indy Eleven Pro Academy (Hardin Valley Academy Stadium)",
        "- Mar 08, 2026: Ohio Elite SA v Internationals SC (Seven Hills School)",
        "- Mar 08, 2026: Racing Louisville Academy v Cleveland Force SC (Lynn Family Sports Vision & Training Facility)",
        "- Mar 15, 2026: FC Pride Elite v Racing Louisville Academy (Pride Performance Center)",
        "- Mar 21, 2026: Racing Louisville Academy v FC Alliance (Lynn Family Sports Vision & Training Facility)",
        "- Mar 21, 2026: Ohio Elite SA v Tennessee SC (Seven Hills School)",
        "- Mar 21, 2026: FC Pride Elite v Pittsburgh Riverhounds (Pride Performance Center)",
        "- Mar 21, 2026: Indy Eleven Pro Academy v WNY Flash (Grand Park)",
        "- Mar 22, 2026: Racing Louisville Academy v Tennessee SC (Lynn Family Sports Vision & Training Facility)",
        "- Mar 22, 2026: Ohio Elite SA v FC Alliance (Seven Hills School)",
        "- Mar 22, 2026: Indy Eleven Pro Academy v Pittsburgh Riverhounds (Grand Park)",
        "- Mar 22, 2026: FC Pride Elite v WNY Flash (Pride Performance Center)",
        "- Mar 28, 2026: Indy Eleven Pro Academy v Ohio Elite SA",
        "- Apr 18, 2026: FC Pride Elite v Ohio Elite SA (Pride Performance Center)",
        "- Apr 18, 2026: Indy Eleven Pro Academy v Racing Louisville Academy (Grand Park)",
        "- Apr 25, 2026: Racing Louisville Academy v Ohio Premier (Lynn Family Sports Vision & Training Facility)",
        "- Apr 25, 2026: Ohio Elite SA v GTFC Impact (Ohio Elite Training Center)",
        "- Apr 25, 2026: Indy Eleven Pro Academy v Cleveland Force SC (Grand Park)",
        "- Apr 25, 2026: FC Pride Elite v Internationals SC (Pride Performance Center)",
        "- Apr 26, 2026: Racing Louisville Academy v GTFC Impact (Lynn Family Sports Vision & Training Facility)",
        "- Apr 26, 2026: Indy Eleven Pro Academy v Internationals SC (Grand Park)",
        "- Apr 26, 2026: Ohio Elite SA v Ohio Premier (Ohio Elite Training Center)",
        "- Apr 26, 2026: FC Pride Elite v Cleveland Force SC (Pride Performance Center)",
        "- May 02, 2026: FC Alliance v Racing Louisville Academy (Hardin Valley Academy Stadium)",
        "- May 02, 2026: Tennessee SC v Ohio Elite SA (Richard Siegel Soccer Complex)",
        "- May 03, 2026: FC Alliance v Ohio Elite SA (Hardin Valley Academy Stadium)",
        "- May 03, 2026: Tennessee SC v Racing Louisville Academy (Richard Siegel Soccer Complex)",
        "- May 09, 2026: Tennessee SC v FC Alliance (Bethesda Sports Park)",
        "- May 09, 2026: Ohio Elite SA v Racing Louisville Academy (Ohio Elite Training Center)",
        "- May 09, 2026: Indy Eleven Pro Academy v FC Pride Elite (Grand Park)",
    ]

    seSched = [
        "- Sep 06, 2025: FC Prime v CESA Liberty (Mullins Park)",
        "- Sep 06, 2025: FL Premier FC v GSA (Starkey Ranch District Park)",
        "- Sep 06, 2025: Florida West FC v South Carolina United (North Collier Regional Park)",
        "- Sep 06, 2025: Jacksonville FC v United Futbol Academy (Patton Park)",
        "- Sep 06, 2025: Florida Krush v Alabama FC (Central Winds)",
        "- Sep 06, 2025: Tampa Bay United v Concorde Fire Platinum (Ed Radice Sports Complex)",
        "- Sep 06, 2025: Sporting Jax v Atlanta Fire United (Veterans Park)",
        "- Sep 06, 2025: Orlando Pride v Concorde Fire Premier (Seminole)",
        "- Sep 07, 2025: Florida West FC v CESA Liberty (North Collier Regional Park)",
        "- Sep 07, 2025: FL Premier FC v Concorde Fire Platinum (Starkey Ranch District Park)",
        "- Sep 07, 2025: Jacksonville FC v Atlanta Fire United (Patton Park)",
        "- Sep 07, 2025: FC Prime v South Carolina United (Mullins Park)",
        "- Sep 07, 2025: Tampa Bay United v GSA (Ed Radice Sports Complex)",
        "- Sep 07, 2025: Sporting Jax v United Futbol Academy (Veterans Park)",
        "- Sep 07, 2025: Florida Krush v Concorde Fire Premier (Central Winds)",
        "- Sep 07, 2025: Orlando Pride v Alabama FC (Seminole)",
        "- Sep 13, 2025: United Futbol Academy v Orlando Pride (Fowler Park)",
        "- Sep 13, 2025: Alabama FC v Tampa Bay United (Dunnavant Valley Fields)",
        "- Sep 13, 2025: Atlanta Fire United v Florida Krush (Pinecrest Academy)",
        "- Sep 13, 2025: Concorde Fire Premier v FL Premier FC (Opelika Sportsplex)",
        "- Sep 13, 2025: CESA Liberty v Jacksonville FC (Mesa Soccer Complex)",
        "- Sep 13, 2025: GSA v FC Prime (GSA South - Holman)",
        "- Sep 13, 2025: South Carolina United v Sporting Jax (Southeastern Freight Lines Complex)",
        "- Sep 13, 2025: Concorde Fire Platinum v Florida West FC (GSA East)",
        "- Sep 14, 2025: United Futbol Academy v Florida Krush (Fowler Park)",
        "- Sep 14, 2025: Atlanta Fire United v Orlando Pride (Pinecrest Academy)",
        "- Sep 14, 2025: GSA v Florida West FC (GSA South - Holman)",
        "- Sep 14, 2025: Concorde Fire Platinum v FC Prime (GSA East)",
        "- Sep 14, 2025: CESA Liberty v Sporting Jax (Mesa Soccer Complex)",
        "- Sep 14, 2025: South Carolina United v Jacksonville FC (Southeastern Freight Lines Complex)",
        "- Sep 14, 2025: Concorde Fire Premier v Tampa Bay United (Opelika Sportsplex)",
        "- Sep 14, 2025: Alabama FC v FL Premier FC (Dunnavant Valley Fields)",
        "- Sep 20, 2025: Florida West FC v Concorde Fire Premier (JetBlue Park)",
        "- Sep 20, 2025: FC Prime v Alabama FC (Amelia Earhart)",
        "- Sep 21, 2025: Florida West FC v Alabama FC (JetBlue Park)",
        "- Sep 21, 2025: FC Prime v Concorde Fire Premier (Amelia Earhart)",
        "- Sep 27, 2025: FL Premier FC v United Futbol Academy (Starkey Ranch District Park)",
        "- Sep 27, 2025: Jacksonville FC v Concorde Fire Platinum (Patton Park)",
        "- Sep 27, 2025: Tampa Bay United v Atlanta Fire United (Ed Radice Sports Complex)",
        "- Sep 27, 2025: Florida Krush v South Carolina United (Shane Kelly Park)",
        "- Sep 27, 2025: Sporting Jax v GSA (Veterans Park)",
        "- Sep 27, 2025: Orlando Pride v CESA Liberty (Seminole)",
        "- Sep 28, 2025: FL Premier FC v Atlanta Fire United (Starkey Ranch District Park)",
        "- Sep 28, 2025: Tampa Bay United v United Futbol Academy (Ed Radice Sports Complex)",
        "- Sep 28, 2025: Jacksonville FC v GSA (Patton Park)",
        "- Sep 28, 2025: Florida Krush v CESA Liberty (Shane Kelly Park)",
        "- Sep 28, 2025: Orlando Pride v South Carolina United (Seminole)",
        "- Sep 28, 2025: Sporting Jax v Concorde Fire Platinum (Veterans Park)",
        "- Oct 04, 2025: Alabama FC v Sporting Jax (Dunnavant Valley Fields)",
        "- Oct 04, 2025: Concorde Fire Premier v Jacksonville FC (Georgia Sports Park)",
        "- Oct 04, 2025: United Futbol Academy v Florida West FC (Fowler Park)",
        "- Oct 04, 2025: Atlanta Fire United v FC Prime (Pinecrest Academy)",
        "- Oct 04, 2025: GSA v CESA Liberty (GSA East - Friends Stadium)",
        "- Oct 04, 2025: Concorde Fire Platinum v South Carolina United (Georgia Sports Park)",
        "- Oct 05, 2025: Atlanta Fire United v Florida West FC (Pinecrest Academy)",
        "- Oct 05, 2025: United Futbol Academy v FC Prime (Fowler Park)",
        "- Oct 05, 2025: Concorde Fire Platinum v CESA Liberty (Georgia Sports Park)",
        "- Oct 05, 2025: GSA v South Carolina United (GSA East - Friends Stadium)",
        "- Oct 05, 2025: Concorde Fire Premier v Sporting Jax (Georgia Sports Park)",
        "- Oct 05, 2025: Alabama FC v Jacksonville FC (Dunnavant Valley Fields)",
        "- Oct 18, 2025: Sporting Jax v Orlando Pride (Veterans Park)",
        "- Oct 18, 2025: South Carolina United v Atlanta Fire United (Southeastern Freight Lines Complex)",
        "- Oct 18, 2025: CESA Liberty v United Futbol Academy (Mesa Soccer Complex)",
        "- Oct 18, 2025: Alabama FC v Concorde Fire Platinum (Dunnavant Valley Fields)",
        "- Oct 18, 2025: Concorde Fire Premier v GSA (Georgia Soccer Park)",
        "- Oct 19, 2025: CESA Liberty v Atlanta Fire United (Mesa Soccer Complex)",
        "- Oct 19, 2025: South Carolina United v United Futbol Academy (Southeastern Freight Lines Complex)",
        "- Oct 19, 2025: Alabama FC v GSA (Dunnavant Valley Fields)",
        "- Oct 19, 2025: Concorde Fire Premier v Concorde Fire Platinum (Georgia Sports Park)",
        "- Oct 25, 2025: South Carolina United v FL Premier FC (Southeastern Freight Lines Complex)",
        "- Oct 25, 2025: Concorde Fire Platinum v Orlando Pride (Georgia Soccer Park)",
        "- Oct 25, 2025: United Futbol Academy v Concorde Fire Premier (Fowler Park)",
        "- Oct 25, 2025: GSA v Florida Krush (GSA East - Family)",
        "- Oct 25, 2025: Atlanta Fire United v Alabama FC (Pinecrest Academy)",
        "- Oct 25, 2025: CESA Liberty v Tampa Bay United (Mesa Soccer Complex)",
        "- Oct 26, 2025: Concorde Fire Platinum v Florida Krush (Georgia Soccer Park)",
        "- Oct 26, 2025: CESA Liberty v FL Premier FC (Mesa Soccer Complex)",
        "- Oct 26, 2025: Atlanta Fire United v Concorde Fire Premier (Notre Dame Academy)",
        "- Oct 26, 2025: South Carolina United v Tampa Bay United (Southeastern Freight Lines Complex)",
        "- Oct 26, 2025: GSA v Orlando Pride (GSA East - Friends Stadium)",
        "- Oct 26, 2025: United Futbol Academy v Alabama FC (Fowler Park)",
        "- Nov 08, 2025: Atlanta Fire United v GSA (Pinecrest Academy)",
        "- Nov 08, 2025: Concorde Fire Platinum v United Futbol Academy (Georgia Sports Park)",
        "- Nov 08, 2025: Concorde Fire Premier v CESA Liberty (Georgia Sports Park)",
        "- Nov 08, 2025: Alabama FC v South Carolina United (Dunnavant Valley Fields)",
        "- Nov 09, 2025: United Futbol Academy v GSA (Fowler Park)",
        "- Nov 09, 2025: Alabama FC v CESA Liberty (Dunnavant Valley Fields)",
        "- Nov 09, 2025: Atlanta Fire United v Concorde Fire Platinum (Pinecrest Academy)",
        "- Nov 09, 2025: Concorde Fire Premier v South Carolina United (Georgia Sports Park)",
        "- Nov 15, 2025: United Futbol Academy v Atlanta Fire United (Fowler Park)",
        "- Nov 22, 2025: Concorde Fire Premier v Alabama FC (Georgia Sports Park)",
        "- Nov 22, 2025: GSA v Concorde Fire Platinum (GSA East - Friends Stadium)",
        "- Dec 13, 2025: CESA Liberty v South Carolina United (Mesa Soccer Complex)",
        "- Mar 14, 2026: Florida West FC v Orlando Pride (Bayshore Sports Complex)",
        "- Mar 14, 2026: FC Prime v Florida Krush (Mullins Park)",
        "- Mar 14, 2026: FL Premier FC v Jacksonville FC (Wiregrass Ranch Sports Campus)",
        "- Mar 14, 2026: Tampa Bay United v Sporting Jax (Ed Radice Sports Complex)",
        "- Mar 15, 2026: FC Prime v Orlando Pride (Mullins Park)",
        "- Mar 15, 2026: Tampa Bay United v Jacksonville FC (Ed Radice Sports Complex)",
        "- Mar 15, 2026: Florida West FC v Florida Krush (Bayshore Sports Complex)",
        "- Mar 15, 2026: FL Premier FC v Sporting Jax (Wiregrass Ranch Sports Campus)",
        "- Mar 21, 2026: FL Premier FC v FC Prime (Wiregrass Ranch Sports Campus)",
        "- Mar 21, 2026: Tampa Bay United v Florida West FC (Ed Radice Sports Complex)",
        "- Mar 22, 2026: FL Premier FC v Florida West FC (Wiregrass Ranch Sports Campus)",
        "- Mar 22, 2026: Tampa Bay United v FC Prime (Ed Radice Sports Complex)",
        "- Mar 28, 2026: FL Premier FC v Tampa Bay United (Wiregrass Ranch Sports Campus)",
        "- Mar 28, 2026: Sporting Jax v Jacksonville FC (Veterans Park)",
        "- Mar 28, 2026: Florida Krush v Orlando Pride (Central Winds)",
        "- Mar 28, 2026: Florida West FC v FC Prime (Bayshore Sports Complex)",
        "- Mar 29, 2026: Jacksonville FC v Orlando Pride (Patton Park)",
        "- Apr 12, 2026: Jacksonville FC v Florida Krush (Patton Park)",
        "- Apr 18, 2026: Orlando Pride v FL Premier FC (-)",
        "- Apr 18, 2026: Florida Krush v Tampa Bay United (Central Winds)",
        "- Apr 18, 2026: FC Prime v Sporting Jax (Mullins Park)",
        "- Apr 18, 2026: Florida West FC v Jacksonville FC (North Collier Regional Park)",
        "- Apr 19, 2026: Orlando Pride v Tampa Bay United (-)",
        "- Apr 19, 2026: FC Prime v Jacksonville FC (Mullins Park)",
        "- Apr 19, 2026: Florida Krush v FL Premier FC (Central Winds)",
        "- Apr 19, 2026: Florida West FC v Sporting Jax (Bayshore Sports Complex)",
        "- Apr 25, 2026: Sporting Jax v Florida Krush (Veterans Park)"
    ]

    swSched = [
        "- Sep 06, 2025: LV Heat Surf v Utah Royals FC-AZ (Heritage Park)",
        "- Sep 06, 2025: LAFC So Cal v San Diego Surf (Oak Park High School)",
        "- Sep 06, 2025: Legends FC v Rebels SC (Silverlakes Complex)",
        "- Sep 06, 2025: Eagles SC v Slammers FC HB Koge (Pleasant Valley Fields)",
        "- Sep 06, 2025: Sporting CA USA v LA Breakers FC (Silverlakes Complex)",
        "- Sep 06, 2025: Phoenix Rising v Beach FC (CA) (PRFC Youth Soccer Facility)",
        "- Sep 06, 2025: So Cal Blues v SLAMMERS FC (OC Great Park)",
        "- Sep 06, 2025: Legends FC San Diego v Pateadores (Miramesa High School)",
        "- Sep 13, 2025: San Diego Surf v Arizona Arsenal (Surf Sports Park)",
        "- Sep 13, 2025: Legends FC v Beach FC (CA) (Silverlakes Complex)",
        "- Sep 13, 2025: So Cal Blues v Phoenix Rising (OC Great Park)",
        "- Sep 13, 2025: Rebels SC v LV Heat Surf (Southwestern College)",
        "- Sep 13, 2025: LAFC So Cal v LA Breakers FC (Oak Park High School)",
        "- Sep 13, 2025: Pateadores v Slammers FC HB Koge (Great Park)",
        "- Sep 13, 2025: Eagles SC v Utah Royals FC-AZ (Pleasant Valley Fields)",
        "- Sep 14, 2025: So Cal Blues v Arizona Arsenal (OC Great Park)",
        "- Sep 14, 2025: San Diego Surf v LV Heat Surf (San Diego High Educational Complex)",
        "- Sep 14, 2025: Pateadores v Phoenix Rising (Great Park)",
        "- Sep 14, 2025: Beach FC (CA) v Utah Royals FC-AZ (El Camino College)",
        "- Sep 20, 2025: LA Breakers FC v Eagles SC (Bell Gardens Sports Center)",
        "- Sep 20, 2025: San Diego Surf v SLAMMERS FC (Surf Sports Park)",
        "- Sep 20, 2025: Legends FC San Diego v Rebels SC (Miramesa High School)",
        "- Sep 20, 2025: Slammers FC HB Koge v Legends FC (Saddleback College)",
        "- Sep 21, 2025: LAFC So Cal v Sporting CA USA (Oak Park High School)",
        "- Sep 27, 2025: San Diego Surf v Rebels SC (Surf Sports Park)",
        "- Sep 27, 2025: LA Breakers FC v SLAMMERS FC (Silverlakes)",
        "- Sep 27, 2025: LV Heat Surf v Arizona Arsenal (Heritage Park)",
        "- Sep 27, 2025: Legends FC San Diego v Sporting CA USA (Torrey Pines High School)",
        "- Sep 27, 2025: Eagles SC v LAFC So Cal (Pleasant Valley Fields)",
        "- Sep 27, 2025: So Cal Blues v Legends FC (OC Great Park)",
        "- Sep 27, 2025: Beach FC (CA) v Pateadores (El Camino College)",
        "- Sep 27, 2025: Utah Royals FC-AZ v Slammers FC HB Koge (Wild Horse Pass)",
        "- Oct 04, 2025: Utah Royals FC-AZ v LAFC So Cal (Scottsdale Sports Complex)",
        "- Oct 04, 2025: LV Heat Surf v Slammers FC HB Koge (Heritage Park)",
        "- Oct 04, 2025: Sporting CA USA v Beach FC (CA) (Silverlakes Soccer Complex)",
        "- Oct 04, 2025: Pateadores v LA Breakers FC (Great Park)",
        "- Oct 04, 2025: Arizona Arsenal v Legends FC (Copper Sky Recreation Complex)",
        "- Oct 04, 2025: Phoenix Rising v San Diego Surf (PRFC Youth Soccer Facility)",
        "- Oct 04, 2025: So Cal Blues v Eagles SC (OC Great Park)",
        "- Oct 04, 2025: SLAMMERS FC v Rebels SC (Arroyo Park)",
        "- Oct 05, 2025: Phoenix Rising v Legends FC (PRFC Youth Soccer Facility)",
        "- Oct 18, 2025: San Diego Surf v So Cal Blues (Surf Sports Park)",
        "- Oct 18, 2025: LAFC So Cal v Phoenix Rising (Oak Park High School)",
        "- Oct 18, 2025: Sporting CA USA v Utah Royals FC-AZ (Silverlakes Soccer Complex)",
        "- Oct 18, 2025: Slammers FC HB Koge v Arizona Arsenal (Silverlakes Complex)",
        "- Oct 18, 2025: SLAMMERS FC v Beach FC (Arroyo Park)",
        "- Oct 18, 2025: Legends FC v LV Heat Surf (Silverlakes Complex)",
        "- Oct 18, 2025: Rebels SC v LA Breakers FC (Monte Vista High School)",
        "- Oct 19, 2025: Beach FC (CA) v Arizona Arsenal (El Camino College)",
        "- Oct 19, 2025: San Diego Surf v Utah Royals FC-AZ (Surf Sports Park)",
        "- Oct 19, 2025: LA Breakers FC v LV Heat Surf (Bell Gardens Sports Center)",
        "- Oct 19, 2025: Rebels SC v So Cal Blues (Monte Vista High School)",
        "- Oct 19, 2025: Eagles SC v Phoenix Rising (Pleasant Valley Fields)",
        "- Oct 25, 2025: Phoenix Rising v SLAMMERS FC (PRFC Youth Soccer Facility)",
        "- Oct 25, 2025: Utah Royals FC-AZ v Legends FC San Diego (Bell Road Sports Complex)",
        "- Oct 25, 2025: Beach FC (CA) v So Cal Blues (Long Beach City College)",
        "- Oct 25, 2025: Arizona Arsenal v Eagles SC (Santos Soccer Complex)",
        "- Oct 25, 2025: Legends FC v LA Breakers FC (Silverlakes Complex)",
        "- Oct 25, 2025: Pateadores v San Diego Surf (Great Park)",
        "- Oct 25, 2025: Sporting CA USA v Slammers FC HB Koge (Silverlakes Soccer Complex)",
        "- Oct 26, 2025: LV Heat Surf v LAFC So Cal (Heritage Park)",
        "- Oct 26, 2025: Arizona Arsenal v Legends FC San Diego (Copper Sky Recreation Complex)",
        "- Oct 26, 2025: Utah Royals FC-AZ v SLAMMERS FC (Bell Road Sports Complex)",
        "- Nov 01, 2025: LA Breakers FC v Beach FC (CA) (Bell Gardens Sports Center)",
        "- Nov 01, 2025: Legends FC v LAFC So Cal (Silverlakes Complex)",
        "- Nov 01, 2025: Rebels SC v Sporting CA USA (Monte Vista High School)",
        "- Nov 01, 2025: Legends FC San Diego v Phoenix Rising (Canyon Crest Academy)",
        "- Nov 01, 2025: Slammers FC HB Koge v So Cal Blues (Silverlakes Complex)",
        "- Nov 02, 2025: Sporting CA USA v SLAMMERS FC (Silverlakes Soccer Complex)",
        "- Nov 05, 2025: Arizona Arsenal v Utah Royals FC-AZ (Arizona Athletic Grounds)",
        "- Nov 08, 2025: LAFC So Cal v Legends FC San Diego (Oak Park High School)",
        "- Nov 08, 2025: Legends FC v Pateadores (Silverlakes Complex)",
        "- Nov 08, 2025: Slammers FC HB Koge v Rebels SC (Arroyo Park)",
        "- Nov 09, 2025: Phoenix Rising v Arizona Arsenal (PRFC Youth Soccer Facility)",
        "- Nov 09, 2025: Sporting CA USA v San Diego Surf (Silverlakes Soccer Complex)",
        "- Nov 09, 2025: SLAMMERS FC v Eagles SC (Arroyo Park)",
        "- Nov 22, 2025: Slammers FC HB Koge v Legends FC San Diego (Saddleback College)",
        "- Mar 21, 2026: LAFC So Cal v Arizona Arsenal (-)",
        "- Mar 21, 2026: Beach FC (CA) v Legends FC San Diego (-)",
        "- Mar 21, 2026: Sporting CA USA v LV Heat Surf (-)",
        "- Mar 21, 2026: So Cal Blues v Pateadores (-)",
        "- Mar 21, 2026: Slammers FC HB Koge v Phoenix Rising (-)",
        "- Mar 21, 2026: Eagles SC v Rebels SC (-)",
        "- Mar 21, 2026: LA Breakers FC v San Diego Surf (-)",
        "- Mar 21, 2026: Legends FC v Utah Royals FC-AZ (-)",
        "- Mar 22, 2026: SLAMMERS FC v Arizona Arsenal (-)",
        "- Mar 22, 2026: Beach FC (CA) v LAFC So Cal (-)",
        "- Mar 22, 2026: Sporting CA USA v Eagles SC (-)",
        "- Mar 22, 2026: Pateadores v LV Heat Surf (-)",
        "- Mar 22, 2026: Rebels SC v Phoenix Rising (-)",
        "- Mar 22, 2026: Legends FC San Diego v So Cal Blues (-)",
        "- Mar 22, 2026: LA Breakers FC v Utah Royals FC-AZ (-)",
        "- Mar 22, 2026: San Diego Surf v Slammers FC HB Koge (Surf Sports Park)",
        "- Apr 11, 2026: Eagles SC v Beach FC (CA) (-)",
        "- Apr 11, 2026: Rebels SC v LAFC So Cal (-)",
        "- Apr 11, 2026: SLAMMERS FC v LV Heat Surf (-)",
        "- Apr 11, 2026: Pateadores v Sporting CA USA (Great Park)",
        "- Apr 11, 2026: Legends FC San Diego v San Diego Surf (Miramesa High School)",
        "- Apr 12, 2026: Legends FC San Diego v Eagles SC (Miramesa High School)",
        "- Apr 18, 2026: LAFC So Cal v Pateadores (-)",
        "- Apr 18, 2026: Eagles SC v San Diego Surf (-)",
        "- Apr 18, 2026: LV Heat Surf v So Cal Blues (-)",
        "- Apr 18, 2026: Legends FC v Legends FC San Diego (Silverlakes Complex)",
        "- Apr 19, 2026: Pateadores v SLAMMERS FC (-)",
        "- Apr 25, 2026: Slammers FC HB Koge v LA Breakers FC (-)",
        "- Apr 25, 2026: So Cal Blues v LAFC So Cal (-)",
        "- Apr 25, 2026: Phoenix Rising v LV Heat Surf (-)",
        "- Apr 25, 2026: Arizona Arsenal v Rebels SC (-)",
        "- Apr 25, 2026: Beach FC (CA) v San Diego Surf (-)",
        "- Apr 25, 2026: Legends FC v Sporting CA USA (Silverlakes Complex)",
        "- Apr 25, 2026: Slammers FC HB Koge v SLAMMERS FC (Saddleback College)",
        "- Apr 25, 2026: Utah Royals FC-AZ v Pateadores (Wild Horse Pass)",
        "- Apr 26, 2026: Arizona Arsenal v Pateadores (-)",
        "- Apr 26, 2026: Utah Royals FC-AZ v Rebels SC (-)",
        "- May 02, 2026: Rebels SC v Beach FC (CA) (-)",
        "- May 02, 2026: Pateadores v Eagles SC (-)",
        "- May 02, 2026: Phoenix Rising v LA Breakers FC (-)",
        "- May 02, 2026: SLAMMERS FC v Legends FC (-)",
        "- May 02, 2026: LV Heat Surf v Legends FC San Diego (-)",
        "- May 02, 2026: LAFC So Cal v Slammers FC HB Koge (-)",
        "- May 02, 2026: Utah Royals FC-AZ v So Cal Blues (-)",
        "- May 02, 2026: Arizona Arsenal v Sporting CA USA (-)",
        "- May 03, 2026: Arizona Arsenal v LA Breakers FC (-)",
        "- May 03, 2026: Phoenix Rising v Sporting CA USA (-)",
        "- May 09, 2026: LV Heat Surf v Eagles SC (-)",
        "- May 09, 2026: LA Breakers FC v Legends FC San Diego (-)",
        "- May 09, 2026: Rebels SC v Pateadores (-)",
        "- May 09, 2026: Beach FC (CA) v Slammers FC HB Koge (-)",
        "- May 09, 2026: So Cal Blues v Sporting CA USA (-)",
        "- May 09, 2026: San Diego Surf v Legends FC (Surf Sports Park)",
        "- May 09, 2026: Utah Royals FC-AZ v Phoenix Rising (REATA - Field 21)",
        "- May 09, 2026: SLAMMERS FC v LAFC So Cal (Saddleback College)",
        "- May 16, 2026: LV Heat Surf v Beach FC (CA) (-)",
        "- May 16, 2026: Eagles SC v Legends FC (-)",
        "- May 16, 2026: SLAMMERS FC v Legends FC San Diego (-)",
        "- May 16, 2026: LA Breakers FC v So Cal Blues (-)",
    ]

    texasSched = [
        "Aug 24, 2025: Real Colorado Athletico v Colorado Rapids (Real Colorado Soccer Complex)",
        "Aug 24, 2025: Colorado Rush Academy Blue v Real Colorado National (Colorado Academy)",
        "Aug 30, 2025: Real Colorado Athletico v Albion Hurricanes FC (Real Colorado Soccer Complex)",
        "Aug 30, 2025: Colorado Rush Academy Blue v Challenge SC (Colorado Academy)",
        "Aug 31, 2025: Real Colorado Athletico v Challenge SC (Real Colorado Soccer Complex)",
        "Aug 31, 2025: Colorado Rush Academy Blue v Albion Hurricanes FC (Colorado Academy)",
        "Sep 06, 2025: Classics Elite v West Side Alliance (CE Soccer Complex)",
        "Sep 06, 2025: Sting Austin v OK Energy FC (Round Rock Multipurpose Complex)",
        "Sep 07, 2025: Classics Elite v OK Energy FC (CE Soccer Complex)",
        "Sep 07, 2025: Sting Austin v West Side Alliance (Round Rock Multipurpose Complex)",
        "Sep 13, 2025: DKSC v Dallas Texans (Cox Soccer Complex)",
        "Sep 13, 2025: Sting Royal v Sting Black (Rolling Hills Soccer Complex)",
        "Sep 14, 2025: Real Colorado Athletico v Real Colorado National (Real Colorado Soccer Complex)",
        "Sep 20, 2025: Sting Black v Dallas Texans (Memorial High School)",
        "Sep 20, 2025: OK Energy FC v FC Dallas (Edmond Soccer Club)",
        "Sep 20, 2025: Challenge SC v Colorado Rapids (Burroughs Park)",
        "Sep 20, 2025: Albion Hurricanes FC v Real Colorado National (Campbell Road Sports Park)",
        "Sep 20, 2025: DKSC v SOLAR SC (Beacon Park)",
        "Sep 20, 2025: Colorado Rush Academy Blue v Sting Austin (Stargate)",
        "Sep 20, 2025: Real Colorado Athletico v Classics Elite (Real Colorado Soccer Complex)",
        "Sep 21, 2025: Real Colorado Athletico v Sting Austin (Real Colorado Soccer Complex)",
        "Sep 21, 2025: Challenge SC v Real Colorado National (Burroughs Park)",
        "Sep 21, 2025: Albion Hurricanes FC v Colorado Rapids (Campbell Road Sports Park)",
        "Sep 21, 2025: Colorado Rush Academy Blue v Classics Elite (Aurora Sports Park)",
        "Sep 27, 2025: West Side Alliance v FC Dallas (RiverCity Parks)",
        "Sep 27, 2025: Real Colorado National v Dallas Texans (Real Colorado Soccer Complex)",
        "Sep 27, 2025: OK Energy FC v Sting Royal (North Oklahoma City FC)",
        "Sep 27, 2025: Colorado Rapids v SOLAR SC (Regis University)",
        "Sep 28, 2025: West Side Alliance v Sting Royal (RiverCity Parks)",
        "Sep 28, 2025: Colorado Rapids v Dallas Texans (Regis University)",
        "Sep 28, 2025: Real Colorado National v SOLAR SC (Real Colorado Soccer Complex)",
        "Oct 04, 2025: Colorado Rapids v Sting Royal (Regis University)",
        "Oct 04, 2025: Real Colorado National v FC Dallas (Real Colorado Soccer Complex)",
        "Oct 04, 2025: Albion Hurricanes FC v Sting Black (Campbell Road Sports Park)",
        "Oct 04, 2025: Challenge SC v DKSC (Burroughs Park)",
        "Oct 05, 2025: Real Colorado National v Sting Royal (Real Colorado Soccer Complex)",
        "Oct 05, 2025: SOLAR SC v Dallas Texans (OAK GROVE)",
        "Oct 05, 2025: Albion Hurricanes FC v DKSC (Campbell Road Sports Park)",
        "Oct 05, 2025: Challenge SC v Sting Black (Burroughs Park)",
        "Oct 05, 2025: Colorado Rapids v FC Dallas (Colorado School of Mines)"
        "Oct 11, 2025: West Side Alliance v Dallas Texans (RiverCity Parks)",
        "Oct 18, 2025: DKSC v Colorado Rapids (Beacon Park)",
        "Oct 18, 2025: Sting Black v Real Colorado National (Memorial High School)",
        "Oct 18, 2025: West Side Alliance v Albion Hurricanes FC (RiverCity Parks)",
        "Oct 18, 2025: OK Energy FC v Challenge SC (North Oklahoma City FC)",
        "Oct 18, 2025: Sting Austin v Dallas Texans (Round Rock Multipurpose Complex)",
        "Oct 18, 2025: Classics Elite v SOLAR SC (CE Soccer Complex)",
        "Oct 19, 2025: Sting Black v Colorado Rapids (Memorial High School)",
        "Oct 19, 2025: Real Colorado Athletico v Colorado Rush Academy Blue (Highland Heritage Regional Park)",
        "Oct 19, 2025: OK Energy FC v Albion Hurricanes FC (North Oklahoma City FC)",
        "Oct 19, 2025: Sting Royal v FC Dallas (Tidwell Middle School)",
        "Oct 19, 2025: DKSC v Real Colorado National (Beacon Park)",
        "Oct 19, 2025: West Side Alliance v Challenge SC (RiverCity Parks)",
        "Oct 19, 2025: Classics Elite v Dallas Texans (CE Soccer Complex)",
        "Oct 19, 2025: Sting Austin v SOLAR SC (Round Rock Multipurpose Complex)",
        "Oct 25, 2025: Sting Black v West Side Alliance (Memorial High School)",
        "Oct 25, 2025: FC Dallas v Colorado Rush Academy Blue (Lovejoy Stadium)",
        "Oct 25, 2025: Sting Royal v Real Colorado Athletico (Gene Pike Middle School)",
        "Oct 25, 2025: DKSC v OK Energy FC (Beacon Park)",
        "Oct 26, 2025: FC Dallas v Real Colorado Athletico (Toyota Soccer Center)",
        "Oct 26, 2025: Sting Black v OK Energy FC (Memorial High School)",
        "Oct 26, 2025: DKSC v West Side Alliance (Beacon Park)",
        "Oct 26, 2025: Sting Royal v Colorado Rush Academy Blue (Medlin Middle School)",
        "Oct 26, 2025: Sting Austin v Classics Elite (Leander High School Bible Memorial Stadium)",
        "Nov 08, 2025: Sting Royal v Classics Elite (Boswell High School)",
        "Nov 08, 2025: FC Dallas v Sting Austin (Toyota Soccer Center)",
        "Nov 08, 2025: SOLAR SC v Colorado Rush Academy Blue (OAK GROVE)",
        "Nov 08, 2025: Dallas Texans v Real Colorado Athletico (Nolan Catholic School)",
        "Nov 08, 2025: Colorado Rapids v Real Colorado National (Regis University)",
        "Nov 09, 2025: FC Dallas v Classics Elite (Toyota Soccer Center)",
        "Nov 09, 2025: Sting Royal v Sting Austin (Boswell High School)",
        "Nov 09, 2025: SOLAR SC v Real Colorado Athletico (OAK GROVE)",
        "Nov 09, 2025: Dallas Texans v Colorado Rush Academy Blue (Arlington Heights High School)",
        "Nov 09, 2025: West Side Alliance v OK Energy FC (RiverCity Parks)",
        "Nov 22, 2025: Sting Austin v Colorado Rapids (Cedar Ridge High School)",
        "Nov 22, 2025: FC Dallas v Albion Hurricanes FC (Toyota Soccer Center)",
        "Nov 22, 2025: Sting Royal v Challenge SC (Boswell High School)",
        "Nov 22, 2025: Colorado Rush Academy Blue v Sting Black (Stargate)",
        "Nov 22, 2025: Real Colorado Athletico v DKSC (Real Colorado Soccer Complex)",
        "Nov 22, 2025: Classics Elite v Real Colorado National (CE Soccer Complex)",
        "Nov 22, 2025: OK Energy FC v Dallas Texans (North Oklahoma City FC)",
        "Nov 23, 2025: Real Colorado Athletico v Sting Black (Real Colorado Soccer Complex)",
        "Nov 23, 2025: Classics Elite v Colorado Rapids (CE Soccer Complex)",
        "Nov 23, 2025: Sting Austin v Real Colorado National (Cedar Ridge High School)",
        "Nov 23, 2025: Sting Royal v Albion Hurricanes FC (Boswell High School)",
        "Nov 23, 2025: FC Dallas v Challenge SC (Toyota Soccer Center)",
        "Nov 23, 2025: Colorado Rush Academy Blue v DKSC (Stargate)",
        "Nov 30, 2025: SOLAR SC v Sting Black (OAK GROVE)",
        "Dec 13, 2025: Albion Hurricanes FC v Challenge SC (Campbell Road Sports Park)",
        "Dec 13, 2025: SOLAR SC v West Side Alliance (Carroll Senior High School)",
        "Jan 31, 2026: Colorado Rapids v OK Energy FC (Regis University)",
        "Jan 31, 2026: Real Colorado National v West Side Alliance (Real Colorado Soccer Complex)",
        "Feb 01, 2026: Real Colorado National v OK Energy FC (Real Colorado Soccer Complex)",
        "Feb 01, 2026: Colorado Rapids v West Side Alliance (Regis University)",
        "Feb 07, 2026: West Side Alliance v Colorado Rush Academy Blue (RiverCity Parks)",
        "Feb 07, 2026: OK Energy FC v Real Colorado Athletico (North Oklahoma City FC)",
        "Feb 08, 2026: West Side Alliance v Real Colorado Athletico (RiverCity Parks)",
        "Feb 08, 2026: OK Energy FC v Colorado Rush Academy Blue (North Oklahoma City FC)",
        "Feb 21, 2026: Colorado Rush Academy Blue v Colorado Rapids (Stargate)",
        "Apr 18, 2026: Sting Royal v DKSC",
        "Apr 18, 2026: FC Dallas v Sting Black (Toyota Soccer Center)",
        "Apr 18, 2026: SOLAR SC v OK Energy FC (OAK GROVE)",
        "Apr 19, 2026: Albion Hurricanes FC v Classics Elite",
        "Apr 19, 2026: Challenge SC v Sting Austin",
        "Apr 25, 2026: SOLAR SC v Albion Hurricanes FC",
        "Apr 25, 2026: Dallas Texans v Challenge SC (Ross Stewart Soccer Complex)",
        "Apr 26, 2026: FC Dallas v DKSC (Toyota Soccer Center)",
        "Apr 26, 2026: Dallas Texans v Albion Hurricanes FC (Ross Stewart Soccer Complex)",
        "Apr 26, 2026: SOLAR SC v Challenge SC (OAK GROVE)",
        "May 02, 2026: Sting Black v Sting Austin",
        "May 02, 2026: Dallas Texans v FC Dallas (Ross Stewart Soccer Complex)",
        "May 02, 2026: SOLAR SC v Sting Royal (OAK GROVE)",
        "May 02, 2026: DKSC v Classics Elite (Cox Soccer Complex)",
        "May 03, 2026: Sting Black v Classics Elite",
        "May 03, 2026: DKSC v Sting Austin (Cox Soccer Complex)",
        "May 09, 2026: Albion Hurricanes FC v Sting Austin",
        "May 09, 2026: SOLAR SC v FC Dallas",
        "May 09, 2026: DKSC v Sting Black (Cox Soccer Complex)",
        "May 09, 2026: Dallas Texans v Sting Royal (Ross Stewart Soccer Complex)",
        "May 10, 2026: Challenge SC v Classics Elite"
    ]

    # ECNL RL

    rlConf = [
        "ECNL RL Girls Florida",
        "ECNL RL Girls Golden State",
        "ECNL RL Girls NorCal",
        "ECNL RL Girls Southern Cal",
        "ECNL RL Girls Mid-America",
        "ECNL RL Girls Mountain",
        "ECNL RL Girls Greater Michigan Alliance",
        "ECNL RL Girls Northwest"
    ]

    rlFLSouClubs = [
        "Cape Coral SA",
        "FC Prime",
        "FC Prime Miami",
        "FHFC",
        "Florida West FC",
        "SFFA",
        "Sunrise Surf",
        "SWFL Premier FC",
        "Team Boca Soccer",
    ]

    rlFLSouSched = [
        "- Sep 06, 2025: Sunrise Surf v FC Prime Miami (Nob Hill Soccer Park)",
        "- Sep 06, 2025: SFFA v SWFL Premier FC (Canyon District Park)",
        "- Sep 06, 2025: Team Boca Soccer v Cape Coral SA (Fau Glades)",
        "- Sep 07, 2025: SFFA v FHFC (Canyon District Park)",
        "- Sep 14, 2025: Sunrise Surf v SFFA (Nob Hill Soccer Park)",
        "- Sep 20, 2025: Florida West FC v SFFA (Jim Jeffers)",
        "- Sep 20, 2025: FC Prime v FC Prime Miami (Miami Dade College Kendall Campus)",
        "- Sep 21, 2025: Cape Coral SA v SFFA (Cape Coral Sports Complex)",
        "- Sep 27, 2025: FC Prime v Cape Coral SA (Mullins Park)",
        "- Sep 27, 2025: SWFL Premier FC v Team Boca Soccer (Lakewood Ranch Park)",
        "- Sep 27, 2025: FC Prime Miami v Florida West FC (Miami Dade College)",
        "- Sep 27, 2025: FHFC v Sunrise Surf (Fishhawk Sports Complex)",
        "- Sep 28, 2025: FHFC v Team Boca Soccer (Fishhawk Sports Complex)",
        "- Sep 28, 2025: FC Prime Miami v Cape Coral SA (Tamarac Sports Complex)",
        "- Sep 28, 2025: SWFL Premier FC v Sunrise Surf (Lakewood Ranch Park)",
        "- Sep 28, 2025: FC Prime v Florida West FC (Mullins Park)",
        "- Oct 04, 2025: FC Prime Miami v SFFA (Miami Dade College)",
        "- Oct 05, 2025: SWFL Premier FC v FHFC (Lakewood Ranch Park)",
        "- Oct 05, 2025: FC Prime Miami v Team Boca Soccer (Tamarac Sports Complex)",
        "- Oct 11, 2025: Team Boca Soccer v Florida West FC (SPANISH RIVER SPORTS COMPLEX)",
        "- Oct 11, 2025: FC Prime Miami v FHFC (Miami Dade College)",
        "- Oct 12, 2025: FC Prime v FHFC (Mullins Park)",
        "- Oct 18, 2025: FC Prime v Team Boca Soccer (Mullins Park)",
        "- Oct 18, 2025: FHFC v Florida West FC (Fishhawk Sports Complex)",
        "- Oct 18, 2025: SFFA v Sunrise Surf (Canyon District Park)",
        "- Oct 18, 2025: SWFL Premier FC v Cape Coral SA (Lakewood Ranch Park)",
        "- Oct 19, 2025: FHFC v Cape Coral SA (Fishhawk Sports Complex)",
        "- Oct 19, 2025: Team Boca Soccer v SFFA (Fau Glades)",
        "- Oct 19, 2025: SWFL Premier FC v Florida West FC (Lakewood Ranch Park)",
        "- Oct 25, 2025: Florida West FC v FC Prime (JetBlue Park)",
        "- Oct 25, 2025: FHFC v SFFA (Fishhawk Sports Complex)",
        "- Oct 25, 2025: Sunrise Surf v Team Boca Soccer (Nob Hill Soccer Park)",
        "- Oct 25, 2025: Cape Coral SA v FC Prime Miami (Pelican Soccer Complex)",
        "- Oct 26, 2025: SWFL Premier FC v SFFA (Lakewood Ranch Park)",
        "- Oct 26, 2025: Florida West FC v FC Prime Miami (JetBlue Park)",
        "- Oct 26, 2025: Cape Coral SA v FC Prime (Cape Coral Sports Complex)",
        "- Nov 01, 2025: Sunrise Surf v Florida West FC (Nob Hill Soccer Park)",
        "- Nov 01, 2025: Team Boca Soccer v FC Prime (Fau Glades)",
        "- Nov 01, 2025: SFFA v Cape Coral SA (Canyon District Park)",
        "- Nov 02, 2025: Sunrise Surf v Cape Coral SA (Mullins Park)",
        "- Nov 02, 2025: SFFA v Florida West FC (Canyon District Park)",
        "- Nov 08, 2025: Florida West FC v Cape Coral SA (JetBlue Park)",
        "- Nov 08, 2025: SFFA v FC Prime Miami (Canyon District Park)",
        "- Nov 09, 2025: FC Prime v SFFA (Mullins Park)",
        "- Feb 21, 2026: Team Boca Soccer v FC Prime Miami (FAU GAME FIELD)",
        "- Feb 21, 2026: FC Prime Miami v FC Prime (Miami Dade College)",
        "- Feb 22, 2026: FHFC v SWFL Premier FC (Fishhawk Sports Complex)",
        "- Feb 22, 2026: FC Prime v Sunrise Surf (Mullins Park)",
        "- Feb 28, 2026: FC Prime Miami v SWFL Premier FC (Miami Dade College)",
        "- Mar 01, 2026: FC Prime v SWFL Premier FC (Mullins Park)",
        "- Mar 07, 2026: Florida West FC v Sunrise Surf (Big Corkscrew Island Regional Park)",
        "- Mar 07, 2026: FHFC v FC Prime (Fishhawk Sports Complex)",
        "- Mar 07, 2026: Cape Coral SA v Team Boca Soccer (Pelican Soccer Complex)",
        "- Mar 07, 2026: SWFL Premier FC v FC Prime Miami (Lakewood Ranch Park)",
        "- Mar 08, 2026: FHFC v FC Prime Miami (Fishhawk Sports Complex)",
        "- Mar 08, 2026: SWFL Premier FC v FC Prime (Lakewood Ranch Park)",
        "- Mar 08, 2026: Florida West FC v Team Boca Soccer (Big Corkscrew Island Regional Park)",
        "- Mar 08, 2026: Cape Coral SA v Sunrise Surf (Cape Coral Sports Complex)",
        "- Mar 14, 2026: FC Prime Miami v Sunrise Surf (Miami Dade College)",
        "- Mar 28, 2026: Sunrise Surf v SWFL Premier FC (Nob Hill Soccer Park)",
        "- Mar 28, 2026: Team Boca Soccer v FHFC (Fau Glades)",
        "- Mar 29, 2026: Sunrise Surf v FHFC (Nob Hill Soccer Park)",
        "- Mar 29, 2026: Cape Coral SA v Florida West FC (Cape Coral Sports Complex)",
        "- Mar 29, 2026: Team Boca Soccer v SWFL Premier FC (Fau Glades)",
        "- Mar 29, 2026: SFFA v FC Prime (Canyon District Park)",
        "- Apr 11, 2026: Florida West FC v SWFL Premier FC (Big Corkscrew Island Regional Park)",
        "- Apr 11, 2026: Team Boca Soccer v Sunrise Surf (Fau Glades)",
        "- Apr 11, 2026: Cape Coral SA v FHFC (Pelican Soccer Complex)",
        "- Apr 12, 2026: Florida West FC v FHFC (Big Corkscrew Island Regional Park)",
        "- Apr 12, 2026: SFFA v Team Boca Soccer (Canyon District Park)",
        "- Apr 12, 2026: Cape Coral SA v SWFL Premier FC (Cape Coral Sports Complex)",
        "- Apr 12, 2026: Sunrise Surf v FC Prime (Nob Hill Soccer Park)"
    ]

    rlFLNorClubs = [
        "FL Premier FC",
        "Florida Krush",
        "Jacksonville FC",
        "Orlando City",
        "Sporting Club Tallahassee",
        "Sporting Jax",
        "St. Petersburg FC",
        "Tampa Bay United",
        "West Florida Flames",
    ]

    rlFLNorSched = [
        "- Sep 06, 2025: Jacksonville FC v St. Petersburg FC (Patton Park)",
        "- Sep 06, 2025: Orlando City v Sporting Club Tallahassee (Seminole)",
        "- Sep 06, 2025: Sporting Jax v Tampa Bay United (Losco Park)",
        "- Sep 07, 2025: Jacksonville FC v Tampa Bay United (Patton Park)",
        "- Sep 07, 2025: Florida Krush v Sporting Club Tallahassee (Shane Kelly Park)",
        "- Sep 07, 2025: Sporting Jax v St. Petersburg FC (Veterans Park)",
        "- Sep 13, 2025: Tampa Bay United v FL Premier FC (Ed Radice Sports Complex)",
        "- Sep 13, 2025: Sporting Club Tallahassee v Sporting Jax (Florida State University Rec SportsPlex)",
        "- Sep 13, 2025: West Florida Flames v Florida Krush (East Lake Meadows Sports Complex)",
        "- Sep 14, 2025: Sporting Club Tallahassee v Jacksonville FC (Florida State University Rec SportsPlex)",
        "- Sep 14, 2025: St. Petersburg FC v Tampa Bay United (Sawgrass Lake Complex)",
        "- Sep 14, 2025: FL Premier FC v Florida Krush (Starkey Ranch District Park)",
        "- Sep 20, 2025: West Florida Flames v Jacksonville FC (East Lake Meadows Sports Complex)",
        "- Sep 20, 2025: Florida Krush v Tampa Bay United (Shane Kelly Park)",
        "- Sep 20, 2025: FL Premier FC v Sporting Jax (Wiregrass Ranch Sports Campus)",
        "- Sep 20, 2025: Orlando City v St. Petersburg FC (Seminole)",
        "- Sep 21, 2025: FL Premier FC v Jacksonville FC (Wiregrass Ranch Sports Campus)",
        "- Sep 21, 2025: Orlando City v Tampa Bay United (Seminole)",
        "- Sep 21, 2025: Florida Krush v St. Petersburg FC (Shane Kelly Park)",
        "- Sep 21, 2025: West Florida Flames v Sporting Jax (East Lake Meadows Sports Complex)",
        "- Sep 26, 2025: Tampa Bay United v West Florida Flames (Ed Radice Sports Complex)",
        "- Sep 27, 2025: Sporting Club Tallahassee v Florida Krush (Florida State University Rec SportsPlex)",
        "- Sep 28, 2025: Tampa Bay United v St. Petersburg FC (Wesley Chapel District Park)",
        "- Sep 28, 2025: Sporting Club Tallahassee v Orlando City (Florida State University Rec SportsPlex)",
        "- Oct 04, 2025: Sporting Jax v Jacksonville FC (Veterans Park)",
        "- Oct 04, 2025: West Florida Flames v Orlando City (East Lake Meadows Sports Complex)",
        "- Oct 04, 2025: FL Premier FC v Sporting Club Tallahassee (Starkey Ranch District Park)",
        "- Oct 05, 2025: West Florida Flames v Sporting Club Tallahassee (East Lake Meadows Sports Complex)",
        "- Oct 05, 2025: FL Premier FC v Orlando City (Starkey Ranch District Park)",
        "- Oct 12, 2025: Sporting Club Tallahassee v FL Premier FC (Florida State University Rec SportsPlex)",
        "- Oct 18, 2025: Orlando City v West Florida Flames (Seminole)",
        "- Oct 18, 2025: St. Petersburg FC v Sporting Jax (Sawgrass Lake Complex)",
        "- Oct 18, 2025: Florida Krush v FL Premier FC (Shane Kelly Park)",
        "- Oct 18, 2025: Tampa Bay United v Jacksonville FC (Ed Radice Sports Complex)",
        "- Oct 19, 2025: Florida Krush v West Florida Flames (Shane Kelly Park)",
        "- Oct 19, 2025: St. Petersburg FC v Jacksonville FC (Sawgrass Lake Complex)",
        "- Oct 19, 2025: Orlando City v FL Premier FC (Seminole)",
        "- Oct 19, 2025: Tampa Bay United v Sporting Jax (Ed Radice Sports Complex)",
        "- Oct 25, 2025: Jacksonville FC v Florida Krush (Patton Park)",
        "- Oct 25, 2025: FL Premier FC v West Florida Flames (Starkey Ranch District Park)",
        "- Oct 25, 2025: Sporting Club Tallahassee v Tampa Bay United (Florida State University Rec SportsPlex)",
        "- Oct 26, 2025: Sporting Club Tallahassee v St. Petersburg FC (Florida State University Rec SportsPlex)",
        "- Oct 26, 2025: Sporting Jax v Florida Krush (Veterans Park)",
        "- Nov 01, 2025: Jacksonville FC v Orlando City (Patton Park)",
        "- Nov 02, 2025: St. Petersburg FC v FL Premier FC (Sawgrass Lake Complex)",
        "- Nov 02, 2025: Sporting Jax v Orlando City (Veterans Park)",
        "- Nov 02, 2025: Sporting Club Tallahassee v West Florida Flames (Florida State University Rec SportsPlex)",
        "- Nov 08, 2025: St. Petersburg FC v West Florida Flames (Sawgrass Lake Complex)",
        "- Mar 07, 2026: Orlando City v Jacksonville FC (Seminole)",
        "- Mar 07, 2026: Tampa Bay United v Sporting Club Tallahassee (Ed Radice Sports Complex)",
        "- Mar 07, 2026: Florida Krush v Sporting Jax (Central Winds)",
        "- Mar 08, 2026: St. Petersburg FC v Sporting Club Tallahassee (Sawgrass Lake Complex)",
        "- Mar 08, 2026: Orlando City v Sporting Jax (Seminole)",
        "- Mar 08, 2026: Florida Krush v Jacksonville FC (Shane Kelly Park)",
        "- Mar 13, 2026: Florida Krush v Orlando City (Central Winds)",
        "- Mar 28, 2026: St. Petersburg FC v Florida Krush (Sawgrass Lake Complex)",
        "- Mar 28, 2026: Jacksonville FC v FL Premier FC (Patton Park)",
        "- Mar 28, 2026: Sporting Jax v West Florida Flames (Losco Park)",
        "- Mar 29, 2026: Jacksonville FC v West Florida Flames (Patton Park)",
        "- Mar 29, 2026: Sporting Jax v FL Premier FC (Veterans Park)",
        "- Mar 29, 2026: Tampa Bay United v Florida Krush (Ed Radice Sports Complex)",
        "- Apr 11, 2026: Orlando City v Florida Krush (Seminole)",
        "- Apr 11, 2026: FL Premier FC v St. Petersburg FC (ZEPH-SAM PASCO PARK)",
        "- Apr 11, 2026: Jacksonville FC v Sporting Club Tallahassee (Patton Park)",
        "- Apr 11, 2026: West Florida Flames v Tampa Bay United (East Lake Meadows Sports Complex)",
        "- Apr 12, 2026: FL Premier FC v Tampa Bay United (ZEPH-SAM PASCO PARK)",
        "- Apr 12, 2026: West Florida Flames v St. Petersburg FC (East Lake Meadows Sports Complex)",
        "- Apr 12, 2026: Sporting Jax v Sporting Club Tallahassee (Losco Park)",
        "- Apr 18, 2026: West Florida Flames v FL Premier FC (East Lake Meadows Sports Complex)",
        "- Apr 18, 2026: Jacksonville FC v Sporting Jax (Patton Park)",
        "- Apr 18, 2026: Tampa Bay United v Orlando City (Ed Radice Sports Complex)",
        "- Apr 19, 2026: St. Petersburg FC v Orlando City (Sawgrass Lake Complex)"
    ]

    rlNWClubs=[
        "3RSC",
        "Central Washington",
        "Eastside FC",
        "Eastside TImbers",
        "Northwest United FC",
        "Oregon Surf",
        "PaxNW SC",
        "Portland Thorns",
        "Seattle United",
        "Snohomish United",
        "Washington Premier",
        "XF",
    ]

    rlNWSched = [
        "- Aug 01, 2025: PacNW SC v Eastside FC (Washington Premier FC Sports Complex)",
        "- Aug 01, 2025: Portland Thorns v Washington Premier (Washington Premier FC Sports Complex)",
        "- Aug 02, 2025: Eastside FC v Portland Thorns (Washington Premier FC Sports Complex)",
        "- Aug 02, 2025: Washington Premier v 3RSC (Washington Premier FC Sports Complex)",
        "- Aug 03, 2025: Portland Thorns v PacNW SC (Washington Premier FC Sports Complex)",
        "- Aug 03, 2025: 3RSC v Eastside FC (Washington Premier FC Sports Complex)",
        "- Aug 09, 2025: Washington Premier v PacNW SC (WPFC Field Complex)",
        "- Dec 13, 2025: Seattle United v Washington Premier (Shoreline A/B fields)",
        "- Dec 13, 2025: Oregon Surf v 3RSC (THPRD Rec Center)",
        "- Dec 13, 2025: Portland Thorns v Central Washington (Tualatin High School)",
        "- Dec 13, 2025: XF v PacNW SC (Marymoor Park)",
        "- Dec 14, 2025: Snohomish United v XF (GrassLawn)",
        "- Dec 14, 2025: Portland Thorns v 3RSC (Tigard High School)",
        "- Jan 04, 2026: Northwest United FC v Seattle United (Skagit Valley College)",
        "- Jan 10, 2026: XF v Oregon Surf (Marymoor Park)",
        "- Jan 10, 2026: PacNW SC v Eastside Timbers (Saghalie Park)",
        "- Jan 10, 2026: Snohomish United v 3RSC (Lake Tye)",
        "- Jan 10, 2026: Seattle United v Portland Thorns (Genesee Park Playfield)",
        "- Jan 10, 2026: Eastside FC v Washington Premier (PRESTON PARK ATHLETIC FIELDS)",
        "- Jan 11, 2026: Washington Premier v Oregon Surf (WPFC Field Complex)",
        "- Jan 11, 2026: XF v Portland Thorns (Marymoor Park)",
        "- Jan 11, 2026: Northwest United FC v 3RSC (Mount Vernon High School)",
        "- Jan 16, 2026: Oregon Surf v PacNW SC (Valley Ridge Park)",
        "- Jan 17, 2026: Eastside Timbers v XF (Eastside Timbers Sports Complex)",
        "- Jan 17, 2026: Eastside FC v Seattle United (PRESTON PARK ATHLETIC FIELDS)",
        "- Jan 24, 2026: Central Washington v PacNW SC (Central Washington Recreation Sports Complex)",
        "- Jan 24, 2026: Oregon Surf v Snohomish United (Mountain View Champions Park)",
        "- Jan 24, 2026: Portland Thorns v Northwest United FC (Tigard High School)",
        "- Jan 24, 2026: Eastside Timbers v Seattle United (Eastside Timbers Sports Complex)",
        "- Jan 24, 2026: Eastside FC v XF (PRESTON PARK ATHLETIC FIELDS)",
        "- Jan 25, 2026: Eastside Timbers v Northwest United FC (Eastside Timbers Sports Complex)",
        "- Jan 31, 2026: Seattle United v Oregon Surf (Genesee Park Playfield)",
        "- Jan 31, 2026: 3RSC v Eastside Timbers (Niel F. Lampson Stadium)",
        "- Jan 31, 2026: PacNW SC v Snohomish United (Starfire Sports)",
        "- Jan 31, 2026: Northwest United FC v XF (Mount Vernon High School)",
        "- Feb 07, 2026: Seattle United v XF (Shoreline A/B fields)",
        "- Feb 07, 2026: Portland Thorns v Eastside Timbers (Tigard High School)",
        "- Feb 07, 2026: Snohomish United v Washington Premier (Lake Tye)",
        "- Feb 07, 2026: Eastside FC v Oregon Surf (Central Park)",
        "- Feb 07, 2026: PacNW SC v Northwest United FC (Renton Memorial Stadium)",
        "- Feb 21, 2026: XF v Washington Premier (Marymoor Park)",
        "- Feb 21, 2026: Oregon Surf v Northwest United FC (Conestoga Middle School)",
        "- Feb 22, 2026: Seattle United v PacNW SC (Shorewood High School)",
        "- Feb 22, 2026: Portland Thorns v Snohomish United (Tualatin High School)",
        "- Feb 22, 2026: Washington Premier v Eastside Timbers (WPFC Field Complex)",
        "- Feb 28, 2026: 3RSC v Central Washington (Southridge HS Stadium)",
        "- Feb 28, 2026: Eastside Timbers v Eastside FC (Eastside Timbers Sports Complex)",
        "- Mar 01, 2026: Snohomish United v Central Washington (Snohomish High School)",
        "- Mar 14, 2026: Oregon Surf v Portland Thorns",
        "- Mar 14, 2026: Snohomish United v Seattle United (Snohomish High School)",
        "- Mar 21, 2026: Oregon Surf v Eastside Timbers",
        "- Mar 21, 2026: 3RSC v XF",
        "- Mar 21, 2026: Central Washington v Seattle United (Chesterly Park)",
        "- Mar 21, 2026: Northwest United FC v Washington Premier (Skagit Valley College)",
        "- Mar 22, 2026: 3RSC v Seattle United",
        "- Mar 22, 2026: Central Washington v XF (Chesterly Park)",
        "- Mar 28, 2026: 3RSC v PacNW SC",
        "- Mar 28, 2026: Eastside FC v Northwest United FC (PRESTON PARK ATHLETIC FIELDS)",
        "- Mar 28, 2026: Central Washington v Washington Premier (Chesterly Park)",
        "- Mar 28, 2026: Eastside Timbers v Snohomish United (Eastside Timbers Sports Complex)",
        "- Apr 11, 2026: Oregon Surf v Central Washington (PCC Rock Creek)",
        "- Apr 18, 2026: Snohomish United v Northwest United FC (Snohomish High School)",
        "- Apr 18, 2026: Central Washington v Eastside Timbers (Chesterly Park)",
        "- Apr 18, 2026: Northwest United FC v Snohomish United (Skagit Valley College)",
        "- Apr 19, 2026: Central Washington v Eastside FC (Chesterly Park)",
        "- Apr 25, 2026: Snohomish United v Eastside FC (Snohomish High School)",
        "- Apr 25, 2026: Northwest United FC v Central Washington (Skagit Valley College)"
    ]

    rlMichClubs = [
        "Cap City Athletic 1847",
        "Detroit City FC West",
        "Legends FC Michigan",
        "Liverpool FC IA GMA",
        "Liverpool FC IA Michigan North Oakland",
        "Michigan Burn",
        "Michigan Rangers FC",
        "Nationals SC Cap Area",
        "Nationals SC Union",
        "Plymouth Reign SC",
        "Portage SC",
        "TKO Premier SC"
    ]

    rlMichSched = [
        "- Aug 23, 2025: Michigan Rangers FC v Cap City Athletic 1847 (Hamilton High School)",
        "- Aug 23, 2025: Nationals SC Cap Area v Legends FC Michigan (Hope Sports Complex)",
        "- Aug 24, 2025: Michigan Rangers FC v Legends FC Michigan (Hamilton High School)",
        "- Aug 24, 2025: Nationals SC Cap Area v Cap City Athletic 1847 (Hope Sports Complex)",
        "- Sep 06, 2025: Cap City Athletic 1847 v Liverpool FC IA GMA (East Lansing Soccer Complex)",
        "- Sep 06, 2025: Legends FC Michigan v Liverpool FC IA Michigan North Oakland (Legacy Center Sports Complex)",
        "- Sep 07, 2025: Legends FC Michigan v Liverpool FC IA GMA (Legacy Center Sports Complex)",
        "- Sep 07, 2025: Cap City Athletic 1847 v Liverpool FC IA Michigan North Oakland (East Lansing Soccer Complex)",
        "- Sep 14, 2025: Plymouth Reign SC v Portage SC (Lake Pointe Soccer Complex)",
        "- Sep 20, 2025: Detroit City FC West v Portage SC (Independence Park)",
        "- Sep 20, 2025: Plymouth Reign SC v TKO Premier SC (Lake Pointe Soccer Complex)",
        "- Sep 20, 2025: Liverpool FC IA GMA v Liverpool FC IA Michigan North Oakland (Wisner Stadium)",
        "- Sep 21, 2025: Detroit City FC West v TKO Premier SC (Independence Park)",
        "- Sep 27, 2025: Liverpool FC IA GMA v Michigan Burn (Avondale High School)",
        "- Sep 27, 2025: Liverpool FC IA Michigan North Oakland v Nationals SC Union (Clarkston High School pond)",
        "- Sep 27, 2025: Detroit City FC West v Plymouth Reign SC (Independence Park)",
        "- Sep 27, 2025: Portage SC v Michigan Rangers FC (Portage Soccer Complex)",
        "- Sep 28, 2025: Portage SC v Nationals SC Cap Area (Portage Soccer Complex)",
        "- Sep 28, 2025: Liverpool FC IA Michigan North Oakland v Michigan Burn (Clarkston Stadium High School Field)",
        "- Sep 28, 2025: TKO Premier SC v Michigan Rangers FC (Kalamazoo Soccer Complex)",
        "- Sep 28, 2025: Liverpool FC IA GMA v Nationals SC Union (Avondale High School)",
        "- Sep 29, 2025: TKO Premier SC v Nationals SC Cap Area (Kalamazoo Soccer Complex)",
        "- Oct 04, 2025: Nationals SC Cap Area v Liverpool FC IA GMA (Hope Sports Complex)",
        "- Oct 11, 2025: Legends FC Michigan v Detroit City FC West (Legacy Center Sports Complex)",
        "- Oct 11, 2025: Cap City Athletic 1847 v Plymouth Reign SC (East Lansing Soccer Complex)",
        "- Oct 11, 2025: TKO Premier SC v Nationals SC Union (Kalamazoo Soccer Complex)",
        "- Oct 11, 2025: Portage SC v Michigan Burn (Portage Soccer Complex)",
        "- Oct 12, 2025: Legends FC Michigan v Plymouth Reign SC (Legacy Center Sports Complex)",
        "- Oct 12, 2025: Michigan Rangers FC v Liverpool FC IA Michigan North Oakland (Hamilton High School)",
        "- Oct 12, 2025: TKO Premier SC v Michigan Burn (Kalamazoo Soccer Complex)",
        "- Oct 12, 2025: Portage SC v Nationals SC Union (Portage Soccer Complex)",
        "- Oct 12, 2025: Cap City Athletic 1847 v Detroit City FC West (East Lansing Soccer Complex)",
        "- Oct 15, 2025: Nationals SC Cap Area v Liverpool FC IA Michigan North Oakland (Hope Sports Complex)",
        "- Oct 19, 2025: Portage SC v TKO Premier SC (Portage Soccer Complex)",
        "- Oct 25, 2025: Plymouth Reign SC v Nationals SC Cap Area (High Velocity Sports Dome)",
        "- Oct 25, 2025: Detroit City FC West v Michigan Rangers FC (Independence Park)",
        "- Oct 25, 2025: TKO Premier SC v Liverpool FC IA Michigan North Oakland (Kalamazoo Soccer Complex)",
        "- Oct 25, 2025: Nationals SC Union v Cap City Athletic 1847 (Oakland University Upper Fields)",
        "- Oct 25, 2025: Portage SC v Liverpool FC IA GMA (Portage Soccer Complex)",
        "- Oct 25, 2025: Michigan Burn v Legends FC Michigan (Legacy Center Sports Complex)",
        "- Oct 26, 2025: Plymouth Reign SC v Michigan Rangers FC (Lake Pointe Soccer Complex)",
        "- Oct 26, 2025: Portage SC v Liverpool FC IA Michigan North Oakland (Portage Soccer Complex)",
        "- Oct 26, 2025: Michigan Burn v Cap City Athletic 1847 (The Sports Academy)",
        "- Oct 26, 2025: TKO Premier SC v Liverpool FC IA GMA (Kalamazoo Soccer Complex)",
        "- Oct 26, 2025: Nationals SC Union v Legends FC Michigan (Oakland University Upper Fields)",
        "- Oct 26, 2025: Detroit City FC West v Nationals SC Cap Area (Independence Park)",
        "- Oct 29, 2025: Nationals SC Union v Michigan Burn (Oakland University Upper Fields)",
        "- Nov 01, 2025: Liverpool FC IA GMA v Detroit City FC West (Avondale High School)",
        "- Nov 01, 2025: Legends FC Michigan v TKO Premier SC (Legacy Center Sports Complex)",
        "- Nov 01, 2025: Nationals SC Union v Nationals SC Cap Area (Oakland University Upper Fields)",
        "- Nov 01, 2025: Michigan Burn v Michigan Rangers FC (The Sports Academy)",
        "- Nov 01, 2025: Cap City Athletic 1847 v Portage SC (East Lansing Soccer Complex)",
        "- Nov 02, 2025: Liverpool FC IA GMA v Plymouth Reign SC (Avondale High School)",
        "- Nov 02, 2025: Michigan Burn v Nationals SC Cap Area (The Sports Academy)",
        "- Nov 02, 2025: Legends FC Michigan v Portage SC (Legacy Center Sports Complex)",
        "- Nov 02, 2025: Cap City Athletic 1847 v TKO Premier SC (East Lansing Soccer Complex)",
        "- Nov 02, 2025: Nationals SC Union v Michigan Rangers FC (Evolution Sportsplex Dome)",
        "- Nov 08, 2025: Nationals SC Cap Area v Michigan Rangers FC (Hope Sports Complex)",
        "- Nov 08, 2025: Nationals SC Union v Detroit City FC West (Oakland University Upper Fields)",
        "- Nov 09, 2025: Michigan Burn v Detroit City FC West (Anchor Bay High School)",
        "- Nov 09, 2025: Nationals SC Union v Plymouth Reign SC (Oakland University Upper Fields)",
        "- Nov 15, 2025: Michigan Rangers FC v Liverpool FC IA GMA (Hudsonville Freshman Campus)",
        "- Nov 15, 2025: Liverpool FC IA Michigan North Oakland v Plymouth Reign SC (Clarkston Stadium High School Field)",
        "- Nov 16, 2025: Cap City Athletic 1847 v Legends FC Michigan (Spartan Greens Turf Complex)",
        "- Nov 16, 2025: Liverpool FC IA Michigan North Oakland v Detroit City FC West (Clarkston High School pond)",
        "- Dec 12, 2025: Michigan Burn v Plymouth Reign SC (Evolution Sportsplex Dome)"
    ]

    rlMounClub = [
        "Arsenal Colorado",
        "Boise Thorns FC",
        "City SC Utah",
        "Colorado EDGE",
        "Colorado Rapids Central",
        "Colorado Rapids North",
        "Colorado Rapids South",
        "Colorado Rush Academy White",
        "Idaho Rush",
        "La ROca RC",
        "NUU Avalanche",
        "Pride SC",
        "Real Colorado",
        "Utah Avalanche",
        "Utah Surf",
    ]

    rlMounSched = [
        "- Aug 23, 2025: Colorado EDGE v Colorado Rapids Central (Stenger Soccer Complex)",
        "- Aug 23, 2025: Real Colorado v Colorado Rapids South (Highland Heritage Regional Park)",
        "- Aug 23, 2025: Colorado Rapids North v Pride SC (Dick's Sporting Goods Park)",
        "- Aug 23, 2025: Colorado Rush Academy White v Arsenal Colorado (Colorado Academy)",
        "- Aug 24, 2025: Colorado Rapids Central v Colorado Rush Academy White (Dick's Sporting Goods Park)",
        "- Aug 24, 2025: Colorado EDGE v Pride SC (Stenger Soccer Complex)",
        "- Aug 24, 2025: Colorado Rapids South v Colorado Rapids North (Gates South Soccer Complex)",
        "- Aug 24, 2025: Arsenal Colorado v Real Colorado (Fort Collins Soccer Complex)",
        "- Sep 06, 2025: Arsenal Colorado v Pride SC (Fort Collins Soccer Complex)",
        "- Sep 06, 2025: Colorado Rapids Central v Real Colorado (Dick's Sporting Goods Park)",
        "- Sep 06, 2025: Colorado Rush Academy White v Colorado Rapids North (Colorado Academy)",
        "- Sep 06, 2025: Colorado EDGE v Colorado Rapids South (Stenger Soccer Complex)",
        "- Sep 07, 2025: Pride SC v Real Colorado (Pride Soccer Complex)",
        "- Sep 07, 2025: Colorado Rapids Central v Colorado Rapids South (Dick's Sporting Goods Park)",
        "- Sep 07, 2025: Colorado EDGE v Colorado Rush Academy White (Stenger Soccer Complex)",
        "- Sep 07, 2025: Arsenal Colorado v Colorado Rapids North (Fort Collins Soccer Complex)",
        "- Sep 20, 2025: Colorado Rapids North v Colorado Rapids Central (Dick's Sporting Goods Park)",
        "- Sep 21, 2025: Colorado Rush Academy White v Pride SC (Trailblazer Stadium)",
        "- Sep 21, 2025: Real Colorado v Colorado EDGE (Highland Heritage Regional Park)",
        "- Sep 21, 2025: Colorado Rapids South v Arsenal Colorado (Gates South Soccer Complex)",
        "- Sep 27, 2025: Colorado EDGE v Colorado Rapids North (Stenger Soccer Complex)",
        "- Sep 28, 2025: Colorado Rapids South v Pride SC (Gates South Soccer Complex)",
        "- Sep 28, 2025: Arsenal Colorado v Colorado Rapids Central (Fort Collins Soccer Complex)",
        "- Sep 28, 2025: Colorado Rush Academy White v Real Colorado (Colorado Academy)",
        "- Oct 04, 2025: Colorado Rapids North v Arsenal Colorado (Stargate Charter School)",
        "- Oct 04, 2025: Real Colorado v Pride SC (Highland Heritage Regional Park)",
        "- Oct 04, 2025: Colorado Rush Academy White v Colorado EDGE (Colorado Academy)",
        "- Oct 04, 2025: Colorado Rapids South v Colorado Rapids Central (Gates South Soccer Complex)",
        "- Oct 05, 2025: Colorado EDGE v Arsenal Colorado (Stenger Soccer Complex)",
        "- Oct 05, 2025: Real Colorado v Colorado Rapids North (Highland Heritage Regional Park)",
        "- Oct 05, 2025: Colorado Rush Academy White v Colorado Rapids South (Colorado Academy)",
        "- Oct 05, 2025: Colorado Rapids Central v Pride SC (Dick's Sporting Goods Park)",
        "- Oct 11, 2025: Colorado Rapids North v Colorado Rush Academy White (Stargate Charter School)",
        "- Oct 12, 2025: Real Colorado v Colorado Rapids Central (Highland Heritage Regional Park)",
        "- Oct 12, 2025: Pride SC v Arsenal Colorado (Pride Soccer Complex)",
        "- Oct 12, 2025: Colorado Rapids South v Colorado EDGE (Gates South Soccer Complex)",
        "- Oct 18, 2025: Colorado Rapids Central v Colorado Rapids North (Aurora Sports Park)",
        "- Oct 18, 2025: Colorado EDGE v Real Colorado (Stenger Soccer Complex)",
        "- Oct 18, 2025: Pride SC v Colorado Rush Academy White (Pride Soccer Complex)",
        "- Oct 18, 2025: Arsenal Colorado v Colorado Rapids South (Fort Collins Soccer Complex)",
        "- Oct 19, 2025: Colorado Rapids Central v Colorado EDGE (Dick's Sporting Goods Park)",
        "- Oct 19, 2025: Pride SC v Colorado Rapids North (Pride Soccer Complex)",
        "- Oct 19, 2025: Colorado Rapids South v Real Colorado (Gates South Soccer Complex)",
        "- Oct 19, 2025: Arsenal Colorado v Colorado Rush Academy White (Fort Collins Soccer Complex)",
        "- Oct 26, 2025: Pride SC v Colorado EDGE (Pride Soccer Complex)",
        "- Oct 26, 2025: Real Colorado v Arsenal Colorado (Highland Heritage Regional Park)",
        "- Oct 26, 2025: Colorado Rapids North v Colorado Rapids South (Stargate Charter School)",
        "- Oct 26, 2025: Colorado Rush Academy White v Colorado Rapids Central (Addenbrooke Classical)",
        "- Nov 01, 2025: Pride SC v Colorado Rapids Central (El Pomar Olin Field)",
        "- Nov 01, 2025: Colorado Rapids South v Colorado Rush Academy White (Gates South Soccer Complex)",
        "- Nov 01, 2025: Arsenal Colorado v Colorado EDGE (Fort Collins Soccer Complex)",
        "- Nov 01, 2025: Colorado Rapids North v Real Colorado (Trail Winds)",
        "- Nov 02, 2025: Colorado Rapids North v Colorado EDGE (Horizon High School)",
        "- Nov 02, 2025: Pride SC v Colorado Rapids South (El Pomar Olin Field)",
        "- Nov 02, 2025: Colorado Rapids Central v Arsenal Colorado (Northfield Sports Complex)",
        "- Nov 02, 2025: Real Colorado v Colorado Rush Academy White (Highland Heritage Regional Park)",
        "- Nov 08, 2025: Utah Surf v Colorado Rapids North (Lakeside Sports Park)",
        "- Nov 08, 2025: Real Colorado v Idaho Rush (Highland Heritage Regional Park)",
        "- Nov 08, 2025: Colorado Rush Academy White v NUU Avalanche (Addenbrooke Classical)",
        "- Nov 08, 2025: Pride SC v Boise Thorns FC (Pride Soccer Complex)",
        "- Nov 08, 2025: City SC Utah v Arsenal Colorado (Dumke Field (Westminster University))",
        "- Nov 09, 2025: City SC Utah v Colorado Rapids North (Rowland Hall Steiner Fields)",
        "- Nov 09, 2025: Colorado EDGE v NUU Avalanche (David Lorenz Park)",
        "- Nov 09, 2025: Pride SC v Idaho Rush (Pride Soccer Complex)",
        "- Nov 09, 2025: Real Colorado v Boise Thorns FC (Highland Heritage Regional Park)",
        "- Nov 09, 2025: Utah Surf v Arsenal Colorado (Lakeside Sports Park)",
        "- Nov 15, 2025: Colorado Rapids South v NUU Avalanche (David A. Lorenz Regional Park)",
        "- Nov 15, 2025: Colorado Rapids Central v Utah Avalanche (Denver South High School)",
        "- Nov 15, 2025: La Roca FC v Pride SC (La Roca Park)",
        "- Nov 15, 2025: City SC Utah v Real Colorado (Summit Academy High School Stadium)",
        "- Nov 16, 2025: Colorado Rapids Central v NUU Avalanche (Northfield Sports Complex)",
        "- Nov 16, 2025: Colorado Rapids South v Utah Avalanche (Cherokee Trail High School)",
        "- Nov 16, 2025: City SC Utah v Pride SC (Salt Lake County Athletic Fields)",
        "- Nov 16, 2025: La Roca FC v Real Colorado (La Roca Park)",
        "- Nov 22, 2025: Real Colorado v Utah Surf (Highland Heritage Regional Park)",
        "- Nov 22, 2025: Colorado EDGE v La Roca FC (David Lorenz Park)",
        "- Nov 22, 2025: Colorado Rush Academy White v City SC Utah (Colorado Academy)",
        "- Nov 22, 2025: Idaho Rush v Colorado Rapids South (Optimist Sports Complex)",
        "- Nov 22, 2025: NUU Avalanche v Colorado Rapids North (Sky View High School Football Field)",
        "- Nov 22, 2025: Boise Thorns FC v Colorado Rapids Central (Eagle High School)",
        "- Nov 22, 2025: Utah Avalanche v Arsenal Colorado (St. Joseph Catholic High School)",
        "- Nov 23, 2025: Colorado EDGE v City SC Utah (David Lorenz Park)",
        "- Nov 23, 2025: Boise Thorns FC v Colorado Rapids South (Rocky Mountain High School)",
        "- Nov 23, 2025: Idaho Rush v Colorado Rapids Central (Optimist Sports Complex)",
        "- Nov 23, 2025: NUU Avalanche v Arsenal Colorado (Hansen Family Sports Complex)",
        "- Nov 23, 2025: Colorado Rush Academy White v La Roca FC (Denver Christian School)",
        "- Nov 23, 2025: Pride SC v Utah Surf (Pride Soccer Complex)",
        "- Nov 23, 2025: Utah Avalanche v Colorado Rapids North (St. Joseph Catholic High School)",
        "- Dec 06, 2025: Colorado EDGE v Utah Avalanche (David Lorenz Park)",
        "- Dec 07, 2025: Colorado Rush Academy White v Utah Avalanche (Trailblazer Stadium)",
        "- Dec 13, 2025: Utah Avalanche v Real Colorado (Murray City Park)",
        "- Dec 13, 2025: Utah Surf v Colorado Rapids Central (Utah Valley University Geneva Fields)",
        "- Dec 13, 2025: NUU Avalanche v Pride SC (Sky View High School Football Field)",
        "- Dec 13, 2025: Arsenal Colorado v Boise Thorns FC (Loveland Sports Park)",
        "- Dec 13, 2025: La Roca FC v Colorado Rapids South (Spence Eccles Ogden Community Sports Complex)",
        "- Dec 14, 2025: Utah Surf v Colorado Rapids South (Utah Valley University Geneva Fields)",
        "- Dec 14, 2025: Colorado Rapids North v Boise Thorns FC (Stargate Charter School)",
        "- Dec 14, 2025: Utah Avalanche v Pride SC (Murray City Park)",
        "- Dec 14, 2025: NUU Avalanche v Real Colorado (Hansen Family Sports Complex)",
        "- Dec 14, 2025: La Roca FC v Colorado Rapids Central (Lakeside Sports Complex)",
        "- Dec 14, 2025: Arsenal Colorado v Idaho Rush (Loveland Sports Park)",
        "- Jan 17, 2026: Idaho Rush v Colorado Rush Academy White (Eagle High School)",
        "- Jan 17, 2026: Boise Thorns FC v Colorado EDGE (Rocky Mountain High School)",
        "- Jan 18, 2026: Boise Thorns FC v Colorado Rush Academy White (Rocky Mountain High School)",
        "- Jan 18, 2026: Idaho Rush v Colorado EDGE (Centennial High School)",
        "- Jan 24, 2026: Colorado EDGE v Utah Surf (Trailblazer Stadium)",
        "- Jan 24, 2026: Colorado Rapids North v La Roca FC (Trail Winds)",
        "- Jan 24, 2026: Colorado Rapids Central v City SC Utah (Aurora Sports Park)",
        "- Jan 25, 2026: Arsenal Colorado v La Roca FC (University Northern CO)",
        "- Jan 25, 2026: Colorado Rapids South v City SC Utah (Aurora Sports Park)",
        "- Jan 25, 2026: Colorado Rush Academy White v Utah Surf (Addenbrooke Classical)",
        "- Feb 28, 2026: Utah Avalanche v Boise Thorns FC (Murray City Park)",
        "- Feb 28, 2026: NUU Avalanche v Idaho Rush (Hansen Family Sports Complex)",
        "- Mar 01, 2026: City SC Utah v La Roca FC",
        "- Mar 01, 2026: Utah Avalanche v Idaho Rush (Murray City Park)",
        "- Mar 01, 2026: NUU Avalanche v Boise Thorns FC (Hansen Family Sports Complex)",
        "- Mar 08, 2026: La Roca FC v NUU Avalanche (La Roca Park)",
        "- Mar 15, 2026: NUU Avalanche v Utah Avalanche",
        "- Mar 15, 2026: Utah Surf v City SC Utah",
        "- Mar 15, 2026: Idaho Rush v Boise Thorns FC (Eagle High School)",
        "- Mar 21, 2026: City SC Utah v Idaho Rush",
        "- Mar 21, 2026: La Roca FC v Boise Thorns FC (La Roca Park)",
        "- Mar 22, 2026: City SC Utah v Boise Thorns FC",
        "- Mar 22, 2026: La Roca FC v Idaho Rush (La Roca Park)",
        "- Mar 22, 2026: Utah Avalanche v Utah Surf (St. Joseph Catholic High School)",
        "- Mar 28, 2026: City SC Utah v Utah Surf",
        "- Mar 28, 2026: Utah Avalanche v NUU Avalanche",
        "- Mar 28, 2026: Boise Thorns FC v Idaho Rush (Boise Timbers|Thorns - Soccer Complex)",
        "- Mar 29, 2026: City SC Utah v Utah Avalanche",
        "- Mar 29, 2026: Utah Surf v NUU Avalanche",
        "- Apr 12, 2026: NUU Avalanche v La Roca FC",
        "- Apr 18, 2026: Idaho Rush v NUU Avalanche",
        "- Apr 18, 2026: La Roca FC v Utah Surf (La Roca Park)",
        "- Apr 18, 2026: Boise Thorns FC v Utah Avalanche (Boise Timbers|Thorns - Soccer Complex)",
        "- Apr 19, 2026: Idaho Rush v Utah Avalanche",
        "- Apr 19, 2026: La Roca FC v City SC Utah (La Roca Park)",
        "- Apr 19, 2026: Boise Thorns FC v NUU Avalanche (Boise Timbers|Thorns - Soccer Complex)",
        "- Apr 23, 2026: Utah Surf v La Roca FC (Utah Valley University Geneva Fields)",
        "- Apr 26, 2026: City SC Utah v Utah Avalanche",
        "- Apr 26, 2026: Utah Surf v NUU Avalanche",
        "- May 02, 2026: Utah Surf v Boise Thorns FC (Utah Valley University Geneva Fields)",
        "- May 03, 2026: NUU Avalanche v City SC Utah",
        "- May 03, 2026: Utah Surf v Idaho Rush (Utah Valley University Geneva Fields)",
        "- May 03, 2026: Utah Avalanche v La Roca FC (Murray City Park)",
        "- May 09, 2026: Idaho Rush v City SC Utah",
        "- May 09, 2026: Boise Thorns FC v La Roca FC (Boise Timbers|Thorns - Soccer Complex)",
        "- May 10, 2026: Idaho Rush v La Roca FC",
        "- May 10, 2026: Utah Surf v Utah Avalanche",
        "- May 10, 2026: Boise Thorns FC v City SC Utah (Boise Timbers|Thorns - Soccer Complex)",
        "- May 16, 2026: Boise Thorns FC v Utah Surf (Boise Timbers|Thorns - Soccer Complex)",
        "- May 17, 2026: City SC Utah v NUU Avalanche",
        "- May 17, 2026: Idaho Rush v Utah Surf",
        "- May 17, 2026: La Roca FC v Utah Avalanche (La Roca Park)"
    ]

    rlMidClubs = [
        "Chattanooga Red Wolves SC",
        "FC Alliance",
        "Germantown Legends",
        "Indy Eleven Spirit",
        "Lobos Rush",
        "Mississippi Rush United",
        "Tennessee SC Murfreesboro",
        "Tennessee United",
        "Tupelo FC"
    ]

    rlMidSched = [
        "- Oct 04, 2025: Mississippi Rush United v Tupelo FC (Freedom Ridge Park)",
        "- Oct 05, 2025: Mississippi Rush United v Tupelo FC (Freedom Ridge Park)",
        "- Nov 15, 2025: Chattanooga Red Wolves SC v FC Alliance (Ringgold High School)",
        "- Nov 15, 2025: Tennessee SC Murfreesboro v Germantown Legends (Siegel High School)",
        "- Nov 16, 2025: Tennessee SC Murfreesboro v Lobos Rush (Siegel High School)",
        "- Nov 18, 2025: Lobos Rush v Germantown Legends (W.C. Johnson Turf Park)",
        "- Nov 23, 2025: Tennessee SC Murfreesboro v Chattanooga Red Wolves SC (Blackman High School)",
        "- Dec 20, 2025: FC Alliance v Tennessee United (Hardin Valley Academy Stadium)",
        "- Jan 17, 2026: Tennessee SC Murfreesboro v FC Alliance (Lebanon Sports Complex)",
        "- Feb 07, 2026: Chattanooga Red Wolves SC v Tennessee United (University of Tennessee - Chattanooga)",
        "- Feb 14, 2026: FC Alliance v Indy Eleven Spirit (Hardin Valley Academy Stadium)",
        "- Feb 15, 2026: Chattanooga Red Wolves SC v Indy Eleven Spirit (University of Tennessee - Chattanooga)",
        "- Feb 15, 2026: Tennessee United v Tennessee SC Murfreesboro (Drakes Creek Park (DCP))",
        "- Feb 19, 2026: Germantown Legends v Lobos Rush (Mike Rose Soccer Complex)",
        "- Feb 21, 2026: Germantown Legends v Tupelo FC",
        "- Feb 21, 2026: Tennessee United v Indy Eleven Spirit (Moss Wright Park (MWP))",
        "- Feb 21, 2026: Lobos Rush v Mississippi Rush United (W.C. Johnson Turf Park)",
        "- Feb 21, 2026: Chattanooga Red Wolves SC v Tennessee SC Murfreesboro (University of Tennessee - Chattanooga)",
        "- Feb 22, 2026: Germantown Legends v Mississippi Rush United",
        "- Feb 22, 2026: Tennessee SC Murfreesboro v Indy Eleven Spirit (Oakland High School)",
        "- Feb 22, 2026: Lobos Rush v Tupelo FC (W.C. Johnson Turf Park)",
        "- Mar 07, 2026: Germantown Legends v Indy Eleven Spirit",
        "- Mar 07, 2026: Tupelo FC v Chattanooga Red Wolves SC (BankPlus Sportsplex at Ballard Park)",
        "- Mar 07, 2026: Lobos Rush v Tennessee United (W.C. Johnson Turf Park)",
        "- Mar 07, 2026: Mississippi Rush United v Tennessee SC Murfreesboro (Freedom Ridge Park)",
        "- Mar 08, 2026: Tennessee United v Germantown Legends",
        "- Mar 08, 2026: Tupelo FC v Tennessee SC Murfreesboro (BankPlus Sportsplex at Ballard Park)",
        "- Mar 08, 2026: Lobos Rush v Indy Eleven Spirit (W.C. Johnson Turf Park)",
        "- Mar 08, 2026: Mississippi Rush United v Chattanooga Red Wolves SC (Freedom Ridge Park)",
        "- Mar 14, 2026: Indy Eleven Spirit v Tennessee SC Murfreesboro (Goebel Soccer Complex)",
        "- Mar 21, 2026: Mississippi Rush United v FC Alliance (Freedom Ridge Park)",
        "- Mar 22, 2026: Tupelo FC v FC Alliance (BankPlus Sportsplex at Ballard Park)",
        "- Mar 22, 2026: FC Alliance v Tennessee SC Murfreesboro (Clinton High School)",
        "- Mar 28, 2026: Germantown Legends v FC Alliance",
        "- Mar 28, 2026: Lobos Rush v Chattanooga Red Wolves SC (W.C. Johnson Turf Park)",
        "- Mar 28, 2026: Tupelo FC v Tennessee United (BankPlus Sportsplex at Ballard Park)",
        "- Mar 29, 2026: Germantown Legends v Chattanooga Red Wolves SC",
        "- Mar 29, 2026: Lobos Rush v FC Alliance (W.C. Johnson Turf Park)",
        "- Mar 29, 2026: Mississippi Rush United v Tennessee United (Freedom Ridge Park)",
        "- Apr 11, 2026: Tennessee United v Lobos Rush (Moss Wright Park (MWP))",
        "- Apr 11, 2026: Chattanooga Red Wolves SC v Tupelo FC",
        "- Apr 11, 2026: FC Alliance v Mississippi Rush United (Hardin Valley Academy Stadium)",
        "- Apr 11, 2026: Indy Eleven Spirit v Germantown Legends (Goebel Soccer Complex)",
        "- Apr 12, 2026: Chattanooga Red Wolves SC v Mississippi Rush United",
        "- Apr 12, 2026: Germantown Legends v Tennessee United",
        "- Apr 12, 2026: Indy Eleven Spirit v Lobos Rush (Goebel Soccer Complex)",
        "- Apr 18, 2026: Germantown Legends v Tennessee SC Murfreesboro",
        "- Apr 18, 2026: Tennessee United v Chattanooga Red Wolves SC",
        "- Apr 18, 2026: Indy Eleven Spirit v FC Alliance (Goebel Soccer Complex)",
        "- Apr 19, 2026: Indy Eleven Spirit v Chattanooga Red Wolves SC (Goebel Soccer Complex)",
        "- Apr 19, 2026: Tennessee United v FC Alliance (Drakes Creek Park (DCP))",
        "- Apr 19, 2026: Lobos Rush v Tennessee SC Murfreesboro (W.C. Johnson Turf Park)",
        "- Apr 25, 2026: Chattanooga Red Wolves SC v Lobos Rush",
        "- Apr 25, 2026: Tennessee United v Tupelo FC",
        "- Apr 25, 2026: FC Alliance v Germantown Legends (Clinton High School)",
        "- Apr 25, 2026: Tennessee SC Murfreesboro v Mississippi Rush United (Richard Siegel Soccer Complex)",
        "- Apr 26, 2026: Tennessee United v Mississippi Rush United",
        "- Apr 26, 2026: Chattanooga Red Wolves SC v Germantown Legends",
        "- Apr 26, 2026: FC Alliance v Lobos Rush (Clinton High School)",
        "- Apr 26, 2026: Tennessee SC Murfreesboro v Tupelo FC (Richard Siegel Soccer Complex)",
        "- May 02, 2026: Tupelo FC v Germantown Legends",
        "- May 02, 2026: FC Alliance v Chattanooga Red Wolves SC (Clinton High School)",
        "- May 02, 2026: Mississippi Rush United v Lobos Rush (Freedom Ridge Park)",
        "- May 02, 2026: Indy Eleven Spirit v Tennessee United (Goebel Soccer Complex)",
        "- May 03, 2026: Tupelo FC v Lobos Rush",
        "- May 03, 2026: Mississippi Rush United v Germantown Legends (Freedom Ridge Park)",
        "- May 03, 2026: Tennessee SC Murfreesboro v Tennessee United (Richard Siegel Soccer Complex)",
        "- May 09, 2026: Indy Eleven Spirit v Mississippi Rush United",
        "- May 10, 2026: Indy Eleven Spirit v Mississippi Rush United",
        "- May 16, 2026: Indy Eleven Spirit v Tupelo FC",
        "- May 17, 2026: Indy Eleven Spirit v Tupelo FC"
    ]

    rlSoCalClubs = [
        "Beach FC (CA)",
        "Legends FC",
        "Legends FC San Diego",
        "LV Heat Surg",
        "Pateadores",
        "Rebels",
        "San Diego Surf",
        "SLAMMERS FC",
        "Slammers FC HB Koge",
        "So Cal Blues SC",
        "Sporting CA USA"
    ]

    rlSoCalSched = [
        "- Sep 06, 2025: Sporting CA USA v Pateadores (Silverlakes Soccer Complex)",
        "- Sep 06, 2025: Legends FC v Rebels SC (Silverlakes Complex)",
        "- Sep 06, 2025: San Diego Surf v Beach FC (CA) (Surf Sports Park)",
        "- Sep 06, 2025: So Cal Blues SC v Slammers FC HB Koge (OC Great Park)",
        "- Sep 07, 2025: Legends FC San Diego v SLAMMERS FC (Miramesa High School)",
        "- Sep 13, 2025: SLAMMERS FC v San Diego Surf (Orange County Great Park)",
        "- Sep 13, 2025: Pateadores v Beach FC (CA) (Great Park)",
        "- Sep 14, 2025: Rebels SC v So Cal Blues SC (Monte Vista High School)",
        "- Sep 14, 2025: Legends FC San Diego v Legends FC (Torrey Pines High School)",
        "- Sep 14, 2025: Slammers FC HB Koge v Sporting CA USA (Orange County Great Park)",
        "- Sep 20, 2025: Legends FC v Slammers FC HB Koge (Silverlakes Complex)",
        "- Sep 20, 2025: San Diego Surf v Legends FC San Diego (Surf Sports Park)",
        "- Sep 20, 2025: So Cal Blues SC v LV Heat Surf (Silverlakes)",
        "- Sep 21, 2025: SLAMMERS FC v LV Heat Surf (Bonita Canyon Sports Park)",
        "- Sep 21, 2025: Pateadores v Rebels SC (Arroyo Park)",
        "- Sep 27, 2025: Slammers FC HB Koge v San Diego Surf (Arroyo Park)",
        "- Sep 27, 2025: SLAMMERS FC v Pateadores (Orange County Great Park)",
        "- Sep 27, 2025: Rebels SC v Sporting CA USA (Monte Vista High School)",
        "- Sep 27, 2025: LV Heat Surf v Beach FC (CA) (Heritage Park Sports Complex)",
        "- Sep 28, 2025: Legends FC San Diego v So Cal Blues SC (Miramesa High School)",
        "- Oct 04, 2025: Legends FC v So Cal Blues SC (Silverlakes Complex)",
        "- Oct 04, 2025: San Diego Surf v LV Heat Surf (Surf Sports Park)",
        "- Oct 04, 2025: Slammers FC HB Koge v Rebels SC (Orange County Great Park)",
        "- Oct 05, 2025: Rebels SC v LV Heat Surf (Monte Vista High School)",
        "- Oct 11, 2025: Beach FC (CA) v Legends FC (El Camino College)",
        "- Oct 11, 2025: Sporting CA USA v SLAMMERS FC (Silverlakes Soccer Complex)",
        "- Oct 12, 2025: Beach FC (CA) v SLAMMERS FC (Long Beach City College)",
        "- Oct 12, 2025: Pateadores v Legends FC San Diego (Arroyo Park)",
        "- Oct 18, 2025: LV Heat Surf v Slammers FC HB Koge (Heritage Park Sports Complex)",
        "- Oct 18, 2025: Rebels SC v Beach FC (CA) (Southwestern College)",
        "- Oct 18, 2025: So Cal Blues SC v Sporting CA USA (OC Great Park)",
        "- Oct 18, 2025: Legends FC v San Diego Surf (Silverlakes Complex)",
        "- Oct 19, 2025: Legends FC San Diego v Sporting CA USA (Miramesa High School)",
        "- Oct 25, 2025: Legends FC v LV Heat Surf (Silverlakes Complex)",
        "- Oct 25, 2025: So Cal Blues SC v Pateadores (OC Great Park)",
        "- Oct 25, 2025: SLAMMERS FC v Rebels SC (Saddleback College)",
        "- Oct 26, 2025: Sporting CA USA v LV Heat Surf (Silverlakes Soccer Complex)",
        "- Nov 01, 2025: Pateadores v Legends FC (Great Park)",
        "- Nov 01, 2025: San Diego Surf v Sporting CA USA (Surf Sports Park)",
        "- Nov 01, 2025: Slammers FC HB Koge v SLAMMERS FC (Arroyo Park)",
        "- Nov 02, 2025: Beach FC (CA) v Legends FC San Diego (Long Beach City College)",
        "- Nov 08, 2025: San Diego Surf v So Cal Blues SC (Surf Sports Park)",
        "- Nov 08, 2025: Sporting CA USA v Beach FC (CA) (Silverlakes Soccer Complex)",
        "- Nov 08, 2025: LV Heat Surf v Legends FC San Diego (Heritage Park Sports Complex)",
        "- Nov 08, 2025: Slammers FC HB Koge v Pateadores (Orange County Great Park)",
        "- Nov 15, 2025: LV Heat Surf v Pateadores (Heritage Park Sports Complex)",
        "- Nov 15, 2025: SLAMMERS FC v Legends FC (Chapparosa Park)",
        "- Nov 15, 2025: Legends FC San Diego v Slammers FC HB Koge (Miramesa High School)",
        "- Nov 16, 2025: Beach FC (CA) v So Cal Blues SC (Dignity Health Sports Park)",
        "- Nov 22, 2025: Sporting CA USA v Legends FC (Sommer Bend Sports Park)",
        "- Nov 22, 2025: Beach FC (CA) v Slammers FC HB Koge (El Camino College)",
        "- Nov 22, 2025: So Cal Blues SC v SLAMMERS FC (OC Great Park)",
        "- Nov 22, 2025: Rebels SC v Legends FC San Diego (Monte Vista High School)",
        "- Nov 23, 2025: Pateadores v San Diego Surf (Arroyo Park)",
        "- Mar 14, 2026: So Cal Blues SC v Legends FC San Diego",
        "- Mar 14, 2026: Rebels SC v SLAMMERS FC",
        "- Mar 14, 2026: LV Heat Surf v Sporting CA USA",
        "- Mar 15, 2026: Beach FC (CA) v Pateadores (El Camino College)",
        "- Mar 21, 2026: Sporting CA USA v So Cal Blues SC",
        "- Mar 21, 2026: Rebels SC v Legends FC",
        "- Mar 21, 2026: San Diego Surf v Slammers FC HB Koge (Surf Sports Park)",
        "- Mar 21, 2026: Beach FC (CA) v LV Heat Surf (Long Beach City College)",
        "- Mar 21, 2026: Legends FC San Diego v Pateadores (Canyon Crest Academy)",
        "- Mar 22, 2026: So Cal Blues SC v Rebels SC",
        "- Mar 22, 2026: SLAMMERS FC v Sporting CA USA",
        "- Mar 22, 2026: Pateadores v LV Heat Surf (Bonita Creek Football Field)",
        "- Mar 22, 2026: Legends FC v Beach FC (CA) (Silverlakes Complex)",
        "- Mar 22, 2026: Slammers FC HB Koge v Legends FC San Diego (Orange County Great Park)",
        "- Mar 28, 2026: LV Heat Surf v Legends FC",
        "- Mar 28, 2026: So Cal Blues SC v San Diego Surf",
        "- Mar 28, 2026: Rebels SC v Pateadores (Southwestern College)",
        "- Mar 28, 2026: Legends FC San Diego v Beach FC (CA) (Torrey Pines High School)",
        "- Mar 29, 2026: SLAMMERS FC v Slammers FC HB Koge (Arroyo Park)",
        "- Apr 04, 2026: Sporting CA USA v Rebels SC",
        "- Apr 04, 2026: Legends FC v SLAMMERS FC (Silverlakes Complex)",
        "- Apr 04, 2026: Legends FC San Diego v San Diego Surf (Torrey Pines High School)",
        "- Apr 11, 2026: LV Heat Surf v So Cal Blues SC",
        "- Apr 11, 2026: Sporting CA USA v Legends FC San Diego",
        "- Apr 11, 2026: LV Heat Surf v Rebels SC",
        "- Apr 11, 2026: San Diego Surf v SLAMMERS FC (Surf Sports Park)",
        "- Apr 11, 2026: Pateadores v Slammers FC HB Koge (Arroyo Park)",
        "- Apr 11, 2026: Beach FC (CA) v Rebels SC (El Camino College)",
        "- Apr 12, 2026: Slammers FC HB Koge v Legends FC (Arroyo Park)",
        "- Apr 18, 2026: SLAMMERS FC v So Cal Blues SC",
        "- Apr 18, 2026: Sporting CA USA v Slammers FC HB Koge",
        "- Apr 18, 2026: Beach FC (CA) v San Diego Surf",
        "- Apr 18, 2026: Legends FC v Legends FC San Diego (Silverlakes Complex)",
        "- Apr 19, 2026: San Diego Surf v Pateadores (Surf Sports Park)",
        "- Apr 25, 2026: So Cal Blues SC v Beach FC (CA)",
        "- Apr 25, 2026: SLAMMERS FC v Legends FC San Diego",
        "- Apr 25, 2026: Slammers FC HB Koge v LV Heat Surf",
        "- Apr 25, 2026: Sporting CA USA v San Diego Surf",
        "- Apr 25, 2026: Legends FC v Pateadores (Silverlakes Complex)",
        "- Apr 26, 2026: Legends FC San Diego v LV Heat Surf",
        "- Apr 26, 2026: Pateadores v So Cal Blues SC (Bonita Creek Football Field)",
        "- May 02, 2026: Rebels SC v Slammers FC HB Koge",
        "- May 02, 2026: So Cal Blues SC v Legends FC",
        "- May 02, 2026: LV Heat Surf v San Diego Surf",
        "- May 02, 2026: Pateadores v SLAMMERS FC (Arroyo Park)",
        "- May 02, 2026: Beach FC (CA) v Sporting CA USA (Long Beach City College)",
        "- May 09, 2026: LV Heat Surf v SLAMMERS FC",
        "- May 09, 2026: Pateadores v Sporting CA USA",
        "- May 09, 2026: San Diego Surf v Legends FC (Surf Sports Park)",
        "- May 09, 2026: Legends FC San Diego v Rebels SC (Canyon Crest Academy)",
        "- May 10, 2026: San Diego Surf v Rebels SC (Surf Sports Park)",
        "- May 10, 2026: Slammers FC HB Koge v Beach FC (CA) (Arroyo Park)",
        "- May 16, 2026: SLAMMERS FC v Beach FC (CA)",
        "- May 16, 2026: Slammers FC HB Koge v So Cal Blues SC",
        "- May 16, 2026: Legends FC v Sporting CA USA (Silverlakes Complex)",
        "- May 16, 2026: Rebels SC v San Diego Surf (Southwestern College)"
    ]

    rlNorCalClubs =[
        "Association FC",
        "Burlingame SC",
        "California Magic",
        "Eastshore Alliance FC",
        "Elk Grove Soccer",
        "Folsom Lake Surf",
        "Livermore Fusion SC",
        "Los Gatos United",
        "North Coast FC",
        "Pajaro Valley",
        "Palo Alto SC",
        "Reno APEX SC",
        "Revolution FC",
        "San Francisco Elite",
        "San Ramon FC",
        "SF United FC",
        "Solano Surf",
        "Stanford Strikers",
        "Stanislaus United",
        "Valley Surf",
        "Walnut Creek Surf",
        "West Coast Soccer Club",
    ]

    rlNorCalSched = [
        "- Sep 06, 2025: Stanford Strikers10G v San Ramon FC (Rossotti Field)",
        "- Sep 06, 2025: Palo Alto SC v El Camino FC (Cubberley Football Field)",
        "- Sep 06, 2025: Revolution FC v West Coast Soccer Club (Sunset Sports Complex (SSC))",
        "- Sep 06, 2025: Walnut Creek Surf v Elk Grove Soccer (Northgate High School)",
        "- Sep 06, 2025: Folsom Lake Surf v Livermore Fusion SC (Econome Family Park)",
        "- Sep 06, 2025: Solano Surf v Reno APEX SC (Rodriguez High School)",
        "- Sep 06, 2025: Pajaro Valley v San Francisco Elite (Watsonville High School)",
        "- Sep 06, 2025: California Magic v Burlingame SC (Campolindo High School)",
        "- Sep 07, 2025: SF United FC v North Coast FC (Pollicita Middle School)",
        "- Sep 07, 2025: Los Gatos United v Eastshore Alliance FC (Leigh High School)",
        "- Sep 12, 2025: West Coast Soccer Club v Stanislaus United (Legacy Fields Sports Complex)",
        "- Sep 13, 2025: El Camino FC v Reno APEX SC",
        "- Sep 13, 2025: Stanford Strikers10G v Palo Alto SC (Kelly Park)",
        "- Sep 13, 2025: San Ramon FC v California Magic (Sunrise Ridge Park)",
        "- Sep 13, 2025: Elk Grove Soccer v SF United FC (Hal Bartholomew Sports Park)",
        "- Sep 13, 2025: Eastshore Alliance FC v Pajaro Valley (El Cerrito High School)",
        "- Sep 13, 2025: Folsom Lake Surf v Walnut Creek Surf (Econome Family Park)",
        "- Sep 13, 2025: Association FC v North Coast FC (Alden E. Oliver Sports Park)",
        "- Sep 13, 2025: San Francisco Elite v Solano Surf (Pollicita Middle School)",
        "- Sep 21, 2025: Valley Surf v Association FC (River Islands Sports Park)",
        "- Sep 21, 2025: Livermore Fusion SC v Solano Surf (Robertson Park)",
        "- Sep 21, 2025: Palo Alto SC v West Coast Soccer Club (Cubberley)",
        "- Sep 21, 2025: San Ramon FC v Pajaro Valley (Rancho San Ramon Community Park)",
        "- Sep 21, 2025: North Coast FC v Revolution FC (Petaluma Community Sports Fields)",
        "- Sep 21, 2025: Reno APEX SC v Elk Grove Soccer (Bishop Manogue High School Soccer Field)",
        "- Sep 21, 2025: Los Gatos United v Burlingame SC (Monta Vista High School)",
        "- Sep 21, 2025: San Francisco Elite v Folsom Lake Surf (Skyline College)",
        "- Sep 21, 2025: Stanislaus United v Stanford Strikers10G (Mary Grogan Community Park)",
        "- Sep 21, 2025: California Magic v Walnut Creek Surf (Acalanes High School)",
        "- Sep 21, 2025: SF United FC v El Camino FC (Beach Chalet Athletic Fields)",
        "- Sep 27, 2025: Livermore Fusion SC v North Coast FC (Robertson Park)",
        "- Sep 27, 2025: Folsom Lake Surf v Revolution FC (Econome Family Park)",
        "- Sep 27, 2025: SF United FC v Los Gatos United (Polo Fields)",
        "- Sep 27, 2025: Association FC v Palo Alto SC (Alden E. Oliver Sports Park)",
        "- Sep 27, 2025: Reno APEX SC v Valley Surf (Devere Mautino Park)",
        "- Sep 27, 2025: El Camino FC v Walnut Creek Surf (Salinas Regional Soccer Complex)",
        "- Sep 27, 2025: California Magic v Pajaro Valley (Wilder Sports Complex)",
        "- Sep 28, 2025: Valley Surf v Revolution FC (River Islands Sports Park)",
        "- Sep 28, 2025: Burlingame SC v Stanford Strikers10G (Skyline College)",
        "- Sep 28, 2025: West Coast Soccer Club v Eastshore Alliance FC (Legacy Fields Sports Complex)",
        "- Sep 28, 2025: North Coast FC v San Francisco Elite (Petaluma Community Sports Fields)",
        "- Sep 28, 2025: Elk Grove Soccer v Solano Surf (Franklin High School Football Field)",
        "- Oct 04, 2025: Elk Grove Soccer v Association FC (Hal Bartholomew Sports Park)",
        "- Oct 04, 2025: Livermore Fusion SC v El Camino FC (Robertson Park)",
        "- Oct 04, 2025: Stanford Strikers10G v Reno APEX SC (Kelly Park)",
        "- Oct 04, 2025: Stanislaus United v North Coast FC (Modesto Junior College)",
        "- Oct 04, 2025: Palo Alto SC v California Magic (El Camino Park)",
        "- Oct 04, 2025: San Ramon FC v Los Gatos United (Rancho San Ramon Community Park)",
        "- Oct 04, 2025: Walnut Creek Surf v Burlingame SC (Arbolado Park)",
        "- Oct 04, 2025: Pajaro Valley v West Coast Soccer Club (Watsonville High School)"
        "- Nov 08, 2025: Revolution FC v San Francisco Elite (Sunset Sports Complex (SSC))",
        "- Nov 08, 2025: Los Gatos United v Livermore Fusion SC (Union Middle School)",
        "- Nov 09, 2025: Solano Surf v Folsom Lake Surf (Octo Inn Soccer Complex)",
        "- Nov 15, 2025: Eastshore Alliance FC v Valley Surf (El Cerrito High School)",
        "- Mar 14, 2026: Elk Grove Soccer v California Magic",
        "- Mar 14, 2026: Burlingame SC v El Camino FC",
        "- Mar 14, 2026: Reno APEX SC v Folsom Lake Surf",
        "- Mar 14, 2026: Eastshore Alliance FC v Revolution FC",
        "- Mar 14, 2026: San Ramon FC v SF United FC",
        "- Mar 14, 2026: Palo Alto SC v Stanislaus United",
        "- Mar 14, 2026: Valley Surf v Livermore Fusion SC (River Islands Sports Park)",
        "- Mar 14, 2026: West Coast Soccer Club v Stanford Strikers10G (Legacy Fields Sports Complex)",
        "- Mar 14, 2026: Los Gatos United v Pajaro Valley (Union Middle School)",
        "- Mar 15, 2026: Stanislaus United v Valley Surf (Mary Grogan Community Park)",
        "- Mar 21, 2026: Valley Surf v North Coast FC (River Islands Sports Park)",
        "- Mar 22, 2026: El Camino FC v Association FC",
        "- Mar 22, 2026: Eastshore Alliance FC v SF United FC",
        "- Mar 22, 2026: Pajaro Valley v Solano Surf",
        "- Mar 22, 2026: California Magic v Stanford Strikers10G",
        "- Mar 22, 2026: Palo Alto SC v Valley Surf",
        "- Mar 22, 2026: San Francisco Elite v West Coast Soccer Club",
        "- Mar 22, 2026: Livermore Fusion SC v Burlingame SC (Robertson Park)",
        "- Mar 22, 2026: Folsom Lake Surf v San Ramon FC (Econome Family Park)",
        "- Mar 22, 2026: Reno APEX SC v North Coast FC (Bishop Manogue High School Soccer Field)",
        "- Mar 22, 2026: Stanislaus United v Walnut Creek Surf (Mary Grogan Community Park)",
        "- Mar 22, 2026: Revolution FC v Los Gatos United (Heritage High School)",
        "- Mar 29, 2026: El Camino FC v Elk Grove Soccer",
        "- Mar 29, 2026: Reno APEX SC v Los Gatos United",
        "- Mar 29, 2026: Walnut Creek Surf v Revolution FC",
        "- Mar 29, 2026: Stanford Strikers10G v San Francisco Elite",
        "- Mar 29, 2026: Burlingame SC v West Coast Soccer Club",
        "- Mar 29, 2026: Valley Surf v California Magic (River Islands Sports Park)",
        "- Mar 29, 2026: Association FC v Folsom Lake Surf (Skyline High School)",
        "- Mar 29, 2026: North Coast FC v Pajaro Valley (Petaluma Community Sports Fields)",
        "- Mar 29, 2026: Stanislaus United v Eastshore Alliance FC (Mary Grogan Community Park)",
        "- Mar 29, 2026: San Ramon FC v Palo Alto SC (Rancho San Ramon Community Park)",
        "- Mar 29, 2026: SF United FC v Livermore Fusion SC (Pollicita Middle School)",
        "- Apr 11, 2026: Pajaro Valley v Burlingame SC",
        "- Apr 11, 2026: Stanford Strikers10G v Los Gatos United",
        "- Apr 11, 2026: El Camino FC v San Ramon FC",
        "- Apr 11, 2026: Solano Surf v Valley Surf",
        "- Apr 11, 2026: Association FC v SF United FC (Alden E. Oliver Sports Park)",
        "- Apr 11, 2026: Stanislaus United v Revolution FC (Modesto Junior College)",
        "- Apr 11, 2026: West Coast Soccer Club v Reno APEX SC (Legacy Fields Sports Complex)",
        "- Apr 11, 2026: Palo Alto SC v Eastshore Alliance FC (Mayfield Soccer Complex)",
        "- Apr 11, 2026: California Magic v San Francisco Elite (Saint Mary's College)",
        "- Apr 11, 2026: North Coast FC v Walnut Creek Surf (Petaluma Community Sports Fields)",
        "- Apr 11, 2026: Folsom Lake Surf v Elk Grove Soccer (Econome Family Park)",
        "- Apr 12, 2026: San Francisco Elite v Stanislaus United (Pollicita Middle School)",
        "- Apr 18, 2026: Burlingame SC v Association FC",
        "- Apr 18, 2026: Eastshore Alliance FC v El Camino FC",
        "- Apr 18, 2026: Revolution FC v Pajaro Valley",
        "- Apr 18, 2026: Walnut Creek Surf v Reno APEX SC",
        "- Apr 18, 2026: California Magic v Stanislaus United",
        "- Apr 18, 2026: SF United FC v Stanford Strikers10G (Pollicita Middle School)",
        "- Apr 18, 2026: Valley Surf v San Francisco Elite (River Islands Sports Park)",
        "- Apr 18, 2026: Los Gatos United v Solano Surf (Union Middle School)",
        "- Apr 18, 2026: San Ramon FC v Elk Grove Soccer (Rancho San Ramon Community Park)",
        "- Apr 18, 2026: Livermore Fusion SC v West Coast Soccer Club (Cayetano Park)",
        "- Apr 25, 2026: Revolution FC v California Magic",
        "- Apr 25, 2026: Reno APEX SC v Eastshore Alliance FC",
        "- Apr 25, 2026: Elk Grove Soccer v Livermore Fusion SC",
        "- Apr 25, 2026: Walnut Creek Surf v San Ramon FC",
        "- Apr 25, 2026: Pajaro Valley v Stanford Strikers10G",
        "- Apr 25, 2026: Burlingame SC v Valley Surf",
        "- Apr 25, 2026: Solano Surf v SF United FC (Vanden High School)",
        "- Apr 25, 2026: Association FC v West Coast Soccer Club (Skyline High School)",
        "- Apr 25, 2026: Los Gatos United v Stanislaus United (Union Middle School)",
        "- Apr 25, 2026: San Francisco Elite v El Camino FC (Pollicita Middle School)",
        "- Apr 25, 2026: Folsom Lake Surf v Palo Alto SC (Econome Family Park)",
        "- May 02, 2026: North Coast FC v Solano Surf (Petaluma Community Sports Fields)",
        "- May 03, 2026: Revolution FC v Association FC",
        "- May 03, 2026: Solano Surf v California Magic",
        "- May 03, 2026: Pajaro Valley v Folsom Lake Surf",
        "- May 03, 2026: Elk Grove Soccer v Palo Alto SC",
        "- May 03, 2026: Reno APEX SC v SF United FC",
        "- May 03, 2026: El Camino FC v Stanislaus United",
        "- May 03, 2026: San Francisco Elite v Walnut Creek Surf",
        "- May 03, 2026: Valley Surf v Los Gatos United (River Islands Sports Park)",
        "- May 03, 2026: San Ramon FC v Burlingame SC (San Ramon Sports Park - Tiffany Roberts)",
        "- May 03, 2026: North Coast FC v Stanford Strikers10G (Petaluma Community Sports Fields)",
        "- May 03, 2026: Livermore Fusion SC v Eastshore Alliance FC (Robertson Park)",
        "- May 09, 2026: Association FC v San Francisco Elite (Alden E. Oliver Sports Park)",
        "- May 09, 2026: North Coast FC v Palo Alto SC (Petaluma Community Sports Fields)"
    ]

    rlGoldClubs = [
        "Bay Area Surf",
        "COSC",
        "Davis Legacy",
        "De Anza Force",
        "Marin FC",
        "Mustang SC",
        "MVLA",
        "Placer United",
        "Pleasanton RAGE",
        "San Juan SC",
    ]

    rlGoldSched = [
        "- Aug 24, 2025: Bay Area Surf v Marin FC (Gunderson High School)",
        "- Aug 24, 2025: Mustang SC v San Juan SC (Provident Field @ MSC)",
        "- Aug 24, 2025: Pleasanton RAGE v MVLA (Val Vista)",
        "- Aug 24, 2025: Placer United v De Anza Force (Del Oro High School)",
        "- Sep 07, 2025: Placer United v San Juan SC (Placer High School)",
        "- Sep 07, 2025: Marin FC v Mustang SC (Marin Academy)",
        "- Sep 07, 2025: Davis Legacy v Bay Area Surf (Davis Legacy Soccer Complex)",
        "- Sep 07, 2025: Pleasanton RAGE v De Anza Force (Val Vista)",
        "- Sep 14, 2025: Bay Area Surf v Mustang SC",
        "- Sep 14, 2025: MVLA v San Juan SC (Foothill College)",
        "- Sep 14, 2025: COSC v Pleasanton RAGE (Edison High School Fields)",
        "- Sep 14, 2025: De Anza Force v Davis Legacy (De Anza College)",
        "- Sep 14, 2025: Marin FC v Placer United (Dominican University)",
        "- Sep 21, 2025: MVLA v Marin FC (Foothill College)",
        "- Sep 21, 2025: COSC v Mustang SC (Edison High School Fields)",
        "- Sep 21, 2025: Placer United v Bay Area Surf (Del Oro High School)",
        "- Sep 21, 2025: De Anza Force v San Juan SC (Prospect High School)",
        "- Sep 21, 2025: Pleasanton RAGE v Davis Legacy (Val Vista)",
        "- Sep 28, 2025: Davis Legacy v Mustang SC",
        "- Sep 28, 2025: MVLA v Bay Area Surf (Foothill College)",
        "- Sep 28, 2025: San Juan SC v Pleasanton RAGE (San Juan Soccer Complex)",
        "- Sep 28, 2025: Marin FC v De Anza Force (San Rafael High School)",
        "- Sep 28, 2025: COSC v Placer United (Edison High School Fields)",
        "- Oct 05, 2025: Mustang SC v De Anza Force (Provident Field @ MSC)",
        "- Oct 05, 2025: COSC v Bay Area Surf (Edison High School Fields)",
        "- Oct 05, 2025: Pleasanton RAGE v Placer United (Val Vista)",
        "- Oct 05, 2025: Davis Legacy v MVLA (Davis Legacy Soccer Complex)",
        "- Oct 05, 2025: San Juan SC v Marin FC (San Juan Soccer Complex)",
        "- Oct 12, 2025: Marin FC v COSC (College of Marin)",
        "- Oct 12, 2025: Placer United v Mustang SC (Del Oro High School)",
        "- Oct 12, 2025: San Juan SC v Davis Legacy (San Juan Soccer Complex)",
        "- Oct 12, 2025: Bay Area Surf v Pleasanton RAGE (Oak Grove High School)",
        "- Oct 12, 2025: MVLA v De Anza Force (Foothill College)",
        "- Oct 19, 2025: Mustang SC v Pleasanton RAGE (Provident Field @ MSC)",
        "- Oct 19, 2025: De Anza Force v Bay Area Surf (Kathleen MacDonald High School)",
        "- Oct 19, 2025: San Juan SC v COSC (San Juan Soccer Complex)",
        "- Oct 19, 2025: Placer United v MVLA (Del Oro High School)",
        "- Oct 19, 2025: Davis Legacy v Marin FC (Davis Legacy Soccer Complex)",
        "- Nov 01, 2025: Bay Area Surf v MVLA (Gunderson High School)",
        "- Nov 02, 2025: San Juan SC v Mustang SC (San Juan Soccer Complex)",
        "- Nov 02, 2025: De Anza Force v COSC (De Anza College)",
        "- Nov 02, 2025: Davis Legacy v Placer United (Davis Legacy Soccer Complex)",
        "- Nov 02, 2025: Marin FC v Pleasanton RAGE (Dominican University)",
        "- Nov 09, 2025: Mustang SC v Bay Area Surf (Provident Field @ MSC)",
        "- Nov 09, 2025: COSC v Marin FC (San Joaquin Memorial)",
        "- Nov 09, 2025: San Juan SC v MVLA (San Juan Soccer Complex)",
        "- Nov 09, 2025: De Anza Force v Placer United (De Anza College)",
        "- Nov 09, 2025: Davis Legacy v Pleasanton RAGE (Davis Legacy Soccer Complex)",
        "- Nov 15, 2025: MVLA v COSC (Graham Middle School)",
        "- Nov 16, 2025: Mustang SC v Marin FC (Provident Field @ MSC)",
        "- Nov 16, 2025: Pleasanton RAGE v San Juan SC (Stanford Sports Complex)",
        "- Nov 16, 2025: Davis Legacy v De Anza Force (Playfields Park)",
        "- Mar 15, 2026: COSC v MVLA (Edison High School Fields)",
        "- Mar 22, 2026: Bay Area Surf v De Anza Force",
        "- Mar 22, 2026: Mustang SC v MVLA",
        "- Mar 22, 2026: Pleasanton RAGE v COSC",
        "- Mar 22, 2026: San Juan SC v Placer United (San Juan Soccer Complex)",
        "- Mar 22, 2026: Marin FC v Davis Legacy (San Rafael High School)",
        "- Mar 29, 2026: De Anza Force v Mustang SC",
        "- Mar 29, 2026: MVLA v Pleasanton RAGE",
        "- Mar 29, 2026: Placer United v COSC",
        "- Mar 29, 2026: Davis Legacy v Bay Area Surf (Davis Legacy Soccer Complex)",
        "- Mar 29, 2026: Marin FC v San Juan SC (Pickleweed Park)",
        "- Apr 05, 2026: Bay Area Surf v Placer United (Kathleen MacDonald High School)",
        "- Apr 12, 2026: Bay Area Surf v San Juan SC",
        "- Apr 12, 2026: De Anza Force v MVLA",
        "- Apr 12, 2026: Mustang SC v Placer United",
        "- Apr 12, 2026: Pleasanton RAGE v Marin FC",
        "- Apr 12, 2026: Davis Legacy v COSC (Davis Legacy Soccer Complex)",
        "- Apr 18, 2026: COSC v Davis Legacy (Edison High School Fields)",
        "- Apr 19, 2026: Marin FC v Bay Area Surf",
        "- Apr 19, 2026: MVLA v Mustang SC",
        "- Apr 19, 2026: Placer United v Pleasanton RAGE",
        "- Apr 19, 2026: COSC v De Anza Force (Edison High School Fields)",
        "- Apr 19, 2026: Davis Legacy v San Juan SC (Davis Legacy Soccer Complex)",
        "- Apr 26, 2026: De Anza Force v Marin FC",
        "- Apr 26, 2026: Mustang SC v Davis Legacy",
        "- Apr 26, 2026: MVLA v Placer United",
        "- Apr 26, 2026: Pleasanton RAGE v Bay Area Surf",
        "- Apr 26, 2026: COSC v San Juan SC (Edison High School Fields)",
        "- May 03, 2026: Bay Area Surf v COSC",
        "- May 03, 2026: Pleasanton RAGE v Mustang SC",
        "- May 03, 2026: San Juan SC v De Anza Force",
        "- May 03, 2026: Marin FC v MVLA (College of Marin)",
        "- May 03, 2026: Placer United v Davis Legacy (Placer Valley Soccer Complex)",
        "- May 09, 2026: De Anza Force v Pleasanton RAGE",
        "- May 09, 2026: Mustang SC v COSC",
        "- May 09, 2026: MVLA v Davis Legacy",
        "- May 09, 2026: San Juan SC v Bay Area Surf",
        "- May 09, 2026: Placer United v Marin FC (Placer Valley Soccer Complex)"
    ]

    club = ""
    conference = ""
    schedule = ""
    reg = random.randint(0, 1)

    if (leagues == "ECNL"):
        conference = random.choice(allConf)
        if "Mid-Atlantic" in conference:
            club = random.choice(midAtlClubs)
            clubGames = [game for game in midAtlSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Midwest" in conference:
            club = random.choice(midWestClubs)
            clubGames = [game for game in midWestSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Northern Cal" in conference:
            club = random.choice(norCalClubs)
            clubGames = [game for game in norCalSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "North Atlantic" in conference:
            club = random.choice(norAtlClubs)
            clubGames = [game for game in norAtlSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "New England" in conference:
            club = random.choice(newEngClubs)
            clubGames = [game for game in newEngSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Northwest" in conference:
            club = random.choice(nwClubs)
            clubGames = [game for game in nwSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Ohio" in conference:
            club = random.choice(ohioClubs)
            clubGames = []
            numGames = 0
            pickedGames = []
            if random.randint(0, 1) == 0:
                clubGames = [game for game in ohioNorSched if club in game]
                numGames = min(random.randint(2, 5), len(clubGames))
                pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            else:
                clubGames = [game for game in ohioSouSched if club in game]
                numGames = min(random.randint(2, 5), len(clubGames))
                pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Southeast" in conference:
            club = random.choice(seClubs)
            clubGames = [game for game in seSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Southwest" in conference:
            club = random.choice(swClubs)
            clubGames = [game for game in swSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        else:
            club = random.choice(texasClubs)
            clubGames = [game for game in texasSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
    elif (leagues == "GA"):
        club = random.choice(gaClubs)
        if "West Florida" in club:
            matches = pd.read_excel("west-florida.xlsx")
            sample_rows = matches.sample(random.randint(2,5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Florida" in club:
            matches = pd.read_excel("florida-united.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())} {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Indy" in club:
            matches = pd.read_excel("indy.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "St. Louis" in club:
            matches = pd.read_excel("st-louis.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Space Coast" in club:
            matches = pd.read_excel("space-coast.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "SoCal Reds" in club:
            matches = pd.read_excel("socal-reds.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Pinecrest" in club:
            matches = pd.read_excel("pinecrest.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Palm Beach" in club:
            matches = pd.read_excel("palm-beach.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "New York" in club:
            matches = pd.read_excel("new-york.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "MidWest" in club:
            matches = pd.read_excel("midwest.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Las Vegas Sports" in club:
            matches = pd.read_excel("las-vegas-sports.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "LA Surf" in club:
            matches = pd.read_excel("la-surf.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Keystone" in club:
            matches = pd.read_excel("keystone.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "HTX" in club:
            matches = pd.read_excel("htx.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Colorado" in club:
            matches = pd.read_excel("colorado.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Central Illinois" in club:
            matches = pd.read_excel("central-illinois.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Bayside" in club:
            matches = pd.read_excel("bayside.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Baltimore" in club:
            matches = pd.read_excel("baltimore.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Las Vegas" in club:
            matches = pd.read_excel("las-vegas.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "San Diego" in club:
            matches = pd.read_excel("san-diego.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "TopHat" in club:
            matches = pd.read_excel("tophat.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        elif "Santa Clara" in club:
            matches = pd.read_excel("santa-clara.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
        else:
            matches = pd.read_excel("real-futbol.xlsx")
            sample_rows = matches.sample(random.randint(2, 5))

            schedList = []
            for _, row in sample_rows.iterrows():
                line = f'- {" ".join(str(row["Date"]).split())}: {row["Team1"].strip()} v {row["Team2"].strip()} ({row["Location"].strip()})'
                schedList.append(line)

            schedule = "\n".join(schedList)

            conference = row["Conference"] + " Conference"
    else:
        conference = random.choice(rlConf)
        if "Florida" in conference:
            if reg == 0:
                club = random.choice(rlFLSouClubs)
                clubGames = [game for game in rlFLSouSched if club in game]
                numGames = min(random.randint(2, 5), len(clubGames))
                pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
                schedule += "\n".join(pickedGames)
            else:
                club = random.choice(rlFLNorClubs)
                clubGames = [game for game in rlFLNorSched if club in game]
                numGames = min(random.randint(2, 5), len(clubGames))
                pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
                schedule += "\n".join(pickedGames)
        elif "Mid-" in conference:
            club = random.choice(rlMidClubs)
            clubGames = [game for game in rlMidSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Mountain" in conference:
            club = random.choice(rlMounClub)
            clubGames = [game for game in rlMounSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Michigan" in conference:
            club = random.choice(rlMichClubs)
            clubGames = [game for game in rlMichSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Northwest" in conference:
            club = random.choice(rlNWClubs)
            clubGames = [game for game in rlNWSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "Southern" in conference:
            club = random.choice(rlSoCalClubs)
            clubGames = [game for game in rlSoCalSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)
        elif "NorCal" in conference:
            club = random.choice(rlNorCalClubs)
            clubGames = [game for game in rlNorCalSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n- ".join(pickedGames)
        else:
            club = random.choice(rlGoldClubs)
            clubGames = [game for game in rlGoldSched if club in game]
            numGames = min(random.randint(2, 5), len(clubGames))
            pickedGames = random.sample(clubGames, numGames) if numGames > 0 else []
            schedule += "\n".join(pickedGames)

    positionList = [
        "Goalkeeper",
        "Right Fullback",
        "Left Fullback",
        "Center Back",
        "Center Back/Sweeper",
        "Defensive Midfielder",
        "Right Midfielder/Winger",
        "Center Midfielder",
        "Striker",
        "Attacking Midfielder",
        "Left Midfielder/Left Winger",
    ]

    position = random.choice(positionList)

    # email content

    openers = [
        "My name is " + first + ".",
        "My name is " + first + ". I play for the " + club + " " + leagues + " team.",
        "My name is " + first + ". I play for the " + club + " " + leagues + " team"
            + " as a " + position + ".",
        "I hope this message finds you well. My name is " + first + " " + last +
            " and I play on the " + club + " " + leagues + " team.",
        "I am excited to share my schedule and invite you to the " + leagues
            + " game over the weekend.",
        "I am excited to share my schedule and invite you to the " + club
            + leagues + " game over the weekend.",
        "I wanted to introduce myself. My name is " + first + " " + last +
            " and I was excited to see that Purdue is coming to my camp.",
        "I wanted to introduce myself. My name is " + first + " " + last +
            " and I was excited to see that Purdue is coming to my state.",
        "I wanted to introduce myself. My name is " + first + " " + last +
            " and I play for the " + club + " " + leagues + " team.",
        "I would like to re-introduce myself. My name is " + first + " " + last +
            ". I play for the " + club + " " + leagues + " team.",
        "I hope you're doing well. I wanted to share a quick update and let you "
            + "know that I'll be competing at the upcoming " + leagues
            + " showcase this month.",
        "I hope you're doing well. I wanted to share a quick update and let you "
            + "know that I'll be competing at the upcoming " + leagues
            + " showcase this weekend.",
        "I hope this email finds you well. I am " + first + " " + last + " and I play"
            + " for the " + club + " " + leagues + " team.",
        "Thank you again for driving through the snow and attending our "
            + club + " showcase events.",
        "Thank you for coming to my game.",
        "Thank you for driving through the snow and attending our "
            + club + " showcase events.",
        "Thank you again for attending our " + club + " showcase events.",
        "Thank you for attending our " + club + " showcase events.",
        "I hope you enjoyed your break. I am excited to see that you'll be "
            + "attending the " + club + " " + leagues + " showcase and I would truly"
            + " appreciate you taking the time to watch me compete.",
        "I hope you enjoyed your weekend. I am excited to see that you'll be "
            + "attending the " + club + " " + leagues + " showcase and I would truly"
            + " appreciate you taking the time to watch me compete.",
        "I recently competed in the " + leagues + " showcase and I wanted"
            + " to share a short highlight video from those matches.",
        "I play for the " + club + " " + leagues + " team.",
        "I wanted to introduce myself and express my excitement about Purdue attending my camp."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I hope you're doing well. I wanted to reach out and introduce myself."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I wanted to share a quick update and introduce myself as a prospective student-athlete."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I’m reaching out because I was excited to see that you’ll be attending an upcoming event I’m participating in."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I wanted to take a moment to introduce myself and share my interest in your program."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I hope you’re having a great week. I wanted to reach out and provide a brief introduction."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I wanted to reach out after seeing that Purdue will be in attendance at one of my upcoming events."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I’m excited to introduce myself and share some information about my recruiting journey."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I wanted to connect and express my interest in Purdue’s soccer program."
            + " My name is " + first + " " + last + " and I play for the " + club + " " + leagues + ".",
        "I hope you’re having a great day. I wanted to reach out and share some information about my recruiting journey.",
        "I wanted to reach out after seeing your team’s recent success this season.",
        "I hope this email finds you well. I wanted to provide a brief update ahead of the upcoming showcase.",
        "I wanted to reach out ahead of this weekend’s games to share my schedule.",
        "I hope you're doing well. I wanted to follow up and express my continued interest in Purdue.",
        "I wanted to introduce myself and share my excitement about the opportunity to compete at the collegiate level.",
        "I hope you’re having a great week. I wanted to connect and introduce myself as a prospective student-athlete.",
        "I wanted to reach out and thank you for your time and consideration.",
        "I’m reaching out to share my schedule and express my interest in your program.",
        "I wanted to provide a quick introduction ahead of the upcoming showcase.",
        "I compete for the " + club + " " + leagues + " team."
    ]

    context = [
        "I'm a " + position + " and I'm very interested in learning more about your program and would love the "
            + "opportunity to attend an ID camp and explore the possibility of playing soccer at Purdue.",
        "I'm a " + position + " and I'm very interested in learning more about Purdue's program. I would love the "
            + "opportunity to explore the possibility of playing soccer at your school.",
        "I'm a " + position + " scored " + str(random.randint(1, 5)) + " goals and had " + str(random.randint(1, 5))
            + " assists last weekend.",
        "I am a Class of 2028 " + position + " with a strong interest in Purdue, both academically"
            + " and athletically.",
        "I am a " + position + " sophomore in the graduating Class of 2028 with a " + str(GPA) + " GPA.",
        "I understand that you will have a representative for your team at the camp I am "
             + "attending. I play " + position + " and I hope to get time to meet and talk"
             + " to them and learn more about your team's needs.",
        "I am honored to be selected for an 'all-star' match, representing the top players in the league.",
        "I am contacting you today because I am interested in attending and playing soccer at Purdue University."
            + " I am a strong " + position + " player with a " + GPA + " GPA.",
        "I am contacting you today because I am interested in attending and playing soccer at Purdue University."
            + " I believe I could be an asset to your team both on the field as an athlete and off the field as a student.",
        "I am a " + position + " and I am interested in your school.",
        "I am a " + position + " in the Class of 2028 and focused on continuing my development",
        "I maintain a " + GPA + " GPA and is an excellent " + position + ".",
        "I am a 2028 " + position + " and excited about the opportunity to continue my development in this environment.",
        "I am a sophomore, graduating 2028 and I play " + position + ".",
        "I am a " + position + " for the " + club + " team.",
        "I'm excited to see that you'll be attending the " + leagues + " Showcase and I would truly appreciate you taking the time to"
            + " watch me compete. It would be an honor to have you attend my games this weekend.",
        "I'm a " + position + " and currently compete in the " + leagues + " league.",
        "I currently serve as a team captain and bring strong leadership on and off the field.",
        "I recently competed in a " + leagues + " weekend of games.",
        "I'll be competing at an upcoming " + leagues + " showcase this weekend.",
        "I am a versatile " + position + " who can contribute in multiple roles.",
        "I am a " + position + " who values both technical development and team success.",
        "I currently compete at a high level and am focused on improving every aspect of my game.",
        "I play a key role within my team and take pride in my work ethic.",
        "I am a " + position + " in the Class of 2028 who is highly motivated to play at the next level.",
        "I compete regularly against top clubs in the " + leagues + " league.",
        "I am committed to balancing strong academics with competitive soccer.",
        "I take pride in being a coachable and disciplined player.",
        "I am focused on continuing to grow physically, technically, and tactically.",
        "I bring leadership, consistency, and energy to every match.",
        "I primarily play as a " + position + ", but I also have experience in other positions, which has helped me become"
            + " a more adaptable player.",
        "As a " + position + ", I bring composure on the ball, strong decision-making, and a physical presence in the air"
            + " and in 1v1 situations."
    ]

    # i wanna play soccer
    main = [
        "I have been looking into your team, the campus, and the academic opportunities and I feel like"
            + " your school would be a great fit for me.",
        "I am taking rigorous courses such as AP Precalculus, AP Spanish Language, and AP World History while maintaining"
            + " my GPA and excelling in my games.",
        "If you come to my matches, you may just find your diamond (me)!",
        "From my first kick at age " + str(random.randint(3, 6)) + ", my passion for soccer has driven me with unwavering"
            + " determination. Now, at age 16, I'm even more committed to excelling and would like to share how I align with your"
            +  " team's goals.",
        "I am very interested in learning more about your program and would love to stay in touch moving forward." +
            " If you are recruiting a " + position + " for the Class of 2028, I would really appreciate the opportunity to remain connected.",
        "I am currently uncommitted, but working towards making the best choice. If you would like to learn more about me, please " +
            "contact my coaches.",
        "I am a captain this year and I have a strong passion for the game with a goal of playing at the collegiate level while" +
            " achieving my academic goals when I graduate in 2028.",
        "I want to experience college as a Purdue student athlete, and ultimately convince you that I would be a valuable part of the"
            + " Big Ten championship. I want to be the best " + position + " you've ever had.",
        "I've had success regularly scoring against and beating these top clubs, and I currently lead my team in goals." +
            " I get to train and compete alongside teammates who have been called up to youth national teams for various countries" +
            " and that pushes us to a higher level every day!",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Wisconsin this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Illinois this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Washington this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Michigan this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against UCLA this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Penn State this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Northwestern this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Ohio this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against USC this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Michigan this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Indiana this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Nebraska this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Minnesota this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Rutgers this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Maryland this past season. I would love the opportunity to compete at this high of a level.",
        "I think it would be great to play for your program because of your success on the field, such as leading your team to an upset"
            + " against Oregon this past season. I would love the opportunity to compete at this high of a level.",
        "I am very interested in learning more about Purdue’s program and would love the opportunity to explore the possibility of playing soccer at your school.",
        "I believe Purdue would be a great fit for me both athletically and academically.",
        "I think it would be an incredible opportunity to compete at a high level within your program.",
        "I admire the success of your team and would love the chance to contribute to that environment.",
        "I am very interested in staying connected throughout the recruiting process.",
        "I would love the opportunity to attend an ID camp and learn more about your program.",
        "I am excited about the possibility of continuing my development within your program.",
        "I am eager to find a program that challenges me and supports my long-term goals.",
        "I am extremely interested in Purdue University because of the opportunities your program provides, as well as strong academics.",
        "As I go through the recruiting process, I'm really looking forward to finding a school that fits me both academically and athletically."
            + " I remain very interested in your school. I would love the opportunity to continue learning more about your program.",
        "I wanted to thank you for making it to our games; it means a lot."
        "I believe my work ethic and mindset would allow me to contribute positively to your program.",
        "I am confident that my skill set aligns well with the style of play within your program.",
        "I am motivated to compete at the Big Ten level and continue developing as a player.",
        "I value programs that emphasize both competitive excellence and academic success.",
        "I am committed to pushing myself every day to reach my full potential as a student-athlete.",
        "I believe Purdue provides an environment that would challenge me and help me grow.",
        "I take pride in representing my team with professionalism and intensity.",
        "I am eager to learn more about your expectations and what you look for in prospective players.",
        "I am excited by the opportunity to compete against top-level competition.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Minnesota.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Indiana.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Iowa.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Wisconsin.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Nebraska.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Ohio.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Illinois.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Michigan.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Washington.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against UCLA.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Penn State.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Maryland.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Rutgers.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Oregon.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against USC.",
        "I would like to congratulate your team on achieving a " + str(random.randint(1, 4)) + "-0 shutout victory against"
            + " against Northwestern.",
        "I'm reaching out because the Boilermakers program at Purdue University, West Lafayette is one I'm very interested in."
    ]

    # glaze purdue kinda
    main2 = [
        "I am interested in the medical field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the engineering field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the computer science field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the business field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the veterinary field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the dental field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the AI field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the data science field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the IT field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the economics field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I am interested in the psychology field and your school offers a great curriculum. I love the overall culture"
        + " that it has. I feel that I am great at what I do and I hope to visit during one of my upcoming soccer trips!",
        "I know that Purdue University has a good psychology program and I hope to one day have a career in sports using psychology." +
        " Sports, especially soccer, is my passion.",
        "I know that Purdue University has a good CS program and I hope to one day have a career in sports using CS." +
        " Sports, especially soccer, is my passion.",
        "I know that Purdue University has a good engineering program and I hope to one day have a career in sports using engineering." +
        " Sports, especially soccer, is my passion.",
        "I know that Purdue University has a good business program and I hope to one day have a career in sports using business." +
        " Sports, especially soccer, is my passion.",
        "I know that Purdue University has a good economics program and I hope to one day have a career in sports using economics." +
        " Sports, especially soccer, is my passion.",
        "I know that Purdue University has a good analytics program and I hope to one day have a career in sports using analytics." +
        " Sports, especially soccer, is my passion.",
        "It would be an honor to have you attend one of my games this weekend.",
        "I would love the opportunity to visit campus during one of my upcoming soccer trips.",
        "I am interested in engineering and hope to one day pursue a career in sports using that background.",
        "I am interested in CS and hope to one day pursue a career in sports using that background.",
        "I am interested in analytics and hope to one day pursue a career in sports using that background.",
        "I am interested in economics and hope to one day pursue a career in sports using that background.",
        "I am interested in business and hope to one day pursue a career in sports using that background.",
        "I am interested in psychology and hope to one day pursue a career in sports using that background.",
        "I value strong academics and am looking for a university that prepares me for life beyond soccer.",
        "I am interested in combining athletics with a challenging academic program.",
        "I hope to pursue a career where I can stay connected to sports beyond my playing career.",
        "I am passionate about learning and continuously improving both on and off the field.",
        "I would love the opportunity to meet the coaching staff and learn more about the program culture.",
        "I am excited by the balance Purdue offers between athletics, academics, and campus life.",
        "I am interested in exploring internship and research opportunities while competing as a student-athlete.",
        "I value leadership, accountability, and growth within a team environment.",
        "I am excited about the opportunity to represent Purdue both on and off the field.",
        "My collegiate aspirations are to play soccer at the highest level while pursing my academic interests."
            + " College soccer will offer not only athletic opportunities but also an environment conducive to growth.",
        "I also wanted to congratulate you on coaching two players that signed professional contracts this year! "
            + "I hope to reach that sort of achievement with your team.",
        "Purdue stands out to me because of its strong academics and competitive athletics, and I would love the"
            + " opportunity to continue developing as a student athlete in an environment like yours.",
        "I love your school's program, campus and I find myself being a good fit there.",
        "Though I am currently undecided on my major, I have definitively decided that Purdue is the school for me."
            + " I appreciate the broad selection you guys have to offer and your excellent soccer program that I would"
            + " love to be a part of.",
        "I am very interested in attending Purdue University because of the women's soccer program's competitive Big Ten"
            + " environment and the strong academics.",
        "Your beautiful campus and sense of school spirit is exactly what I am looking for as a student athlete.",
        "I take pride in reading the game, breaking up plays, and connecting clean passes out of the back.",
        "Purdue stands out to me because of its outstanding academic reputation, strong values, and the opportunities it"
            + " provides for student-athletes to succeed both during and after college.",
        "I am interested in playing at Purdue University due to hte quality of your program, the way your team plays,"
            + " and the opportunity to play D1 soccer.",
    ]

    # sell urself
    main3 = [
        "Eager to contribute, learn from your coaching and stand out as a dedicated tema member"
            + ", I'm excited at the prospect of bringing my unique blend of dedication and skill to your team.",
        "What sets me apart is my relentless pursuit of improvement. I embrace challenges as stepping stones, and I thrive"
            + " under pressure, constantly learning.",
        "On and off the field, I blend perseverance, teamwork, and humility. I uplift teammates to achieve success.",
        "I'm more than just a player; I'm a driven athlete with dreams, a resilient teammate, and a diligent scholar.",
        "I hope you'll watch my play as I'm excited to show you how I can contribute to Purdue in a few years!",
        "I would appreciate the chance to stay in touch as the recruiting process continues.",
        "As a player, I'm best known for my speed, high press, and finishing. I would love for you to see me in action!",
        "I'm a versatile and coachable player who incorporates creative elements in my play to help my team succeed.",
        "I am in the process of looking at schools and I know I want to play D1 soccer.",
        "I have additional resources showcasing my abilities on the pitch if you should be interested.",
        "I can contribute to your team with my IQ and ability to read the game and predict the play, my quick thinking and"
            + " fast moves are truly valuable assets.",
        "I am driven, determined, versatile and really interested in being a part of your 2028 recruiting class!",
        "I would love to be added to your recruiting watchlist. I plan to follow up before upcoming showcases and with"
            + " with progress updates throughout my season.",
        "I'd appreciate it if you'd add me to any mailing lists for camps, clinics, or other program events!"
    ]

    closings = [
        "Thanks so much,",
        "Thank you,",
        "Best regards,",
        "Looking forward to hearing from you,",
        "Sincerely,",
        "Thank you for your time,",
        "Thank you for your time and consideration,"
        "Thanks,",
        "Best,",
    ]

    outro = [
        "Thank you for your time. Boiler up!",
        "Thank you for your time. Go Boilermakers!",
        "Safe travels.",
        "Thank you for your time and consideration!",
        "Thank you again for your time, and I hope to connect with you at the event.",
        "Feel free to contact me. I would love to talk!",
        "If you are interested, I would love it if you could see me play in a tournament environment!",
        "If you have available time, I would love if you'd stop by and watch me play!",
        "I would love the opportunity to show you my game in person at the last showcase before June 15th and playoffs!",
        "I look forward to hearing from you.",
        "I would love yo see you at a game to watch me play!",
        "I hope to see you on the sidelines, and I look forward to staying in touch!",
        "Please feel free to reach out if you need any additional information.",
        "I hope you or a member of your staff will be able to see me play.",
        "I would love the opportunity to play in front of you next weekend!"
        ]


    wnt = [
        "Spain WNT",
        "United States WNT",
        "Germany WNT",
        "England WNT",
        "Sweden WNT",
        "Brazil WNT",
        "France WNT",
        "Japan WNT",
        "Canada WNT",
        "Netherlands WNT",
        "Norway WNT",
        "Italy WNT",
        "Denmark WNT",
        "Australia WNT",
        "Iceland WNT",
        "China WNT",
        "Belgium WNT",
        "Austria WNT",
        "Colombia WNT"
    ]

    month = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    soccerECNL = [
        "- U17 " + random.choice(wnt) + " " + random.choice(month) + " " + str(random.randint(2024, 2026)),
        "- U16 " + random.choice(wnt) + " " + random.choice(month) + " " + str(random.randint(2024, 2026)),
        "- U15 " + random.choice(wnt) + " " + random.choice(month) + " " + str(random.randint(2024, 2026)),
        "- U" + str(random.randint(15, 17)) + " ECNL " + random.choice(allConf) + " 2024-2025",
        "- ECNL National Champion " + str(random.randint(2024, 2026)),
        "- ECNL National Finalist " + str(random.randint(2024, 2026)),
        "- ECNL National Playoffs Participant " + str(random.randint(2024, 2026)),
        "- ECNL National Selection Game Invitee " + str(random.randint(2024, 2026)),
        "- ECNL All-Conference First Team " + str(random.randint(2024, 2026)),
        "- ECNL All-Conference Second Team " + str(random.randint(2024, 2026)),
        "- ECNL Conference Golden Boot " + str(random.randint(2024, 2026)),
        "- ECNL Conference Golden Glove " + str(random.randint(2024, 2026)),
        "- ECNL Phoenix Showcase Standout XI",
        "- ECNL Florida Showcase Invitee",
        "- U.S. Youth National Team Regional ID Center Invitee",
        "- Team capitan " + str(random.randint(2024, 2026)),
        "- ECNL All-American Team" + str(random.randint(2024, 2026)),
        "- " + str(random.randint(2, 8)) + " time USYNT ID Center Invitee"
    ]

    soccerGA = [
        "- U17 " + random.choice(wnt) + " " + random.choice(month) + " " + str(random.randint(2024, 2026)),
        "- U16 " + random.choice(wnt) + " " + random.choice(month) + " " + str(random.randint(2024, 2026)),
        "- U15 " + random.choice(wnt) + " " + random.choice(month) + " " + str(random.randint(2024, 2026)),
        "- U" + str(random.randint(15, 17)) + " GA " + random.choice(allConf) + " Conference 2024-2025",
        "- GA Champions Cup Qualifier " + str(random.randint(2024, 2026)),
        "- " + str(random.randint(2024, 2026)) + " GA National Talent ID Invitee",
        "- " + str(random.randint(2024, 2026)) + " GA All-Star Team Selection",
        "- GA Playoffs Participant " + str(random.randint(2024, 2026)),
        "- GA National Finalist " + str(random.randint(2024, 2026)),
        "- GA National Champion " + str(random.randint(2024, 2026)),
        "- GA Golden Boot Nominee",
        "- GA Golden Glove Nominee",
        "- " + random.choice(wnt) + " U" + str(random.randint(15, 17)) + " Camp Invitee",
        "- Team capitan " + str(random.randint(2024, 2026)),
    ]

    soccerECNLRL = [
        "- U17 ECNL RL" + random.choice(allConf) + " Conference 2024-2025",
        "- U16 ECNL RL" + random.choice(allConf) + " Conference 2024-2025",
        "- U15 ECNL RL" + random.choice(allConf) + " Conference 2024-2025",
        "- ECNL RL Conference Champion " + str(random.randint(2024, 2026)),
        "- ECNL RL Conference Finalist " + str(random.randint(2024, 2026)),
        "- ECNL RL Playoffs Participant " + str(random.randint(2024, 2026)),
        "- ECNL RL National Finals Qualifier " + str(random.randint(2024, 2026)),
        "- ECNL RL All-Conference First Team " + str(random.randint(2024, 2026)),
        "- ECNL RL All-Conference Second Team " + str(random.randint(2024, 2026)),
        "- ECNL RL Conference Golden Boot " + str(random.randint(2024, 2026)),
        "- ECNL RL Conference Golden Glove " + str(random.randint(2024, 2026)),
        "- ECNL RL Regional Selection Game Invitee",
        "- ECNL RL Showcase Standout XI",
        "- Promoted to ECNL First Team " + str(random.randint(2024, 2026))
    ]

    academic = [
        "- " + GPA + " Unweighted GPA",
        "- 4." + str(random.randint(3, 8)) + " Weighted GPA",
        "- Top " + str(random.choice([5, 10, 15])) + "% of Class",
        "- Principal’s Honor Roll (All Semesters)",
        "- National Honor Society Member",
        "- AP Scholar with Distinction",
        "- Completed " + str(random.randint(6, 12)) + " AP Courses",
        "- Dual Enrollment Student",
        "- Student-Athlete Academic Award",
        "- Academic All-Conference",
        "- " + str(random.randint(100, 300)) + "+ Community Service Hours",
        "- Volunteer Youth Soccer Coach",
        "- STEM Club President",
        "- Peer Math Tutor",
        "- National Science Honor Society Member",
        "- Mu Alpha Theta Member",
        "- DECA Member",
        "- High Honor Roll"
    ]

    # phone number

    phone = "("

    for i in range (0, 3):
        phone += str(random.randint(0, 9))

    phone += ") "

    for i in range(0, 3):
        phone += str(random.randint(0, 9))

    phone += "-"

    for i in range(0, 4):
        phone += str(random.randint(0, 9))

    # email

    studentEmail = ""
    x = random.randint(0, 3)

    if x == 0:
        studentEmail += last
    elif x == 1:
        studentEmail += first
    elif x == 2:
        studentEmail += first + last
    else:
        studentEmail += last + first

    x = random.randint(0, 2)
    if x == 0:
        studentEmail += "soccer"
    elif x == 1:
        studentEmail += str(random.randint(0, 9))
    else:
        studentEmail += str(random.randint(0, 9)) + str(random.randint(0, 9))

    emailDom = [
        "@gmail.com",
        "@yahoo.com",
        "@hotmail.com",
        "@outlook.com",
    ]

    studentEmail += str("".join(random.choices(emailDom, weights = [7, 1, 1, 1], k = 1)))
    studentEmail = studentEmail.lower()

    # youtube
    yt = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=MCWJNOfJoSM",
        "https://www.youtube.com/watch?v=8C3we1FSAA0",
        "https://www.youtube.com/watch?v=_RD6s35qC4g",
        "https://www.youtube.com/watch?v=ksG9O8PHXbI",
        "https://www.youtube.com/watch?v=_C0k7buhrwk",
        "https://www.youtube.com/watch?v=ttzRTS7INrk"
    ]

    # x

    xAcc = "@"
    x = random.randint(0, 2)
    if x == 0:
        xAcc += first
    elif x == 1:
        xAcc += last
    else:
        xAcc += first + last

    x = random.randint(0, 2)
    if x == 0:
        xAcc += "Soccer"
    elif x == 1:
        xAcc += str(random.randint(0, 9))
    else:
        xAcc += str(random.randint(0, 9)) + str(random.randint(0, 9))

    # instagram
    ig = "@"
    x = random.randint(0, 2)
    if x == 0:
        ig += first
    elif x == 1:
        ig += last
    else:
        ig += first + last

    x = random.randint(0, 2)
    if x == 0:
        ig += "Soccer"
    elif x == 1:
        ig += str(random.randint(0, 9))
    else:
        ig += str(random.randint(0, 9)) + str(random.randint(0, 9))

    email = "From: " + first + " " + last + " <" + studentEmail + ">\n"

    # print recipients
    email += "To: " + TO
    greeting = ""

    if numOfCC != 0:
        email += "\nCC: " + CC
        greeting = random.choice(greetingsMulti)

    if numOfCC == 0:
        greeting = random.choice(greetingsSingle)

    # greeting + coach names
    k = random.randint(0, 1)
    if k == 1:
        if "Coach" in greeting:
            if "esmaster@purdue.edu" in TO:
                email += "\n\n" + greeting + " Masters"
            elif "rmoodie@purdue.edu" in TO:
                email += "\n\n" + greeting + " Moodie"
            elif "robward@purdue.edu" in TO:
                email += "\n\n" + greeting + " Ward"
            else:
                email += "\n\n" + greeting + " Hamner"

            for i in listCC:
                if listCC.index(i) == len(listCC) - 1:
                    email += ", and"
                else:
                    email += ","

                if  "esmaster@purdue.edu" in i:
                    email += " Masters"
                elif "rmoodie@purdue.edu" in i:
                    email += " Moodie"
                elif "robward@purdue.edu" in i:
                    email += " Ward"
                else:
                    email += " Hamner"

            email += ","
        else:
            email += "\n\n" + greeting + ","

    else:
        email += "\n\n" + greeting + ","

    email += "\n\n" + random.choice(openers) + "\n" + random.choice(context) + "\n" + random.choice(main)

    n = random.randint(0, 1)
    if (n == 1):
        email += "\n" + random.choice(main2)
        n = random.randint(0, 1)
        if (n == 1):
            email += "\n" + random.choice(main3)

    o = random.randint(0, 1)
    if (o == 1):
        email += "\n" + random.choice(outro)

    s = random.randint(0, 10)
    stat = ""
    if (s >= 9):
        if (s == 10):
            email += "\n\nHere are some of my academic accomplishments:"
            for i in academic:
                if random.randint(0, 2) == 0:
                    email += "\n" + i

        email += "\n\nHere are some of my soccer accomplishments:"
        if leagues == "ECNL":
            for i in soccerECNL:
                if random.randint(0, 2) == 0:
                    email += "\n" + i
        elif leagues == "GA":
            for i in soccerGA:
                if random.randint(0, 2) == 0:
                    email += "\n" + i
        else:
            for i in soccerECNLRL:
                if random.randint(0, 2) == 0:
                    email += "\n" + i

    p = random.randint(0, 2)
    if (p >= 1):
        email += "\n\nMy schedule:" + "\n" + schedule

    email += "\n\n" + random.choice(closings) + "\n" + first + " " + last

    if (p == 2):
        email += "\n\n" + club + " " + leagues + "\n" + "Class of 2028" + "\n" + position
        if random.randint(0, 1) == 0:
            email += "\nInstagram: " + ig
        if random.randint(0, 1) == 0:
            email += "\nX: " + xAcc
        if random.randint(0, 1) == 0:
            email += "\nYouTube: " + random.choice(yt) + " (please don't click on links you don't trust!!!!)"
        email += "\nEmail: " + studentEmail +"\nPhone: " + phone

    return email

# GENERATE MULTIPLE VERSIONS
NUM_EMAILS = 5

for i in range(NUM_EMAILS):
    print(f"----- OPTION {i+1} -----")
    print(generate_emails())