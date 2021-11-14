# GIT Cheat Sheet 

start repository

```
echo "# YOUR REPOSITORY NAME" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ribeirorod/${REPONAME}.git
git push -u origin main
```

quick checks

```
# remote repository link
git remote -v

# get local repo status
git status

# fetch from remote 
git fetch

#pull from remote/origin
git pull origin

```

branching

```
#list branches
git branch

#create new branch
git checkout -b new_branch

#switch to existing branch
git checout branch_to_go
```

commits

```
# add commit message
git commit -m "Message"

# change commit message
git commit --amend -m
```

Store credentials in cache (in seconds)
    git config credential.helper store --timeout=28800

Copy single file from another branch
    git checkout branch1               # first get back to branch
    git checkout branch2 -- app.js     # then copy the version of app.js from branch 1

git checkout [targetBranch]			# first get back to branch
git merge [MergingBranch]			# branch you want to merge

To push the current branch and set the remote as upstream, use
    git push --set-upstream origin [branch]

delete branch remotely
    git push -d origin "branch"

delete branch locally
    git branch -d [branch]
    git branch -D [branch] #force delete

ignore pending commits - get latest version from remote
git reset --hard origin/develop

