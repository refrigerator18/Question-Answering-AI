# Question-Answering-AI
This program searches a corpus of text files (parsed from wikipedia, https://pypi.org/project/wikipedia/) and returns the most relevant sentence to the users query.


Given a query, the program first finds the most relevant file by using tf-idf values (https://en.wikipedia.org/wiki/Tf%E2%80%93idf). The tf-idf values are summed for every word in the query which is also in the file. Then the file with the highest value is returned. 

After the file is determined, the program returns the sentence with the highest matching word measure (the sum of idf values for any word in the query that also appears in the sentence). In the case of a tie the sentence with the higher query term density is returned. Query term density is defined as the proportion of words in the sentence that are also words in the query.

Usage and examples:
##
<img width="993" alt="Screen Shot 2020-08-10 at 6 49 50 PM" src="https://user-images.githubusercontent.com/57844356/89844997-8984f680-db3a-11ea-8a6d-461a9c5ddef2.png">

##
<img width="992" alt="Screen Shot 2020-08-10 at 6 51 00 PM" src="https://user-images.githubusercontent.com/57844356/89845049-aae5e280-db3a-11ea-8898-4a4318ee5388.png">

##
<img width="987" alt="Screen Shot 2020-08-10 at 6 51 35 PM" src="https://user-images.githubusercontent.com/57844356/89845070-b89b6800-db3a-11ea-95fa-2e6237ae768e.png">

##

*This project was created as a part of the online Harvard CS50-AI Course. https://cs50.harvard.edu/ai/2020/*






