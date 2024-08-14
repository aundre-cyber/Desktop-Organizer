# Desktop-Organizer

Keep your download folder organized and move the files to their respective directory

#Make sure to install these packages:
watchdog
python-magic
python-magic-bin


Replace the directory paths with the directory paths of you PC


#To continously run the program use task scheduler:

Open Task Scheduler.
Click on Create Task in the right-hand pane.
Give your task a name and description.
Under the Triggers tab, click New and select At startup.
Under the Actions tab, click New and select Start a program. Browse to your .bat file.
Program/Script: Ensure that the path to the Python executable (e.g., pythonw.exe or python.exe) is correctly entered.
Add Arguments: Ensure that the full path to your script is correctly entered in the "Add arguments (optional)" field.
Start In: Make sure that the "Start in" field points to the directory where your script resides.
Under the Conditions tab, uncheck Stop if the computer switches to battery power if you are on a laptop.
Under the Settings tab, ensure Allow task to be run on demand is checked and set If the task fails, restart every to a desired interval.
Click OK to save and schedule the task.
