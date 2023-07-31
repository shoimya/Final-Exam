# [Web Application Development](https://gitlab.msu.edu/cse477-spring-2023/course-materials/): Final Exam

## Purpose

The purpose of this Final Exam is to assess your understanding of the essential elements of web application development covered this semester; these elements include:

1. Reactive front-end design
2. Design of a data-driven backend
3. Session management
4. Synchronous communication 
5. Web APIs

**NOTE:** Your implementation of the game should be accessible through the project's page of the website you've been building in Homeworks 1-3. There is a FAQ's related gitlab post for exam here: Issue https://gitlab.msu.edu/cse477-spring-2023/course-materials/-/issues/457 

## Exam Goals

For the Final Exam, you will develop a simple version of a NFT (Non-Fungible Token) trading marketplace website. [NFT](https://en.wikipedia.org/wiki/Non-fungible_token ) is a digital identifier associated with a digital content (for example an image or a video) that also establishes its ownership. Transactions such as change in ownership of NFT are recorded on a [blockchain](https://en.wikipedia.org/wiki/Blockchain ) platform which is basically a distributed database. Data on blockchain has the property of being immutable hence it is widely used to validate sequence of events from past for digital transactions such as the ones related to NFTs. An NFT trading marketplace website where NFTs are sold or purchased therefore provides the functionality for users to upload their digital art work to be traded as an NFT. The marketplace also provides the functionality of  recording NFT related transactions on a blockchain after transactions are validated. To trade NFTs,  users also need to have their own individual [crypto wallets](https://crypto.com/university/crypto-wallets ) with tokens that can be used to buy or sell NFT artwork. A token is a digital form of an equivalent asset such as cash or crypto. A crypto wallet stores users private keys which is used to access digital tokens stored on blockchain and used in place of actual money for transactions. Users public key is stored on the blockchain and together the private and public key are used to enable transactions such as buying and selling of NFTs. 

The NFT trading website that you will build will however only include basic functionality to mimic or simulate a NFT trading application.  The first basic functionality that your final NFT trading website will include is the ability to create users accounts that will be used for selling or purchasing NFTs. There will also be a default administrator account that will be created once the application starts. In practice, user wallets are securely located on their personal machines with a private key, but for this application the user created on the trading platform needs to maintain one wallet in the database that will mimic holding a private key. The public key for the user is stored on the blockchain related database along with a random number of tokens for that user when the application starts. We will remove the complicated signature verification process that goes with public and private keys in practical scenarios and assume the keys to be the same, so you just need do a key match comparison where required.  Users should have the option to upload their own digital files (very small sized jpg images only) or use an in-built function provided by the marketplace application to generate random small sized jpg images. Each NFT should be accompanied with some text description that should be editable only by the user that owns it. Since relational database such as [MySQL](https://www.mysql.com/) does not support maintaining actual files, you can use BLOB type option to store file related data on MYSQL and save the actual files in a folder within the flask setup using proper file naming convention to identify the file authorship. Application user’s wallet related data will also be maintained on MYSQL. Whenever a transaction (buying or selling) takes place, blockchain will be invoked and transactions related to blockchain will be recorded on MYSQL tables after verification. Hence you will be required to implement a number of SQL tables for the application. 

Your implementation of the NFT marketplace web application will be a trimmed down basic version of a fully functional marketplace such as OpenSea (https://opensea.io/) as described below. 

## Specific Requirements

 Your implementation must adhere to the following requirements. Specifically, you need to implement:   

1.  **A Signup System:** You will develop pages that allow your users to first signup with a username and password and then use the credentials to login. Only logged in users should be allowed to use the NFT marketplace application. Users must have the ability to logout as well. Make sure that all stored passwords are encrypted. The logged in user should be able to retrieve data related to them from database.  

2. **The Interface**: On user's first sign-in, they should be prompted with a welcome message and the option to either go to NFT related Seller’s page or NFT related Buyer’s page. Every user that signs up will be a seller as well as a buyer. The Buyer’s page should show all NFT’s created by all other users along with a specified token amount to buy it and some text describing the artwork.  There will also be a 'Buy' button next to each NFT content. Once a logged in user pushes 'Buy' button, the token amount possessed by the user is checked from blockchain data specific for that user followed by a transaction over blockchain if the amount is equal or more than the NFT being purchased. If the transaction is valid, the ownership of the NFT content is changed, and the amount associated with the two users (buyer and seller) is changed accordingly. The blockchain transaction states (called chain) also updated and stored on MYSQL database. If the transaction is invalid, which could occur if the user has insufficient tokens in their account on blockchain, then an error message pops up. Note that when a transaction is requested, a blockchain [mining](https://www.edureka.co/blog/blockchain-mining/) process also takes place. A typical NFT marketplace allows for a bidding process on any digital content, but we simplify the process here and only make transactions with fixed number of tokens without involving any bidding process.  

When a user clicks on the “Seller” page, they are routed to a page which shows either all the earlier NFTS created by them or any empty page if none was created. This page will also always show a ‘Create NFT’ and a ‘Upload NFT’ option on the top of main’s section along with two text boxes, one for generating a description of the NFT and one for the number of tokens the NFT digital art will sell for or is valued at. Once the text boxes are filled and the ‘Create NFT’ button is clicked, a random NFT will be created and shown along with other previously generated NFTs for that user if that exists. Each NFT will also show an ‘Edit’ button next to it. The ‘Edit’ button is used to change the description and the token amount associated with the owned NFTs that the user may want to change any time. You are welcome to either use the keyboards physical ‘Enter’ button to record changes after the user is done with editing or transition the ‘Edit’ button to an ‘Enter’ button on screen that can be clicked to record changes to NFT description and the token amount. Each NFT image the users create should be available to other users in their ‘Buying’ page section when they log in. A visual representation of the required elements of the two pages (Buying and Selling) excluding the navigation links is given here ![seller](https://gitlab.msu.edu/cse477-spring-2023/course-materials/-/blob/main/homework/Final-Exam/seller.jpg). You are welcome to format the elements with your own choice.

You need to store the current state of the NFTs (with ownerships history included) in the form of a chain existing in a blockchain network and the token changes for any user in persistent database for accessing and viewing later. A transaction related data that is encoded into a black and then appended to a chain should include the parties involved in transaction, ownership of NFT, transaction related information as well as NFT information.  Once the user signs out and logins again, they should be able to look at their NFTs and the NFT’s that others have created. The state of the blockchain should also be persistent so that it can invoked with the latest changes when a new valid transaction takes place. Users should be able to use their native keyboard to enter text wherever required on the page. You also need to create a link which available to user so that they can see information related to their personal wallet. If time permits, you are welcome to add more functionality to the interface, for example a NFT related Rating or a Commenting section.   

3. **The Transaction Validating and Recording System:** A successful transaction (selling and buying process) happens with an ownership change which is recorded on the blockchain related data (the chain). The initial record in blockchain (called a Genesis Block) from when the NFT came into existence keeps appending valid records to it thus providing proof of successful ownership changes over time. Data is only appended to the Block related to an NFT for valid transactions (successful purchase and owner transfer).  Normally a blockchain mining process takes place in nodes (computing devices) other than the node that is requesting the transaction to place but for simulation purpose only, the mining process for your application will be done on the same server hosting the blockchain platform. The purpose of mining is to validate and verify any transaction that is requested to be processed. Since other participating blockchain nodes also hold the current state of Block (transaction history) for an NFT, a mutual verified decision to allow a transaction to take process makes it more secure and trustworthy.  A description on the basics of blockchain mining process is given [here](https://en.bitcoin.it/wiki/Mining). 

Finally, when an administrator logs into the trading platform, they should be able to see all NFTs uploaded on the marketplace. Against each NFT, administrator will see a ‘Show’ button which once clicked, should display the current state of the blockchain state for that NFT with timestamps and ownership changes.   A visual representation of the required elements of the administrator page excluding the navigation links is given here ![buyer](https://gitlab.msu.edu/cse477-spring-2023/course-materials/-/blob/main/homework/Final-Exam/buyer.jpg). You are welcome to format the elements with your own choice. 

**NOTE:** Your implementation of the game should be accessible through the project's page of the website you've been building in Homeworks 1-3. 

## Getting started with the Exam

A flask application setup is provided to you for getting started with the exams. You can start coding your exams by first pulling the flask application into the course repository and copying it over to your personal repository. The application includes some functions that you would have to complete before they can be used. You might need to create more functions depending on your implementation. To pull changes to the course repository, type:

```bash
git pull https://gitlab.msu.edu/cse477-spring-2023/course-materials.git 
``` 

To start composing the exam container locally, type:

```bash
docker-compose -f docker-compose.yml -p exam-container up
``` 

You should now be able to see the exam container up and running at http://0.0.0.0:8080/home.html


Be sure to perform all development in the `Final-Exam` directory of your <u>Personal Course Repository</u> 



##### Submit Exam Code

1. Submit your assignment by navigating to the main directory of your <u>Personal Course Repository</u> and Pushing your repo to Gitlab; you can do this by running the following commands:

   ```bash
   git add .
   git commit -m 'submitting Final Exam'
   git push
   ```

2. You have now submitted the Final Exam; you can run the same commands to re-submit anytime before the deadline. Please check that your submission was successfully uploaded by navigating to the corresponding directory in Personal Course Repository online.


**Deploy your web application to Google Cloud**

Deploy your Dockerized App to Google Cloud by running the commands below from the Final Exam directory.

```bash
gcloud builds submit --tag gcr.io/cse477-spring-2023/exam
gcloud run deploy --image gcr.io/cse477-spring-2023/exam --platform managed
```

As we did in the homeworks, please retain the <u>Service URL</u>; You can visit the <u>Service URL</u> above to see a live version of your web application. 



##### Submit Final Exam Survey:

[Submit the Service URL for your live web application in this Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfsBhV9p-omn3ccjmNFyRRZgR-qwQnl70fkDVp7WpsKWrcv0w/viewform). 




## Rubric

This assignment is graded on a 100 point scale; all individual requirements recieve an "all or nothing" grade. The following guide will be used when grading your submission: 


**Specific Requirements:**

* <u> xx/15 points:</u>  The Signup System Requirements were met 

* <u>xx /20 points:</u>  NFT Creation with Editable Details Requirement were met

* <u>xx/20 points:</u> Successful Transaction (NFT Owner Transfer) Requirements were met

* <u>xx/20 points:</u> NFT Data Synchronization Requirements were met

* <u>xx/15 points:</u> Displaying NFT Blockchain State Data in Administrator Mode Requirements were met


**General Requirements:**

* <u>xx/5</u>: Does the code adhere to Frontend best practices covered throughout the semester?
* <u>xx/5</u>: Does the code adhere to Backend best practices covered throughout the semester?



**Please note that you will receive a 0 on the assignment if any of the following conditions are met:**


* Your containerized application does not compile
* Your application is non-functional
* Your submission was late
* Your work was plagiarized, borrowed, or copied
  * If this condition is met, you will also fail the course.
