package net841bc.vertexwebdemo;

import io.reactivex.Single;
import io.vertx.reactivex.core.*;
import io.vertx.reactivex.ext.web.client.WebClient;

public class RxClient {

	public static void main(String[] args) {
		
		Vertx vertx = Vertx.vertx();
		
		String api1 = "http://www.163.com";
		String api2 = "http://www.baidu.co";
		
		WebClient client = WebClient.create(vertx);
		
		Single<String> res1 = client.getAbs(api1).rxSend().map(ar -> ar.statusMessage());
		Single<String> res2 = client.getAbs(api2).rxSend().map(ar -> ar.statusMessage()).onErrorReturnItem("Sorry");
		
		Single.zip(
				res1,
				res2,
				(a, b) -> a+b).subscribe(System.out::println, Throwable::printStackTrace);

	}

}
