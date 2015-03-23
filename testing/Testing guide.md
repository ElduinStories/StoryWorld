This is a guide for using storyworld. In this testing folder some sample "stories" have been prepared for testing purposes.

Step 1: Prep
First make the file Storworld/stw executable "sudo chmod u+x stw" And then add the StoryWorld folder to your PATH to make it accessible "export PATH=$PATH:/path/to/StoryWolrd/Folder/" If you want this to be accessible in any terminal you open add it to your ~/.bashrc file (and run "source ~/.bashrc" in any terminal you opened before making that edit)

Step 2: Initialization
move to the StoryWorld/testing folder and type "stw init" This will create a hidden folder in this directory .storyworld this is where storyworld puts all its working files

Step 3: Adding storyfiles
At present StoryWorld has an index of storyfiles to include in the history. To add story files type "stw add path/to/file"

for example while in StoryWorld/testing you can add 2 ready-made storyfiles
test.sty
test2.sty

Step 3: Building history
After the index is updated you can build the world using "stw build -w" if you do not include the -w it will construct the timeline but not the world states.

Step 4: Inspecting History
now that you have a world. You should check out some things in it.

Type
"stw view -h" this will display the timeline
"stw view -e -i event0" will display the event with event id of "event0" leaving out the -i argument will display all arguments
"stw view -t 2" will diplay the entire worldstate at time 2
"stw view -t 6 -p obj1" will display the state of just obj1 at time 6
