
# branch name
bugfix => bugfix/models
feature => feature/login
refactor => refactor/models
overview => overview/models

# commit 
feature => feature/login
[UPDATE] login Viewset
[FEATURE] add role to accessToken
[CLEAN_UP] validate serializer
[BUGFIX] add min length to password and required


# branches
- master -> build & deploy -> product
- develop -> devs & merges
- staging 
- demo

bugfix/models -> develop -> accept 

develop - (merge) -> master

feature/login -> fetch & pull -> (overview/models) -> feature/login