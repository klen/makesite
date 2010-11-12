git clone %(repo)s %(deploy_dir)s/source
cd %(deploy_dir)s/source
git push origin origin:refs/heads/%(branch)s
git fetch origin
git checkout --track origin/%(branch)s
