package net841bc.vertexwebdemo;

import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;

import javax.imageio.ImageIO;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.DeploymentOptions;
import io.vertx.core.Vertx;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.http.HttpServerResponse;
import io.vertx.ext.web.Router;

public class MyVerticle extends AbstractVerticle {
	
	@Override
	public void start() throws Exception {
		Router router = Router.router(vertx);
		router.get("/").handler(request -> {
			
			  HttpServerResponse response = request.response();
			  response.putHeader("content-type", "text/plain");
			  response.setChunked(true);
			 
			  response.end("Hello World!");
		});
		
		router.get("/watermark").handler(request -> {
			
			HttpServerResponse response = request.response();
			response.setChunked(true);
						
			vertx.executeBlocking(promis -> {
				
				try {
					BufferedImage image = ImageIO.read(new File("a.jpg"));
					
					Graphics2D g = image.createGraphics();
					g.setFont(Font.decode("宋体"));
					g.drawString("你好", 100, 100);
					g.dispose();
					
					ByteArrayOutputStream out = new ByteArrayOutputStream();
					
					ImageIO.write(image, "JPEG", out);
					
					final Buffer buffer = Buffer.buffer();
					buffer.appendBytes(out.toByteArray());
					
					promis.complete(buffer);
				}catch(Exception e) {
					promis.fail(e);
				}
			}, ar -> {
				
				if(ar.succeeded()) {
					response.putHeader("content-type", "image/jpeg");
					response.end((Buffer)ar.result());
				} else {
					response.putHeader("content-type", "text/plain");
					response.end(ar.cause().toString());
				}
			});
			
		});
		
		vertx.createHttpServer().requestHandler(router).listen(8080);
	}

	public static void main(String[] args) {
		Vertx vertx = Vertx.vertx();
		vertx.deployVerticle("net841bc.vertexwebdemo.MyVerticle", new DeploymentOptions().setInstances(4));
		
	}

}
