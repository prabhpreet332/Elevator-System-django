echo "Args recieved: $1 $2 $3"
# $1 - UserName (dockerhub)
# $2 - Repository Name
# $3 - Branch Name

# bash ./scripts/build-image.sh "ps332" "prabhpreet332/github-ci-cd" "refs/heads/feature/tag-creation" 

# Retrieves the Image name from name of repository (example: `github-ci-cd` from `prabhpreet332/github-ci-cd`)
REPOSITORY_NAME=$2
ARR_REPOSITORY_NAME=(${REPOSITORY_NAME///// })
IMAGE_NAME=${ARR_REPOSITORY_NAME[1]}

# Removes the `/` from the branch name and replace it with `_`
IMAGE_TAG=`echo "$3" | sed -r 's/[//]+/_/g'`
echo "Building image for image:tag ->" "$IMAGE_NAME:$IMAGE_TAG"  

docker build -t $IMAGE_NAME .
docker tag $IMAGE_NAME $1/$IMAGE_NAME:$IMAGE_TAG
docker push $1/$IMAGE_NAME:$IMAGE_TAG
