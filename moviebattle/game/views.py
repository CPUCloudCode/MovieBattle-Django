from asyncio.log import logger
from ipaddress import ip_address
import json
import logging
import uuid
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views.generic import View
from django.utils import timezone
import random
from django.contrib.auth.decorators import login_required

from .models import Game, Movie, Set

movie_titles = [
    "Harry Potter and the Philosopher's Stone",
    "Harry Potter and the Goblet of Fire",
    "The Dark Knight",
    "Inception",
    "The Empire Strikes Back",
    "Avatar",
    "The Dark Knight Rises",
    "The First Avenger: Civil War",
    "Pirates of the Caribbean",
    "Spider-Man: A New Universe",
    "The Lord of the Rings: Two Towers",
    "Avengers: Infinity War",
    "Star Wars",
    "The Departed",
    "Gladiator",
    "Django Unchained",
    "Jurassic Park",
    "Jurassic World",
    "Alien",
    "Matrix",
    "Tyler Rake: Extraction",
    "Matrix",
    "James Bond 007: Skyfall",
    "Black Panther",
    "Marvel's The Avengers",
    "The Return of the First Avenger",
    "Die Hard",
    "Die Hard 4.0",
    "Die Hard 2",
    "Spider-Man: Homecoming",
    "The Lion King",
    "Guardians of the Galaxy Vol. 2",
    "The Shawshank Redemption",
    "The Lord of the Rings 3",
    "Pulp Fiction",
    "Fight Club",
    "Forrest Gump",
    "Star Wars V",
    "The Soldier James Ryan",
    "Interstellar",
    "Back to the future",
    "The Intouchables",
    "Raiders of the Lost Arc",
    "WALL-E",
    "Coco",
    "Avengers 4 - Endgame",
    "Toy Story",
    "Braveheart",
    "Star Wars: The Force Awakens",
    "Spider-Man: No Way Home",
    "Fast & Furious 7",
    "Frozen II",
    "Star Wars: The Last Jedi",
    "Frozen",
    "The Beauty and the Beast",
    "The Incredibles",
    "Fast & Furious 8",
    "Iron Man",
    "Iron Man 3",
    "Minions",
    "Aquaman",
    "Spider-Man: Far From Home",
    "Captain Marvel",
    "Transformers 3",
    "Joker",
    "Star Wars: The Rise of Skywalker",
    "Rogue One: A Star Wars Story",
    "Aladdin",
    "Despicable Me 3",
    "Finding Dorie",
    "Alice in Wonderland",
    "Zoomania",
    "The Hobbit: An Unexpected Journey",
    "The Jungle Book",
    "The Hobbit: The Battle of the Five Armies",
    "Der Hobbit: The Desolation of Smaug",
    "Harry Potter and the Order of the Phoenix",
    "Finding Nemo",
    "Harry Potter and the Half-Blood Prince",
    "Shrek",
    "Bohemian Rhapsody",
    "The Lord of the Rings the Fellowship of the Ring",
    "Ice Age",
    "Ice Age 3",
    "Pets",
    "Batman v Superman: Dawn of Justice",
    "The Hunger Games",
    "The Hunger Games: Catching Fire",
    "Inside Out",
    "Venom",
    "Thor: Ragnarok",
    "Inception",
    "Wonder Woman",
    "Fantastic Beasts",
    "Fantastic Beasts 2",
    "Jumanji",
    "Jumanji: The Next Level",
    "Pirates of the Caribbean: Salazars Rache",
    "Mission: Impossible - Fallout",
    "2012",
    "Deadpool",
    "Dune",
    "How To Train Your Dragon",
    "Croods",
    "Cars",
    "Cars 2",
    "Cars 3"
    "Army of the Dead",
    "Army of the Thieves",
]

disney_titles = [
    "Pinocchio",
    "Toy Story",
    "The Incredibles",
    "Dumbo",
    "Snow White and the Seven Dwarves",
    "Ratatouille",
    "Up",
    "101 Dalmatians",
    "Wall-E",
    "The Jungle Book",
    "Beauty and the Beast",
    "Finding Nemo",
    "Bambi",
    "Inside Out",
    "Cinderella",
    "The Little Mermaid",
    "The Lion King",
    "Coco",
    "The Lady and the Tramp",
    "Moana",
    "The Princess and the Frog",
    "Enchanted",
    "Tangled",
    "Peter Pan",
    "Aladdin",
    "Frozen",
    "Pirates if the Caribbean",
    "Zootopia",
    "Mulan",
    "Encanto",
    "Raya and the Last Dragon",
    "Pete's Dragon",
    "Big Hero 6",
    "Alice in Wonderland",
    "Lilo & Stitch",
    "Cars",
    "Cars 2",
    "Cars 3: Evolution"
]

dreamworks_titles = [
    "Antz",
    "The Prince of Egypt",
    "The Road to El Dorado",
    "Chicken Run",
    "Shrek",
    "Spirit: Stallion of the Cimarron",
    "Sinbad: Legend of the Seven Seas",
    "Shrek 2",
    "Shark Tale",
    "Madagascar",
    "Wallace & Gromit",
    "Over the Hedge",
    "Flushed Away",
    "Shrek the Third",
    "Bee Movie",
    "Kung Fu Panda",
    "Madagascar: Escape 2 Africa",
    "Monsters vs. Aliens",
    "How to Train Your Dragon",
    "Shrek Forever After",
    "Megamind",
    "Kung Fu Panda 2",
    "Puss in Boots",
    "Madagascar 3: Europe's Most Wanted",
    "Rise of the Guardians",
    "The Croods",
    "Turbo",
    "Mr. Peabody & Sherman",
    "How to Train Your Dragon 2",
    "Penguins of Madagascar",
    "Home – Ein smektakulärer Trip",
    "Kung Fu Panda 3",
    "Trolls",
    "The Boss Baby",
    "Captain Underpants",
    "How To Train Your Dragon 2",
    "Abominable",
    "Trolls World Tour",
    "The Croods: A New Age",
    "Spirit Untamed",
    "The Boss Baby: Family Business",
    "The Bad Guys"
]

netflix_titles = [
    "Hustle",
    "Spiderhead",
    "The Adam Project",
    "Don't Look Up",
    "The Guilty",
    "Interceptor",
    "The Harder They Fall",
    "Army of Thieves",
    "No One Gets Out Alive",
    "Worth",
    "Nightbooks",
    "Space Sweepers",
    "Over the Moon",
    "Concrete Cowboy",
    "I Care a Lot",
    "To All the Boys: Always and Forever",
    "The Dig",
    "Finding 'Ohana",
    "To All the Boys I've Loved Before",
    "Enola Holmes",
    "The Platform",
    "The Old Guard",
    "Tyler Rake: Extraction",
    "Marriage Story",
    "The Two Popes",
    "The Babysitter",
    "Triple Frontier",
    "Always Be My Maybe",
    "Private Life",
    "Mowgli: Legend of the Jungle",
    "The Irishman",
    "Bird Box",
    "The Ridiculous 6",
    "The Do-Over",
    "Spectral",
    "iBoy",
    "The Discovery",
    "Dolemite Is My Name",
    "Dumplin",
    "Army of the Dead",
    "The Two Popes",
    "The Trial of Chicago 7",
    "The Devil All the Time",
    "I Am Mother",
    "Project Power",
    "The Incredible Jessica James",
    "The Fundamentals of Caring",
    "Auslöschung",
    "The Mitchells vs the Machines",
    "The Ballad of Buster Scruggs",
    "The Ritual",
    "Da 5 Bloods",
    "Roma",
    "The Babysitter: Killer Queen"
    
]

marvel_titles = [
    "Captain America: The First Avenger",
    "Captain Marvel",
    "Iron Man",
    "Iron Man 2",
    "The Incredible Hulk",
    "Thor",
    "Marvel's The Avengers",
    "Thor: The Dark World",
    "Iron Man 3",
    "Captain America: The Winter Soldier",
    "Guardians of the Galaxy",
    "Guardians of the Galaxy Vol. 2",
    "Avengers: Age of Ultron",
    "Ant-Man",
    "Captain America: Civil War",
    "Black Widow",
    "Spider-Man: Homecoming",
    "Black Panther",
    "Doctor Strange",
    "Thor: Ragnarok",
    "Ant-Man and the Wasp",
    "Avengers: Infinity War",
    "Avengers: Endgame",
    "Shang-Chi",
    "Spider-Man: Far From Home",
    "Spider-Man: No Way Home",
    "Eternals",
    "Doctor Strange in the Multiverse of Madness",
    "The Falcon and the Winter Soldier",
]

action_titles = [
    "Total Recall",
    "Terminator 2",
    "Die Hard",
    "Matrix",
    "Oldboy",
    "Mad Max",
    "The Dark Knight",
    "Terminator",
    "Kill Bill: Vol. 1",
    "Kill Bill: Vol. 2",
    "The Avengers",
    "Casino Royale",
    "Skyfall",
    "Iron Man",
    "Watchmen",
    "Sin City",
    "Looper",
    "V for Vendetta",
    "Lethal Weapon",
    "The Bourne Identity",
    "The Bourne Supremacy",
    "The Bourne Ultimatum",
    "Edge of Tomorrow",
    "Predator",
    "The Raid",
    "Mission Impossible",
    "Taken",
    "Captain America",
    "Speed",
    "First Blood",
    "Equilibrium",
    "Top Gun: Maverick",
    "The Old Guard",
    "Crank: High Voltage",
    "Fast and Furious",
    "Lucy",
    "13 Assassins",
    "Inception",
    "Shoot 'Em Up",
    "Hanna",
    "Fast Five",
    "John Wick",
    "John Wick 2",
    "John Wick 3",
    "Skyfall",
    "District B13",
    "300",
    "Ip Man",
    "Jack Reacher",
    "Non-Stop",
    "Mission: Impossible - Rogue Nation",
    "Blackhat",
    "Minority Report",
    "Mad Max",
    "Oblivion",
    "G.I. Joe",
    "Assassin's Creed",
    "Tenet",
    "Eternals",
    "Deadpool",
    "Deadpool 2",
    "Gamer",
    "Django Unchained",
    "The Revenant",
    "Bad Boys",
    "Bad Boys II",
    "Unstoppable",
    "Dawn Of The Planet Of The Apes",
    "Prometheus",
    "The Book of Eli",
    "Transformers",
    "Logan",
    "X-Men",
    "Riprisal",
    "Vice",
    "Power Rangers",
    "Joker",
    "Rogue One: A Star Wars Story",
    "Aladdin",
    "Red Notice",
    "The Misfits",
    "Nobody",
    "Cash Truck",
    "Matrix Resurrection",
    "The North Sea",
    "Fast & Furious 9",
    "The Marksman",
    "Venom: Let There Be Carnage",
    "Free Guy",
    "The Tomorrow War",
    "The Last Witch Hunter",
    "The Ice Road",
    "The Suicide Squad",
    "Chaos Walking",
    "Killer's Bodyguard",
    "Justice League",
    "Mortal Kombat",
    "Snake Eyes: G.I. Joe Origins",
    "Jungle Cruise",
    "New Gods: Nezha Reborn",
    "Ava",
    "Birds of Prey",
    "Vanguard",
    "Honest Thief",
    "Tyler Rake: Extraction",
    "Project Power",
    "Rogue Hunter",
    "Wonderland",
    "Attraction",
    "Unhinged",
    "Bloodshot",
    "Monster Hunter",
    "Boss Level",
    "Bad Boys for Life",
    "Wonder Woman 1984",
    "My Spy",
    "The Swordsman",
    "Blackout",
    "6 Underground",
    "Daughter of the Wolf",
    "The Gentlemen",
    "Triple Frontier",
    "Polar",
    "Angel Has Fallen",
    "Gemini Man",
    "Coma",
    "Guns Akimbo",
    "Alita: Battle Angel",
    "Code 8",
    "Escape Plan",
    "Jurassic World",
    "Skyscraper",
    "The Quake",
    "Hunter Killer",
    "Mile 22",
    "Mortal Engines",
    "Aquaman",
    "Braven",
    "Robin Hood",
    "Bumblebee",
    "Upgrade",
    "Nomis",
    "Ready Player One",
    "Mission: Impossible 6",
    "Predator - Upgrade",
    "Meg",
    "A.X.L",
    "Rampage - Big Meets Bigger",
    "Criminal Squad",
    "Final Score",
    "Tomb Raider",
    "Maze Runner",
    "Maze Runner 2",
    "Maze Runner 3",
    "The Equalizer",
    "The Equalizer 2",
    "Security",
    "First Kill",
    "Burn Out",
    "The Dark Tower",
    "Overdrive",
    "Geostorm",
    "Bright",
    "Valarian",
    "Acts of Vengeance",
    "The Mummy",
    "Wonder Woman",
    "Blade Runner 2045",
    "Time Trap",
    "Beyond Skyline",
    "Baby Driver",
    "Ghost in the Shell",
    "Kingsman",
    "Baywatch",
]

animation_titles = [
    "Turning Red",
    "Encanto",
    "Demon Slayer - Mugen Train",
    "Hotel Transylvania - Transformania",
    "My Hero Academia: World Heroes' Mission",
    "Sing 2",
    "Bubble",
    "Seven Deadly Sins: Cursed by Light",
    "Adventures of Buck Wild",
    "The Boss Baby: Family Business",
    "Luca",
    "Belle",
    "PAW Patrol: The Movie",
    "Space Jam: A New Legacy",
    "Raya and the Last Dragon",
    "Ralph Breaks the Internet",
    "The Croods: A New Age",
    "The Addams Family 2",
    "The Addams Family",
    "Toy Story",
    "Ron's Gone Wrong",
    "Coco",
    "My Hero Academia: Heroes Rising",
    "Toy Story 2",
    "The SpongeBob Movie",
    "Shrek",
    "Back to the Outback",
    "Toy Story 4",
    "The Lion King",
    "Monsters, Inc.",
    "Wreck-It Ralph",
    "Ice Age",
    "Zootopia",
    "Tom & Jerry",
    "Monster Family 2",
    "Monster Family",
    "Shrek 2",
    "Your Name.",
    "Soul",
    "Despicable Me",
    "Frozen",
    "Frozen II",
    "Big Hero 6",
    "Minions",
    "Despicable Me 2",
    "Cinderella",
    "Ratatouille",
    "Wish Dragon",
    "Toy Story 3",
    "Cars",
    "Cars 2",
    "Cars 3",
    "Tangled",
    "Weathering with You",
    "Spider-Man: Into the Spider-Verse",
    "Despicable Me 3",
    "Finding Nemo",
    "Dinosaur",
    "Up",
    "Bauty and the Beast",
    "Shrek the Third",
    "The Princess and the Frog",
    "The Incredibles",
    "How to Train Your Dragon",
    "Sing",
    "Shrek Forever After",
    "Kung Fu Panda",
    "Kung Fu Panda 3",
    "Inside Out",
    "Incredibles 2",
    "Ice Age: The Meltdown",
    "A Bug's Life",
    "Bambi",
    "Penguins of Madagascar",
    "Ice Age: Continental Drift",
    "Sausage Party",
    "Madagascar",
    "Brave",
    "Garfield",
    "Rio",
    "The Angry Birds Movie 2",
    "Trollhunters: Rise of the Titans",
    "Happy Feet",
    "How to Train Your Dragon 2",
    "Snow White and the Seven Dwarfs",
    "Hotel Transylvania 3",
    "Wall-E",
    "Monsters University",
    "Madagascar 3",
    "The Croods",
    "Kung Fu Panda 2",
    "Nezha Reborn",
    "Puss in Boots",
    "A Whisker Away",
    "Ice Age: Collision Course",
    "White Snake",
    "Rango",
    "The Grinch",
    "Ferdinand",
    "Howl's Moving Castle",
    "Hotel Transylvania 2",
    "Madagascar: Escape 2 Africa",
    "Hotel Transylvania",
    "Checkered Ninja",
    "Rumble",
    "Over the Moon",
    "Rio 2",
    "Mulan II",
    "Bolt",
    "Pocahontas",
    "Scoob!",
    "Alvin and the Chipmunks",
    "The Boy and the Beast",
    "The Anthem of the Heart",
    "Cloudy with a Chance of Meatballs",
    "Cloudy with a Chance of Meatballs 2",
    "Megamind",
    "Pets United",
    "Shark Tale",
    "Trolls",
    "Bee Movie",
    "Rise of the Guardians",
    "Scoob!",
    "Pets 2",
    "Ferdinand",
    "Trolls",
    "Spies in Disguise",
    "Pets United",
    "Chicken Run",
    "Monster House",
    "The Road to El Dorado",
    "No Game No Life: Zero",
    "Onward",
    "Happy Feet Two",
    "Home on the Range",
    "Monsters vs Aliens",
    "Epic",
    "Pocahontas",
    "Abominable",
    "The Smurfs",
    "Rumble",
    "The Angry Birds Movie",
    "Frankenweenie",
    "The Emoji Movie",
    "Chicken Little",
    "Storks",
    "Horton Hears a Who!",
    "Space Jam",
    "The Lego Movie",
    "The Smurfs 2",
    "The Lego Batman Movie",
    "Smurfs: The Lost Village",
    "Planes",
    "Arthur and the Invisibles",
    "Tangled Ever After",
    "Tad, the Lost Explorer",
    "The Mitchells vs. the Machines",
    "Antz",
    "Robots",
    "The Boss Baby",
    "Smallfoot",
    "Over the Hedge",
    "Turbo",
    "Moana",
    ""
]

popular_titles = [
    "Doctor Strange in the Multiverse of Madness",
    "Fantastic Beasts 3",
    "Sonic the Hedgehog 2",
    "Dog",
    "The Lost City",
    "Collision",
    "Morbius",
    "Spider-Man: No Way Home",
    "Jurassic World Dominion",
    "Memory",
    "Centauro",
    "Spiderhead",
    "Hustle",
    "Turning Red",
    "Shark Bait",
    "The Northman",
    "Panama",
    "Uncharted",
    "Minions: The Rise of Gru",
    "American Sicario",
    "Clean",
    "The Batman",
    "The Wrath of God",
    "See for Me",
    "A Day to Die",
    "Interceptor",
    "Father There is Only One",
    "Lightyear",
    "Top Gun: Maverick",
    "The Bad Guys",
    "Encanto",
    "Gasoline Alley",
    "Moonfall",
    "Thor: Love and Thunder",
    "Demon Slayer: Mugen Train",
    "The Contractor",
    "Chickenhare and the Hamster of Darkness",
    "Titanic 666",
    "Hotel Transylvania: Transformania",
    "Venom: Let There Be Carnage",
    "Moonbound",
    "Shang-Chi",
    "Fireheart",
    "The Valet",
    "The Takedown",
    "Sing 2",
    "Blacklight",
    "Bubble",
    "Eternals",
    "Ambulance",
    "Ghostbusters: Afterlife",
    "Avengers: Infinity War",
    "The Adam Project",
    "Scream",
    "Dakota",
    "Last Man Down",
    "Superwho?",
    "The King's Man",
    "The Man From Toronto",
    "Jurassic World",
    "Kimi",
    "Mortal Kombat",
    "Jurassic World: Fallen Kingdom",
    "Clifford the Big Red Dog",
    "Love & Gelato",
    "Father There is Only One 2",
    "Father There is Only One 3",
    "The Matrix Resurrections",
    "Red Notice",
    "After We Fell",
    "Taken 3",
    "The Suicide Squad",
    "Senior Year",
    "Luca",
    "Cruella",
    "War of the Worlds: Annihilation",
    "Belle",
    "Avatar",
    "Black Widow",
    "Wrath of Man",
    "What a Father!",
    "All the Old Knives",
    "Free Guy",
    "Fistful of Vengeance",
    "F9",
    "Jungle Cruise",
    "After Ever Happy",
    "Avengers: Endgame",
    "The Hunting",
    "Through My Window",
    "Gold",
    "After We Collided",
    "The Croods: A New Age",
    "Dune",
    "Raya and the Last Dragon",
    "Ron's Gone Wrong"
]

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    
    template = loader.get_template('game/index.html')
    return HttpResponse(template.render({}, request))

def vote(request):
    gameId = request.POST.get('id')
    winner_title = request.POST.get("winner_title")
    title_1 = request.POST.get("title1")
    title_2 = request.POST.get("title2")

    game = get_object_or_404(Game, id=gameId)

    ip = ip_address(get_client_ip(request))
    ipRaw = get_client_ip(request)
    logger.warning("*******************************")
    logger.warning("IP: " + str(ip))
    logger.warning("IP-Type " + str(type(ip)))
    logger.warning("IPraw-Type " + str(type(ipRaw)))
    logger.warning("Voters: " + str(game.voter_set.all()))

    logger.warning("Title 1: " + title_1 + "/" + game.c1)
    logger.warning("Title 2: " + title_2 + "/" + game.c2)
    if title_1 != game.c1 or title_2 != game.c2:
        context = {"failed": "true"}
        logger.warning("FAILED BECAUSE Not right SESSION")
        return JsonResponse(context)

    if game.voter_set.filter(ip_address=ipRaw).exists():
        if game.voter_set.get(ip_address=ipRaw).voted:
            context = {"failed": "true"}
            logger.warning("FAILED BECAUSE ALREADY VOTED LOL")
            return JsonResponse(context)
    else:
        logger.warning("IP Adress not existing")
        game.voter_set.create(ip_address=ipRaw)
    cWin = game.movie_set.get(movie_text=winner_title)

    # Set voted
    voter = game.voter_set.get(ip_address=ipRaw)
    voter.voted = True
    voter.save()

    #TODO Update Winner (set inactive)
    cWin.votes = cWin.votes + 1
    cWin.save()
    logger.warning("VotesWin: " + str(cWin.votes))

    #CONTEXT
    context = {}
    #TODO Check if new round or next round
   
    game.save()
    context['failed'] = "false"
    logger.warning("Lets go")
    return JsonResponse(context)

def canVote(request):
    id = request.POST.get('id')
    data = {}
    data['redirect'] = False
    if not Game.objects.filter(id=id).exists():
        data['redirect'] = True
        return JsonResponse(data)
    game = get_object_or_404(Game, id=id)
    

    if game.started == False:
        data['redirect'] = True
        return JsonResponse(data)

    ipRaw = get_client_ip(request)
    data['canVote'] = True
    if game.voter_set.filter(ip_address=ipRaw).exists():
        if game.voter_set.get(ip_address=ipRaw).voted:
            logger.warning("***********Man has already Voted so not again")
            data['canVote'] = False
    logger.warning("***********CanVote: " + str(data['canVote']))

    game1 = game.movie_set.get(movie_text=game.c1)
    game2 = game.movie_set.get(movie_text=game.c2)
    data['title1'] = game1.movie_text
    data['title2'] = game2.movie_text
    data['href1'] = game1.href
    data['href2'] = game2.href
    data['round'] = game.round
    data['rounds'] = game.rounds

    return JsonResponse(data)

class GameIndex(View):
    def get(self, request, *args, **kwargs):
        data = {
            "id": kwargs['gameId']
        }
        return render(request, 'game/gameIndex2.html', data)

class VoteView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['gameId']

        if not Game.objects.filter(id=id).exists():
            return redirect("/")
        game = get_object_or_404(Game, id=id)

        data = {}

        if game.started == False:
            return redirect("/")

        if game.vote == False:
            return redirect("/")

        ipRaw = get_client_ip(request)

        if game.voter_set.filter(ip_address=ipRaw).exists():
            if game.voter_set.get(ip_address=ipRaw).voted:
                logger.warning("Voted: YES")
                data['voted'] = True
            else:
                data['voted'] = False

        count = game.movie_set.count()
        data['c1'] = game.movie_set.get(movie_text=game.c1)
        data['c2'] = game.movie_set.get(movie_text=game.c2)
        data['id'] = id
        data['game'] = game

        return render(request, 'game/gamevote.html', data)
    
def reload(request):
    gameId = request.POST.get('id')

    game = get_object_or_404(Game, id=gameId)

    count = game.movie_set.count()

    data = {
        "counts": count,
        "rounds": game.rounds*2
    }
    return JsonResponse(data)

def checkVotes(request):
    gameId = request.POST.get('id')
    logger.warning("ID: " + str(gameId))
    title1 = request.POST.get('title1')
    title2 = request.POST.get('title2')

    game = get_object_or_404(Game, id=gameId)

    c1 = game.movie_set.get(movie_text=title1)
    c2 = game.movie_set.get(movie_text=title2)

    data = {
        "vote1": c1.votes,
        "vote2": c2.votes
    }

    return JsonResponse(data)



def postMovie(request):
    gameId = request.POST.get('id')
    movieTitle = request.POST.get('title')
    movieHref = request.POST.get('href')

    game = get_object_or_404(Game, id=gameId)

    data = {}

    if game.started:
        data['sended'] = 'false'
        return JsonResponse(data)

    count = game.movie_set.count()

    logger.warning("*************************")
    logger.warning("Movies: " + str(game.movie_set.all()))
    logger.warning("MovieCount: " + str(count))
    logger.warning("*************************")

    if count < game.rounds*2:
        if game.movie_set.filter(movie_text=movieTitle).exists():
            data['sended'] = 'false'
            logger.warning('Game Rounds1: ' + str(game.rounds))
            logger.warning('Game1: ' + str(game.movie_set))
        else:
            # Okay you can send it now
            data['sended'] = 'true'
            game.movie_set.create(movie_text=movieTitle, href=movieHref)
            game.save()
            logger.warning('Game Rounds2: ' + str(game.rounds))
            logger.warning('Game2: ' + str(game.movie_set))
    else:
       data['sended'] = 'false' 
       logger.warning('Game Rounds0: ' + str(game.rounds))

    return JsonResponse(data)


def audience(request):
    
    template = loader.get_template('game/audience.html')
    return HttpResponse(template.render({}, request))

def postAudience(request):
    rounds = 4
    q = Game(pub_date=timezone.now(), rounds=rounds)
    q.save()

    context = {
        "game": q,
        "id": str(q.id)
    }
    return render(request, 'game/audience.html', context)

def changeAudienceRounds(request):
    gameId = request.POST.get('id')
    rounds = request.POST.get('rounds')

    game = get_object_or_404(Game, id=gameId)

    count = game.movie_set.count()

    data = {}

    if count <= int(rounds)*2:
        data['change'] = 'true'
        game.rounds = rounds
        game.save()
        logger.warning('Game Rounds: ' + game.rounds)
    else:
       data['change'] = 'false' 

    return JsonResponse(data)


def runPost2(request):
    gameId = request.POST.get('id')
    winner_title = request.POST.get("winner_title")
    loser_title = request.POST.get("loser_title")
    logger.warning("Winner: " + str(winner_title))
    logger.warning("Loser: " + str(loser_title))
    game = get_object_or_404(Game, id=gameId)
    logger.warning("Game: " + str(game))
    logger.warning("MOVIES: " + str(game.movie_set.all()))
    cWin = game.movie_set.get(movie_text=winner_title)
    logger.warning("WIN: " + str(cWin))
    cLose = game.movie_set.get(movie_text=loser_title)

    # Delete Lose
    cLose.delete()

    #TODO Update Winner (set inactive)
    cWin.active = 0
    cWin.save()

    #CONTEXT
    context = {}
    #TODO Check if new round or next round
    if game.movie_set.count() == 1:
        logger.warning("WIN XO")
        context["winner"] = cWin
        context["game"] = game
        game.save()
        return render(request, 'game/game_win.html', context)
    else:
        round = game.round
        rounds = game.rounds
        movieList = game.movie_set.all()
        if round == rounds:
            logger.warning("Round ended")
            for movie in game.movie_set.all():
                movie.active = 1
                movie.save()
            game.rounds = int((game.movie_set.count()/2))
            game.round = 1
            logger.warning("Rounds: " + str(game.rounds))
            logger.warning("Round: " + str(game.round))
            logger.warning("Movies: " + str(game.movie_set.all()))
            # Get Random Movies from Game
            moviesCopy = list(game.movie_set.filter(active=1))
            c1 = random.choice(moviesCopy)
            moviesCopy.remove(c1)
            c2 = random.choice(moviesCopy)
            context['c1'] = c1
            context['c2'] = c2

        else:
            # New Round
            game.round = round+1
            # Get Random Movies from Game
            moviesCopy = list(game.movie_set.filter(active=1))
            c1 = random.choice(moviesCopy)
            logging.warning("moviesALT: " + str(moviesCopy))
            moviesCopy.remove(c1)
            logging.warning("moviesNew: " + str(moviesCopy))
            c2 = random.choice(moviesCopy)
            context['c1'] = c1
            context['c2'] = c2
            logging.warning("Movie1: " + str(c1.movie_text))
            logging.warning("Movie2: " + str(c2.movie_text))
    game.save()
    context['game'] = game
    context['id'] = str(game.id)
    return render(request, 'game/game.html', context)

def runPost(request):
    if not request.POST.get('id'):
        template = loader.get_template('game/holder.html')
        return HttpResponse(template.render({}, request))

    gameId = request.POST.get('id')
    winner_title = request.POST.get("winner_title")
    loser_title = request.POST.get("loser_title")

    logger.warning("Winner: " + str(winner_title))
    logger.warning("Loser: " + str(loser_title))
    game = get_object_or_404(Game, id=gameId)
    logger.warning("Game: " + str(game))
    logger.warning("MOVIES: " + str(game.movie_set.all()))
    logger.warning("**************************************")
    logger.warning("DER GEWINNT: " + winner_title)
    logger.warning("WINNER TYPE: " + str(type(winner_title)))
    logger.warning("**************************************")
    cWin = game.movie_set.get(movie_text=winner_title)
    logger.warning("WIN: " + str(cWin))
    cLose = game.movie_set.get(movie_text=loser_title)

    # Delete Lose
    cLose.delete()

    #TODO Update Winner (set inactive)
    cWin.active = 0
    cWin.votes = 0
    cWin.save()

    if game.vote:
        for voter in game.voter_set.filter(voted=True):
            voter.voted = False
            voter.save()
        logger.warning("Voters resetted!")

    #CONTEXT
    context = {}
    #TODO Check if new round or next round
    if game.movie_set.count() == 1:
        logger.warning("WIN XO")
        context["winner"] = cWin.movie_text
        context["href"] = cWin.href
        game.delete()
        return render(request, 'game/game_win.html', context)
    else:
        round = game.round
        rounds = game.rounds
        movieList = game.movie_set.all()
        if round == rounds:
            logger.warning("Round ended")
            for movie in game.movie_set.all():
                movie.active = 1
                movie.save()
            game.rounds = int((game.movie_set.count()/2))
            game.round = 1
            logger.warning("Rounds: " + str(game.rounds))
            logger.warning("Round: " + str(game.round))
            logger.warning("Movies: " + str(game.movie_set.all()))
            # Get Random Movies from Game
            moviesCopy = list(game.movie_set.filter(active=1))
            c1 = random.choice(moviesCopy)
            moviesCopy.remove(c1)
            c2 = random.choice(moviesCopy)
            context['c1'] = c1.movie_text
            context['c2'] = c2.movie_text
            context['href1'] = c1.href
            context['href2'] = c2.href

        else:
            # New Round
            game.round = round+1
            # Get Random Movies from Game
            moviesCopy = list(game.movie_set.filter(active=1))
            c1 = random.choice(moviesCopy)
            logging.warning("moviesALT: " + str(moviesCopy))
            moviesCopy.remove(c1)
            logging.warning("moviesNew: " + str(moviesCopy))
            c2 = random.choice(moviesCopy)
            context['c1'] = c1.movie_text
            context['c2'] = c2.movie_text
            context['href1'] = c1.href
            context['href2'] = c2.href
            logging.warning("Movie1: " + str(c1.movie_text))
            logging.warning("Movie2: " + str(c2.movie_text))
    game.c1 = c1.movie_text
    game.c2 = c2.movie_text
    game.save()
    context['game'] = str(game)
    context['round'] = game.round
    context['rounds'] = game.rounds
    context['id'] = str(game.id)
    logger.warning("Lets go")
    return JsonResponse(context)


class RunView(View):
    def get(self, request, *args, **kwargs):
        gameId = request.POST.get('id')
        winner_title = request.POST.get("winner_title")
        loser_title = request.POST.get("loser_title")

        game = get_object_or_404(Game, id=gameId)
        cWin = game.movie_set.get(movie_text=winner_title)
        cLose = game.movie_set.get(movie_text=loser_title)

        # Delete Lose
        cLose.delete()

        #TODO Update Winner (set inactive)
        cWin.active = 0

        #CONTEXT
        context = {
            "game": game,
            "id": str(game.id)
        }

        #TODO Check if new round or next round
        if game.movie_set.count() == 1:
            logger.log("Win")

        else:
            round = game.round
            rounds = game.rounds
            movieList = game.movie_set.all()
            if round == rounds:
                for movie in movieList:
                    movie.active = 1
                game.rounds = game.movie_set.count()
                game.round = 1
            else:
                # New Round
                game.round = round+1
                # Get Random Movies from Game
                moviesCopy = game.movie_set.filter(active=1).copy()
                c1 = random.choice(moviesCopy)
                moviesCopy.remove(c1)
                c2 = random.choice(moviesCopy)
                context = {
                    "c1": c1,
                    "c2": c2,
                }
        
        return render(request, 'game/game.html', context)

def postGame(request):
    rounds = "4"
    if request.POST.get('rounds') != None:
        rounds = request.POST.get('rounds')
    q = Game(pub_date=timezone.now(), rounds=rounds)
    q.save()

    copy = movie_titles.copy()
    copy.extend(action_titles)

    if request.POST.get('category') != None:
        category = request.POST.get('category')
        if category.lower() == 'dreamworks':
            copy = dreamworks_titles.copy()
            if len(copy) < int(rounds)*2:
                rounds = 16
                q.rounds = 16
                q.save()
        elif category.lower() == 'disney':
            copy = disney_titles.copy()
            if len(copy) < int(rounds)*2:
                rounds = 16
                q.rounds = 16
                q.save()
        elif category.lower() == 'netflix':
            copy = netflix_titles.copy()
            if len(copy) < int(rounds)*2:
                rounds = 16
                q.rounds = 16
                q.save()
        elif category.lower() == 'marvel':
            copy = marvel_titles.copy()
            if len(copy) < int(rounds)*2:
                rounds = 8
                q.rounds = 8
                q.save()
        elif category.lower() == 'action':
            copy = action_titles.copy()
            if len(copy) < int(rounds)*2:
                rounds = 16
                q.rounds = 16
                q.save()
        elif category.lower() == 'popular':
            copy = popular_titles.copy()
            if len(copy) < int(rounds)*2:
                rounds = 16
                q.rounds = 16
                q.save()
        elif category.lower() == 'animation':
            copy = animation_titles.copy()
            if len(copy) < int(rounds)*2:
                rounds = 16
                q.rounds = 16
                q.save()


    logger.warning("******************************************")
    logger.warning("ROUNDS: " + str(rounds))
    logger.warning("Copy: " + str(copy))
    for x in range(0, int(rounds)*2):
        rndChoice = random.choice(copy)
        logger.warning("RNDCHOICE: " + str(rndChoice) + " " + str(x))
        if x == 1:
            c1 = q.movie_set.create(movie_text=rndChoice)
        elif x == 2:
            c2 = q.movie_set.create(movie_text=rndChoice)
        else:
            q.movie_set.create(movie_text=rndChoice)
        copy.remove(rndChoice)

    logger.warning("MovieSet: " + str(q.movie_set.all()))

    context = {
        "game": q,
        "c1": c1,
        "c2": c2,
        "id": str(q.id)
    }
    return render(request, 'game/game.html', context)

def postAudienceGame(request):
    
    gameId = request.POST.get('id')
    vote = request.POST.get('audienceVote')
    logger.warning('Vote: ' + str(vote))
    game = get_object_or_404(Game, id=gameId)
    logger.warning("---------------------Vote available: " + str(vote))
    if vote == "on":
        game.vote = True
    
    copy = game.movie_set.all()

    rndChoice = random.choice(copy)
    c1 = rndChoice
    rndChoice = random.choice(copy)
    while rndChoice==c1:
        rndChoice = random.choice(copy)
    c2 = rndChoice

    context = {
        "game": game,
        "c1": c1,
        "c2": c2,
        "id": str(game.id)
    }
    game.c1 = c1.movie_text
    game.c2 = c2.movie_text
    logger.warning("C1-HREF: " + c1.href)
    logger.warning("C2-HREF: " + c2.href)
    game.started = True
    game.save()
    return render(request, 'game/game.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
        
   
class HostIndex(View):
    def get(self, request, *args, **kwargs):
        setId = kwargs['setId']
        
        set = get_object_or_404(Set, id=setId)
        
        movies = set.entertainment_set.all()

        logger.warning("Movielist: " + str(movies) + " - " + str(len(movies)))

        context = {
            "set": set,
            "id": str(set.id),
            "entries": len(movies)
        }
        return render(request, 'game/game_host.html', context)

def postHostGame(request):
    
    logger.warning("ID: " + request.POST.get('id'))
    logger.warning("Mode: " + request.POST.get('mode'))

    setId = request.POST.get('id')
    mode = request.POST.get('mode')
    rounds = request.POST.get('rounds')
    
    # Get Set
    set = get_object_or_404(Set, id=setId)
    
    # Create new Game
    game = Game(pub_date=timezone.now(), rounds=rounds)
    game.save()
    if mode == "multiplayer":
        game.vote = True
    
    # Randomize Set Movie List
    entertainmentRandom = list(set.entertainment_set.all()).copy()
    random.shuffle(entertainmentRandom)

    # Copy Movies from Set to Game
    for x in range(int(rounds)*2):
        entertainment = entertainmentRandom[x]
        game.movie_set.create(movie_text=entertainment.title, href=entertainment.href)
        
    # Go on
    copy = game.movie_set.all()

    rndChoice = random.choice(copy)
    c1 = rndChoice
    rndChoice = random.choice(copy)
    while rndChoice==c1:
        rndChoice = random.choice(copy)
    c2 = rndChoice

    context = {
        "game": game,
        "c1": c1,
        "c2": c2,
        "id": str(game.id)
    }
    game.c1 = c1.movie_text
    game.c2 = c2.movie_text
    logger.warning("C1-HREF: " + c1.href)
    logger.warning("C2-HREF: " + c2.href)
    game.started = True
    game.save()
    return render(request, 'game/game.html', context)
    logger.warning("Funktionier!")
    logger.warning("Game: " + str(game))

def marketplaceView(request):
     # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        sets = Set.objects.all().values()
        ren = []
        for set in sets:
            logger.warning("---------------------------------------")
            logger.warning("OBJ: " + str(set))
            logger.warning("ID: " + str(set['id']) + " - " + str(set['title']))
            object = {"id": str(set['id']), "title": str(set['title']), "poster": str(set['poster']), "description": str(set['description'])}
            logger.warning("Object: " + str(object))
            ren.append(object)
        logger.warning("Ren: " + str(ren))
        return JsonResponse({"test": ren}, status = 200)

    return JsonResponse({}, status = 400)