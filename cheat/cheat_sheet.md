
## NPM - React

### `killall -s KILL node` kill all running node processes




docker run -d -p 3000:3000 --name metabase metabase/metabase

===================================================== BASH =====================================================



===================================================== GIT- =====================================================

git remote -v

git status

git fetch

git pull origin

git branch

git checkout -b [new_branch]

git checkout [branch_to_go]

prompt> git add some-file
prompt> git commit -m "Refactor to simplify"


Store credentials for a period based
git config credential.helper store --timeout=28800

copy single file from another branch

git checkout branch1               # first get back to branch
git checkout branch2 -- app.js     # then copy the version of app.js from branch 1

git checkout [targetBranch]			# first get back to branch
git merge [MergingBranch]			# branch you want to merge

To push the current branch and set the remote as upstream, use
git push --set-upstream origin [branch]

delete branch remotely
git push -d origin applift_scaling

delete branch locally
git branch -d [branch]
git branch -D [branch] #force delete


git reset --hard origin/develop

# change commit message
git commit --amend -m
=====================================================DOCKER=====================================================

location on the pme /home/pmeadm/bin/docker-compose

stop container
docker ps -a -q --filter="name=<containerName>"

stop containers in image
docker ps -a -q  --filter ancestor=<image-name>
docker stop $(docker ps -q --filter ancestor=<image-name> )

