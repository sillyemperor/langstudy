# 通过vertx cli执行，会默认使用HazelcastClusterManager，本程序需要独立Zookeeper服务器，所以直接是java启动


# 程序编译，复制依赖包
```
mvn clean compile dependency:copy-dependencies
```

# 启动HTTP服务
```
java -cp target/dependency/*:target/classes io.vertx.core.Launcher run MyHttpVerticle  --cluster --cluster-pt899 --cluster-host localhost
```

# 启动后端服务
```
java -cp target/dependency/*:target/classes io.vertx.core.Launcher run MyBackendVerticle  --cluster --cluster-pt899 --cluster-host localhost --instances 4
```
