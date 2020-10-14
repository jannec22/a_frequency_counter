# "a" frequency counter

this software uses common crawl API to retrive random portions of internet, which are then processed against the number of occurances of "a" and "all other" letters

to run, check [reqirements.txt](./requirements.txt)
then:

```
./get_random_internet_portion.sh 2 | ./find_letter_frequency.py 'a' 10
```

get_random_internet_portion.sh may take additional arguments:
  1. number of random segments to process from snaphot
  2. year of the snapshot (list available in [here](./segments.csv))
  3. day of the snapshot (list available in [here](./segments.csv))

find_letter_frequency.py takes optional argument:
  1. letter to finf frequency of
  2. max source number to process (from segment)


get_random_internet_portion.sh outputs a list of randomly selected segments from the snapshot.
if no year or day parameters given, random ones are choosen

find_letter_frequency.py reads segment urls from stdin and iterates on [max source number] of documents in them
1000 will be used if no [max source number given]
it outputs the percentage frequency of a letter "a" in the given data set.