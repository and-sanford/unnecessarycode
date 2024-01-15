#!/bin/bash

# Check for necessary commands
if ! command -v amixer &> /dev/null; then
  echo "Error: amixer is not installed. Please install it to control volume."
  exit 1
fi

if ! command -v paplay &> /dev/null; then
  echo "Error: paplay is not installed. Please install it to play sounds."
  exit 1
fi

if ! command -v espeak &> /dev/null; then
  echo "Error: espeak is not installed. Please install it for text-to-speech."
  exit 1
fi


# Get the current date in YYYY-MM-DD format
current_date=$(date +"%Y-%m-%d")

# Check if the user's timezone is in the United States
if [[ $(timedatectl status | grep "Time zone:" | awk '{print $3}') =~ ^America/ ]]; then
  # User is in the US, use YYYY-MM-DD format
  formatted_date=$current_date
else
  # User is outside the US, format as MM/DD/YY with flags
  formatted_date=$(date +"%m/%d/%y")
fi

# Print the formatted date based on the user's timezone
echo "Today's date is: $formatted_date"

# Set a random volume between 40% and 80%
# (Note: Replace this with the appropriate command for your operating system)
# Example for Linux using amixer:
amixer sset Master $((40 + RANDOM % 41))%

# Generate the Lost countdown beep
paplay /path/to/lost_beep.wav  # Replace with the actual path to the sound file

# Read out the date using text-to-speech
# (Note: Replace this with the appropriate command for your text-to-speech engine)
# Example using espeak:
espeak "$formatted_date"

