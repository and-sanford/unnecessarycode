#!/usr/bin/env python3

import re
import os
import platform
import logging
import time
import threading
from tqdm import tqdm  # Install tqdm through pip: pip install tqdm


def get_current_date() -> str:
    """
    Retrieves the current date in a consistent format.

    Returns:
        str: The extracted month and day (e.g., Nov 09).
    """
    logging.info("Retrieving current date in a consistent format.")

    try:
        system = platform.system()
        logging.info(f"Detected operating system: {system}")

        if system == "Windows":
            raw_date_time = os.popen("echo %DATE%").read().strip()
        elif system in ["Linux", "Darwin"]:
            raw_date_time = os.popen("date +'%b %d'").read().strip()
        else:
            raw_date_time = os.popen("date").read().strip()

        month_day = re.match(r"^\w{3}\s+\d{2}", raw_date_time).group()
        logging.info(f"Extracted month and day: {month_day}")
        return month_day

    except Exception as e:
        logging.critical("Failed to retrieve current date.", exc_info=True)
        return None


def is_dec_25() -> bool:
    """
    Checks if today is December 25th.

    Returns:
        bool: True if it's Christmas, False otherwise.
    """
    logging.info("Checking if today is December 25th.")

    current_date = get_current_date()

    if current_date:
        patterns = [
            r"Dec\s+25",
            r"Dec\.?\s+25",
            r"Dece?\w*\s+25",
            r"25\s+Dec",
            r"25/12",
            r"\d{2}/12",
            r"12-25",
            r"X{2,}\s+25\s+Dec",
        ]
        logging.info("Using the following patterns for date matching:")
        for pattern in patterns:
            logging.info(pattern)

        for pattern in patterns:
            if re.search(pattern, current_date, flags=re.IGNORECASE):
                logging.info("Match found! It's Christmas!")
                return True

        logging.info("No match found. It's not Christmas yet.")
        return False

    else:
        logging.warning("Could not determine if it's Christmas due to date retrieval error.")
        return False


def get_days_to_christmas(current_date):
    # ... (logic to calculate remaining days to Christmas based on current date) ...
    # This example assumes the current date format is "Month Day"
    month, day = current_date.split()
    christmas_month, christmas_day = "Dec", 25

    month_diff = (int(christmas_month) - int(month)) * 30
    day_diff = int(christmas_day) - int(day)

    return month_diff + day_diff

def main():
    while True:
        try:
            christmas_checker = is_dec_25()
            logging.info("Created isItChristmasYet instance.")

            if christmas_checker:
                print("It is Christmas!")
                break
            else:
                current_date = get_current_date()
                days_to_christmas = get_days_to_christmas(current_date)
                days_in_year = 365  # Adjust for leap years if needed
                progress = (days_in_year - days_to_christmas) / days_in_year

                print("It is not Christmas yet.")
                with tqdm(total=100, desc="Days until Christmas: ", unit="%", leave=True) as pbar:
                    pbar.update(int(progress * 100))

        except Exception as e:
            logging.critical("Unexpected error occurred.", exc_info=True)
            break

        logging.info("Main execution complete.")

        invalid_count = 0
        while True:
            user_choice = input("Check again (c), indefinitely (i), or end (e)? ").lower()
            if user_choice in ["c", "i", "e"]:
                break
            print("Invalid choice. Please enter 'c', 'i', or 'e'.")
            invalid_count += 1

            if invalid_count >= 2:
                logging.critical("User failed to provide valid input 2 times. Will run indefinitely.")
                user_choice = "i"  # Force indefinite checking
                break

        if user_choice == "c":
            continue
        elif user_choice == "i":
            logging.info("Starting indefinite checking loop with multithreading.")
            thread = threading.Thread(target=indefinite_checking_loop)
            thread.start()

            # Allow user to press Enter to stop the loop
            input("Press Enter to stop checking: ")
            thread.join()  # Wait for the thread to finish

            logging.info("Indefinite checking loop stopped.")
        else:
            logging.info("Ending program.")
            break


def indefinite_checking_loop():
    logging.debug("Indefinite checking loop thread started.")
    while True:
        time.sleep(1)
        check = is_dec_25()
        if check:
            print("It is Christmas!")
            break
        logging.debug("Not Christmas yet, continuing loop.")
    logging.debug("Indefinite checking loop thread finished.")


if __name__ == "__main__":
    main()
