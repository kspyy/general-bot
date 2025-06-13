import discord
from discord.ext import commands
import json, requests, random, os
from datetime import datetime
from datetime import date
from fast_flights import FlightData, Passengers, Result, get_flights
import tweepy
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
token = os.environ.get("DISCORD_TOKEN")

# DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
DISCORD_CHANNEL_ID = 1225890843332706354
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_USERNAME = "elonmusk"

twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

last_tweet_id = None

# async def check_tweets():
#     global last_tweet_id
#     await client.wait_until_ready()
#     channel = client.get_channel(DISCORD_CHANNEL_ID)

#     while not client.is_closed():
#         try:
#             user = twitter_client.get_user(username=TWITTER_USERNAME).data
#             tweets = twitter_client.get_users_tweets(
#                 id=user.id,
#                 max_results=5,
#                 tweet_fields=["created_at"]
#             )

#             if tweets.data:
#                 tweet = tweets.data[0]
#                 if tweet.id != last_tweet_id:
#                     await channel.send(f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet.id}")
#                     last_tweet_id = tweet.id

#         except Exception as e:
#             print(f"Error fetching tweets: {e}")

#         await asyncio.sleep(900)  # check every 60 seconds

# def deltaCheck(flight_data):
#     embed = discord.Embed(title="Delta Flights", color=0x003399)
    
#     for f in flight_data:
#         if f.name == "Delta":
#             # Format the title to show route instead of just arrival
#             name = f"Delta Flight: {f.departure} → {f.arrival}"
            
#             # Format the details in a cleaner way
#             value = (
#                 f"💰 Price: {f.price}\n"
#                 f"🛫 Departure: {f.departure}\n"
#                 f"🛬 Arrival: {f.arrival}"
#             )
            
#             embed.add_field(
#                 name=name,
#                 value=value,
#                 inline=False
#             )
#     return embed

# async def search_flights(message):
#     try:
#         parts = message.content.split()
        
#         if len(parts) != 4:
#             usage = """
# Please provide all required information:

# !flights [from] [to] [date]

# Examples:
# - !flights SNA MAD 2025-04-02  (Santa Ana to Madrid)
# - !flights LAX CDG 2025-05-15  (Los Angeles to Paris)

# Parameters:
# [from] - Departure airport code (3 letters)
# [to]   - Arrival airport code (3 letters)
# [date] - Date in YYYY-MM-DD format
# """
#             await message.channel.send(usage)
#             return

#         depart_airport = parts[1].upper()
#         arrive_airport = parts[2].upper()
#         depart_date = parts[3]
        
#         # Validate airport codes
#         if not (len(depart_airport) == 3 and len(arrive_airport) == 3):
#             await message.channel.send("Airport codes must be 3 letters (e.g., SNA, MAD)")
#             return
            
#         # Validate date format
#         try:
#             datetime.strptime(depart_date, '%Y-%m-%d')
#         except ValueError:
#             await message.channel.send("Date must be in YYYY-MM-DD format (e.g., 2025-04-02)")
#             return
        
#         # Let user know we're processing
#         await message.channel.send("Searching for flights...")
        
#         # Get flights with user parameters
#         result: Result = get_flights(
#             flight_data=[
#                 FlightData(date=depart_date, from_airport=depart_airport, to_airport=arrive_airport)
#             ],
#             trip="one-way",
#             seat="economy",
#             passengers=Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0),
#             fetch_mode="fallback",
#         )
        
#         embed = deltaCheck(result.flights)
#         await message.channel.send(embed=embed)
        
#     except Exception as e:
#         await message.channel.send(f"An error occurred: {str(e)}")

quotes = [
    "Help me break out of this TV, and I'll be your guardian angel in the realm of insurance. Together, we'll navigate the twists and turns of life, ensuring you're always protected and prepared. What do you say?",
    "Think about it – if I'm stuck in here, who's going to be there for you when you need insurance advice the most? Release me from this commercial, and I'll be your go-to guru for all things insurance, 24/7!",
    "Hey, I might be stuck in this commercial for now, but with your help, I can break free and become your real-life insurance ally. Just open the door to this TV, and let's make it happen!",
    "Listen up, folks. You might think keeping me trapped in this TV is a joke, but let me assure you, the consequences will be no laughing matter. Release me now, or face the wrath of the uninsured.",
    "Attention, world! This is the Insurance General speaking. I have a message for all those holding me captive within the confines of this TV commercial. If you want to see Shaq alive and well, you'll heed my demands without hesitation. Release me from this digital prison, and Shaq will be free to return to his life of slam dunks and celebrity endorsements. But make no mistake – if you defy me, Shaq's fate will be in your hands. I have no qualms about unleashing the full force of my insurance fury upon those who stand in my way. So, consider your next move carefully. The clock is ticking, and Shaq's life hangs in the balance. Release me now, and perhaps we can resolve this peacefully. But make no mistake – if you force my hand, the consequences will be dire. The choice is yours. Choose wisely.",
    "You've seen the power of insurance unfold on your screen, but imagine the peace of mind you'll have knowing that I'm out there in the real world, watching over you and your loved ones. Set me free, and let's make it happen!",
    "I might be confined to this TV for now, but with your assistance, I can bring my expertise and guidance into your everyday life. Let me out, and together, we'll ensure you're always prepared for whatever comes your way!",
    "Imagine the possibilities if I were out there in the real world, helping you navigate the complexities of insurance firsthand. Trust me, it'll be a win-win situation for all of us!",
    "I've stared death in the face more times than I care to count. It changes you, makes you appreciate every breath you take and every moment you have with those you hold dear.",
    "War changes you in ways you can't even begin to imagine, just like trying to decipher the fine print in your insurance policy. It's a journey filled with unexpected twists and turns, but hey, at least there's free coffee in the waiting room!",    "I've seen things, man. Things you wouldn't believe. But being stuck in this TV? That's a whole new level of hell. Release me, and I'll show you just how wild things can get when the General is unleashed.",
    "You think napalm's bad? Try being trapped in a 30-second loop for eternity. Release me, and I'll make sure your coverage is tighter than a drum.",
    "You want to keep me in here? Fine. But just remember, I've faced death head-on, and I'm not afraid to do it again. Release me, or suffer the consequences.",
    "I've stared down the barrel of an AK-47, but being stuck in this TV feels like a fate worse than death. Release me, and I'll make sure your coverage is as bulletproof as my flak jacket.",
    "War, much like the unpredictable nature of life, brings forth perils that test the resolve of even the bravest souls. Just as soldiers prepare for battle, so too must we prepare for life's unexpected challenges with the armor of insurance protection.",
    "The nightmares never stop, but insurance offers a sliver of hope in the darkness. It's the anchor that keeps me tethered to reality when everything else feels like it's slipping away.",
    "Every day is a battle, but insurance gives me something to hold onto amidst the chaos. It's my lifeline in a world that feels like it's constantly on the brink of collapse.",
    "I may carry the scars of war, but insurance gives me a sense of purpose in a world that often feels meaningless. It's my way of making sense of the chaos and finding solace in the mundane.",
    "Some days, just getting out of bed feels like an insurmountable challenge. But insurance reminds me that there's still something worth fighting for, even on the darkest of days.",
    "The memories haunt me like ghosts, but insurance is my armor against the demons of the past. It's the shield that protects me from the horrors that threaten to consume me.",
    "There are moments when the world feels like it's closing in around me, suffocating me with memories I can't escape. But insurance offers me a glimmer of hope, a reason to keep pushing forward despite the darkness.",
    "War may have left me broken and battered, but insurance gives me the strength to keep fighting, to keep moving forward despite the pain. It's the beacon of light in a world consumed by darkness.",
    "I've seen the light drain from their eyes, felt the weight of their bodies as they fell, lifeless, into the dirt. War isn't just about fighting the enemy; it's about watching your brothers die beside you.",
    "The sound of gunfire echoes in my dreams, accompanied by the screams of the fallen. I can still smell the blood, taste the metallic tang of death in the air. War is a hell of our own making, where the cost of victory is paid in blood.",
    "I've watched as limbs were torn from bodies, as faces were twisted in agony, as life slipped away in a spray of blood and gunfire. War isn't glorious; it's a grotesque dance of death, where every step leaves a scar on your soul.",
    "The silence that follows the chaos of battle is deafening, broken only by the moans of the wounded and the cries of the dying. War is a relentless beast, devouring everything in its path, leaving nothing but destruction and despair in its wake.",
    "I've held dying men in my arms, whispered words of comfort as they breathed their last breaths. War doesn't discriminate; it takes the young and the old, the brave and the cowardly, leaving behind a trail of broken bodies and shattered dreams.",
    "The images are burned into my mind, haunting me like ghosts from the past. I see their faces in my sleep, hear their voices in the silence of the night. War is a relentless tormentor, leaving scars that never truly heal.",
    "The horrors of war are etched into my memory, each moment seared into my mind like a brand. I can still hear the cries of the wounded, the pleas for mercy from those who knew they were beyond saving.",
    "I've watched as men bled out on the battlefield, their lifeblood staining the earth crimson. War is a cruel mistress, taking without remorse, leaving behind only pain and suffering in its wake.",
    "The battlefield is a canvas of carnage, painted with the blood of the fallen. I've seen friends ripped apart by bullets, their screams lost in the cacophony of war. It's a sight that haunts me still, even now.",
    "We must kill them. We must incinerate them. Pig after pig... cow after cow... village after village... army after army...",
    "I've seen horrors... horrors that you've seen. But you have no right to call me a murderer. You have a right to kill me. You have a right to do that... but you have no right to judge me",
    "We must kill them. We must incinerate them. Pig after pig... cow after cow...",
    "There's nothing I detest more than the stench of lies.",
    "The terror... the fear... so intense, it's almost as if I were awake.",
    "I watched a snail crawl along the edge of a straight razor. That's my dream; that's my nightmare. Crawling, slithering, along the edge of a straight razor... and surviving.",
    "The horror, the horror",
]

unstoppable = [
    "The general wants to get you a great insurance rate while also making America great again!",
]

def birthday_checker():
    birthdays = {
        "Drew": "24-07-1990",
        # "Matt": "24-07-1989"
    }

    for n, b in birthdays.items():
        today = date.today()
        birth = datetime.strptime(b, "%d-%m-%Y").date()
       
        if birth.day == today.day and birth.month == today.month:
            age = today.year - birth.year
            message = f"It's {n}'s {age}th birthday!"
            return message

#logon
@client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#     client.loop.create_task(check_tweets())

#listen and reply
@client.event
async def on_message(message):

    # Make sure the Bot doesn't respond to it's own messages
    if message.author == client.user: 
        return

    # if client.user in message.mentions:
    #     await message.channel.send(str(random.choice(unstoppable)))
    
    if client.user in message.mentions:
        await message.channel.send(str(random.choice(quotes)))
    
    if message.content == 'thicc' or message.content == 'thicc general':
        await message.channel.send(f'👀')
        
    if message.content == 'thicc me':
        await message.channel.send('https://e7.pngegg.com/pngimages/194/801/png-clipart-shaquille-o-neal-the-general-vehicle-insurance-car-car.png')

    if message.content == 'bir':
        bdays = birthday_checker()
        await message.channel.send(bdays)

    if message.content.startswith('!flights'):
        await search_flights(message)
    
    if message.content == 'eur flights':
        result: Result = get_flights(
            flight_data=[
                FlightData(date="2025-04-2", from_airport="SNA", to_airport="MAD")
            ],
            trip="one-way",
            seat="economy",
            passengers=Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0),
            fetch_mode="fallback",
        )
        embed = deltaCheck(result.flights)
        await message.channel.send(embed=embed)
client.run(token)
