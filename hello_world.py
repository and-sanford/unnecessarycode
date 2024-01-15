#!/usr/bin/env python3

import threading
import random
import googletrans
from googletrans import Translator
from loguru import logger
import subprocess

logger.add("output.log", rotation="1 MB")


def _get_random_language():
    logger.debug("Generating a random language code...")
    language = random.choice(list(googletrans.LANGUAGES))
    logger.debug(f"Generated language code: {language}")
    return language


def _get_random_languages_threaded():
    logger.debug("Generating two random language codes using threads...")
    threads = []
    languages = []

    for _ in range(2):
        thread = threading.Thread(target=languages.append, args=(_get_random_language(),))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    logger.debug(f"Generated language codes: {languages}")
    while len(set(languages)) != 2:  # Ensure both languages are unique
        logger.debug("Generated duplicate language codes. Regenerating...")
        languages = _get_random_languages_threaded()
    return languages


def main():
    while True:
        languages = _get_random_languages_threaded()
        translator = Translator()

        max_invalid_attempts = 2
        invalid_attempts = 0

        while True:
            logger.info("Choose a language from the following:")
            for i, language in enumerate(languages):
                logger.info(f"{i + 1}. {language}")

            try:
                choice = int(input("Enter your choice (number): ")) - 1
                if 0 <= choice < len(languages):
                    break
            except ValueError:
                logger.warning("Invalid input. Please enter a number.")
                invalid_attempts += 1

            if invalid_attempts > max_invalid_attempts:
                logger.warning(
                    "Too many invalid choices. Proceeding with a random language."
                )
                choice = random.randrange(len(languages))
                break

            logger.warning("Invalid choice. Please try again.")

        translated_text = translator.translate("Hello, world!", dest=languages[choice]).text

        with open("translated_text.txt", "w", encoding="utf-8") as file:
            file.write(translated_text)

        logger.success("The translated text has been written to translated_text.txt.")

        try:
            with open("translated_text.txt", "r", encoding="utf-8") as file:
                text_to_translate = file.read()
            translated_text = translator.translate(
                text_to_translate, dest=languages[choice]
            ).text
            with open("translated_text.txt", "w", encoding="utf-8") as file:
                file.write(translated_text)
            logger.success(
                "The text from output.txt has been translated and saved to translated_text.txt."
            )

            with open("translated_text.txt", "r", encoding="utf-8") as file:
                translated_text = file.read()
            english_text = translator.translate(translated_text, src=languages[choice]).text
            with open("final_output.txt", "w", encoding="utf-8") as file:
                file.write(english_text
        except FileNotFoundError:
            logger.error("output.txt not found.")

        try:
            with open("final_output.txt", "r", encoding="utf-8") as file:
                english_text = file.read()
            subprocess.call(["echo", english_text])
            logger.success("The contents of final_output.txt have been echoed to the console.")
        except FileNotFoundError:
            logger.error("final_output.txt not found.")


if __name__ == "__main__":
    main()
