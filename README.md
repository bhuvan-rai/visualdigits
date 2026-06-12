# visual digits

A silly small Python app made in VSCODE that guesses handwritten digits from 0 to 9.

-> The app uses a simple manually trained dataset , NOT mnist. You draw a digit, tell the app what digit it is, and it saves that example. After enough examples are trained, the app can guess new drawings.

"Features"
- Draw digits with the mouse
- Guess digits from 0 to 9
- Manually train the app by approving the correct digit
- Saves training data locally in digit_data.json
- Built with Python and Tkinter
- No machine learning library required

"Files"
1) main.py - the GUI app
2) training.py - training and prediction logic
3) digit_data.json - training dataset
4) main-tr.py - the GUI app + training feature 

(if you want to add more data excluding the already 102 samples , use the main-tr.py)

"Requirements"
1) Computer (🥀🥀🤧)
2) Python 

"How to Run"
1) Open a terminal in the 'project folder' and run:
python main.py

"Training ur dataset"

1) Run main-tr.py
2) Draw a digit in the white box.
3) Click the correct digit button under 'Train as'
4) Repeat this many times for digits 0 to 9.
The app will save your examples into digit_data.json.
For better results, train each digit multiple times.
NOTE: the only difference between main.py and main-tr.py is that 'main-tr.py' also has the additional training feature , so i suggest you download main-tr.py instead of main.py if you feel like training it yourself 
( currently it only contains 102 samples )

"working"

The drawing is converted into a small 28 x 28 grid of pixels. When you click a training button, the app saves that grid with the correct digit label.
When guessing, the app compares your new drawing with the saved examples and chooses the closest matching digit.
Publishing a Guess-Only Version

This is a beginner-friendly handwritten digit guesser. It is not meant to be as accurate as a real neural network model, but it is easy to understand, edit, and train manually.
