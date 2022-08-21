Welcome to my attempt to solve the coding interview challenge for the internship position at Banxware! 

In general my files should be straightforward: on any machine running python, it would be possible to use requirements.txt to re-create my virtual environment. I used pip. 

For my framework, since I don't have much experience with frameworks and zero with Typescript, I used Dash from Plot.ly to make a few simple graphs.

I was able to mush the data from the api calls around to get it into some sort of shape for the charts. I did some separation of my functions and data by making everything into a module and importing functions from my file, funkies.py, but the truth is, it got a bit messier than I would have liked. I wasn't sure how to untangle it without taking longer than I think is reasonable. However, someday I would like to be able to write encapsulated enough to do unit tests. 

When it came time to do integration testing, my code failed: I wrote test.py to check the dataframes against one another by merging them, SQL inner join style, but before I could do so, it became clear that the data available at the verification endpoint is in some way corrupted. There are dates for a month called "0" and there are 31 days in April, and 30 in February - for instance.

I wrote the test.py file as best I could: trying to show the shape of the type of test I would have written. I also made a graph of the verification endpoint data so one can see that it is, in its shape, not so radically different from mine, but the Merchant Foo does go into the red at some point in the vefification data, so that is a big difference.

That is where things are at the moment.

