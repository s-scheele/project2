Workout Competetion - Apart

SEE setup.txt FOR RPI WIRING SETUP.

------------------------

Workouts:

1 - Pushups
2 - Crunches
3 - Bicycle Crunches
4 - Lunges
5 - Squats
6 - High Knees
7 - Burpees
8 - Pullups

Buttons:
Red button = "no"
Yellow button = "enter"
Green button = "yes"

------------------------

INSTRUCTIONS:

main_player1.py:
This is the "Initiator". 

You run the .py file, and when you are ready to initiate a workout, 
you press the "enter" button to send a request to someone running player2.

You now wait for player2 to hit their yes button, and for them to choose
a workout. When they have done that, the workout will show on the OLED.

You can now either choose to hit the "yes" button, or the "no" button.
The "no" button will halt the program, and you'll have to start again.
The "yes" button will start a 10 second countdown on the OLED for you and your,
oponent so that you have the time to get ready for your first set.
 
Once the timer has reached 0, the text WORKOUT will display, and you
know have 30 seconds (displayed on the other LED), to complete the set.

Once the timer has run to zero, you now have to use either the "yes" or "no"
button. The yes button indicating that you completed the workout and vice versa.

Then player 2 has to declare if he completed.
If either player didn't complete the set, a winning and a losing message
is displayed, to each player respectivly.

If both players complete the set, the 10 second OLED countdown will start
again, and the procedure repeats until one of the players does not hit 
complete their set.

------------------------

main_player2.py
This is the "Receiver".

You run the .py file, and wait for someone running player1, to initiate.
This will be indicated with the yellow "enter" light lighting up.

You then have to click the "yes" button, and the game will start.
You now have to select the workout you wish to challange the other player in.
 - The LED board will light up with numbers 1 through 8 (refer to the top
of this README file, to see which number represents which workout).

When you select a workout, with the button under the LED, the name of the 
workout will display on your OLED. You now have to wait for the other player
to accept this challange.

When accepted, a 10 second counter starts on the OLED, ending in a "WORKOUT" 
string being displayed.

A new timer, this time on the LED (with buttons) will start, giving you 30 
seconds to complete the set.

When the timer hits 0, you wait until you see either the "yes" or "no" LED
to light up, indicating your opponents ability to complete the set.

If the opponent lights up the "yes" light, you now have to declare if you
completed the set or not. Use the "yes" and "no" buttons.

If both players complete the set, the 10 second OLED countdown will start
again, and the procedure repeats until one of the players does not hit 
complete their set.

------------------------
