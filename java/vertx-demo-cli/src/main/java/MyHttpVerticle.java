import io.vertx.core.AbstractVerticle;
import io.vertx.core.Promise;
import io.vertx.core.eventbus.EventBus;
import io.vertx.core.http.HttpServer;
import io.vertx.core.http.HttpServerResponse;

import org.apache.commons.codec.digest.DigestUtils;

public class MyHttpVerticle extends AbstractVerticle {

	@Override
	public void start(Promise<Void> startPromise) throws Exception {
		
		System.out.println("Start "+this.deploymentID()+" "+Thread.currentThread().getName());
		
		HttpServer server = vertx.createHttpServer();
		
		EventBus eb = vertx.eventBus();
		
		System.out.println("EventBus "+eb.getClass());

		server.requestHandler(request -> {
			
			HttpServerResponse response = request.response();
			response.putHeader("content-type", "text/plain");

			// Write to the response and end it
//			response.end(DigestUtils.sha256Hex("Hello"));
			
			eb.request("news.uk.sport", "Hello", ar -> {
				if (ar.succeeded()) {
					System.out.println("Received reply: " + ar.result().body());
					
					// Write to the response and end it
					response.end(ar.result().body() + "");
				}
			});

		});

		server.listen(8080);
	}

}
