import io.vertx.core.AbstractVerticle;
import io.vertx.core.Promise;
import io.vertx.core.eventbus.EventBus;

import org.apache.commons.codec.digest.DigestUtils;

public class MyBackendVerticle extends AbstractVerticle {

	@Override
	public void start(Promise<Void> startPromise) throws Exception {

		final String id = this.deploymentID() + " " + Thread.currentThread().getName();

		System.out.println("Start " + id);

		EventBus eb = vertx.eventBus();

		eb.consumer("news.uk.sport", message -> {
			String s = message.body().toString();
			
			System.out.println(id+" have received a message: " + s);
			
			String hash = DigestUtils.sha256Hex(s);
			message.reply(hash+" from "+id);
		});
	}

}
