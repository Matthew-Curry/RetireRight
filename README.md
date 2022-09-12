# RetireRight
RetireRight is a personal finance SPA intended to help users think holistically about the lifestyle they want to live and the role money plays within it.
Rather than focusing on abstract concepts like "risk tolarance" or solely on investment numbers, the app allows users to define different "scenarios" 
holding lifestyle choice variables. A scenario includes information such as cost of housing, money spent on yearly travel, how many and what
age to have children, etc. Then, in addition to investment choice information, the application runs a Monte Carlo simulation and displays to users the 
percent chance they will have enough money to fund their retirement, along with a graph of the best, worst, and average result of the simulation.

Link to the application: https://rightretire.com/

## Code
The backend is written in Python and the frontend is written in Vue.

### backend
#### Holds two folders: <br> <br>
**handlers:** The code for AWS lambda functions matching one for one with the REST API calls the SPA needs to make. <br>
**layers:** Holds folders defining the lambda layers that are shared among the functions to perform core applicaiton functionality. <br>

#### Layers include: <br> <br>
**domain:** Holds Scenario and User domain objects used by the application. These objects are primarily used to translate data from the request to DynamoDB, and from DynamoDB back into the application. <br>
**dynamo_utils:** Holds utility class to retrieve cached dynamo resources from a warm lambda start, as well as a query formatter helper method. <br>
**writer:** Utility methods to write HTTP responses containing all needed CORS headers. <br>
**simulator:** Exposes core simulation method to simulate a given scenario for a given user <br>


