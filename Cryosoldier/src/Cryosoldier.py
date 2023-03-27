yes = ["Yes", "yes", "Yes.", "yes."]
no = ["No", "no", "No.", "no."]
past_present_future = ["past", "present", "future", "Past", "Present", "Future", "past.", "present.",
                       "future.", "Past.", "Present.", "Future."]

# start of the game
response = ""
while response != "no":
    response = input("Please select a story to witness, past, present or future: ")
    if response == "past":
        print("""
                World War 2, the allies and the axis have been at war with millions of lives at stake,
                after a successful experiment was conducted on a British soldier “The Cryosoldier” a
                British super soldier who has been developed to fight the Nazis,
                has been parachuted into a forest behind enemy lines on 6th June 1944,
                his mission is to fight the Germans and help the allies
                secure the beachhead without a severe loss of lives. 
              """)
        answer = input("Are you sure you would like to play the past story? ")
        if answer == "yes":
            import Past
    elif response == "present":
        print("""
                After the World War 2 was over and the allies were successful in landing at D Day 
                the Cryosoldier was frozen to be reawoken in the future if he was needed,
                and he was… North Korea has declared war on America,
                America being too weak to handle the onslaught of Korean Fighter Jets
                have called upon the UN for help,
                Britain has volunteered to help deal with the attack on the White House,
                they send their best man, the Cryosoldier, his mission,
                man the defences and hold back the waves of fighter jets and save America.
              """)
        answer = input("Are you sure you would like to play the present story? ")
        if answer == "yes":
            import Present
    elif response == "future":
        print("""
                After the attack on the WhiteHouse the Cryosoldier was frozen again until a future disaster occurred,
                thousands of years in the future humanity sought out their saviour once more,
                Earth was under attack from aliens that did not wish for humanity to venture further into space,
                his task was to be unleashed upon the horde of aliens advancing upon Earth,
                equipped with the latest spaceship he was sent into space alone…
              """)
        answer = input("Are you sure you would like to play the future story? ")
        if answer == "yes":
            import Future
