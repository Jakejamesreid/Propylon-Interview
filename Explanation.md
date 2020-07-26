# Explanation

After analysing the README file I gained an understanding for the tasks at hand. Now I could start to develop a strategy for tackling the tasks that were outlined. I have listed the 4 tasks below for easy reference.

1. The current implementation loads previously obtained offline copy of the data obtained from the endpoints. Update the module to fetch the latest data from the API endpoint if the parameter passed is the URL to the endpoint instead of a filename.

2. The current implementation of the `filter_bills_sponsored_by` appears to be correct. It is also reasonably quick when processing offline data. However, when the complete dataset obtained from the API is loaded, it is noticeably slower. Refactor the implementation to be faster than the current inefficient implementation.

3. Provide an implementation for the unimplemented function `filter_bills_by_last_updated`. The specification for this is documented in the function's doc-string.

4. Improve the code base as you would any professional quality code. This includes not just error checking and improving code readability but also adding doc-strings, comments where necessary, additional tests if any ...etc.

## Assumptions
1. The readme.md did not specify if this code is meant to be developed for use by an end-user or a developer. It is assumed that this code is being used by other developers and not by and end-user. As such the code does not take user input.
2. It is assumed that the definition of the functions is not to be changed.
3. It is assumed that data is just to be returned from the functions and not stored in a file or printed.

## The Strategy

### Initial Setup
First steps are to set up a git repository for version control. This is important for collaborating with other developers, having a backup of your code, being able to rollback to a previous version of your code, etc. The next step is to then create a virtual environment, which will allow for the projects required dependencies to be kept separate from other projects. These dependencies will be stored in the requirements.txt file.

### Understanding the code provided
I started by gaining an understanding of how the code provided works. To do this I set some breakpoints in the `filter_bills_sponsored_by` function and started stepping through the code. Once I gained an understanding of how the code worked, I then proceeded to rename the variables with names that were more meaningful. This allows for better readability for myself and other developers. I also made a slight adjustment to the file structure to add a data folder to store the JSON files. This just helps to keep the working area easy to navigate through. A def function was used to replace the lambda expression that was assigned to a  called load. This was done to keep with pep8 standards.

### Solving Task 1
To implement this strategy, the most logical first step seemed to be to start with Task 1 whilst keeping Task 4 in mind throughout. Initial thoughts were that the endpoints can be passed to the load function and the implementation can be changed to make an API call to the `legislation` and `members` endpoints, using the `requests` module. Appropriate error handling must also be used in the event that the API call fails.

Once this is implementation is functional, unit tests can be developed for testing the functionality of the API calls and the function. Testing API calls in unit tests are best done with the use of mocking. Mocking allows the ability to simulate the data received from the API. This means that the unit tests will not be dependant on a third party.

### Solving Task 2
Ideally, when using an API it is best to keep the number of calls that are made as low as possible, as it is very time-consuming to make an API call and wait for the result. In the current implementation, there are 3 nested loops, giving a time complexity of O(n^3). 

A decorator function can be used to time how long each function takes to run. This method will be used for optimising the time taken to run each function as opposed to just timing the entire script. The reason for this is so that each part of the code can be better analysed to identify where the bottlenecks are occurring. This data can then be used to analyse the performance increase after optimisations are made. Some possible optimisation techniques are as follows:

* There might be an option to filter the data using the API. 
* If it is okay to change the argument passed to the `filter_bills_sponsored_by` function to be the URI of the sponsor as opposed to the pId, then the implementation will be much more simple. 
* A generator could be used for more efficient use of memory

At this point, it is good to ensure that all test cases are still functioning correctly.

### Solving Task 3
The third task on initial examination also appears to be a simple enough solution. The `legislation` endpoint accepts a start and end date as parameters. So the implementation will be very similar to the `filter_bills_sponsored_by` function. A start and end date will be provided to the legislation endpoint to return a list of bills last updated within this date range.

Test cases will then be developed to ensure correct functionality.

### Solving Task 4
Ideally, this task would have already been completed as the parameters for completing this task were considered at each step of the way. Nevertheless, this is still a good opportunity to revise the code and ensure that everything is as optimised as possible and that the unit test covers all edge cases.

## The solution
An easy solution for this task is to simply pass the member_id (the URI for the member) to the `filter_bills_sponsored_by` function as opposed to the pId parameter. This would then give the ability to use just the legislation endpoint with member_id as a parameter and all the bills sponsored by that member would be returned. This would also mean that the member's endpoint would not be needed. The same could be done for the `filter_bills_by_last_updated` function where the start_date and end_date parameters could be passed to the endpoint. As it is the weekend and not possible to get an answer as to whether this method is suitable I will assume that the function's definition is not to be changed.

### Implementing the API call
The requests module was used to make the API call. The original parameters used to obtain the data in the offline JSON files were not provided so the default values have been used.

** Issue ** Ideally when making the get request the parameters would be passed to the params keyword as a key-value pair. Unfortunately, this method could not be used as an issue with URL encoding was experienced when passing the `memberURI` as a parameter. When this parameter was passed the requests module failed to correctly build the URL, resulting in no data being returned from the legislation endpoint. For this reason, the parameters were passed with the URI as a string to the get method.

### Refactor the implementation of `filter_bills_sponsored_by`
The implementation of the `filter_bills_sponsored_by` function is now much more simple and efficient than the original. By knowing the memberId (the URI of the member) the bills sponsored by this member can easily be found by passing the memberId as an argument to the legislation endpoint. The method to obtain the memberId is also pretty simple. A call is made to the members' endpoint and the data is looped over until a member with the user-defined pId value is found. A generator expression was used to reduce memory usage and time is taken to iterate over the list.

### Provide an implementation for the unimplemented function `filter_bills_by_last_updated`
Originally I had thought that the endpoint parameters date_start and date_end could be used to return the bills last updated between these dates. On further inspection, this was not the case so the implementation had to be changed. These dates might refer to when the bill was created as opposed to when it was last updated.

To use the `filter_bills_by_last_updated` function the developer must pass a start and end date for the date range of bills that were last updated. If the developer does not pass a date, the default values will be applied. A call is then made to the legislation endpoint to return the list of bills. Whilst iterating over the bills, the lastUpdated data for each bill is compared to the date parameters passed to the function to ensure that it is within the correct range. If so the bill is appended to a list of bills to be returned to the user. There is also a check to ensure that no duplicate bills are added as the same bill can be updated more than once within the specified time range.


### Improve the code base as you would any professional quality code
The cprofiler module was imported to create a cprofiler decorator called `profile`. A decorator is a function that takes another function as an argument and adds some extra functionality. The functionality being added here is to add profiling to any function passed to the `profile` decorator.

To use this profiler add the @profile decorator above any functions definition.

Auto pep8 was installed to format the code to help ensure that it adheres to the pep guidelines. These guidelines help to keep the code readable and uniform.

Comments were added where code might be ambiguous for other developers to understand. 
 

#### Test Cases

The initial plan was to use the mock object library to test the APIs in the unit test. Unfortunately, this was unsuccessful due to using multiple API calls in the same function. This made the method for patching the API call unclear as the patch seemed to apply to all requests made within the function being patched. There did not seem to be an option to patch specific get requests. The attempt made can be seen below.
```
patch('oireachtas_api.requests.get')
def test_filter_bills_sponsored_by_response(self, mock_get):
    # Configure the mock to return a response with offline data.
    with open(os.path.join(sys.path[0]+'\\data\\legislation.json')) as json_file:
        mock_get.return_value.ok = json.load(json_file)

    sponsoredBills = filter_bills_sponsored_by("GerryAdams")

    # If the request is sent successfully, then I expect a response to be returned.
    self.assertIsNotNone(sponsoredBills)
```

The original test case `TestFilterBillByLastUpdated` could not be used as if a bill was updated, the expected bills would no longer be valid. This means that this test case could potentially fail as the lastUpdated date for each bill changes.

The test cases that are used generally check that data is or isn't received and ensures that the appropriate errors are raised. 