### --- PROJECT NAME / DESC --- ###

Virtual bookshelf, a small website that enables storing, editing and deleting of book
entries

### --- PARAMETERS --- ###

Must be able to take form inputs and save to an sql database
from the database must be able to grab those entries and populate them on the index.html
Must be able to edit on click of a link button
Finally must be able to delete entries on click

### --- HOW IT WORKS --- ###

There are three html pages, one to add books to the db one to edit the db item
and a main index page for showing the book list

Using a wtform and flask we catch the post that happens when a user enters information
into the fields and hits submit, form there that information is passed to the main.py 
and fed into the sql class object. It's formatted and saved to the sql database as per the
class attributes.

from there that db information sent as a variable to the index html and using jinja
is formatted to show it as a list

```
    <ul>
    {% if books|length == 0 %}
        <p>Library Is Empty!</p>
    {% else %}    
        {% for book in books: %}
            <li>
                <a href="delete/{{book.id}}">Delete</a>
                {{book.title}} - {{book.author}} - {{book.rating}}/10.0
                <a href="{{ url_for('edit', id=book.id) }}">Edit Rating</a>
            </li>
        {% endfor %}
    {% endif %}
    </ul>

```

There are finally two buttons next to each entry, one leads to an edit.html file to
edit the rating of the book, the other is a delete button.

The edit rating page finds the id of the book we hit "edit rating for" then passes us
to a templated edit page for that book. We can then post the new rating and sql will update
that field.

The delete button captures the id of the book it was made for in the for loop finds the 
relevant id in the database and deletes it.


### --- TO DO / FUTURE PLANS --- ### 

SQL is an amazingly strong database tool and while i have no plans to continue this PROJECT
it will be heavily used during my portfolio projects