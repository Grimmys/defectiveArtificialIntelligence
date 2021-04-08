![Defective Artificial Intelligence](https://github.com/Grimmys/defectiveArtificialIntelligence/blob/main/screenshots/game_title.png)

A very small game made for the Pygame Community Easter Jam, respecting the main theme " High Tech " and the bonus theme " Hide ".

# Goal of the game

You have been selected to help find an intruder among a group of cells.

Each level is procedurally generated, and all cells but one are following the same model.
Of course, you should find the one that is different.

![An example of a game instance](https://github.com/Grimmys/defectiveArtificialIntelligence/blob/main/screenshots/game_in_progress.png)

In this game instance of the first level, you can see that one cell is paler and more flattened than others: click on it, and let's go to next level!

Be cautious before making a guess : you have a limited number of attempts before being forced to restart from level 1.

My current record is 15 levels, do you think you can do better? 

# Controls
* R : Reset level generation (only available on tweaking mode, it's like cheating)
* Left click (on a artificial cell) : Submit your guess about the intruder

 # Tips
 
 The five first levels are easy, because the intruder is really different from others by its appareance.
 But after level ten, it will be really hard to find the intruder only by its look. You will have to examine its behaviour, because yes, cells of a same generation should have a similar behaviour!
 
 ![An harder game instance](https://github.com/Grimmys/defectiveArtificialIntelligence/blob/main/screenshots/harder_generation.png)
 
 In this generation for example, the intruder cannot be found so easily...
 
 # Attributes of a cell
 
 To find the intruder, you should take care about the following physical details:
 
 * the color
 * the width / the height
 * the proportion of " black points " in the design of the cell
 
 After a few levels, you will have to care about the behaviour too:
 
 * the reactivity (i.e. if the movement or the teleporation is rather slow or rather fast)
 * the movement direction preferences
 * the action preferences (in some generations the cells are really lazy and do next to nothing, in others you may see them using teleporation every time)

# Any question?

If you have a question or a suggestion, don't hesitate to contact me by e-mail (grimmys.programming@gmail.com) or by Discord (Grimmys#0373).
