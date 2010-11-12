git clone {{repo}} {{deploy_dir}}/source
cd {{deploy_dir}}/source
git push origin origin:refs/heads/{{branch}}
git fetch origin
git checkout --track origin/{{branch}}
