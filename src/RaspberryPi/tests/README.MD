
## How To

* To run all the unit tests, run the test_unit_runner
* It will run all the unit tests that it is configured to test

* To run all the simulated tests, run python main.py --test
* It will run all the simulated tests

## Add Tests

* To add a unit test (class not test function that can be added to an existing unit test):
*   Create the unit test using the unittest library provided by python
*   Add it to the list of unit tests that the test_unit_runner uses to import them and then test them

* To add a simulated test:
*   Create a new test file that runs through what the sensor data would appear like for the object
*   In Main.py add the file via an import in the self_test() function


## TODO

* As the software develops further, tests need to be maintained
* As of now, there are not a lot of unit tests to be added, however, whenever a unit test can be made we should make one
* Unit test classes should really be testing only one function in depth but there's not much to test yet
* Create more simulated tests that also check against a file for what the output should be
