### --- Project Mail Merge --- ###

Today we're using what we have learnt about files, directories and paths to do a mail merging challenge

### --- OBJECTIVES --- ###

We are tasked with taking the names file, the letters file and merging them so that we get named letters in our 
ready to send folder. 

This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

### --- Flow --- ###

1/ we open the names.txt file and read each named
2/ we then open the letter file 
3/ using a for loop we strip the name from the text file and tell the code to replace 
the PLACEHOLDER constant with the name currently stripped
4/ we then save the completed letter in the ready to send file
5/ loop continues until all names are completed