using sync dev workflow

git config --global alias.sync-dev '!sh -c "read -p \"Commit message: \" msg && git commit -m \"[sync-dev] $msg\""'
git config --global --unset alias.sync-dev
