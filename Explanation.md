# Explanation

After analysing the README file I gained an understanding for the tasks at hand. Now I could start to develop a strategy for takling the tasks that were outlined. I have listed the 4 tasks below for easy reference.

1. The current implementation loads previously obtained offline copy of the data obtained from the endpoints. Update the module to fetch the latest data from the api endpoint if the parameter passed is the URL to the endpoint instead of a filename.

2. The current implementation of the `filter_bills_sponsored_by` appears to be correct. It is also reasonably quick when processing the offline data. However, when the complete dataset obtained from the api is loaded, it is noticeably slower. Refactor the implementation to be faster than the current inefficient implementation.

3. Provide an implementation for the unimplemented function `filter_bills_by_last_updated`. The specification for this is documented in the function's doc-string.

4. Improve the code base as you would any professional quality code. This includes not just error checking and improving code readability but also adding doc-strings, comments where necessary, additional tests if any ...etc.

## The Strategy
Here I will explain the my plan for solving eash task.

### Initial Setup
First steps are to set up a git repository for version control. This is important for collaborating with other developers, having a backup of your code, being able to rollback to a previous version of your code, etc. The next step is to then create a virtual environment, which will allow for the projects required dependencies to be kept separate from other projects. These dependencies will be stored in the requirements.txt file.

### Understanding the code provided
I started by gaining an understanding of how the code provided works. To do this I set some breakpoints in the `filter_bills_sponsored_by` function and started stepping through the code. Once I gained an understanding of how the code worked, I then proceeded to rename the variables with names that were more meaningful. This allows for better readibility for myself and other developers. I also made a slight adjustment to the file structure to add add a data folder to store the JSON files. This just helps to keep the working area easy to navigate through. A def function was used to replace the lambda expression that was assigned to a variable. This was done to keep with pep8 standards.

### Solving Task 1
To implement this strategy, the most logical 1st step seemed to be to understand start with Task 1 whilst keeping Task 4 in mind throughout. My initial thoughts are that this will be a simple enough task. I can use the `requests` module to make an API call to the `legislation` and `members` api endpoints. The results of these API calls can then be passed to the anonymous function used to load the offline files. I must also ensure to incorporate appropriate error handling in the event that the API caoll fails.

Once this is implementation is functional, I can develop a unit test for testing the functionality of the API call. Testing API calls in unit tests requires the use of mocking. Mocking allows us to simulate that we received the data from the API. This means that our unit tests will not be dependant on a third party.

### Solving Task 2
Ideally when using an API we want the amount of calls that we make to be as low as possible as it is very time consuming to make an API call and wait for the result. In the current implementation we have 3 nested loops, giving a time complexity of O(n^3). A decorator function can be used to time how long each function takes to run. I will use this method for for optimising the time taken as oppossed to just timing the entire script. The reason for this is that I don't want the time taken for the API call to be included due the uncontrollable time variance that will occur. This data can then be used to analyse the performance increase after optimisations are made. Some possible optimisation techniques are as follows:
* There might be an option to filter the data using the API. 
* If it is okay to change the arguement passed to the function to be the name of the sponsor as opposed to the pId, then we can easily remove the inner most loop. 
* The legislation endpoint also provides a filter by member URI option. This can be used to reduce the amount of loops needed.
* A generator could be used for more efficient use of memory

At this point it is good to ensure that all test cases are still functioning correctly.

### Solving Task 3
The third task on initial examination also appears to be a simple enough solutions. The `legislation` endpoint accepts a start and end date as parameters. So the implementation will be very similar to the `filter_bills_sponsored_by` function.

Test cases will then be developed to ensure correct functionality.

### Solving Task 4
Ideally this task would have already been completed as the parameters for completeing this task were considered at each step of the way. Nevertheless this is still a good opportunity to revise the code and ensure that everything is as optomised as possible and that the unit test cover all edge cases.

## The solution
An easy solution for this task is to simply pass the member_id (the URI for the member) to the `filter_bills_sponsored_by` function as opposed to the pId parameter. This would then give the ability to use just the legislation endpoint with member_id as a parameter and all the bills sponsored by that member would be returned. This would also mean that the member's endpoint would not be needed. The same could be done for the `filter_bills_by_last_updated` function where the start_date and end_date parameters could be passed to the end point. As it is the weekend and not possible to get an answer as to wether this method is suitable I will assume that the functions definition is not to be changed.

The implemented solution uses the members endpoint to obtain a list of the members and extracts the URI of the member whose pId was entered. The member URI is then passed to the legislation endpoint to return all the bills sponsored by that member.

### Implementing the API call
The requests module was used to make the API call. The original parameters used to obtain the data in the offline json files was not provided so I have estimated the parameters based off of the information in these files. The following parameters were chosen to pass to the legislation endpoint:
* bill_status: Current,Withdrawn,Enacted,Rejected,Defeated,Lapsed
* bill_source: Government,Private Member
* date_start: 1900-01-01
* date_end: 2099-01-01
* member_id: {user defined}
* lang: en

** Issue ** Ideally when making the get request the parameters would be passed to the params keyword as a key value pair. Unfortunately this method could not be used as an issue with url encoding was experienced when passing the `memberURI` as a parameter. When this parameter was passed the requests module failed to correctly build the url, resulting in no data being returned from the legislation endpoint. For this reason the parameters were passed with the URI as a string to the get method.

### Refactor the implementation of `filter_bills_sponsored_by`
The implementation of the `filter_bills_sponsored_by` function is now much more simple and efficient than the orignal. By knowing the memberId (the URI of the member) the bills sponsored by this member can easily be found by passing the memberId as an arguement to the legislation endpoint. The method to obtain the memberId is also pretty simple. A call is made to the members endpoint and the data is looped over until a member with the user defined pId value is found. A generator expression was used to reduce memory usage and time taken to iterate over the list.
