
## docker mongo 初始化

Start the Database
> docker run --name some-mongo -d mongo --auth


初始化一个管理员，用于管理admin db : 只能操作admin，用于进行人员的增删改。
```
db.createUser({ user: 'mongo_user_admin', pwd: 'admin_1980675dfg', roles: [{role: 'userAdminAnyDatabase', db: 'admin'}]})
```


MongoDB里内置一些用户角色。也支持自定义。

用上面的用户， 创建对应数据库的操作权限。
> 

