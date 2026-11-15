# TO THE STARS AND BEYOND: A Day Beneath Mars
# Ren'Py 8.x / 1280 x 720. Replace the built-in image declarations with art
# when available; the placeholders keep the prototype playable without assets.
# Educational tutorial: engineering timings and energy costs are game values.


define nova = Character("NOVA", color="#91DDF9")
define aya = Character("Commander Aya", color="#FFE2AB")
define rio = Character("Botanist Rio", color="#B5EEBB")
define sol = Character("Engineer Sol", color="#E8BCFF")

# Use available room art, with built-in fallbacks for rooms that have no image yet.
image bg lobby = Transform("bg_lobby.jpeg", xysize=(1280, 720))
image bg quarters = Transform("bg_quarters.png", xysize=(1280, 720))
image bg greenhouse = Transform("bg_greenhouse.jpeg", xysize=(1280, 720))
image bg water lab = Transform("bg_water_lab.jpeg", xysize=(1280, 720))
image bg life support = Transform("bg_life_support.png", xysize=(1280, 720))
image bg gym = Transform("bg_gym.jpeg", xysize=(1280, 720))
image bg comms = Transform("bg_comms.jpeg", xysize=(1280, 720))
image bg airlock = Transform("bg_airlock.png", xysize=(1280, 720))
image bg surface = Transform("bg_surface.png", xysize=(1280, 720))
image bg impact = Transform("bg_impact.jpeg", xysize=(1280, 720))
image bg rover camera = Transform("bg_rover_cam.jpeg", xysize=(1280, 720))

play music "audio/Space Cinematic Ambient Free Music No Copyright.mp3" loop volume 0.5

# A lightweight, consistent style for buttons (no external GUI assets needed).
style mars_button:
    background "#243B51"
    hover_background "#397188"
    insensitive_background "#1E2938"
    xpadding 14
    ypadding 9
style mars_button_text:
    color "#F0F8FF"
    hover_color "#FFFFFF"
    insensitive_color "#7C91A1"
    size 19
style small_mars_button is mars_button:
    xpadding 8
    ypadding 6
style small_mars_button_text is mars_button_text:
    size 16
style action_mars_button is mars_button:
    background "#284F62"
    hover_background "#4A9DA6"
    xpadding 10
    ypadding 12
style action_mars_button_text is mars_button_text:
    size 19

init python:
    # Rooms form an actual navigable graph. Directions are deliberate:
    # the only route outside is through the airlock.
    ROOMS = {
        "lobby": {"name": "CENTRAL LOBBY", "bg": "bg lobby", "description": "The heart of the underground settlement.",
                  "exits": {"left": "quarters", "right": "greenhouse", "up": "life_support", "down": "airlock"}},
        "quarters": {"name": "SLEEPING QUARTERS", "bg": "bg quarters", "description": "Four beds, four explorers, one home away from Earth.",
                     "exits": {"right": "lobby", "up": "comms"}},
        "greenhouse": {"name": "GREENHOUSE", "bg": "bg greenhouse", "description": "The plants live on clean water, nutrients and managed light.",
                       "exits": {"left": "lobby", "right": "water_lab"}},
        "water_lab": {"name": "WATER LAB", "bg": "bg water lab", "description": "Recycling and testing keep the water loop safe.",
                      "exits": {"left": "greenhouse", "right": "life_support"}},
        "life_support": {"name": "LIFE SUPPORT", "bg": "bg life support", "description": "Sensors guard the atmosphere and radiation shelter.",
                         "exits": {"left": "water_lab", "right": "gym", "down": "lobby"}},
        "gym": {"name": "EXERCISE ROOM", "bg": "bg gym", "description": "A treadmill, cycle and resistance equipment.",
                "exits": {"left": "life_support", "right": "comms"}},
        "comms": {"name": "COMMUNICATIONS", "bg": "bg comms", "description": "Messages to Earth cannot arrive immediately.",
                  "exits": {"left": "gym", "down": "quarters"}},
        "airlock": {"name": "AIRLOCK", "bg": "bg airlock", "description": "Check the seals and command robots before going outside.",
                    "exits": {"up": "lobby", "down": "surface"}},
        "surface": {"name": "MARS SURFACE FEED", "bg": "bg surface", "description": "Remote view of two rovers and solar arrays; you remain indoors.",
                    "exits": {"up": "airlock", "right": "impact"}},
        "impact": {"name": "IMPACT FIELD FEED", "bg": "bg impact", "description": "Remote close-up of meteorite fragments and old impact scars.",
                   "exits": {"left": "surface"}},
    }

    # Position labels and map nodes, informational only (no teleporting).
    MAP_NODES = [
        ("quarters", 78, 275), ("lobby", 330, 275), ("greenhouse", 595, 275), ("water_lab", 885, 275),
        ("life_support", 330, 115), ("gym", 595, 115), ("comms", 885, 115),
        ("airlock", 330, 430), ("surface", 595, 430), ("impact", 885, 430),
    ]

    # Task locations and original 460-minute / 80% total budget.
    TASKS = [
        ("farm", "Grow crops", "greenhouse", 50, 12),
        ("rover", "Collect a rover sample", "surface", 60, 14),
        ("water", "Service water recycling", "water_lab", 40, 10),
        ("air", "Balance the cabin air", "life_support", 45, 8),
        ("exercise", "Complete crew exercise", "gym", 120, 12),
        ("mining", "Study impact fragments", "impact", 70, 12),
        ("solar", "Clean solar arrays", "surface", 35, 6),
        ("morale", "Support the crew", "comms", 40, 6),
    ]
    TASK_BY_ID = {row[0]: row for row in TASKS}

    # Each mission has one reasoning decision followed by three or four
    # REAL clickable actions. Correct actions advance, unsafe actions explain
    # the problem and let the child retry. Their positions are shuffled.
    TASK_INFO = {
        "farm": {
            "intro": "The seedlings are wilting. Rio asks you to rescue the crop without wasting water.",
            "question": "How should you investigate the unhealthy plants?",
            "choices": [
                ("Read the moisture and nutrient sensors first", True, ""),
                ("Pour untreated Martian dirt on every plant", False, "Martian regolith may contain harmful compounds; the crop needs a controlled system."),
                ("Turn off every sensor to save energy", False, "Without measurements, you could harm the whole crop."),
            ],
            "steps": [
                ("A sensor says the roots are dry. Find the correct control!", [("READ ROOT DATA", True, ""), ("IGNORE SENSORS", False, "The plants need a diagnosis first."), ("EMPTY TANK", False, "Do not waste the water reserve.")]),
                ("The roots need a measured drink.", [("START METERED PUMP", True, ""), ("FLOOD ALL TRAYS", False, "Too much water can harm plants."), ("ADD RAW DIRT", False, "This is a water-based growing system.")]),
                ("Light is low under the soil shielding.", [("ALIGN LIGHT PIPE", True, ""), ("BREAK THE MIRROR", False, "The mirrors guide light to the crops."), ("DISABLE ALL LIGHT", False, "Plants need enough useful light to grow.")]),
            ],
            "success": "Rio sees the leaves lifting. You saved the crop by checking data before acting."
        },
        "rover": {
            "intro": "One of the two rovers has detected a promising sample. NOVA gives you one minute of real time to practise the route.",
            "question": "What is the safest first step for a remote rover?",
            "choices": [
                ("Scan the terrain and plan a route", True, ""),
                ("Drive straight toward the steepest slope", False, "A rover can become trapped or flip on unsafe ground."),
                ("Ignore the battery reading", False, "The rover needs power to finish and transmit its findings."),
            ],
            "steps": [
                ("Camera view: rocks block the centre. Where should you steer?", [("TURN RIGHT", True, ""), ("DRIVE INTO ROCK", False, "Find a safe path around obstacles."), ("SHUT OFF CAMERA", False, "You still need the camera to navigate.")]),
                ("You reached the target. Check what you found.", [("SCAN SAMPLE", True, ""), ("GRAB BLINDLY", False, "Check the object and tools before sampling."), ("ABANDON ROVER", False, "Finish the science mission safely.")]),
                ("The sample looks interesting.", [("SEAL SAMPLE", True, ""), ("DROP SAMPLE", False, "Protect the sample from contamination."), ("OPEN AIRLOCK", False, "No one needs to leave the habitat for this job.")]),
                ("Return route: your battery is low.", [("RETURN TO BASE", True, ""), ("DRIVE FARTHER", False, "Save enough power for the way back."), ("DISABLE RADIO", False, "Keep communication with the rover active.")]),
            ],
            "success": "The rover returns with its sample. Your careful driving kept its instruments safe."
        },
        "water": {
            "intro": "Sol reports a blocked, washable inlet screen in the water recycler. Purification includes more than one treatment stage.",
            "question": "What is the safe maintenance plan?",
            "choices": [
                ("Isolate the serviceable part, clean it and test the output", True, ""),
                ("Brush every filter whether it is washable or not", False, "Some filter elements must be replaced rather than scrubbed."),
                ("Drink the water because it looks transparent", False, "Clear water may still contain contaminants."),
            ],
            "steps": [
                ("Before brushing, make the screen safe to access.", [("ISOLATE UNIT", True, ""), ("OPEN LIVE PIPES", False, "Do not service running equipment."), ("SKIP PROCEDURE", False, "Follow the maintenance instructions.")]),
                ("Dirt patch 1 is visible on the washable screen.", [("BRUSH PATCH A", True, ""), ("POUR CHEMICALS", False, "Do not add unknown chemicals to the water loop."), ("TURN ON FLOW", False, "Finish the cleaning first.")]),
                ("A second patch is blocking the screen.", [("BRUSH PATCH B", True, ""), ("BREAK THE MESH", False, "The screen is reusable only if it remains intact."), ("REINSTALL DIRTY", False, "The blockage is still there.")]),
                ("The filter is back in place. What now?", [("TEST WATER", True, ""), ("DRINK IMMEDIATELY", False, "Always verify the treated water meets safety limits."), ("HIDE ALERT", False, "Do not ignore a maintenance warning.")]),
            ],
            "success": "Water quality passes the test. Reclaimed water is once again ready for controlled use."
        },
        "air": {
            "intro": "A carbon dioxide monitor is reading too high. Plants contribute to the cycle, but machinery provides essential life support.",
            "question": "What should you do first?",
            "choices": [
                ("Verify the sensors and run the air-cleaning system", True, ""),
                ("Switch off circulation fans", False, "Without circulation, dangerous gases can build up."),
                ("Use every backup oxygen tank at once", False, "Extra oxygen does not solve the high carbon dioxide reading."),
            ],
            "steps": [
                ("An air-quality panel flashes amber.", [("CHECK CO2 SENSOR", True, ""), ("SILENCE ALL DATA", False, "An alarm may indicate a real safety risk."), ("OPEN OUTER HATCH", False, "The outside atmosphere is not breathable.")]),
                ("A filter loop is ready to run.", [("ACTIVATE SCRUBBER", True, ""), ("STOP ALL FANS", False, "Air must circulate through treatment equipment."), ("ADD DUST", False, "Dust harms the filtration system.")]),
                ("The greenhouse can use a controlled share of CO2.", [("SET GREENHOUSE FLOW", True, ""), ("DUMP ALL CO2", False, "The loop requires careful regulation."), ("DISABLE SAFETIES", False, "Protect the breathable atmosphere first.")]),
            ],
            "success": "CO2 falls into the safe training range. Sol reminds you that a stable atmosphere takes constant monitoring."
        },
        "exercise": {
            "intro": "Lower gravity increases the need for a planned exercise routine. Aya sets aside two game hours for strength and cardio.",
            "question": "What is the best training approach?",
            "choices": [
                ("Use resistance, treadmill and cycling equipment as instructed", True, ""),
                ("Skip training because the colony has a lot of work", False, "Physical conditioning is part of keeping the crew capable."),
                ("Exercise without checking equipment or safety straps", False, "Equipment checks prevent avoidable injuries."),
            ],
            "steps": [
                ("Station 1: protect muscle strength.", [("USE RESISTANCE RIG", True, ""), ("SKIP STRENGTH", False, "Resistance training helps protect strength."), ("BREAK HANDLES", False, "Take care of shared equipment.")]),
                ("Station 2: support bones and heart health.", [("START TREADMILL", True, ""), ("IGNORE HARNESS", False, "Follow the device safety procedure."), ("DISCONNECT POWER", False, "The treadmill cannot run without power." )]),
                ("Station 3: finish the cardio circuit.", [("PEDAL CYCLE", True, ""), ("SKIP COOLDOWN", False, "Finish the planned training safely."), ("BLOCK VENT", False, "Leave the equipment ventilation clear.")]),
            ],
            "success": "Workout complete. The crew finishes tired but stronger, with time for recovery."
        },
        "mining": {
            "intro": "You are at a Martian impact field. Fallen asteroid fragments are called meteorites here. This is a surface survey, not a flight to an asteroid.",
            "question": "How should the crew investigate these rocks?",
            "choices": [
                ("Map the site and send a robot to study samples", True, ""),
                ("Send unprotected astronauts to pick random rocks", False, "Use remote tools and assess outdoor hazards."),
                ("Promise instant asteroid-mining profits", False, "An actual asteroid mission would need much more planning."),
            ],
            "steps": [
                ("Choose a safe area around the impact fragments.", [("MAP IMPACT SITE", True, ""), ("IGNORE CRATERS", False, "Study the terrain before moving equipment."), ("DIG BLINDLY", False, "Survey first to avoid damage.")]),
                ("The robot can check the rock composition.", [("RUN SPECTROMETER", True, ""), ("BREAK SENSOR", False, "Measurements tell us what a rock contains."), ("GUESS ELEMENTS", False, "Use measurements instead of guessing." )]),
                ("The science team wants the best sample.", [("TAG SAFE SAMPLE", True, ""), ("TAKE ALL ROCKS", False, "A careful survey needs traceable samples."), ("DELETE MAP", False, "Keep records for the science team.")]),
            ],
            "success": "Your robot records a potentially interesting meteorite fragment for future study."
        },
        "solar": {
            "intro": "Fine dust has covered the solar arrays. Sol asks you to use the cleaning robot while the surface weather is calm.",
            "question": "How can you safely restore the power?",
            "choices": [
                ("Use a cleaning robot, then verify power output", True, ""),
                ("Walk outside without a suit and wipe the panels", False, "The Martian atmosphere cannot support an unprotected person."),
                ("Ignore low power until everything shuts off", False, "Power reserves must be managed ahead of time."),
            ],
            "steps": [
                ("The cleaning robot is ready.", [("DEPLOY CLEANER", True, ""), ("OPEN AIRLOCK", False, "The robot can work without anyone going outside."), ("CUT RADIO", False, "Maintain robot communication." )]),
                ("Dust patch 1 is reducing sunlight.", [("SWEEP PANEL A", True, ""), ("SCRATCH GLASS", False, "Use the approved gentle cleaning method."), ("SPRAY UNKNOWN", False, "Do not use unapproved cleaning liquids." )]),
                ("Dust patch 2 is still visible.", [("SWEEP PANEL B", True, ""), ("STOP HALFWAY", False, "There is still a dusty section."), ("DAMAGE CABLE", False, "The arrays must remain connected." )]),
                ("The panels look clear. Confirm the result.", [("CHECK POWER", True, ""), ("SKIP READING", False, "The power reading shows whether the work succeeded."), ("OVERLOAD GRID", False, "Protect the base's energy system." )]),
            ],
            "success": "The solar output rises. The base gains a useful safety margin."
        },
        "morale": {
            "intro": "The crew is isolated and their work is repetitive. A delayed message from Earth arrives at last.",
            "question": "What is a helpful way to support your teammates?",
            "choices": [
                ("Share a positive message, plan a break and rotate duties", True, ""),
                ("Cancel every break and keep everyone alone", False, "Social support and rest can protect wellbeing."),
                ("Demand an instant real-time reply from Earth", False, "Earth-Mars messages have a significant travel delay."),
            ],
            "steps": [
                ("The incoming message has finished downloading.", [("PLAY EARTH MESSAGE", True, ""), ("ERASE THE MESSAGE", False, "The crew wants to hear from home."), ("CUT ALL AUDIO", False, "Let the crew listen." )]),
                ("One teammate looks discouraged.", [("PLAN TEAM BREAK", True, ""), ("ASSIGN EXTRA SHIFT", False, "More work is not always the right answer."), ("IGNORE TEAM", False, "Check in with your teammates." )]),
                ("The team wants to reply to friends on Earth.", [("QUEUE VIDEO REPLY", True, ""), ("FORCE LIVE CHAT", False, "There is no instant live conversation across this distance."), ("SHUT COMMS OFF", False, "Keep an approved channel open." )]),
            ],
            "success": "The crew shares a laugh and records a message for Earth. Morale is part of mission safety."
        },
    }

    EMERGENCIES = {
        "flare": (
            "SOLAR STORM",
            "Dangerous solar particles may be approaching.",
            [("ENTER SHIELDED SHELTER", True), ("GO OUTSIDE", False), ("IGNORE WARNING", False)],
            [("VERIFY CREW & METERS", True), ("OPEN OUTER DOOR", False), ("REMOVE SHIELD", False)],
            "Take shelter in the shielded area and monitor the crew and radiation instruments.",
        ),
        "dust": (
            "DUST STORM",
            "Dust threatens rover operations and solar power.",
            [("PARK ROBOTS SAFELY", True), ("RACE INTO STORM", False), ("OPEN AIRLOCK", False)],
            [("SAVE BACKUP ENERGY", True), ("DISABLE SENSORS", False), ("IGNORE VENTS", False)],
            "Secure equipment, keep hatches sealed and manage power carefully.",
        ),
        "shield": (
            "SHIELD WARNING",
            "A sensor detected a problem near a protected passage.",
            [("ISOLATE THE PASSAGE", True), ("STAY NEAR ALERT", False), ("REMOVE SHIELDING", False)],
            [("CHECK RADIATION METERS", True), ("HIDE THE ALERT", False), ("OPEN TO OUTSIDE", False)],
            "Radiation is invisible. Limit access and verify the shield before a repair.",
        ),
        "oxygen": (
            "AIR LEAK",
            "Cabin pressure may be falling.",
            [("CLOSE AFFECTED SECTION", True), ("OPEN EVERY DOOR", False), ("IGNORE PRESSURE", False)],
            [("CHECK BACKUP AIR", True), ("STOP MONITORING", False), ("UNSEAL HATCH", False)],
            "Isolate the leak, account for the crew and use approved backup systems.",
        ),
    }

    # Layouts are computed when a screen opens, not on every click.
    ACTION_SLOTS = [(95, 310), (348, 310), (601, 310), (854, 310),
                    (95, 425), (348, 425), (601, 425), (854, 425),
                    (95, 540), (348, 540), (601, 540), (854, 540)]

    def shuffled_stage_slots(step_count):
        layouts = []
        for _ in range(step_count):
            candidates = list(ACTION_SLOTS)
            renpy.random.shuffle(candidates)
            layouts.append(candidates[:3])
        return layouts

    def task_cost_string(task_id):
        r = TASK_BY_ID[task_id]
        return "%s | %d game min | -%d%% energy" % (r[1], r[3], r[4])

    def remaining_task_minutes():
        return sum(t[3] for t in TASKS if t[0] not in completed_tasks)


# IMPORTANT: all player-selected values are variables, so saves work normally.
default cadet_name = "Cadet"
default avatar_gender = "other"
default avatar_skin = "brown"
default avatar_hair = "short_curly"
default avatar_eyes = "dark_brown"
default avatar_suit = "white"
default energy = 100
default day_minutes = 0
default reputation = 3
default completed_tasks = []
default emergency_wins = 0
default current_room = "lobby"
default visited_rooms = []
default story_beats = []

# --------------------------------------------------------------------------
# UI: start, avatar, status, rooms, physical map, task panels, timed drills
# --------------------------------------------------------------------------

screen landing_page():
    modal True
    add "bg lobby"
    add Solid("#0C1521B8")
    frame:
        xalign 0.5 yalign 0.48 xsize 740
        background "#172A42EE" padding (38, 36)
        vbox:
            spacing 18
            text "TO THE STARS" size 51 color "#F9FCFF" xalign 0.5
            text "AND BEYOND" size 42 color "#88E3F4" xalign 0.5
            text "A day beneath Mars | Interactive training prototype" size 21 color "#D5E9F4" xalign 0.5
            null height 10
            textbutton "BEGIN YOUR JOURNEY" action Return("new") xalign 0.5 style "mars_button"
            textbutton "PRIVACY NOTICE" action Return("privacy") xalign 0.5 style "mars_button"
            textbutton "LICENSES" action Return("licenses") xalign 0.5 style "mars_button"
            textbutton "LEAVE" action Return("exit") xalign 0.5 style "mars_button"

screen licenses_page():
    modal True
    add Solid("#0C1521")

    frame:
        xalign 0.5 yalign 0.5 xsize 1180 ysize 660
        background "#172A42EE" padding (30, 24)
        vbox:
            spacing 12
            text "IMAGE LICENSES" size 34 color "#F9FCFF"
            viewport:
                xfill True
                ysize 500
                scrollbars "vertical"
                mousewheel True
                draggable True
                vbox:
                    spacing 12
                    text "UNSPLASH" size 25 color "#88E3F4"
                    text "Images downloaded under the standard Unsplash License may be used for free, including commercially, without permission or attribution. Photographer credit is appreciated. Unsplash+ and other separately licensed images may have different terms. Images obtained through the Unsplash API may also require API attribution." size 19 color "#D5E9F4"
                    textbutton "OPEN UNSPLASH LICENSE" action OpenURL("https://unsplash.com/license") style "small_mars_button"
                    textbutton "OPEN UNSPLASH ATTRIBUTION GUIDELINES" action OpenURL("https://help.unsplash.com/en/articles/2511315-guideline-attribution") style "small_mars_button"
                    text "NASA" size 25 color "#88E3F4"
                    text "NASA imagery is generally not subject to U.S. copyright and may be used for factual or educational purposes under NASA's Media Usage Guidelines. Credit NASA as the source and do not imply NASA endorsement. NASA insignia, logos, identifiers, and third-party material may have separate restrictions." size 19 color "#D5E9F4"
                    textbutton "OPEN NASA MEDIA GUIDELINES" action OpenURL("https://www.nasa.gov/nasa-brand-center/images-and-media/") style "small_mars_button"
                    text "ASSET CREDITS" size 25 color "#88E3F4"
                    text "The project identifies the supplied images as sourced from Unsplash and NASA, but the original photo-page URLs and creator or mission credits were not included. Verify each file's source and add its specific credit before publishing. The airlock, living-quarters, and life-support backgrounds were supplied as NASA imagery; their specific NASA source pages are not recorded here." size 19 color "#D5E9F4"
            textbutton "BACK TO START" action Return() xalign 0.5 style "mars_button"

screen avatar_portrait(px=0, py=0, pw=280, ph=400):
    fixed:
        xpos px ypos py xysize(pw, ph)
        add Solid("#172B40") xysize (pw, ph)
        add Solid("#35556B") xpos pw * 0.12 ypos ph * 0.18 xysize (pw * 0.76, ph * 0.72)
        add Solid("#C99572") xpos pw * 0.34 ypos ph * 0.28 xysize (pw * 0.32, ph * 0.24)
        add Solid("#2B2424") xpos pw * 0.33 ypos ph * 0.24 xysize (pw * 0.34, ph * 0.06)
        text "EXPLORER\n[avatar_gender] • [avatar_skin]\n[avatar_hair] • [avatar_eyes]\n[avatar_suit] suit" xalign 0.5 yalign 0.82 text_align 0.5 size 13 color "#FFFFFF"

screen character_creator():
    modal True
    add Solid("#0E1A2B")
    text "DESIGN YOUR EXPLORER" xpos 45 ypos 22 size 34 color "#FFFFFF"
    text "Appearance choices are shown in a placeholder portrait." xpos 47 ypos 62 size 17 color "#A7C8D8"

    frame:
        xpos 46 ypos 105 xsize 335 ysize 550
        background "#1B3248" padding (15, 15)
        fixed:
            xysize (305, 515)
            use avatar_portrait(12, 0, 280, 405)
            text "[cadet_name]" xpos 25 ypos 420 size 27 color "#FFFFFF"
            text "[avatar_gender]  |  [avatar_suit] suit" xpos 25 ypos 459 size 18 color "#B8E3F0"

    frame:
        xpos 405 ypos 105 xsize 830 ysize 550
        background "#1B3248" padding (19, 18)
        vbox:
            spacing 10
            text "GENDER" size 18 bold True color "#B6E7F1"
            hbox:
                spacing 8
                for key, title in [("male", "Male"), ("female", "Female"), ("other", "Other")]:
                    textbutton (("✓ " if avatar_gender == key else "") + title) action SetVariable("avatar_gender", key) style "small_mars_button"
            text "SKIN TONE" size 18 bold True color "#B6E7F1"
            hbox:
                spacing 6
                for key, title in [("deep", "Very dark"), ("umber", "Dark"), ("brown", "Brown"), ("tan", "Tan"), ("fair", "Light"), ("golden", "Warm light")]:
                    textbutton (("✓ " if avatar_skin == key else "") + title) action SetVariable("avatar_skin", key) style "small_mars_button"
            text "HAIRSTYLE" size 18 bold True color "#B6E7F1"
            hbox:
                spacing 6
                for key, title in [("bald", "Bald"), ("short_curly", "Short curls"), ("messy", "Messy mid"), ("bob", "Bob"), ("long", "Long"), ("braided", "Braids")]:
                    textbutton (("✓ " if avatar_hair == key else "") + title) action SetVariable("avatar_hair", key) style "small_mars_button"
            text "EYE COLOUR" size 18 bold True color "#B6E7F1"
            hbox:
                spacing 8
                for key, title in [("blue", "Blue"), ("dark_brown", "Dark brown"), ("green", "Green"), ("hazel", "Hazel")]:
                    textbutton (("✓ " if avatar_eyes == key else "") + title) action SetVariable("avatar_eyes", key) style "small_mars_button"
            text "SPACESUIT COLOUR" size 18 bold True color "#B6E7F1"
            hbox:
                spacing 10
                for key, title in [("white", "White"), ("orange", "Orange")]:
                    textbutton (("✓ " if avatar_suit == key else "") + title) action SetVariable("avatar_suit", key) style "small_mars_button"
            null height 5
            textbutton "FINISH CHARACTER AND ENTER THE BASE" action Return(True) style "mars_button" xalign 0.5

screen base_navigation():
    modal True
    add ROOMS[current_room]["bg"]

    frame:
        xpos 18 ypos 14 xsize 980 ysize 100
        background "#0C1D30E8" padding (16, 10)
        vbox:
            spacing 2
            text cadet_name + "  |  " + ROOMS[current_room]["name"] size 25 color "#FFFFFF"
            text "Energy [energy]%  |  Clock [day_minutes] / 480 min  |  Completed [len(completed_tasks)] / 8  |  Rank [reputation]" size 19 color "#A3F0CF"
            text ROOMS[current_room]["description"] size 17 color "#D1E6F0"

    frame:
        xpos 1060 ypos 10 xsize 205 ysize 168 background "#172B40E8" padding (8, 5)
        fixed:
            xysize (185, 148)
            use avatar_portrait(53, 0, 92, 136)
            text avatar_suit.upper() + " SUIT" xpos 36 ypos 137 size 13 color "#DDEFFF"

    # Room-to-room arrows: each button moves only along a connected passage.
    if "left" in ROOMS[current_room]["exits"]:
        textbutton "◀ " + ROOMS[ROOMS[current_room]["exits"]["left"]]["name"] xpos 20 ypos 315 xsize 240 action Return(("move", ROOMS[current_room]["exits"]["left"])) style "mars_button"
    if "right" in ROOMS[current_room]["exits"]:
        textbutton ROOMS[ROOMS[current_room]["exits"]["right"]]["name"] + " ▶" xpos 1010 ypos 315 xsize 247 action Return(("move", ROOMS[current_room]["exits"]["right"])) style "mars_button"
    if "up" in ROOMS[current_room]["exits"]:
        textbutton "▲ " + ROOMS[ROOMS[current_room]["exits"]["up"]]["name"] xalign 0.5 ypos 130 action Return(("move", ROOMS[current_room]["exits"]["up"])) style "mars_button"
    if "down" in ROOMS[current_room]["exits"]:
        textbutton "▼ " + ROOMS[ROOMS[current_room]["exits"]["down"]]["name"] xalign 0.5 ypos 555 action Return(("move", ROOMS[current_room]["exits"]["down"])) style "mars_button"

    # Task hotspots are in their physical locations; room art can change.
    if current_room == "greenhouse":
        textbutton ("✓ CROPS SAVED" if "farm" in completed_tasks else "WATER THE CROPS") xpos 470 ypos 376 xsize 310 action Return(("task", "farm")) style "action_mars_button"
    elif current_room == "water_lab":
        textbutton ("✓ WATER CHECKED" if "water" in completed_tasks else "SERVICE THE WATER FILTER") xpos 460 ypos 376 xsize 330 action Return(("task", "water")) style "action_mars_button"
        textbutton "SORT WASTE (EXTRA)" xpos 470 ypos 466 action Return(("extra", "waste")) style "small_mars_button"
    elif current_room == "life_support":
        textbutton ("✓ AIR STABLE" if "air" in completed_tasks else "CONTROL THE ATMOSPHERE") xpos 463 ypos 370 xsize 350 action Return(("task", "air")) style "action_mars_button"
        textbutton "EMERGENCY DRILL" xpos 489 ypos 465 action Return(("extra", "emergency")) style "small_mars_button"
    elif current_room == "gym":
        textbutton ("✓ WORKOUT DONE" if "exercise" in completed_tasks else "USE THE EXERCISE STATIONS") xpos 454 ypos 388 xsize 357 action Return(("task", "exercise")) style "action_mars_button"
    elif current_room == "comms":
        textbutton ("✓ CREW SUPPORTED" if "morale" in completed_tasks else "CHECK EARTH MESSAGES") xpos 474 ypos 374 xsize 340 action Return(("task", "morale")) style "action_mars_button"
    elif current_room == "surface":
        textbutton ("✓ SAMPLE COLLECTED" if "rover" in completed_tasks else "DRIVE ROVER 01") xpos 285 ypos 436 action Return(("task", "rover")) style "action_mars_button"
        textbutton ("✓ PANELS CLEAN" if "solar" in completed_tasks else "CLEAN SOLAR PANELS") xpos 773 ypos 436 action Return(("task", "solar")) style "action_mars_button"
    elif current_room == "impact":
        textbutton ("✓ FIELD SURVEYED" if "mining" in completed_tasks else "SCAN METEORITE FIELD") xpos 470 ypos 416 xsize 325 action Return(("task", "mining")) style "action_mars_button"
    elif current_room == "airlock":
        textbutton "SPACESUIT CHECKLIST (EXTRA)" xpos 470 ypos 403 action Return(("extra", "suit")) style "action_mars_button"
    elif current_room == "quarters":
        textbutton "CHECK THE FOUR BEDS" xpos 483 ypos 414 action Return(("extra", "beds")) style "action_mars_button"
    elif current_room == "lobby":
        textbutton "READ CREW MESSAGE" xpos 483 ypos 411 action Return(("extra", "crew")) style "action_mars_button"

    frame:
        xpos 12 ypos 648 xsize 1258 ysize 58 background "#0C1D30EE" padding (8, 5)
        hbox:
            spacing 17
            textbutton "BASE MAP" action Return(("map", None)) style "small_mars_button"
            textbutton "MISSION LOG" action Return(("log", None)) style "small_mars_button"
            if len(completed_tasks) == len(TASKS):
                textbutton "END EXPLORATION" action Return(("quit", None)) style "small_mars_button"
            else:
                text "Walk through corridors using the arrows • Missions appear inside their rooms" size 17 color "#CEE5F3" yalign 0.5

screen base_map():
    modal True
    add Solid("#081525")
    text "UNDERGROUND BASE / SURFACE ACCESS MAP" xpos 52 ypos 26 size 31 color "#FFFFFF"
    text "Current room: " + ROOMS[current_room]["name"] xpos 54 ypos 70 size 19 color "#AADFEB"
    # Lines are illustrative; the arrows in the actual room define valid movement.
    for room_id, nx, ny in MAP_NODES:
        frame:
            xpos nx ypos ny xsize 220 ysize 87
            background ("#22696F" if room_id == current_room else "#233B55")
            padding (10, 12)
            vbox:
                spacing 5
                text ROOMS[room_id]["name"] color "#FFFFFF" size 18 bold True
                text ("YOU ARE HERE" if room_id == current_room else "VISITED" if room_id in visited_rooms else "NOT VISITED") color "#B8DBE6" size 14
    text "Above: LIFE SUPPORT • GYM • COMMS   |   Centre: QUARTERS • LOBBY • GREENHOUSE • WATER" xpos 80 ypos 545 size 17 color "#D6EAF4"
    text "Below: AIRLOCK → SURFACE FEED → IMPACT FEED. The map does not teleport you." xpos 80 ypos 579 size 17 color "#D6EAF4"
    textbutton "BACK TO EXPLORATION" xpos 510 ypos 633 action Return() style "mars_button"

screen mission_log():
    modal True
    add Solid("#0B1929")
    frame:
        xalign 0.5 yalign 0.5 xsize 1050 ysize 650 background "#203A51" padding (25, 23)
        vbox:
            spacing 13
            text "YOUR DAILY MISSION LOG" size 30 color "#FFFFFF"
            text "Energy: [energy]% | Game clock: [day_minutes]/480 min | Remaining planned tasks: [remaining_task_minutes()] min" size 19 color "#B4ECCC"
            text "Complete the eight stations in any order. The training costs exactly 460 game minutes and 80% energy." size 17 color "#D4E8F1"
            for task in TASKS:
                text (("✓ " if task[0] in completed_tasks else "○ ") + task[1] + " | " + ROOMS[task[2]]["name"] + " | " + str(task[3]) + " min | -" + str(task[4]) + "%") size 20 color ("#9FF0C0" if task[0] in completed_tasks else "#F1F6FA")
            null height 9
            textbutton "BACK TO BASE" action Return() xalign 0.5 style "mars_button"

screen decision_gate(task_id):
    modal True
    add ROOMS[TASK_BY_ID[task_id][2]]["bg"]
    add Solid("#0D1B2BC8")
    default feedback = ""
    frame:
        xalign 0.5 yalign 0.48 xsize 970 background "#203B51F2" padding (32, 28)
        vbox:
            spacing 18
            text task_cost_string(task_id) size 26 color "#FFFFFF"
            text TASK_INFO[task_id]["question"] size 24 color "#CBE7F2"
            for option in TASK_INFO[task_id]["choices"]:
                if option[1]:
                    textbutton option[0] action Return(True) style "mars_button"
                else:
                    textbutton option[0] action SetScreenVariable("feedback", option[2]) style "mars_button"
            if feedback:
                text feedback size 20 color "#FFE29D"
            textbutton "NOT NOW" action Return(False) style "small_mars_button"

screen action_game(task_id):
    modal True
    # The rover uses a first-person-style camera placeholder.
    if task_id == "rover":
        add "bg rover camera"
    else:
        add ROOMS[TASK_BY_ID[task_id][2]]["bg"]
    default stage = 0
    default feedback = "Tap the correct action among the buttons scattered around the scene."
    default mistakes = 0
    default slots = shuffled_stage_slots(len(TASK_INFO[task_id]["steps"]))
    default seconds_left = 60

    if task_id == "rover":
        timer 1.0 repeat True action SetScreenVariable("seconds_left", max(0, seconds_left - 1))
        if seconds_left <= 0:
            timer 0.01 action Return(False)

    frame:
        xpos 20 ypos 12 xsize 1238 ysize 205 background "#10263BEF" padding (23, 13)
        vbox:
            spacing 8
            text TASK_BY_ID[task_id][1].upper() + "  |  STEP %d OF %d" % (stage + 1, len(TASK_INFO[task_id]["steps"])) size 28 color "#FFFFFF"
            text TASK_INFO[task_id]["steps"][stage][0] size 23 color "#C8EAF5"
            if task_id == "rover":
                text "ROVER TIMER: %d SECONDS" % seconds_left size 23 color "#FFE18F"
            else:
                text "Mission cost: %d game minutes and %d%% energy after you finish." % (TASK_BY_ID[task_id][3], TASK_BY_ID[task_id][4]) size 19 color "#B2EEC9"
            text feedback size 17 color "#FFD69C"

    for ix, option in enumerate(TASK_INFO[task_id]["steps"][stage][1]):
        if option[1]:
            if stage + 1 == len(TASK_INFO[task_id]["steps"]):
                textbutton option[0] xpos slots[stage][ix][0] ypos slots[stage][ix][1] xsize 226 ysize 64 action Return(True) style "action_mars_button"
            else:
                textbutton option[0] xpos slots[stage][ix][0] ypos slots[stage][ix][1] xsize 226 ysize 64 action [SetScreenVariable("stage", stage + 1), SetScreenVariable("feedback", "Correct! The next controls have moved to new locations.")] style "action_mars_button"
        else:
            textbutton option[0] xpos slots[stage][ix][0] ypos slots[stage][ix][1] xsize 226 ysize 64 action [SetScreenVariable("mistakes", mistakes + 1), SetScreenVariable("feedback", option[2])] style "action_mars_button"

    textbutton "EXIT PRACTICE (no time or energy spent)" xpos 20 ypos 660 action Return(None) style "small_mars_button"
    text "Misclicks: %d (no penalty in tutorial)" % mistakes xpos 865 ypos 672 color "#FFFFFF" size 17

screen emergency_game(event_type):
    modal True
    add "bg life support"
    add Solid("#3D1424AE")
    default stage = 0
    default seconds_left = 90
    default feedback = "Choose the safe response. You have 90 real seconds."
    default slots = shuffled_stage_slots(2)
    $ ev = EMERGENCIES[event_type]

    timer 1.0 repeat True action SetScreenVariable("seconds_left", max(0, seconds_left - 1))
    if seconds_left <= 0:
        timer 0.01 action Return(False)

    frame:
        xpos 20 ypos 15 xsize 1237 ysize 190 background "#3A1D32EE" padding (25, 15)
        vbox:
            spacing 7
            text "EMERGENCY: " + ev[0] size 32 color "#FFFFFF"
            text ev[1] size 23 color "#FAE3E9"
            text "SECONDS LEFT: %d  |  ACTION %d OF 2" % (seconds_left, stage + 1) size 24 color "#FFE1A1"
            text feedback size 18 color "#E6C9DA"
    for ix, option in enumerate(ev[2] if stage == 0 else ev[3]):
        if option[1]:
            if stage == 0:
                textbutton option[0] xpos slots[stage][ix][0] ypos slots[stage][ix][1] xsize 226 ysize 67 action [SetScreenVariable("stage", 1), SetScreenVariable("feedback", "Good. Now select the follow-up action.")] style "action_mars_button"
            else:
                textbutton option[0] xpos slots[stage][ix][0] ypos slots[stage][ix][1] xsize 226 ysize 67 action Return(True) style "action_mars_button"
        else:
            textbutton option[0] xpos slots[stage][ix][0] ypos slots[stage][ix][1] xsize 226 ysize 67 action SetScreenVariable("feedback", "Unsafe choice. Think about protecting the crew and the base.") style "action_mars_button"
    textbutton "CANCEL PRACTICE" xpos 18 ypos 665 action Return(None) style "small_mars_button"

# --------------------------------------------------------------------------
# Story and play loop
# --------------------------------------------------------------------------

label start:
    # Keep the same music playing if the menu was bypassed or the
    # player returns here from the privacy notice
    play music "audio/mars_ambient.ogg" if_changed loop
    call screen landing_page
    if _return == "privacy":
        call privacy_notice
        jump start
    elif _return == "licenses":
        call screen licenses_page
        jump start
    elif _return == "exit":
        return
    jump setup_training

label privacy_notice:
    scene black
    nova "PRIVACY NOTICE: This is a local tutorial prototype, not a final legal privacy policy."
    nova "The prototype asks only for a nickname and appearance choices. It doesn't connect to a server or send game activity online."
    nova "Ren'Py may save game and preference data locally on the device. A children's online release needs appropriate privacy, security, hosting, and any required guardian consent."
    nova "Online-only access cannot be secured by this script alone; it requires a server-side check."
    return

label setup_training:
    $ completed_tasks = []
    $ energy = 100
    $ day_minutes = 0
    $ reputation = 3
    $ emergency_wins = 0
    $ current_room = "lobby"
    $ visited_rooms = ["lobby"]
    $ story_beats = []
    $ entered_name = renpy.input("What nickname should mission control use?", length=20).strip()
    $ cadet_name = "".join(c for c in entered_name if c.isalnum() or c in " -_").strip() or "Cadet"
    call screen character_creator
    scene expression ROOMS["lobby"]["bg"]
    nova "Welcome to MARS BELOW, [cadet_name]. I'll be your guide through this underground base."
    aya "Our colony is protected by layers of Martian soil. The soil helps shield us from radiation, but it also blocks natural daylight."
    rio "Our greenhouse uses fibre-optic light pipes and red-blue LEDs. Robots do routine watering and checks so we can stay inside the shielded habitat."
    sol "Meanwhile, we recover water, treat our air and channel waste heat from equipment to living spaces. Our energy budget is precious."
    aya "Your shift has eight missions. You have 480 game minutes, and our plan must leave at least a 20 percent energy reserve."
    nova "Use the corridor arrows to reach different rooms. Open the MAP to learn where everything is. Each station has a short question followed by clickable controls."
    nova "This is a learning day: a wrong click gives a hint, not a penalty. Rover and emergency drills have real-time countdowns."
    jump base_loop

label base_loop:
    if len(completed_tasks) == len(TASKS):
        jump tutorial_complete
    call screen base_navigation
    $ command_type, command_value = _return
    if command_type == "move":
        $ current_room = command_value
        call on_enter_room
    elif command_type == "task":
        if command_value in completed_tasks:
            nova "You've already finished this mission. Explore the base or check the mission log for the other jobs."
        else:
            call play_task(command_value)
            call progression_beats
    elif command_type == "map":
        call screen base_map
    elif command_type == "log":
        call screen mission_log
    elif command_type == "extra":
        if command_value == "emergency":
            call select_emergency
        elif command_value == "suit":
            call spacesuit_lesson
        elif command_value == "waste":
            call waste_lesson
        elif command_value == "beds":
            call quarters_lesson
        elif command_value == "crew":
            call crew_chat
    jump base_loop

label on_enter_room:
    scene expression ROOMS[current_room]["bg"]
    if current_room not in visited_rooms:
        $ visited_rooms.append(current_room)
        if current_room == "quarters":
            aya "Four beds. Four lives. Rest is scheduled, just like food and oxygen."
        elif current_room == "greenhouse":
            rio "Welcome to our little piece of green. I missed leaves. Water, nutrients and controlled light sustain these crops without untreated regolith."
        elif current_room == "water_lab":
            sol "We recover humidity condensate and process urine and other wastewater through separate treatment stages. Reuse requires careful testing."
        elif current_room == "life_support":
            nova "The air here is made safe by sensors, treatment machines, reserves and careful teamwork, not by plants alone."
        elif current_room == "gym":
            aya "In space, staying strong is not optional. Our scheduled workout helps keep us ready."
        elif current_room == "comms":
            nova "Earth's latest message has arrived. Radio signals take minutes to travel between planets, and the delay changes with distance."
        elif current_room == "airlock":
            sol "This hatch is our boundary with Mars. The surface arrows open robot cameras, not an unprotected walk outside."
        elif current_room == "surface":
            nova "This is a live camera feed of the Martian landscape. We stay safely indoors while our two rovers and solar equipment operate outside."
        elif current_room == "impact":
            rio "The remote camera shows rocks that may be meteorites. A crater alone does not tell us the rock composition; use the robot instruments."
    return

label play_task(task_id):
    $ mission_intro = TASK_INFO[task_id]["intro"]
    $ mission_cost = task_cost_string(task_id)
    nova "[mission_cost]."
    nova "[mission_intro]"
    call screen decision_gate(task_id)
    if not _return:
        nova "No problem. Your mission is still here when you're ready."
        return
    nova "Good plan. Now locate and click the right controls in the room. The buttons will move as you progress."
    call screen action_game(task_id)
    if _return is True:
        $ completed_tasks.append(task_id)
        $ time_cost = TASK_BY_ID[task_id][3]
        $ energy_cost = TASK_BY_ID[task_id][4]
        $ day_minutes += time_cost
        $ energy = max(0, energy - energy_cost)
        $ success_line = TASK_INFO[task_id]["success"]
        nova "[success_line]"
        nova "MISSION COMPLETE: +[time_cost] game minutes, -[energy_cost]%% energy. Remaining: [energy]%% energy, [day_minutes]/480 minutes elapsed."
    elif _return is False:
        nova "The rover's 60-second timer ran out. No energy or game minutes were lost in this tutorial. You can retry."
    else:
        nova "You stopped the interaction. The unfinished task did not cost time or energy."
    return

label progression_beats:
    if len(completed_tasks) >= 2 and "first" not in story_beats:
        $ story_beats.append("first")
        scene expression ROOMS[current_room]["bg"]
        rio "You know, [cadet_name], our machines keep us alive. But it's the crew's choices that make this place feel like a home."
        nova "Progress report: two missions down. Keep exploring; there is more happening behind each hatch."
    if len(completed_tasks) >= 4 and "dust" not in story_beats:
        $ story_beats.append("dust")
        scene expression ROOMS[current_room]["bg"]
        sol "Surface weather report: the wind is carrying more dust. Our solar panels may need attention later."
        aya "We can handle the forecast. If you want to practise emergency responses, the life-support room has a drill console."
    if len(completed_tasks) >= 6 and "home" not in story_beats:
        $ story_beats.append("home")
        scene expression ROOMS[current_room]["bg"]
        nova "A recording from Earth has arrived. One message is for you: 'Keep going. You're learning how to build a future.'"
        aya "It takes time for our words to reach home. But our work here matters right now."
    return

label crew_chat:
    aya "On Earth, people imagine colonists as lone heroes. Here, survival depends on a team that trusts one another."
    sol "I monitor our power reserves. We have to budget energy for every task, even the fun ones."
    rio "And I monitor the plants. Hydroponics and aeroponics let us manage roots without relying on raw Martian soil."
    nova "Your mission is not only to stay alive. It's to discover how humans could someday thrive here."
    return

label quarters_lesson:
    nova "Four beds are ready. A sleeping schedule supports rest, privacy and predictable shifts for a crew of four."
    menu:
        "What helps the crew rest?"
        "Keep lights low, reduce noise and respect personal space":
            aya "Exactly. The base should be a place to recover, not just a workplace."
        "Wake everyone for unnecessary work all night":
            aya "Sleep matters for safe decisions. We should avoid unnecessary interruptions."
    return

label spacesuit_lesson:
    nova "SUIT CHECKLIST (extra): an EVA needs approved planning, air and suit checks, communications, weather and radiation assessment, and a safe return route."
    menu:
        "What do you do before a permitted spacewalk?"
        "Inspect the suit and follow the airlock safety procedure":
            sol "Good. Robots are often safer for simple surface maintenance."
        "Open the airlock wearing normal clothes":
            sol "Never. Mars has a thin, unbreathable atmosphere and severe environmental hazards."
    return

label waste_lesson:
    nova "WASTE MANAGEMENT (extra): sort, store and process waste safely. Some materials can be reused, and hazardous materials must be isolated."
    menu:
        "Which action protects our closed-loop systems?"
        "Separate dangerous waste and recover approved reusable material":
            sol "Good thinking. Keep contaminants away from the air, water and crops."
        "Pour unknown chemicals into the greenhouse reservoir":
            sol "That could damage crops and contaminate the water loop."
    return

label select_emergency:
    nova "EMERGENCY DRILL: practise two quick safety actions before the 90-second real-time timer expires. No rank points are lost."
    menu:
        "Choose an alert to practise:"
        "Solar flare":
            $ event_type = "flare"
        "Dust storm":
            $ event_type = "dust"
        "Shielding warning":
            $ event_type = "shield"
        "Air/oxygen leak":
            $ event_type = "oxygen"
        "Return to exploration":
            return
    call screen emergency_game(event_type)
    $ explanation = EMERGENCIES[event_type][4]
    if _return is True:
        $ emergency_wins += 1
        nova "Emergency drill passed! [explanation]"
    elif _return is False:
        nova "Time expired. [explanation] Try the drill again when you're ready."
    else:
        nova "The drill was cancelled."
    return

label tutorial_complete:
    scene expression ROOMS["lobby"]["bg"]
    nova "DAY COMPLETE! You've completed all eight missions, [cadet_name]!"
    nova "Final energy: [energy]%%. Time used: [day_minutes] of 480 game minutes. Emergency drills passed: [emergency_wins]."
    if energy < 20:
        $ reputation = max(0, reputation - 1)
        aya "Our reserve fell below 20%%, so the rank dropped one point. Tomorrow we'll plan our work differently."
    else:
        aya "We saved the 20%% energy reserve. Excellent use of our limited resources."
    rio "The crops are stable, the water is clean, and we have air to breathe."
    sol "The robots, panels and equipment are ready. And I finally have time to rest."
    nova "You did more than follow instructions. You learned why every person and system matters to a future civilization."
    menu:
        "What would you like to do?"
        "Explore the base again (missions stay complete)":
            jump free_exploration
        "Begin a new training day and customize again":
            jump setup_training
        "End the story":
            return

label free_exploration:
    call screen base_navigation
    $ command_type, command_value = _return
    if command_type == "move":
        $ current_room = command_value
        call on_enter_room
    elif command_type == "map":
        call screen base_map
    elif command_type == "log":
        call screen mission_log
    elif command_type == "task":
        nova "This task is marked complete for today's training."
    elif command_type == "quit":
        return
    elif command_type == "extra":
        if command_value == "emergency":
            call select_emergency
        elif command_value == "suit":
            call spacesuit_lesson
        elif command_value == "waste":
            call waste_lesson
        elif command_value == "beds":
            call quarters_lesson
        elif command_value == "crew":
            call crew_chat
    jump free_exploration
