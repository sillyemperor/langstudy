package net.x841bc.j8study.stream;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.stream.Collectors;

import org.apache.commons.io.IOUtils;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.concurrent.FutureCallback;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;
import io.reactivex.Observable;
import io.vertx.reactivex.core.Vertx;
import io.vertx.reactivex.ext.web.client.WebClient;

public class CrawlURL {

	public static void main(String[] args) throws FileNotFoundException, IOException, InterruptedException {
		List<String> links = IOUtils.readLines(new FileInputStream("links.txt"));
		links = links.stream().filter(s -> !s.isEmpty()).collect(Collectors.toList());

		{
			long t = System.currentTimeMillis();
			System.out.println("Synchronize");
			links.forEach(i -> {
				try {
					URL url = new URL(i);
//					System.out.println(url);
					try (InputStream io = url.openStream()) {
						byte[] unused = IOUtils.toByteArray(io);
//						System.out.println(data[0]);
					}

				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

			});
			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
		}

		{
			long t = System.currentTimeMillis();
			System.out.println("Multiply Thread");
			links.parallelStream().forEach(i -> {
				try {
					URL url = new URL(i);
//					System.out.println(url);
					try (InputStream io = url.openStream()) {
						byte[] unused = IOUtils.toByteArray(io);
//						System.out.println(unused.length);
					}

				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

			});
			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
		}

		{
			long t = System.currentTimeMillis();
			System.out.println("HttpAsyncClients 1");
			try (CloseableHttpAsyncClient httpclient = HttpAsyncClients.createDefault()) {
				httpclient.start();

				links.stream().map(url -> httpclient.execute(new HttpGet(url), null)).forEach(f -> {
					try {
						org.apache.http.HttpResponse resp = f.get();
						if (resp.getStatusLine().getStatusCode() > 300) {
							throw new Exception();
						}
						byte[] unused = IOUtils.toByteArray(resp.getEntity().getContent());
					} catch (Exception e) {
						e.printStackTrace();
					}
				});
			}
			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
		}
//		
		{
			long t = System.currentTimeMillis();
			System.out.println("HttpAsyncClients 2");
			try (CloseableHttpAsyncClient httpclient = HttpAsyncClients.createDefault()) {
				httpclient.start();

				final CountDownLatch latch = new CountDownLatch(links.size());

				links.forEach(url -> {
					httpclient.execute(new HttpGet(url), new FutureCallback<HttpResponse>() {

						@Override
						public void failed(Exception ex) {
							// TODO Auto-generated method stub

						}

						@Override
						public void completed(HttpResponse result) {

							try {
								if (result.getStatusLine().getStatusCode() > 300) {
									throw new Exception();
								}
								byte[] unused = IOUtils.toByteArray(result.getEntity().getContent());
							} catch (Exception e) {
								e.printStackTrace();
							}
							latch.countDown();
						}

						@Override
						public void cancelled() {
							// TODO Auto-generated method stub

						}
					});
				});

				latch.await();

			}

			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
		}

		{
			long t = System.currentTimeMillis();
			System.out.println("HttpAsyncClients 3");
			try (CloseableHttpAsyncClient httpclient = HttpAsyncClients.createDefault()) {
				httpclient.start();

				links.stream().map(url -> httpclient.execute(new HttpGet(url), null)).collect(Collectors.toList())
						.forEach(f -> {
							try {
								org.apache.http.HttpResponse resp = f.get();
								if (resp.getStatusLine().getStatusCode() > 300) {
									throw new Exception();
								}
								byte[] unused = IOUtils.toByteArray(resp.getEntity().getContent());
							} catch (Exception e) {
								e.printStackTrace();
							}
						});
			}
			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
		}

		{
			Vertx vertx = Vertx.vertx();
			WebClient client = WebClient.create(vertx);

			long t = System.currentTimeMillis();
			System.out.println("Vertx client 1");

			final CountDownLatch latch = new CountDownLatch(links.size());
			links.forEach(url -> {
				client.getAbs(url).send(ar -> {
					if (ar.succeeded()) {
						io.vertx.reactivex.ext.web.client.HttpResponse<io.vertx.reactivex.core.buffer.Buffer> response = ar
								.result();
						byte[] unused = response.body().getBytes();
						latch.countDown();
					} else {
						System.out.println("Something went wrong " + ar.cause().getMessage());
					}

				});
			});

			latch.await();

			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
			vertx.close();
		}

		{
			Vertx vertx = Vertx.vertx();
			WebClient client = WebClient.create(vertx);

			long t = System.currentTimeMillis();
			System.out.println("Vertx client 2");

			final CountDownLatch latch = new CountDownLatch(links.size());
			links.forEach(url -> {
				client.getAbs(url).rxSend()
					.map(io.vertx.reactivex.ext.web.client.HttpResponse::bodyAsBuffer)
					.subscribe(buff -> {
						byte[] unused = buff.getBytes();
						latch.countDown();
					}, error -> {
						System.out.println("Something went wrong " + error.getMessage());
					});
			});

			latch.await();
			
			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
			vertx.close();
		}

		{
			Vertx vertx = Vertx.vertx();
			WebClient client = WebClient.create(vertx);

			long t = System.currentTimeMillis();
			System.out.println("Vertx client 3");
			final CountDownLatch latch = new CountDownLatch(links.size());
			Observable.fromIterable(links)
				.map(url -> client.getAbs(url).rxSend().map(io.vertx.reactivex.ext.web.client.HttpResponse::bodyAsBuffer))
				.subscribe(ar -> {
					ar.subscribe(buff -> {
						byte[] unused = buff.getBytes();
						latch.countDown();
					});
				});
			latch.await();
			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
			vertx.close();
		}
		
		{
			Vertx vertx = Vertx.vertx();
			WebClient client = WebClient.create(vertx);

			long t = System.currentTimeMillis();
			System.out.println("Vertx client 4");
			final CountDownLatch latch = new CountDownLatch(links.size());
			Observable.<String>fromPublisher(s -> {
				try {
					BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream("links.txt")));
					r.lines().forEach(s::onNext);
				} catch(Exception e) {
					s.onError(e);
				}
			})
				.map(url -> client.getAbs(url).rxSend().map(io.vertx.reactivex.ext.web.client.HttpResponse::bodyAsBuffer))
				.subscribe(ar -> {
					ar.subscribe(buff -> {
						byte[] unused = buff.getBytes();
						latch.countDown();
					});
				});
			latch.await();
			t = System.currentTimeMillis() - t;
			System.out.println(t + " " + (t / links.size()));
			System.gc();
			Thread.sleep(3000);
			vertx.close();
		}
	}

}
