#!/bin/bash
set -euxo pipefail

# Making sure we are releasing from the proper branch
#  git_flow: master
#  m_flow: master
m ci assert_branch --type hotfix m

# Make sure we are in a clean state
[ "$(m git status)" == "clean" ] \
  || m message error 'hotfixSetup.sh can only run in a clean git state'


# Gather info
git fetch --tags
currentVersion=$(git describe --tags || echo '0.0.0')
newVersion=$(m ci bump_version --type hotfix "$currentVersion")

# Swith to release branch
git checkout -b "hotfix/$newVersion" \
  || m message error "Unable to switch to hotfix/$newVersion branch"

# Update CHANGELOG and m.json files
m ci release_setup './m' "$newVersion"
