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

OpenSSH access

1. Install the openssh-client if it is not already installed, and of course git:
```
sudo apt update && sudo apt install -y openssh-client git
```
2. Create user's ssh directory and a sub directory where your dedicated GitHub ssh key will be stored:
```
mkdir -p ~/.ssh/github
chmod 700 ~/.ssh ~/.ssh/github
```
3. Generate the SSH key (the output key will have octal permissions 600):
```
ssh-keygen -t rsa -b 4096 -C 'your@email.com' -f ~/.ssh/github/id_rsa -q -N ''
 #-q - silence ssh-keygen; -N '' - empty (without) passphrase, you can assign one if you want
```

4. Copy the content of the file id_rsa.pub, use the following command to output it:
```
cat ~/.ssh/github/id_rsa.pub
```
5. Go to your GitHub account. From the drop-down menu in upper right corner select Your profile. Click on the New SSH Key button and paste the content of ~/.ssh/github/id_rsa.pub in the field Key.

6. Create the ~/.ssh/config file, if it doesn't already exist:
```
touch ~/.ssh/config
chmod 600 ~/.ssh/config
```

Edit the config file and add the following entry for the new SSH key:
```
Host github.com    
IdentityFile ~/.ssh/github/id_rsa
```
7. Test the setup. Use the following command:
```
ssh -T git@github.com
```
Set existing repos to SSH conex
```
git remote set-url origin git@github.com:username/repository-name.git
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

#set upstream branch
git push --set-upstream origin branch-name
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

