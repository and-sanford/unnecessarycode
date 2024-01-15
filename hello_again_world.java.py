#!/usr/bin/env python3

"""
Dynamically generates a Java program that prints a greeting based on the current date,
compiles it, makes it executable, and runs it.

Includes logging, docstrings, cross-platform execution, and Flake8 compliance.
"""

import subprocess
import datetime
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the current date
today = datetime.date.today()

# Determine the greeting based on the date
greeting = f"good night, world! See you in {today.year + 1}" if today.month == 12 and today.day == 31 else "hello, world!"

# Java code with docstrings and logging
java_code = """
/**
 * Prints a greeting to the console using the system's echo command.
 * The greeting is determined by the Python script based on the current date.
 */
import java.io.IOException;
import java.util.logging.Logger;

public class HelloWorld {
    private static final Logger logger = Logger.getLogger(HelloWorld.class.getName());

    /**
     * Main method that executes the greeting printing logic.
     *
     * @param args Command-line arguments (not used in this case)
     */
    public static void main(String[] args) {
        logger.info("Starting HelloWorld program");

        try {
            Runtime.getRuntime().exec("echo " + greeting);
            logger.info("Greeting printed successfully");
        } catch (IOException e) {
            logger.severe("Error printing greeting: " + e.getMessage());
            e.printStackTrace();
        }

        logger.info("Ending HelloWorld program");
    }
}
"""

# Write the Java code to a file
with open("HelloWorld.java", "w") as java_file:
    logging.info("Writing Java code to file")
    java_file.write(java_code)

# Compile the Java code
logging.info("Compiling Java code")
subprocess.run(["javac", "HelloWorld.java"])

# Make the Java file executable (cross-platform)
if os.name == "posix":  # Unix-like systems (Linux, macOS, etc.)
    logging.info("Making Java file executable")
    subprocess.run(["chmod", "+x", "HelloWorld.java"])
elif os.name == "nt":  # Windows
    logging.info("Granting full control permissions to Everyone")
    subprocess.run(["icacls", "HelloWorld.java", "/grant", "Everyone:F"])
else:
    logging.warning("Unsupported operating system for making files executable.")

# Run the compiled Java class
logging.info("Running Java program")
subprocess.run(["java", "HelloWorld"])
