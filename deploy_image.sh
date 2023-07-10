docker build . -t sp-profile-profiler:latest
docker tag sp-profile-profiler:latest 421301571121.dkr.ecr.us-west-1.amazonaws.com/sp-profile-profiler:latest
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 421301571121.dkr.ecr.us-west-1.amazonaws.com/sp-profile-profiler
docker push 421301571121.dkr.ecr.us-west-1.amazonaws.com/sp-profile-profiler
aws lambda update-function-configuration \
    --function-name sp-profile-profiler \
    --image-uri 421301571121.dkr.ecr.us-west-1.amazonaws.com/sp-profile-profiler:latest
