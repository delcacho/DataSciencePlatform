CRUMB=$(curl http://jenkins:8080/crumbIssuer/api/xml?xpath=concat\(//crumbRequestField,%22:%22,//crumb\) -c cookies.txt --user 'admin:jenkins')
curl 'http://jenkins:8080/user/admin/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken' --data 'newTokenName=kb-token' --user 'admin:jenkins' -b cookies.txt
