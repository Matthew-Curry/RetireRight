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
#### Holds two folders:
**handlers:** The code for the AWS lambda functions matching one for one with the REST API calls the SPA needs to make. <br>
**layers:** Holds folders defining the lambda layers that are shared among the functions to perform core applicaiton functionality. <br>

#### Layers include:
**domain:** Holds Scenario and User domain objects used by the application. These objects are primarily used to translate data from the request to DynamoDB, and from DynamoDB back into the application. <br>
**dynamo_utils:** Holds utility class to retrieve cached dynamo resources from a warm lambda start, as well as a query formatter helper method. <br>
**writer:** Utility methods to write HTTP responses containing all needed CORS headers. <br>
**simulator:** Exposes core simulation method to simulate a given scenario for a given user <br>

### frontend
Application code is in the src folder

**api:** Holds Javascript methods used by the app to make calls to the backend REST API <br>
**cognito:** Javascript wrapper around the AWS cognito SDK to handle calls to the service for auth functionality <br>
**components/pages:** Application pages used by the router <br>
**components/core:** Core application components <br>
**router**: The vue router to the different pages, handles auth flow. <br>
**App.vue**: The core app. Responsible for updating and mediating data to the other components. <br>

## Infrastructure
* API Gateway for backend REST API, proxies to the lambdas
* Lambda for backend compute
* DynamoDB for data
* S3 to host artifacts and the Vue frontend
* CodePipeline + CodeBuild to deploy code and artifacts
* Cloudfront for CDN
* WAF for security around Cloudfront
* Route53 for DNS

## Next Steps
* Review and expand on frontend styling
* Explore ways to improve the simulation, including more descriptive lifestyle variables in an intuitive way
* Explore AWS SAM and Amplify
