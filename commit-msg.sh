#!/usr/bin/env bash
set -euxo pipefail
#commit_length=`echo $1 | awk '{print length}'`
#commit_subj=`echo $1 | awk '/^\[[0-9][0-9]-.+-[0-9][0-9]-.+\].*/{print $0}'`

commit_length=`git log --pretty=%s --max-count=1 | awk '{print length}'`
commit_subj=`git log --pretty=%s --max-count=1 | awk '/^\[[0-9][0-9]-.+-[0-9][0-9]-.+\].*/{print $0}'`
#commit_text="git log --pretty=%b --max-count=1 | awk '/^\[[0-9][0-9]-.+-[0-9][0-9]-.+\].*/{print $0}'"
if (($commit_length>30))
then
	echo "Length >30!"
	exit 1
elif [ -z $commit_subj ]
then
	echo "Wrong format!"
	exit 1
fi

