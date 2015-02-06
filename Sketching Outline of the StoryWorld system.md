Sketching Outline of the StoryWorld system

Organization of World State

The purpose of the world state is two fold. First its goal is to act as a store of the information of the world as an aid for both players and DMs. This goal is tied to making it easier to find plot hooks, Discover things about the world, make stats and data easy to access and to serve as a backend storage system for potential DM tools we build. The second goal is more then a static data story. The "events" system should allow for reconstruction of the world state at any point in history.

The World state should be compatible with strict Dm'ed games as well as less strict collaborative story telling sessions. The difference being that DM'ed games will probably focus a lot of effort on modifying the precise stats throughout. Where as collaborative story telling mode focuses more on the story. Though if done right should involve just as much care and dedication to detail as if really playing (though precise manipulation of stats will likely be less common)

The World State is broken up into "Objects" 

Characters
Information about a particular character is stored in their Character.json file. This file will include All stats on the standard character sheet. As well as character descriptions (In the forma of data about height weight eye colour) As well as more flexible word description (or pointer to descriptive file). The Goal is that a Character.json would provide enough information that ANYONE could play that character with the information provided. Pointers to back story files should be plentiful.

In addition these character statistics this file also tracks skills you possess spells you know and any other information like that, Weapons you posess, other Gear on your person, your Location, Groups you belong to, as well as Effects you are under. (Notice the capital letters...)


Weapons
Information about a particular weapon is stored in a Weapon.json. Much like Characters, weapons exist as objects in the world and can have backstories (As all objects can)Though in the case of every day weapons such as "steel knife" you bought at a blacksmith in lalaland. Such a weapon's backstory might be as simple as that one line. Epic weapons such as the holy allpowerful sword of his majesty's smite-iness likely will have more back story to them.

The Weapon object also contains all information necessary to know how it would behave if used. (Does it bestow any effect on the user? does it have any special capabilities?) much like the characters, a weapon should contain enough information that anyone could dm a game using it. 

Weapons should also include pointers to thier "location" be it a character, or a actual location


Locations
Locations like the previous two objects can have backstory. Unlike the previous two objects Locations can contain locations. Locations can also contain characters weapons or gear. Ideally something like a city has nested within it multiple other locations. This would be like "lalaland" contains "lalacity" "lalacity" has "the main gate", "the market", "The castle", "the slums", "the not so slums". inside "the market" you have "the blacksmith" "the tailor" "the apothecary" etc. inside the blacksmith you might find big belly bob the blacksmith as well as several weapons maybe some gold bob has stored in a chest in the back.

Designing an entire city in high detail is not an easy task. by nesting locations you can periodically update add details etc to the city. While hiding away unecessary deatils.

TODO: Figure out a method by which to less strictly define a character's location. Since Characters move around... its not like bob is always going to be in his shop. maybe on saturdays he takes his wife betty to the bird bath by the bay. I literally just came up with this object so its pretty rough


Groups
Another thing I just came up with. Groups are collections of characters with some additional information to indicate relationship with the group (leader, aquaintance etc). This might also work for parties. A groups location might be less then well defined. For example an intercity underground network. Or if a party splits up. In these cases I propose that the groups, like locations have subgroups.

Objects
This is the catagory for all those other things in the world. I am of the opinion that even if its a coil of rope it should be stored as a separate argument. granted one with very little information about it possibly just a location. Of course an object might bestow abilities to a holder. or have modifiers on their stats. These will also be tracked by the object object.

Possibly we should combine weapons as a sub class of object? Also objects should be able to contain other objects? such as a chest containing a sword? or a sword that contains a priceless gem? THIS NEEDS THINKING

Knowledge
Honestly no real idea how to handle this. Possibly as a type of object that grants knowledge of a particular fact to a person? hardest one yet

-----------------------------------------------------

There might be more but thats all i can think of for now.

Onto the other aspect of StoryWorld. The dynamic portion

Stories are not static. They are continously evolving. The world becomes richer by adding more and more threads. The Approach I propose is to, on top of the world state info stored in the format above, also have a layer of objects which modify those in the world state known as "events". Events contain some information about when they occur as well as a list of the things that they change. We might want to go the snapshot route with these objects instead of the diff route as it might make it easier to easily construct the state of the world?

Here is the important consideration. Events are a network of story lines. they will point to ones that pre-ceed it. and maybe to ones the follow it but as multiple story lines enter the world and converge it will be difficult to construct a world state by following these paths. there will need to be some kind of backbone which can track the state of the world at any point in history... This sounds like having to re-base is events are added concurrently to another existing story line. 

This is going to be the most complex component to this whole thing. Get it write and we will be able to reconstruct history at any point in time.

-----------------------------------------------------

Lore and True Lore

One last point of discussion, I see two types of Lore in a world. Normal lore is written in stories or from an in-world perspective. This makes them seem like a type of knowledge. Objects just as scrolls could bestow this knowledge. This knowledge however will likely need to be stored in a non-standard format. A text document, an image (if someone found a map?) etc. Lore will need to be organized in a manner that it can be pointed to from the standard objects and events above

True Lore is what I call the the actual facts about the story world. For instance a character might have "knowledge" saying that someone attempted to murder them. but they could be wrong. True lore would be the out of character knowledge about the true story. So they might have mistaken who was trying to kill them. This is important because while characters can only act on Lore, DMing would require True Lore. How do we account for this?
