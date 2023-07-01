# Kind of random sed
I'm sure that almost every one of us has ever used [sed](https://www.gnu.org/software/sed/manual/sed.html) at least one. Or at least heard about it.   
In this example we will write a toy sed plugin that replaces all template occurrences with some predefined random values.   
Actually it's also very very simple to replace templates with an appropriate environment variable value.   
So, let's suppose that we have some templates, like:
- first_name
- last_name
- age
- job_title
  
We have got some json file with such templates as well.
Let's replace all the templates.
## Expected input
Some random json with templates, for example:
```json
{
    "first_name": "{first_name}",
    "second_name": "{second_name}",
    "age": "{age}",
    "job_title": "{job_title}"
}
```
## Expected output
Expected output depends on random and template's values. So, one of the possible outputs can be:
```json
{
    "first_name": "Rob",
    "second_name": "Williams",
    "age": 26,
    "job_title": "Manager"
}
```
## Run it
To make your sed work you need to type:
```bash
$ python3 -m sugaru my.json --plugin random_person
```
