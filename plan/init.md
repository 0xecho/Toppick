<!-- # Toppick
## Description
**tl;dr** This is a website that keeps track of your top picks in a particular category like movies, music, or video games.

If you are like me, you have a lot of things to do. One of them is to have conversations with other people.
A common theme that keeps popping up is "What is your favorite \[Movie or Music or Video game\]?" or more generatlly "What are your top picks for \[Movie or Music or Video game\]?"
If you've met me before, and you've asked me for a list of my top picks, you'll see that they tend to change quite frequently. That's because I'm a a dummy who forgets my top picks every now and then, especially when I've been away from the particular \[Movie or Music or Video game\] I'm interested in. Basically, I'm a dummy who doesn't remember my top picks. So I'm making this small website so I can properly rank my top picks and keep track of them. 

## Features
Basic features:
* **Rank Picks**: This is where you can compare 2 random picks from the same category, choose the one you like the most, and rank it as your top pick.
* **Add new picks**: You can add new picks to the website. These may be movies, music, or video games.
* **Modify a pick**: You can modify a pick that you've already added. Maybe you made a mistake, or maybe season 8 came out and it ruined the whole experience for you (damn you Game of Thrones).
* **View your top picks**: You can view your top picks. You can see the top picks for movies, music, or video games. You can sort them, filter them, search them, export them, import them ... you name it.
And that's it!

## How do I get started?
Head over to the [https://toppicks.top](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and follow the instructions. -->

This website is a top picks website. It keeps track of your top picks in a particular category like movies, music, or video games. Initially it will only have the movies.
Users can register and login to the website. Registration is free. Users register using telegram login which allows for the user to login to the website using their telegram account plus phone number is verified for the user. Users can set their username in the website. Users can have a publically shareable url to their top picks. Users can opt out of sharing their top picks in the settings. 
Once a user has registered, they have no selected movies yet. 
They can head to the select movies page and select movies they have watched by searching for them and labeling them as seen.
Additionally, they can add movies by going to the random movie page. On the random movie page, they are presented with a random movie. The can swipe left or right to label the movie as seen or not seen. 
Users need label at least 10 movies to be able to rank their picks.
Users can rank their picks by going to the rank page. On the rank page, they are presented with two random movies from the list.
Movie list is being pulled from the OMDb API. For every movie that is pulled from the OMDB API, save it to the local database for future use.
Users can view their top picks by going to the top picks page. On the top picks page, they are presented with a list of their top picks. Users can sort their top picks, filter their top picks, search their top picks, export their top picks, import their top picks, and delete their top picks.

Pages needed:
* Home page: Basic description and how to on how the site works.
* Login page: Login page for users. Login using telegram.
* Select movies page: Page for users to select movies they haven't watched yet.
    - Search for movies
    - Label movies as seen
* Random movie page: Page for users to select a random movie they haven't watched yet.
* Rank page: Page for users to rank their picks.
* Top picks page: Page for users to view their top picks.
* Watched movies page: Page for users to view their watched movies.
* Settings page: Page for users to modify their settings.


Future:
add watch list
find other movies i might like
find people with the same interests
import/export data
