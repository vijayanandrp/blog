```bash
git checkout master
git merge --squash yourBranch
git commit # all commit messages of yourBranch in one, really useful
```
 
 > [status 5007e77] Squashed commit of the following: ...
 
 nice! i create a "temp" branch off "master" 
 first to squash "yourBranch" into "temp", 
 
 then merge "temp" into "master". 
 
 – lazieburd Sep 25 '19 at 16:43
 
 https://stackoverflow.com/questions/25356810/git-how-to-squash-all-commits-on-branch
